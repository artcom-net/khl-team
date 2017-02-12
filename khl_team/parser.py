"""Parser module.

This module contains a class that parsing information about hockey teams:
    - team info;
    - team stats;
    - players info;
    - players stats;
    - match info.

"""


import re

from urllib import request
from urllib.parse import urljoin

from bs4 import BeautifulSoup

from khl_team.exceptions import TeamNotExistError


class KHLParser(object):
    """Parser class.

    This class performs parsing of HTML pages on the championat.com.

    """
    _URL = {
        'base': 'https://www.championat.com/',
        'teams': 'hockey/_superleague/1770/teams.html',
        'matches': 'result.html',
        'players': 'players.html',
        'p_stats': 'pstat.html',
        't_stats': 'tstat.html'
    }
    _TAG_CLASSES = {
        'teams': 'sport__tiles__i',
        'matches': (
            'sport__table__tstat__td ',
            'sport__table__tstat__td _big',
            'sport__table__tstat__td _count _big'
        ),
        'meta': 'sport__info__data__i',
    }
    _MATCH_KEYS = ('date', 'time', 'teams', 'score')

    def __init__(self, *args):
        """Initial instance.

        :param args: the sequence of title teams.

        """
        self._team = None
        self.team = args
        self._teams_list = self._parse_teams()
        self._team_dict = None

    @property
    def team(self):
        """Getter team."""

        return self._team

    @team.setter
    def team(self, value):
        """Setter team."""

        self._team = (value,) if isinstance(value, str) else value

    def _parse_teams(self):
        """Parsing a page with a list of teams.

        :return: list of the dicts with keys: team, matches, location, urls.

        """
        team_dict = {}
        dict_list = []
        soup = self._get_soup(KHLParser._get_url(key='teams'))
        for link in soup.find_all('a', KHLParser._TAG_CLASSES['teams']):
            team_dict['team'] = re.search(
                r'(\w+\s?){2}\w+', link.text).group(0)
            team_dict['location'] = link.text.replace(
                team_dict['team'], '').strip()
            team_url = link['href'].replace(KHLParser._URL['matches'], '')
            team_dict['urls'] = {
                'matches': KHLParser._get_url(url=team_url, key='matches'),
                'players': KHLParser._get_url(url=team_url, key='players'),
                'p_stats': KHLParser._get_url(url=team_url, key='p_stats'),
                't_stats': KHLParser._get_url(url=team_url, key='t_stats')
            }
            dict_list.append(team_dict.copy())
            team_dict.clear()
        return dict_list

    def _get_teams_dict(self):
        """Fetches team dictionaries.

        :return: list of the teams dict.

        """
        team_list = []
        for team in self._team:
            try:
                team_list.append(list(
                    filter(lambda d: d['team'] == team, self._teams_list))[0])
            except IndexError:
                raise TeamNotExistError(team)
        return team_list

    def _parse_matches(self):
        """Parses the table of matches.

        Adds to the team dict a new key 'matches' with list of dict : date,
        time, teams, score.

        """
        tmp_list = []
        match_list = []
        soup = self._get_soup(self._team_dict['urls']['matches'])
        for td in soup.find_all('td', KHLParser._TAG_CLASSES['matches']):
            tmp_list.append(' '.join(td.text.split()))
            if len(tmp_list) == 4:
                match_dict = dict((key, value) for key, value in zip(
                    KHLParser._MATCH_KEYS, tmp_list))
                # Parse teams string.
                home_team = re.match(
                    r'\w+(\s\w+)*', match_dict['teams']).group(0)
                guest_team = re.search(
                    r'\w+(\s\w+)*$', match_dict['teams']).group(0)
                match_dict['teams'] = (home_team, guest_team)
                # Parse score string.
                score_list = re.findall(r'\d+', match_dict['score'])
                score = tuple((int(sc) for sc in score_list))
                match_dict['score'] = score
                match_list.append(match_dict.copy())
                match_dict.clear()
                tmp_list.clear()
            self._team_dict['matches'] = match_list

    def _parse_meta(self):
        """Parses additional information.

        Adds to the team dict a few keys: head_coach, arena, president,
        sponsor, site.

        """
        tmp_list = []
        soup = self._get_soup(self._team_dict['urls']['matches'])
        for div in soup.find_all('div', KHLParser._TAG_CLASSES['meta']):
            try:
                tmp_list.append(''.join(div.a.text.strip()))
            except AttributeError:
                tmp_list.append(div.text)
        if len(tmp_list) == 4:
            tmp_list.insert(3, '')
        for val in enumerate(tmp_list):
            if val[0] == 0:
                coach_name = re.match(r'(\w+\s*)+', val[1]).group(0)
                self._team_dict['head_coach'] = coach_name
            elif val[0] == 1:
                arena = re.match(r'\w+((-)?(\s)?\w+)+', val[1]).group(0)
                self._team_dict['arena'] = arena
            elif val[0] == 2:
                president = val[1].split(':')[1]
                self._team_dict['president'] = president
            elif val[0] == 3:
                try:
                    sponsor = val[1].split(':')[1]
                except IndexError:
                    sponsor = None
                self._team_dict['sponsor'] = sponsor
            elif val[0] == 4:
                self._team_dict['site'] = urljoin(
                    'http://', val[1]).replace('///', '//')

    def _parse_players(self):
        """Parse the page with the main information about the players.

        Adds to the team dict a new key 'players' with dicts (key - player
        number, value - dict(number, name, team, role, nationality, date_birth,
        height, weight)).

        """
        tmp_list = []
        none_id = 0
        self._team_dict['players'] = {}
        soup = self._get_soup(self._team_dict['urls']['players'])
        for td in soup.find_all('td'):
            val = ''.join(td.text).strip()
            if val:
                tmp_list.append(val)
                if len(tmp_list) == 1 \
                        and ''.join(tmp_list[0].split()).isalpha():
                    tmp_list.insert(0, 'None%d' % none_id)
                    none_id += 1
            if len(tmp_list) == 7:
                tmp_dict = {
                    'team': self._team_dict['team'],
                    'number': tmp_list[0],
                    'name': tmp_list[1],
                    'role': tmp_list[2],
                    'nationality': tmp_list[3],
                    'date_birth': tmp_list[4],
                    'height': tmp_list[5],
                    'weight': tmp_list[6]
                }
                self._team_dict['players'][tmp_list[0]] = tmp_dict.copy()
                tmp_list.clear()
                tmp_dict.clear()

    def _parse_players_stat(self):
        """Parse the page with player statistics.

        Adds to the player dict a new key 'stats' with dict(games, goals, tbl,
        assist, goals_pass, penalty).

        """
        tmp_list = []
        soup = self._get_soup(self._team_dict['urls']['p_stats'])
        for td in soup.find_all('td'):
            tmp_list.append(''.join(td.text.strip()))
            if len(tmp_list) == 8:
                number, stats = (tmp_list[0], tmp_list[2:])
                tmp_dict = {
                    'games': tmp_list[2],
                    'goals': tmp_list[3],
                    'tbl': tmp_list[4],
                    'assist': tmp_list[5],
                    'goals_pass': tmp_list[6],
                    'penalty': tmp_list[7]
                }
                if number:
                    self._team_dict['players'][number]['stats'] = \
                        tmp_dict.copy()
                # if the player has no number then to map dict by name.
                else:
                    name = list(filter(None, tmp_list))[0]
                    for pl_num in self._team_dict['players']:
                        player = self._team_dict['players'][pl_num]
                        split_name = player['name'].split()
                        f_name = split_name[0]
                        l_name = split_name[2] if len(split_name) == 3 else\
                            split_name[1]
                        if tuple(name.split()) == (f_name, l_name):
                            player['stats'] = tmp_dict.copy()
                tmp_list.clear()
                tmp_dict.clear()

    def _parse_team_stat(self):
        """Parse the page with team statistics.

        Adds to the team dict a new key 'stats' with dict.

        """
        tmp_list = []
        tmp_dict = {}
        key = None
        soup = self._get_soup(self._team_dict['urls']['t_stats'])
        for td in soup.find_all('td'):
            val = td.text
            if val.strip():
                if val.split()[0].isalpha():
                    if key:
                        values = tmp_list.copy() if len(tmp_list) < 7 \
                            else tmp_list[:3]
                        tmp_dict[key] = self._format_team_val(values)
                        tmp_list.clear()
                        key = val
                    else:
                        key = val
                else:
                    tmp_list.append(val)
        self._team_dict['stats'] = tmp_dict.copy()

    def get_data(self):
        """Runs all parsers.

        :return: list with team dicts.

        """
        data = []
        for self._team_dict in self._get_teams_dict():
            self._parse_matches()
            self._parse_meta()
            self._parse_players()
            self._parse_players_stat()
            self._parse_team_stat()
            data.append(self._team_dict.copy())
        return data if len(data) > 1 else data[0]

    @classmethod
    def _get_url(cls, url=None, key=None):
        """Joins _URL path.

        :param url: root path;
        :param key: key of KHLParses._URL;
        :return: joined _URL.

        """
        url = url if url else ''
        path = urljoin(url, cls._URL[key])
        return urljoin(cls._URL['base'], path)

    @staticmethod
    def _get_soup(url):
        """Create a BeautifulSoup object of _URL.

        :return: BeautifulSoup instance.

        """
        html = request.urlopen(url).read()
        return BeautifulSoup(html, 'html.parser')

    @staticmethod
    def _format_team_val(values):
        """Split list in tuples.

        All values command statistics are presented in three different
        meanings:
            - all (value, avg_value);
            - home (value, avg_value);
            - guest (value, avg_value).
        So the list is divided into parts.

        :param values: list of the team stats value;
        :return: list of tuple/tuple.

        """
        if len(values) == 6:
            tuples = [tuple(values[:2]), tuple(values[2:4]), tuple(values[4:])]
        else:
            tuples = tuple(values)
        return tuples

    def __str__(self):
        return '%s%s' % (self.__class__.__name__, self.team)

    def __repr__(self):
        return self.__str__()

"""KHL module.

This module contains classes describing the main entities. They are some of
the interfaces to the data and additional functionality. The title of teams
and parameters statistics are displayed in Russian language only.

"""


from datetime import datetime, timedelta

from icalendar import Alarm, Calendar, Event

from khl_team.parser import KHLParser
from khl_team.exceptions import PlayerNotExistError, MatchNotExistError


class KHLTeam(object):
    """ Hockey team class."""

    _ATTR_INIT = (
        'site', 'arena', 'location', 'team',
        'sponsor', 'stats', 'president',
        'head_coach'
    )

    def __init__(self, team):
        """Initial instance.

        :param team: team title, can take the following values:
        Авангард, Автомобилист, Адмирал, Ак Барс, Амур, Барыс, Витязь,
        Динамо М, Динамо Мн, Динамо Р, Йокерит, Куньлунь Ред Стар, Лада,
        Локомотив, Медвешчак, Металлург Мг, Металлург Нк, Нефтехимик,
        Салават Юлаев, Северсталь, Сибирь, СКА, Слован, Спартак, Торпедо,
        Трактор, ХК Сочи, ЦСКА, Югра.

        """
        self.site = None
        self.arena = None
        self.location = None
        self.team = None
        self.sponsor = None
        self.stats = None
        self.president = None
        self.head_coach = None
        team_data = KHLParser(team).get_data()
        players = team_data['players']
        for attr in KHLTeam._ATTR_INIT:
            setattr(self, attr, team_data[attr])
        self.players = [KHLPlayer(**players[player]) for player in players]
        self.matches = list(
            map(lambda match: KHLEvent(**match), team_data['matches'])
        )

    def get_player(self, number=None, l_name=None, role=None):
        """Gets the list of players.

        :param number: player number;
        :param l_name: last name;
        :param role: player role
        :return: list of players.

        """
        if number:
            attr, val = 'number', number
        elif l_name:
            attr, val = 'l_name', l_name
        elif role:
            attr, val = 'role', role
        else:
            return self.players
        return self._filter_player(attr=attr, attr_val=val)

    def _filter_player(self, attr=None, attr_val=None):
        player_list = list(filter(
            lambda player: attr_val == getattr(player, attr), self.players))
        if player_list:
            return player_list
        else:
            raise PlayerNotExistError

    def get_match(self, opponent=None, played=True, result=None):
        """Gets the list of matches.

        :param opponent: team title;
        :param played: include games played;
        :param result: won/lose;
        :return: list of KHLEvent instance.

        """
        match_list = self._get_not_played_match() if not played \
            else self.matches.copy()
        if opponent:
            match_list = self._get_opponent_match(opponent, match_list)
        if result:
            match_list = self._get_result_match(result, match_list)
        if match_list:
            return match_list
        else:
            raise MatchNotExistError

    def _get_not_played_match(self):
        """Gets a list of upcoming matches.

        :return: list of KHLEvent instance.

        """
        return list(
            filter(lambda match: False is match.is_finished, self.matches)
        )

    @staticmethod
    def _get_opponent_match(opponent, match_list):
        """Gets a list of matches with a certain team.

        :param opponent: team title;
        :param match_list: list of KHLEvent instance;
        :return: list of KHLEvent instance.

        """
        return list(
            filter(lambda match: opponent in match.teams, match_list)
        )

    def _get_result_match(self, result, match_list):
        """Gets a list of matches with a specific result.

        :param result: won/lose;
        :param match_list: list of KHLEvent instance;
        :return: list of KHLEvent instance.

        """
        result_list = []
        if result == 'won':
            result_list = list(
                filter(lambda match: self.team == match.winner, match_list)
            )
        elif result == 'lose':
            result_list = list(
                filter(lambda match: self._lose_check(match), match_list)
            )
        if result_list:
            return result_list
        else:
            raise MatchNotExistError

    def _lose_check(self, match):
        if self.team != match.winner and match.winner is not None:
            return match

    def __str__(self):
        return '%s(%s, %s)' % (
            self.__class__.__name__, self.team, self.location)

    def __repr__(self):
        return self.__str__()


class KHLPlayer(object):
    """Player class."""

    def __init__(self, **kwargs):
        """Initial instance."""

        self.name = None
        self.team = None
        self.f_name = None
        self.l_name = None
        self.number = None
        self.role = None
        self.date_birth = None
        self.nationality = None
        self.height = None
        self.weight = None
        self.stats = None
        for attr in kwargs:
            setattr(self, attr, kwargs[attr])
        self._set_names()

    def _set_names(self):
        """Sets first and last name."""

        split_name = self.name.split()
        self.f_name = split_name[0]
        self.l_name = split_name[2] if len(split_name) == 3 else split_name[1]

    def __str__(self):
        return '%s(%s, %s)' % (self.__class__.__name__, self.name, self.number)

    def __repr__(self):
        return self.__str__()


class KHLEvent(object):
    """Hockey event class."""

    _TODAY = datetime.today()
    _TITLE = 'Hockey: %s - %s'
    _DURATION = timedelta(hours=3)
    _REMIND = timedelta(minutes=15)

    def __init__(self, **kwargs):
        """Initial instance."""

        self.teams = kwargs['teams']
        self.score = kwargs['score']
        self.datetime = datetime.strptime(
            '%s:%s' % (kwargs['date'], kwargs['time']), '%d.%m.%Y:%H:%M'
        )
        self.is_finished = KHLEvent._TODAY > self.datetime
        self.winner = self._get_winner() if self.is_finished else None

    def gen_ics_event(self, title=None, duration=None, remind=None):
        """Generates Event object.

        :param title: event subject;
        :param duration: datetime;
        :param remind: datetime;
        :return: Event instance.

        """
        event = Event()
        alarm = Alarm()
        title = title if title else KHLEvent._TITLE
        dt_end = self.datetime + duration if duration else self.datetime
        alarm.add('trigger', remind if remind else KHLEvent._REMIND)
        event.add('summary', title % self.teams)
        event.add('dtstart', self.datetime)
        event.add('dtend', dt_end)
        event.add_component(alarm)
        return event

    @staticmethod
    def gen_ics(match_list, **kwargs):
        """Generates a byte string with ics headers.

        :param match_list: list of KHLEvent instance;
        :param kwargs: dict with keys(title, duration, remind);
        :return: byte string.

        """
        calendar = Calendar()
        calendar['version'] = '2.0'
        for match in match_list:
            event = match.gen_ics_event(**kwargs)
            calendar.add_component(event)
        return calendar.to_ical()

    def _get_winner(self):
        """Gets winner of match.

        :return: team title.

        """
        if self.score[0] != self.score[1]:
            winner = self.teams[0] if self.score[0] > self.score[1] \
                else self.teams[1]
        else:
            winner = None
        return winner

    def __str__(self):
        return '%s(%s - %s, %s)' % (self.__class__.__name__, self.teams[0],
                                    self.teams[1], self.datetime)

    def __repr__(self):
        return self.__str__()

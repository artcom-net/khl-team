"""Exception module.

Here define all exception classes.

"""


class TeamNotExistError(Exception):

    message = 'team "%s" not exist'

    def __init__(self, team):
        self.team = team

    def __str__(self):
        return TeamNotExistError.message % self.team


class PlayerNotExistError(Exception):
    pass


class MatchNotExistError(Exception):
    pass

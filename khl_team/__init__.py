try:
    from .khl import KHLTeam, KHLEvent
except ImportError:
    pass
from .exceptions import (
    TeamNotExistError,
    MatchNotExistError,
    PlayerNotExistError
)

__version__ = '1.0'

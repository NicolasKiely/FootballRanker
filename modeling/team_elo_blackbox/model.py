""" Model functions and structure for team elo """
import math
from typing import Dict, List, NewType, Tuple

#: Period data type
PeriodType = int

#: Team identifier data type
TeamType = NewType('TeamType', str)

#: Win/Loss flag type
WinType = int

#: Computed Elo data type
EloType = float

#: Match data type
MatchType = NewType(
    'MatchType', Tuple[PeriodType, TeamType, TeamType, WinType]
)


class MatchData(object):
    """ Match-level data for two teams at given period """
    __slots__ = ['_p', '_t1', '_t2', '_v']

    def __init__(self, p: PeriodType, t1: TeamType, t2: TeamType, v: WinType):
        self._p = p
        self._t1 = t1
        self._t2 = t2
        self._v = v

    @property
    def p(self) -> PeriodType:
        """ Match period """
        return self._p

    @property
    def t1(self) -> TeamType:
        """ First team """
        return self._t1

    @property
    def t2(self) -> TeamType:
        """ Second team """
        return self._t2

    @property
    def v(self) -> WinType:
        """ Win condition: 1 if t1 won, -1 if t2 won, 0 otherwise """
        return self._v


class ModelData(object):
    """ Top-level data for model """
    __slots__ = [
        # Indices
        '_periods_index', '_teams_index', '_matches_index',
        # Parameters
        '_match_param', '_is_victor_param', '_elo_sign_param',
        # Variables
        '_elo_initial_vars', '_elo_k_var', '_elo_k_decay_var',
        # Internal/etc
        '_elo_cache'
    ]

    def __init__(
            self, num_periods: int, teams: List[str],
            seasonal_matches: List[Tuple[int, str, str, int]],
            elo_initial_vars: List[Tuple[str, float]],
            elo_k_var: float, elo_k_decay_var: float
    ):
        self._elo_cache = {}

        # Initialize indices
        self._periods_index = [p+1 for p in range(0, num_periods)]
        self._teams_index = [TeamType(t) for t in teams]
        self._matches_index = [
            MatchData(*seasonal_match)
            for seasonal_match in seasonal_matches
        ]

        # Initialize parameters
        self._match_param = {}
        self._is_victor_param = {}
        self._elo_sign_param = {}
        for m in self._matches_index:
            self._match_param[(m.p, m.t1)] = m
            self._match_param[(m.p, m.t2)] = m
            self._is_victor_param[(m.p, m.t1)] = 1 if m.v > 0 else 0
            self._is_victor_param[(m.p, m.t2)] = 1 if m.v < 0 else 0
            self._elo_sign_param[(m.p, m.t1)] = m.v
            self._elo_sign_param[(m.p, m.t2)] = -m.v

        # Initialize decision variables
        self._elo_initial_vars = {
            TeamType(t): e for t, e in elo_initial_vars
        }
        self._elo_k_var = elo_k_var
        self._elo_k_decay_var = elo_k_decay_var

    @property
    def periods_index(self) -> List[PeriodType]:
        """ List of periods """
        return self._periods_index

    @property
    def teams_index(self) -> List[TeamType]:
        """ List of teams """
        return self._teams_index

    @property
    def matches_index(self) -> List[MatchData]:
        """ Returns list of matches """
        return self._matches_index

    @property
    def elo_initial_vars(self) -> Dict[TeamType, EloType]:
        """ Returns decision variable of initial elo values by team """
        return self._elo_initial_vars

    @property
    def elo_k_val(self) -> float:
        """ Return k transfer coefficient """
        return self._elo_k_var

    @property
    def elo_k_decay_val(self) -> float:
        """ Return k decay transfer coefficient """
        return self._elo_k_decay_var

    def match_param(self, p: PeriodType, t: TeamType) -> MatchData:
        """ Get match for given team at given period """
        return self._match_param[(p, t)]

    def elo_initial_val(self, t: TeamType):
        """ Returns initial elo value for given team """
        return self._elo_initial_vars[t]

    def elo(self, m: MatchData, t: TeamType) -> EloType:
        """ Returns ELO for team, cached by period and team """
        if (m.p, t) not in self._elo_cache:
            self._elo_cache[(m.p, t)] = elo(self, m, t)
        return self._elo_cache[(m.p, t)]

    def is_victor_val(self, p: PeriodType, t: TeamType):
        """ Returns 1 if team won match at period p, 0 otherwise """
        return self._is_victor_param[(p, t)]

    def elo_sign_val(self, p: PeriodType, t: TeamType):
        """ Returns 1 if team won, -1 if lost, 0 otherwise at period p """
        return self._elo_sign_param[(p, t)]


def elo(model: ModelData, m: MatchData, t: TeamType) -> EloType:
    """ Computes ELO for given team t at period p"""
    if m.p == 1:
        # Initial period
        return model.elo_initial_val(t)

    else:
        # Get previous match for team
        m_ = model.match_param(m.p-1, t)

        # Compute recursively
        return (
            model.elo(m_, t)
            + model.elo_sign_val(m_.p, t) * elo_delta(model, m_)
        )


def elo_delta(model: ModelData, m: MatchData) -> EloType:
    """ Computes ELO transfer for given team for given match """
    return (
        math.pow(model.elo_k_decay_val, m.p) * model.elo_k_val
        * (
            model.is_victor_val(m.p, m.t1) * model.elo(m, m.t2)
            + model.is_victor_val(m.p, m.t2) * model.elo(m, m.t1)
        )
    )

# rke_client/wallet/cloudcoin.py

"""
Provides a Python object representation of a single CloudCoin, encapsulating
all its properties and state.

This module is the Python equivalent of the Go 'cloudcoin.go' file.
"""

from __future__ import annotations
import logging
from enum import IntEnum
from typing import List, Optional, Tuple

# CORRECTED IMPORT: Use a relative import to go up one level (from wallet/ to rke_client/)
# to find the config.py file. This resolves the Pylance error.
from .. import config

# Configure a logger for this module
logger = logging.getLogger(__name__)


class RaidaStatus(IntEnum):
    """Represents the status of a single RAIDA server's check for this coin."""
    UNTRIED = 0
    PASS = 1
    FAIL = 2
    ERROR = 3
    NORESPONSE = 4

class CoinStatus(IntEnum):
    """Represents the overall authenticity grade of the coin."""
    UNKNOWN = 0
    AUTHENTIC = 1
    FRACKED = 2
    COUNTERFEIT = 3
    LIMBO = 4


class CloudCoin:
    """
    A Python object representing a single CloudCoin. This class is a direct
    port of the CloudCoin struct and its associated methods from cloudcoin.go.
    """
    def __init__(self, sn: int, denomination: int, pownstring: str = "", ans: Optional[List[str]] = None):
        """Initializes a CloudCoin instance."""
        self.sn: int = sn
        self.denomination: int = denomination

        self.ans: List[Optional[str]] = [None] * config.TOTAL_RAIDA_SERVERS
        if ans and len(ans) == config.TOTAL_RAIDA_SERVERS:
            self.ans = ans

        self.pans: List[Optional[str]] = ["0" * 32] * config.TOTAL_RAIDA_SERVERS
        self.statuses: List[RaidaStatus] = [RaidaStatus.UNTRIED] * config.TOTAL_RAIDA_SERVERS

        self.passed: int = 0
        self.failed: int = 0
        self.errors: int = 0
        self.grade_status: CoinStatus = CoinStatus.UNKNOWN

        self.folder: Optional[str] = None
        self.original_filename: Optional[str] = None
        self.price: int = 0
        self.group_name: str = ""
        
        self.pownstring: str = "u" * config.TOTAL_RAIDA_SERVERS
        if pownstring:
            self.set_pownstring(pownstring)
        else:
            self._update_grade_status()

    def set_pownstring(self, pownstring: str):
        """Parses a POWN string and recalculates the coin's grade."""
        if not pownstring or len(pownstring) != config.TOTAL_RAIDA_SERVERS:
            pownstring = "u" * config.TOTAL_RAIDA_SERVERS
        self.pownstring = pownstring.lower()
        self.passed = self.pownstring.count('p')
        self.failed = self.pownstring.count('f')
        self.errors = self.pownstring.count('e')

        status_map = {'p': RaidaStatus.PASS, 'f': RaidaStatus.FAIL, 'e': RaidaStatus.ERROR, 'n': RaidaStatus.NORESPONSE, 'u': RaidaStatus.UNTRIED}
        for i, char in enumerate(self.pownstring):
            self.statuses[i] = status_map.get(char, RaidaStatus.UNTRIED)
        
        self._update_grade_status()

    def _update_grade_status(self):
        """Determines the coin's authenticity grade."""
        # Using constants from the Go code for grading logic
        is_authentic = self.passed >= 14
        is_counterfeit = self.failed >= 12
        if is_authentic:
            self.grade_status = CoinStatus.FRACKED if self.failed > 0 or self.errors > 0 else CoinStatus.AUTHENTIC
        else:
            self.grade_status = CoinStatus.COUNTERFEIT if is_counterfeit else CoinStatus.LIMBO

    def set_an(self, raida_index: int, an: str):
        """Sets the Authenticity Number (AN) for a specific RAIDA index."""
        if 0 <= raida_index < config.TOTAL_RAIDA_SERVERS:
            self.ans[raida_index] = an

    def get_whole_sat(self) -> Tuple[str, str]:
        """Calculates the whole and satoshi parts of the coin's value."""
        # This mapping is a direct port from the Go utils file
        denom_map = {
            -8: ("0", "00_000_001"), -7: ("0", "00_000_010"), -6: ("0", "00_000_100"),
            -5: ("0", "00_001_000"), -4: ("0", "00_010_000"), -3: ("0", "00_100_000"),
            -2: ("0", "01_000_000"), -1: ("0", "10_000_000"), 0: ("1", "00_000_000"),
            1: ("10", "00_000_000"), 2: ("100", "00_000_000"), 3: ("1_000", "00_000_000"),
            4: ("10_000", "00_000_000"), 5: ("100_000", "00_000_000"), 6: ("1_000_000", "00_000_000"),
        }
        return denom_map.get(self.denomination, ("0", "00_000_000"))

    def get_filename(self) -> str:
        """Generates the standard internal filename for this CloudCoin."""
        whole, sat = self.get_whole_sat()
        return (f"{whole}.{sat}.BTC.{self.pownstring}.{self.sn}.extra."
                f"{self.price}.{self.group_name}{config.CC_FILE_BINARY_EXTENSION}")

    def __repr__(self) -> str:
        """Provides a developer-friendly string representation of the coin."""
        return (f"CloudCoin(SN={self.sn}, Denom={self.denomination}, "
                f"Status={self.grade_status.name}, P={self.passed}, F={self.failed})")
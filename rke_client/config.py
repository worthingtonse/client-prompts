# rke_client/config.py

"""
Central repository for all static configuration values, constants, command codes,
and error codes for the RKE/DKE Client.

This module is a direct and faithful Python equivalent of the Go 'config.go'
and 'codes.go' files, consolidating all static data into a single, reliable
source for the entire application. Variable and constant names are preserved
to maintain consistency with the existing ecosystem.
"""

import os
from enum import IntEnum
from pathlib import Path

# -- Application Metadata --
# Mirrored from config.go
VERSION = "25.6.8-python"

# -- Filesystem Paths --
# Use pathlib for OS-agnostic path management.
BASE_DIR = Path(os.path.dirname(os.path.abspath(__file__))).parent
DATA_DIR = BASE_DIR / "data"
WALLETS_DIR = DATA_DIR / "wallets"
KEYS_DIR = DATA_DIR / "encryption_keys"

# Wallet subdirectory names, matching the Go implementation's conventions
BANK_DIR_NAME = "Bank"
FRACKED_DIR_NAME = "Fracked"
COUNTERFEIT_DIR_NAME = "Counterfeit"
LIMBO_DIR_NAME = "Limbo"
IMPORT_DIR_NAME = "Import"
EXPORT_DIR_NAME = "Export"
TRASH_DIR_NAME = "Trash"
IMPORTED_DIR_NAME = "Imported"
SENT_DIR_NAME = "Sent"
SUSPECT_DIR_NAME = "Suspect"

# -- RAIDA Network Configuration --
TOTAL_RAIDA_SERVERS = 25
MIN_QUORUM = 13  # Minimum number of successful RAIDA responses needed for consensus

# Guardian servers for discovering the global RAIDA network.
# This list is the direct Python equivalent of the 'Guardians' array in 'config.go'.
GUARDIAN_SERVERS = [
    "raida-guardian-tx.us",
    "g2.cloudcoin.asia",
    "guardian.ladyjade.cc",
    "watchdog.guardwatch.cc",
    "g5.raida-guardian.us",
    "goodguardian.xyz",
    "g7.ccraida.com",
    "raidaguardian.nz",
    "g9.guardian9.net",
    "g10.guardian25.com",
    "g11.raidacash.com",
    "g12.aeroflightcb300.com",
    "g13.stomarket.co",
    "guardian14.gsxcover.com",
    "guardian.keilagd.cc",
    "g16.guardianstl.us",
    "raida-guardian.net",
    "g18.raidaguardian.al",
    "g19.paolobui.com",
    "g20.cloudcoins.asia",
    "guardian21.guardian.al",
    "rg.encrypting.us",
    "g23.cuvar.net",
    "guardian24.rsxcover.com",
    "g25.mattyd.click",
    "g26.cloudcoinconsortium.art",
]


# -- Cryptographic Constants --

# HKDF domain separation info strings. The "DKE" prefix is for client-side
# clarity, but the byte values match the "RKE" spec for interoperability.
DKE_KEYSHARE_INFO = b"RKE-KeyShare-v1.0"
DKE_ENCRYPTION_INFO = b"RKE-EncryptionKey-v1.0"
DKE_SESSION_INFO = b"RKE-SessionKey-v1.0"

# Keystore configuration for securely caching derived keys
DEFAULT_KEY_TTL_SECONDS = 24 * 60 * 60  # 24 hours
MIN_KEY_TTL_SECONDS = 1 * 60 * 60      # 1 hour
MAX_KEY_TTL_SECONDS = 7 * 24 * 60 * 60 # 7 days


# -- Protocol Command and Status Codes --
# This section is the Python equivalent of 'codes.go', preserving naming conventions.

class ResponseStatus(IntEnum):
    """RAIDA Response Status Codes"""
    SUCCESS = 0xFA
    FAIL = 0xFB
    ALL_PASS = 0xF1
    ALL_FAIL = 0xF2
    MIXED = 0xF3
    ERROR = 0xFB  # General error, alias for FAIL
    TICKET_NOT_FOUND = 0xF5
    INVALID_COMMAND = 0x18
    INVALID_ENCRYPTION = 0x22
    INVALID_PACKET_LENGTH = 0x20
    SECRET_NOT_FOUND = 0x41
    INVALID_PARAMETER = 0x42
    FAILED_AUTH = 0x40
    # Add other status codes from codes.go as needed for client error handling

class COMMAND_GROUP(IntEnum):
    """Top-level command groups, matching codes.go"""
    COMMAND_GROUP_STATUS = 0x0
    COMMAND_GROUP_AUTH = 0x1
    COMMAND_GROUP_HEALING = 0x2
    COMMAND_GROUP_STABLE = 0x3
    COMMAND_GROUP_RKE = 0x4      # Legacy RKE, preserved for consistency
    COMMAND_GROUP_BANKING = 0x5
    COMMAND_GROUP_CHAT_DATA = 0x6
    COMMAND_GROUP_BLOCKCHAIN = 0x7
    COMMAND_GROUP_LOCKER = 0x8
    COMMAND_GROUP_CHANGE = 0x9
    COMMAND_GROUP_SHARD = 0xA
    COMMAND_GROUP_CROSSOVER = 0xB
    COMMAND_GROUP_RPC = 0xC
    COMMAND_GROUP_FILESYSTEM = 0xD
    COMMAND_GROUP_DKE = 0xF      # Distributed Key Exchange group

# Commands within each group that are relevant for the client's core functions.
# Other commands from codes.go can be added here as more features are built.

class AuthCommand(IntEnum):
    """Commands in COMMAND_GROUP_AUTH"""
    COMMAND_DETECT = 10
    COMMAND_DETECT_SUM = 11
    COMMAND_POWN = 20
    COMMAND_POWN_SUM = 21

class HealingCommand(IntEnum):
    """Commands in COMMAND_GROUP_HEALING"""
    COMMAND_GET_TICKET = 40
    COMMAND_VALIDATE_TICKET = 50
    COMMAND_FIND = 60
    COMMAND_FIX = 80

class DKECommand(IntEnum):
    """Commands in COMMAND_GROUP_DKE"""
    COMMAND_GET_KEY_SHARE = 2  # Matches the command on the RAIDA side

class StatusCommand(IntEnum):
    """Commands in COMMAND_GROUP_STATUS"""
    COMMAND_ECHO = 0x28
    COMMAND_VERSION = 0xEE

    # Status codes returned by Content Servers, as defined in the protocol spec
class CS_STATUS_CODE(IntEnum):
    """Content Server response status codes"""
    SESSION_ESTABLISHED = 250
    STALE_KEY = 251
    # NEW TICKET STATUS CODES ADDED HERE
    ALL_TICKETS_VALID = 241
    ALL_TICKETS_FAILED = 242
    SOME_TICKETS_VALID = 243

# -----------------------------------------------------------------------------
# NEW: Content Server Protocol Constants
# -----------------------------------------------------------------------------
# These constants define the structure of the encrypted payload for Type 6 packets
# sent to the Content Server.

# Lengths of payload components in bytes
CS_PAYLOAD = {
    "CC_INFO_LEN": 7,
    "SESSION_ID_LEN": 8,
    "TICKET_LEN": 4,
    "TOTAL_TICKETS": 25,
    "HMAC_LEN": 32
}

# Calculated total length of the tickets block
CS_PAYLOAD["TICKETS_BLOCK_LEN"] = CS_PAYLOAD["TICKET_LEN"] * CS_PAYLOAD["TOTAL_TICKETS"]    
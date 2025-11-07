# rke_client/wallet/wallet.py

"""
Manages a user's entire collection of CloudCoins, including loading them
from the filesystem, organizing them by status, and providing methods to
select coins for various operations.

This module is the Python equivalent of Go's 'wallet.go' and 'init.go'.
"""

import logging
import os
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# The try-except block for 'toml' is correct. This gracefully handles cases
# where the user has not run 'pip install toml'.
try:
    import toml
except ImportError:
    print("FATAL ERROR: The 'toml' library is required. Please install it using: pip install toml")
    exit(1)

# CORRECTED IMPORT: Use relative imports for intra-package modules.
from .. import config
# CORRECTED IMPORT: Import both CloudCoin and the CoinStatus enum.
from .cloudcoin import CloudCoin, CoinStatus

logger = logging.getLogger(__name__)


class Wallet:
    """
    Represents a user's wallet, managing all associated CloudCoins and their
    locations on the filesystem.
    """
    def __init__(self, name: str):
        self.name: str = name
        self.root_path: Path = config.WALLETS_DIR / name
        self.email: str = ""
        self.password_hash: str = ""
        self.balance: int = 0
        self.coins_by_denomination: Dict[int, List[CloudCoin]] = {}
        self._load_config()

    def _load_config(self):
        """Reads the wallet's config.toml file."""
        config_path = self.root_path / config.WALLET_CONFIG_NAME
        if not config_path.is_file():
            logger.warning(f"Wallet config file not found for '{self.name}'.")
            return
        try:
            with open(config_path, "r") as f:
                w_config = toml.load(f)
                self.email = w_config.get("email", "")
                self.password_hash = w_config.get("passwordhash", "")
        except Exception as e:
            logger.error(f"Failed to parse config for wallet '{self.name}': {e}")

    def load_coins_from_disk(self):
        """Scans all standard subdirectories and parses coin files."""
        logger.info(f"Loading coins for wallet '{self.name}' from disk...")
        self.coins_by_denomination = {denom: [] for denom in config.AllDenominations}
        self.balance = 0

        for folder_name in config.WALLET_FOLDER_NAMES:
            folder_path = self.root_path / folder_name
            if not folder_path.is_dir():
                continue

            for filename in os.listdir(folder_path):
                if not filename.endswith(config.CC_FILE_BINARY_EXTENSION):
                    continue
                try:
                    parts = filename.split('.')
                    if len(parts) != 9: continue
                    
                    whole, sat, _, pown, sn_str = parts[0], parts[1], parts[2], parts[3], parts[4]
                    sn = int(sn_str)
                    denomination = self._get_denomination_from_filename_parts(whole, sat)
                    if denomination is None: continue

                    cc = CloudCoin(sn=sn, denomination=denomination, pownstring=pown)
                    cc.original_filename = filename
                    cc.folder = folder_name
                    
                    if folder_name in [config.BANK_DIR_NAME, config.FRACKED_DIR_NAME]:
                        self._read_full_coin_data(cc)
                        self.coins_by_denomination[denomination].append(cc)
                        self.balance += cc.get_value()
                except Exception as e:
                    logger.warning(f"Could not parse filename '{filename}': {e}")
        
        logger.info(f"Finished loading wallet '{self.name}'. Balance: {self.balance / 100000000:.8f} CC")

    def _read_full_coin_data(self, coin: CloudCoin):
        """Reads the full binary data for a coin and populates its ANs."""
        if not coin.folder or not coin.original_filename: return
        file_path = self.root_path / coin.folder / coin.original_filename
        try:
            with open(file_path, "rb") as f:
                data = f.read(config.CC_BINARY_SIZE)
            
            # Extract ANs from the body (offset 7 = header size for this format)
            ans_data = data[7 : 7 + 400]
            for i in range(config.TOTAL_RAIDA_SERVERS):
                an_bytes = ans_data[i * 16 : (i + 1) * 16]
                coin.set_an(i, an_bytes.hex())
        except Exception as e:
            logger.error(f"Failed to read/parse full data for {file_path}: {e}")

    def get_coins_for_encryption(self, count: int = 1) -> Optional[List[CloudCoin]]:
        """Intelligently selects the best available coin(s) for encryption."""
        candidate_coins = []
        # Prioritize authentic coins from the Bank first
        for denom in sorted(self.coins_by_denomination.keys(), reverse=True):
            for coin in self.coins_by_denomination.get(denom, []):
                if coin.folder == config.BANK_DIR_NAME and coin.grade_status == CoinStatus.AUTHENTIC:
                    candidate_coins.append(coin)
        
        # If not enough, consider Fracked coins
        if len(candidate_coins) < count:
            for denom in sorted(self.coins_by_denomination.keys(), reverse=True):
                for coin in self.coins_by_denomination.get(denom, []):
                    if coin.folder == config.FRACKED_DIR_NAME and coin.grade_status == CoinStatus.FRACKED:
                        candidate_coins.append(coin)
        
        if len(candidate_coins) < count:
            logger.error(f"Not enough high-quality coins in wallet '{self.name}' for encryption. Needed {count}, found {len(candidate_coins)}.")
            return None

        return candidate_coins[:count]

    @staticmethod
    def _get_denomination_from_filename_parts(whole: str, sat: str) -> Optional[int]:
        """Helper to convert filename parts back to a denomination enum value."""
        whole_map = {
            "1": config.DEN_1, "10": config.DEN_10, "100": config.DEN_100,
            "1_000": config.DEN_1_000, "10_000": config.DEN_10_000,
            "100_000": config.DEN_100_000, "1_000_000": config.DEN_1_000_000,
        }
        sat_map = {
            "00_000_001": config.DEN_0_000_000_01, "00_000_010": config.DEN_0_000_000_1,
            "00_000_100": config.DEN_0_000_001, "00_001_000": config.DEN_0_000_01,
            "00_010_000": config.DEN_0_000_1, "00_100_000": config.DEN_0_001,
            "01_000_000": config.DEN_0_01, "10_000_000": config.DEN_0_1,
        }
        if sat == "00_000_000":
            return whole_map.get(whole)
        elif whole == "0":
            return sat_map.get(sat)
        return None
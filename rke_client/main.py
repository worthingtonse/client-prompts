# rke_client/main.py


"""
The main executable entry point for the DKE (Distributed Key Exchange) client.

This script demonstrates how to use the client library to perform the full
Master Flow:
1. Discover the global RAIDA network.
2. Initialize a user wallet.
3. Establish a secure session with a target Content Server.

Usage:
    python -m rke_client.main --wallet <wallet_name> --domain <content_server_domain>
"""

import argparse
import asyncio
import logging
import sys
from pathlib import Path

# Add the project root to the Python path to allow absolute imports
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))


from . import config
from .content_server import session
from .raida import  discovery as raida_discovery
from .wallet.wallet import Wallet

# --- Logging Configuration ---
def setup_logging():
    """Configures basic logging for console output."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - [%(module)s] - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    # You can set a more verbose level for debugging specific modules
    logging.getLogger('rke_client.raida.communicator').setLevel(logging.INFO)
    logging.getLogger('rke_client.crypto.keystore').setLevel(logging.INFO)


# --- Main Application Logic ---
async def main(args):
    """The main asynchronous entry point for the application."""
    print("--- DKE Client Initializing ---")

    # STEP 1: Discover the global RAIDA network from Guardians (once at startup)
    global_network = await raida_discovery.discover_network(coin_id=config.COIN_ID)
    if not global_network:
        print("\nFATAL: Could not discover the global RAIDA network. Aborting.")
        return 1

    print(f"Successfully discovered global RAIDA network with {sum(1 for s in global_network.primary if s)} active servers.")

    # STEP 2: Initialize the user's wallet
    print(f"Loading wallet: '{args.wallet}'")
    user_wallet = Wallet(args.wallet)
    user_wallet.load_coins_from_disk()

    if user_wallet.balance == 0:
        print("\nWARNING: Wallet is empty or no authentic coins were found.")
        # We can still proceed, as some operations might not require coins,
        # but DKE authentication will likely fail.

    # STEP 3: Establish a secure session with the Content Server
    print(f"\nAttempting to establish a secure session with '{args.domain}'...")
    active_session = await session.establish_session(
        domain=args.domain,
        wallet=user_wallet,
        global_network=global_network
    )

    # STEP 4: Check the result and print session details
    if active_session:
        print("\n" + "="*50)
        print("✅ SUCCESS: A secure session has been established!")
        print("="*50)
        print(f"   Key Identifier (KID): {active_session.kid.hex()}")
        print(f"   Session Identifier: {active_session.session_identifier.hex()}")
        print("\n   You can now use this session to send encrypted commands.")
        # In a real application, you would now use 'active_session' to create
        # command packets using protocol.create_command_packet().
        return 0
    else:
        print("❌ FAILED: Could not establish a secure session.")
        print("   Please check the logs above for details on the failure.")
        return 1


# --- Script Execution ---
if __name__ == "__main__":
    # Setup command-line argument parsing
    parser = argparse.ArgumentParser(
        description="DKE Client for establishing secure sessions with a Content Server."
    )
    parser.add_argument(
        "-w", "--wallet",
        type=str,
        required=True,
        help="The name of the wallet to use (e.g., 'default')."
    )
    parser.add_argument(
        "-d", "--domain",
        type=str,
        required=True,
        help="The domain of the Content Server (e.g., 'mail.example.com')."
    )

    # Configure logging
    setup_logging()

    # Parse arguments and run the main async function
    parsed_args = parser.parse_args()
    
    try:
        # asyncio.run() is the standard way to execute the top-level async function
        return_code = asyncio.run(main(parsed_args))
        sys.exit(return_code)
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        sys.exit(1)
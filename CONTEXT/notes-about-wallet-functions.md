I think we need to make some changes. 

The wallet-location.csv file should contain a line for each wallet and not just each location. So if there are three locations and each location has 4 wallets, then the file would have 12 rows. 

The row on the top would be considered the active location and the active wallet. Then, the next time a person starts the program, they would start at the last wallet they were using. 

Indexing would start at zero. 
 {
    "locations": [
      {
        "path": "D:\\CloudCoin\\Wallets",
        "wallets": [
          {"index": 0, "name": "Business", "active": true},
          {"index": 1, "name": "Default", "active": false}
        ]
      },
      {
        "path": "E:\\USB\\CloudCoin",
        "wallets": [
          {"index": 2, "name": "Savings", "active": false}
        ]
      }
    ]
  }
We need to add a command called "Show Locations and Wallets" so that the user could see the index number of each wallet. 

Then we would remove the "Set active wallet location" command. 


  Summary - Rename Wallet Command Implemented

  🎯 New Command: Rename Wallet (Menu Option 5)

  Features:
  - Allows renaming any wallet (including active wallet)
  - Renames the physical directory on disk
  - Updates wallet-locations.csv automatically

  🛡️ Name Sanitization Rules:

  1. Leading characters removed:
    - . (periods) - prevents hidden files
    - $ (dollar signs) - prevents Windows shares
  2. Character replacements:
    - Spaces → Hyphens (My Wallet → My-Wallet)
  3. Invalid characters removed:
    - / \ : * ? " < > |
  4. Trailing cleanup:
    - Removes trailing spaces and hyphens
  5. Fallback:
    - If name becomes empty after sanitization → "Wallet"

  🔍 Validation:

  - ✅ Cannot rename to empty name
  - ✅ Cannot rename if wallet with same name already exists in location
  - ✅ Shows sanitized name before applying if changed
  - ✅ Physically renames directory on disk
  - ✅ Updates CSV configuration



3. Changing locations and wallets would be done together and would involve Changing the position of the wallet listed in the wallet-location.csv to the top of the list so the program know which wallet is active. 

4. Instead of swithing locations, they would switch wallets that are in those locations. 

5. The path will need to be validated because someone may unplug their usb drive. Then they would get an error that says the location is not available and perhaps it is a USB drive that needs to be plugged in.

6. Create Wallet comomand
If the user wanted to create a new wallet, the new wallet would be created in the location that the active wallet is in. We may need to change the "Show current wallet location" to show both the wallet and the location if it doesn't already to that. 

7. Deleting Wallets:
The Default Wallet in the Default location cannot be deleted.
wallets cannot be deletet unless they are empty. 
The Default wallet in other locations can be deleted. If all the wallets in a location are deleted, the location will be deleted too. 

2. ✅ Default wallet creation on first run

  - Added automatic detection of missing wallet-locations.csv
  - Creates default wallet structure at program initialization
  - Default wallet path: {exe_dir}/CloudCoin/Pro/Data/Wallets/Default
  - Includes all 19 required folders + transactions.csv
  - Automatically adds to wallet-locations.csv

  3. ✅ Error handling for missing wallets

  - cmd_show_wallet_balance() now validates:
    - Active wallet exists
    - Wallet directory path exists
    - Bank directory exists
    - Fracked directory exists
  - Returns CC_ERROR_INVALID_PATH instead of displaying zeros when wallet doesn't exist
  - Shows clear error messages indicating which path is missing

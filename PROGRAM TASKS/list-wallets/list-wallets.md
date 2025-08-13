# List Wallets

## 1. Overview
The list wallets command scans the wallets directory and returns information about all valid wallets found. It reads each wallet's contents to provide current balance and status information.

## 2. Return Value
The function returns an array of wallet objects containing wallet information, or an error as listed in the error table below.

## 3. Main Function: List Wallets

### 3.1. Parameters

| Name | Type | Description |
|---|---|---|
| $wallets_path | string | The path to the Wallets folder such as: "C:\Users\User\CloudCoin_Pro\Wallets\" |

### 3.2. Return Value
Type: Array of wallet objects
Description: List of all valid wallets with their current information

## 4. Execution Logic

### 4.1. Validate Input Parameters
1. Validate the $wallets_path parameter to ensure the path exists and is accessible.
2. Verify that the specified path is a directory.
3. Check that the application has read permissions for the directory.

### 4.2. Scan Wallet Directories
1. Read all subdirectories within the $wallets_path.
2. Filter out any directories that are collections (utility directories, not actual wallets).
3. For each potential wallet directory, validate that it contains the required wallet structure.

### 4.3. Validate Wallet Structure
For each directory found, verify it contains the required wallet structure as defined in wallet-folder-structure.md:
- Required files: transactions.csv, config.toml
- Required folders: Bank, Fracked, Import, Export, Receipts (minimum)
- Complete folder structure as specified in the wallet structure documentation

### 4.4. Calculate Wallet Contents
For each valid wallet:
1. Calculate the true balance by summing coin values in Bank and Fracked folders.
2. Read coin file values by extracting the number from the beginning of each filename (up to the first space).
3. Count the total number of coin files in the wallet.
4. Update the wallet's internal balance information.

### 4.5. Construct Wallet Information
For each wallet, create a wallet object containing:
- **Name**: The wallet directory name
- **Balance**: Current total balance (sum of Bank + Fracked folders)
- **Coin Count**: Total number of coin files
- **Last Modified**: Timestamp of most recent wallet activity
- **Status**: Wallet status (active, locked, etc.)

### 4.6. Return Results
Return an array containing all valid wallet objects found in the wallets directory.

## 5. Wallet Directory Structure
The function expects to find wallets with this standard structure:

```
$wallets_path/
├── Default/                    (may be skipped as it's a collection)
└── user_wallet_name/
    ├── Bank/
    │   ├── 1,000 CloudCoin #7998 'From Ron'.bin
    │   └── 0.001 CloudCoin #89269 'Task 231'.bin
    ├── Fracked/
    │   └── 0.0000-001 CloudCoin #879398 'j'.bin
    ├── Corrupted/
    ├── Counterfeit/
    ├── Duplicates/
    ├── Encryption_Failed/
    ├── Errored/
    ├── Export/
    ├── Grade/
    ├── Import/
    ├── Imported/
    ├── Limbo/
    ├── Lockered/
    ├── Pending/
    ├── Receipts/
    ├── Sent/
    ├── Suspect/
    ├── Trash/
    ├── Withdrawn/
    ├── transactions.csv
    └── config.toml
```

## 6. Wallet Object Structure
Each wallet object in the returned array contains:

| Field | Type | Description |
|-------|------|-------------|
| name | string | The wallet directory name |
| balance | float | Current total balance in CloudCoins |
| coin_count | integer | Total number of coin files |
| last_modified | datetime | Timestamp of most recent activity |
| status | string | Wallet status (active, locked, error, etc.) |
| path | string | Full path to the wallet directory |

## 7. Collection Filtering
The function must filter out collection directories that are not actual wallets:
- Skip directories that contain utility or system files
- Skip directories that don't have the proper wallet structure
- Skip directories marked as collections in the system

## 8. Balance Calculation Rules
Following the established best practices:
1. **Never Delete Files**: Only read coin files, never modify or delete them
2. **Calculate True Balance**: Sum values from Bank and Fracked folders only
3. **Read Coin Values**: Extract numeric value from filename (first number before space)
4. **Handle Errors Gracefully**: Skip corrupted files but log issues

## 9. Error Handling

| Error Code | Description |
|:-----------|:------------|
| ERROR:PATH-INVALID | The specified wallets path is invalid or does not exist |
| ERROR:CANNOT-ACCESS-DIRECTORY | The application lacks permissions to read the wallets directory |
| ERROR:NOT-A-DIRECTORY | The specified path is not a directory |
| ERROR:WALLET-CORRUPTED | A wallet directory exists but is missing required structure |
| ERROR:PERMISSION-DENIED | Insufficient permissions to read wallet contents |
| ERROR:FILE-SYSTEM-ERROR | General file system error occurred during scanning |

## 10. Best Practices Compliance

This function follows the established best practices:

- **Never Delete Files**: Only reads wallet information, never modifies files
- **Work Out of RAM**: Processes wallet information in memory for performance
- **Consistent Folder Structure**: Expects and validates standard wallet layout
- **Data-Driven Approach**: Focuses on reading and returning wallet data
- **Error Recovery**: Handles various failure scenarios gracefully
- **Detailed Logging**: Can log wallet scanning operations for debugging

## 11. Integration Notes

- This function provides the foundation for wallet management interfaces
- Results can be used to populate wallet selection lists
- Balance information is calculated fresh each time for accuracy
- Function is read-only and safe to call frequently
- Can be extended to include additional wallet metadata as needed
- Wallet structure validation follows the specification in wallet-folder-structure.md
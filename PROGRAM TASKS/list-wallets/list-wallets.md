# List Wallets

## 1. Overview
This document specifies the list-wallets() function. This command scans the wallets directory and returns a simple list of all valid wallet names found. This is used for wallet selection interfaces and initial wallet discovery.

## 2. Return Value
The function returns a JSON array containing wallet names as strings, or an error as listed in the error table below.

## 3. Main Function: List Wallets

### 3.1. Parameters

| Name | Type | Description |
|---|---|---|
| $wallets_path | string | The path to the Wallets folder such as: "C:\Users\User\CloudCoin\Pro\Wallets\" |

### 3.2. Return Value
**Type**: JSON array of strings  
**Description**: Simple list of wallet names found in the wallets directory

### 3.3. Example Function Call
```bash
list-wallets "C:\Users\User\CloudCoin\Pro\Wallets\"
```

### 3.4. Example JSON Output
```json
[
  "Default",
  "MyPersonalWallet", 
  "BusinessWallet",
  "TestWallet"
]
```

## 4. Execution Logic

### 4.1. Validate Input Parameters
1. Validate the $wallets_path parameter to ensure the path exists and is accessible.
2. Verify that the specified path is a directory.
3. Check that the application has read permissions for the directory.

### 4.2. Scan Wallet Directories
1. Read all subdirectories within the $wallets_path.
2. Filter out system/utility directories that are not actual wallets (see Collection Filtering section below).
3. For each potential wallet directory, validate that it contains the required wallet structure.

### 4.3. Validate Wallet Structure
For each directory found, verify it contains the required wallet structure as defined in wallet-folder-structure.md:
- Required files: transactions.csv, config.toml
- Required folders: Bank, Fracked, Import, Export, Receipts (minimum)
- Complete folder structure as specified in the wallet structure documentation

### 4.4. Extract Wallet Names
For each valid wallet directory:
1. Extract the directory name (this becomes the wallet name)
2. Add the wallet name to the results array

### 4.5. Return Results
Return a JSON array containing only the wallet names as strings.

## 5. Wallet Directory Structure
The function expects to find wallets with this standard structure:

```
$wallets_path/
├── Default/                    ← INCLUDE (default user wallet)
│   ├── Bank/
│   ├── Fracked/
│   ├── transactions.csv
│   ├── config.toml
│   └── [other wallet folders...]
├── Templates/                  ← SKIP (template collection)
├── .config/                    ← SKIP (hidden system directory)
├── MyPersonalWallet/           ← INCLUDE (valid user wallet)
│   ├── Bank/
│   ├── Fracked/
│   ├── transactions.csv
│   ├── config.toml
│   └── [other wallet folders...]
├── BusinessWallet/             ← INCLUDE (valid user wallet)
│   ├── Bank/
│   ├── Fracked/
│   ├── transactions.csv
│   ├── config.toml
│   └── [other wallet folders...]
└── TestWallet/                 ← INCLUDE (valid user wallet)
    ├── Bank/
    ├── Fracked/
    ├── transactions.csv
    ├── config.toml
    └── [other wallet folders...]
```

## 6. Output Format

The function returns a simple JSON array containing wallet names:

```json
[
  "Default",
  "MyPersonalWallet", 
  "BusinessWallet",
  "TestWallet"
]
```

### 6.1. JSON Structure
- **Type**: Array of strings
- **Content**: Wallet directory names only
- **Format**: Standard JSON array format
- **Encoding**: UTF-8

## 7. Collection Filtering

The function must filter out system/utility directories that are not actual user wallets:

### 7.1. What are Collections?
Collections are special directories in the Wallets folder that serve system purposes and are NOT user wallets:

| Directory Name | Purpose | Why Skip It |
|----------------|---------|-------------|
| **"Templates"** | Wallet creation templates | Contains templates, not actual coins |
| **"System"** | System configuration files | System directory |
| **"Backup"** | Automated backup storage | Contains backups, not active wallets |
| **".config"** | Hidden configuration directory | System configuration |
| **"Cache"** | Temporary files and cache | Temporary storage |

### 7.2. Collection Detection Rules
A directory should be considered a collection (and skipped) if:

1. **Directory name matches known collection names**: "Templates", "System", "Backup", "Cache"
2. **Directory name starts with dot**: ".config", ".cache", etc.
3. **Missing required wallet files**: No transactions.csv or config.toml
4. **Contains system markers**: Special files indicating it's a system directory

### 7.3. Implementation Logic
```
for each directory in wallets_path:
    if directory_name in ["Templates", "System", "Backup", "Cache"]:
        skip this directory
    else if directory_name starts with ".":
        skip this directory  
    else if missing transactions.csv OR missing config.toml:
        skip this directory
    else:
        include as valid wallet
```

### 7.4. Example Directory Structure
```
C:\Users\User\CloudCoin\Pro\Wallets\
├── Default/                    ← INCLUDE (default user wallet)
├── Templates/                  ← SKIP (template collection)  
├── .config/                    ← SKIP (hidden system directory)
├── MyPersonalWallet/           ← INCLUDE (valid user wallet)
├── BusinessWallet/             ← INCLUDE (valid user wallet)
└── TestWallet/                 ← INCLUDE (valid user wallet)
```

**Result**: `["Default", "MyPersonalWallet", "BusinessWallet", "TestWallet"]` would be returned.

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

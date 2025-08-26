# Create Wallet

## 1. Overview
The create wallet command writes the standard folders and files into the folder specified. It creates a complete wallet structure with all required directories and configuration files.

## 2. Return Value
The variable that is returned will be either "success" or an error as listed in the error table below.

## 3. Main Function: Create Wallet

### 3.1. Parameters

| Name | Type | Description |
|---|---|---|
| $wallets_path | string | The path to the Wallets directory such as: "C:\Users\User\CloudCoin\Pro\Wallets\" |
| $wallet_name | string | The name of the folder to become the wallet. Must not contain any illegal characters for file names. |

### 3.2. Return Value
**Type**: string  
**Description**: Results of this function - either "success" or error code

## 4. Execution Logic

### 4.1. Validate Input Parameters
1. Validate the $wallets_path parameter to ensure the path exists and is accessible.
2. Validate the $wallet_name parameter to ensure it does not contain any characters that are not allowed for folder names.
3. Check that a wallet with that name does not already exist in the wallets directory.

### 4.2. Create Wallet Directory Structure
4. Create the wallet directory: `$wallets_path/$wallet_name`
5. Create all required subdirectories within the wallet folder.
6. Create required configuration files with proper initial content.

### 4.3. Write Wallet Structure
Create the following complete structure in the specified path:

```python
$wallets_path/
└── $wallet_name/
    ├── Bank/                       # Authenticated coins ready for use
    ├── Corrupted/                  # Files that couldn't be read properly
    ├── Counterfeit/                # Coins that failed authentication
    ├── Duplicates/                 # Duplicate coin files found during import
    ├── Encryption_Failed/          # Coins with broken encryption keys
    ├── Errored/                    # Coins that encountered processing errors
    ├── Export/                     # Coins prepared for export to other systems
    ├── Fracked/                    # Partially authenticated coins
    ├── Grade/                      # Coins after grading/authentication process
    ├── Import/                     # New coins waiting to be processed
    ├── Imported/                   # Coins that have been successfully imported
    ├── Limbo/                      # Coins with uncertain authentication status
    ├── Lockered/                   # Coins that have been placed in RAIDA lockers
    ├── Pending/                    # Coins waiting for processing
    ├── Receipts/                   # Transaction receipt files
    ├── Sent/                       # Coins that have been sent to others
    ├── Suspect/                    # Coins with questionable authenticity
    ├── Trash/                      # Deleted or rejected files
    ├── Withdrawn/                  # Coins withdrawn from lockers or external sources
    ├── config.toml                 # Wallet configuration file
    └── transactions.csv            # Transaction history log
```

### 4.4. Create Required Files

#### 4.4.1. Create config.toml
Create `config.toml` file with default wallet configuration:

```toml
[wallet]
name = "$wallet_name"
version = "1.0.0"
created = "YYYY-MM-DDTHH:MM:SSZ"

[settings]
auto_backup = true
encryption_enabled = false
default_timeout = 30000

[raida]
default_timeout = 5000
retry_attempts = 3

[logging]
level = "info"
max_file_size = "10MB"
max_files = 5
```

#### 4.4.2. Create transactions.csv
Create `transactions.csv` file with proper headers:

```csv
Symbol,Task ID,Date & Time,Remarks,Deposit,Withdraw,Description,Balance
```

The file should contain only the header row initially, with no transaction records.

**Task ID Format**: When transactions are added to this file, Task IDs should follow the format: `"command date time microseconds timezone"`

**Examples of Task IDs**:
- `"deposit Aug-19-2025 2:24pm 2321 PST"`
- `"withdraw Aug-19-2025 3:15pm 1847 PST"`
- `"transfer Aug-19-2025 4:30pm 5692 EST"`
- `"pown Aug-18-2025 2:24pm 2321 PST"`

## 5. Detailed Implementation Steps

### 5.1. Parameter Validation
```
1. Check if $wallets_path exists and is a directory
2. Verify write permissions on $wallets_path
3. Validate $wallet_name:
   - No illegal characters: \ / : * ? " < > |
   - Not empty or just whitespace
   - Maximum length (e.g., 255 characters)
   - Not reserved names (CON, PRN, AUX, NUL, etc.)
4. Check if wallet already exists: $wallets_path/$wallet_name
```

### 5.2. Directory Creation
```
1. Create main wallet directory: $wallets_path/$wallet_name
2. Create all required subdirectories (see structure above)
3. Set appropriate permissions on all created directories
```

### 5.3. File Creation
```
1. Create config.toml with wallet-specific configuration
2. Create transactions.csv with proper CSV headers
3. Set appropriate file permissions
4. Verify all files were created successfully
```

### 5.4. Validation
```
1. Verify all directories were created
2. Verify all required files exist and are readable
3. Validate file contents are correct
4. Return success status
```

## 6. File Content Templates

### 6.1. config.toml Template
```toml
[wallet]
name = "{wallet_name}"
version = "1.0.0"
created = "{current_timestamp}"

[settings]
auto_backup = true
encryption_enabled = false
default_timeout = 30000

[raida]
default_timeout = 5000
retry_attempts = 3

[logging]
level = "info"
max_file_size = "10MB"
max_files = 5
```

### 6.2. transactions.csv Template
```csv
Symbol,Task ID,Date & Time,Remarks,Deposit,Withdraw,Description,Balance
```

**Important**: The Task ID column will contain task identifiers in the format: `"command date time microseconds timezone"` when transactions are recorded.

## 7. Error Handling

| Error Code | Description |
|:-----------|:------------|
| ERROR:PATH-INVALID | The specified wallets path is invalid or does not exist. |
| ERROR:CANNOT-FIND-PARENT-FOLDER | The specified wallets directory does not exist. |
| ERROR:CANNOT-WRITE-TO-PARENT | The application lacks permissions to write files to the wallets directory. |
| ERROR:FOLDER-NAME-USES-PROHIBITED-CHARACTERS | The wallet name contains characters that are not allowed in folder names. |
| ERROR:WALLET-ALREADY-EXISTS | A wallet with that name already exists. |
| ERROR:CANNOT-CREATE-DIRECTORY | Failed to create the wallet directory structure. |
| ERROR:CANNOT-CREATE-CONFIG-FILE | Failed to create the config.toml file. |
| ERROR:CANNOT-CREATE-TRANSACTIONS-FILE | Failed to create the transactions.csv file. |
| ERROR:INSUFFICIENT-PERMISSIONS | Insufficient permissions to create wallet files and directories. |
| ERROR:DISK-SPACE-INSUFFICIENT | Not enough disk space to create the wallet. |

## 8. Wallet Name Validation Rules

### 8.1. Prohibited Characters
The wallet name must not contain these characters:
- `\` (backslash)
- `/` (forward slash)  
- `:` (colon)
- `*` (asterisk)
- `?` (question mark)
- `"` (double quote)
- `<` (less than)
- `>` (greater than)
- `|` (pipe)

### 8.2. Reserved Names
The wallet name must not be any of these reserved system names:
- CON, PRN, AUX, NUL
- COM1, COM2, COM3, COM4, COM5, COM6, COM7, COM8, COM9
- LPT1, LPT2, LPT3, LPT4, LPT5, LPT6, LPT7, LPT8, LPT9

### 8.3. Additional Rules
- Minimum length: 1 character
- Maximum length: 255 characters
- Cannot start or end with spaces
- Cannot be only dots (. or ..)

## 9. Integration Notes

- This function creates wallets compatible with all other wallet management functions
- The created wallet structure follows the specification in wallet-folder-structure.md
- Transaction log format follows the updated specification with new Task ID format
- Configuration file format is standard TOML for easy parsing
- Function is atomic - either creates complete wallet or fails cleanly
- Can be extended to support custom wallet templates or configurations
- Task IDs generated by operations will use the human-readable format: "command date time microseconds timezone"

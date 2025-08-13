# Wallet Folder Structure Specification

This document defines the standard folder structure that all CloudCoin wallets must follow. This specification ensures consistency across all wallet implementations and enables proper functionality of wallet management commands.

## Complete Wallet Structure

Every CloudCoin wallet must contain the following structure:

```
wallet_name/
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
├── transactions.csv            # Transaction history log
└── config.toml                 # Wallet configuration file
```

## Folder Purposes and Usage

### Primary Storage Folders
| Folder | Purpose | Contains |
|--------|---------|----------|
| **Bank** | Active, authenticated coins | Coins that passed full authentication and are ready for transactions |
| **Fracked** | Partially authenticated coins | Coins that passed partial authentication (13+ RAIDA responses) |

### Import/Export Folders
| Folder | Purpose | Contains |
|--------|---------|----------|
| **Import** | Incoming coins | New coin files dropped by users for processing |
| **Imported** | Successfully processed imports | Coins that have been successfully imported and processed |
| **Export** | Outgoing coins | Coins prepared for export or sending to others |
| **Sent** | Completed transfers | Coins that have been successfully sent to recipients |
| **Withdrawn** | External withdrawals | Coins withdrawn from RAIDA lockers or other external sources |

### Processing Folders
| Folder | Purpose | Contains |
|--------|---------|----------|
| **Pending** | Awaiting processing | Coins in queue for authentication or other processing |
| **Grade** | Post-authentication | Coins that have completed the grading/authentication process |
| **Suspect** | Questionable coins | Coins with uncertain or suspicious status |
| **Limbo** | Unknown status | Coins where authentication status cannot be determined |

### Error and Rejection Folders
| Folder | Purpose | Contains |
|--------|---------|----------|
| **Counterfeit** | Failed authentication | Coins that failed RAIDA authentication completely |
| **Corrupted** | Unreadable files | Files that cannot be parsed or read properly |
| **Encryption_Failed** | Broken encryption | Coins with corrupted or invalid encryption keys |
| **Errored** | Processing errors | Coins that encountered errors during processing |
| **Duplicates** | Duplicate detection | Duplicate coin files found during import operations |
| **Trash** | Rejected items | Deleted files and permanently rejected items |

### Special Purpose Folders
| Folder | Purpose | Contains |
|--------|---------|----------|
| **Lockered** | RAIDA locker storage | Coins that have been placed in RAIDA lockers for safekeeping |
| **Receipts** | Transaction records | Receipt files documenting all wallet transactions |

## Required Files

### transactions.csv
- **Purpose**: Complete transaction history for the wallet
- **Format**: CSV with columns as defined in transaction-log.md
- **Location**: Root of wallet directory
- **Required**: Yes - every wallet must have this file

### config.toml
- **Purpose**: Wallet configuration and settings
- **Format**: TOML configuration file
- **Location**: Root of wallet directory  
- **Required**: Yes - contains wallet-specific settings

## Folder Creation Rules

### Mandatory Folders
These folders **must** exist in every wallet:
- Bank
- Fracked  
- Import
- Export
- Receipts
- Trash

### Auto-Created Folders
These folders are created automatically when needed:
- Corrupted (when corrupted files are encountered)
- Counterfeit (when counterfeit coins are detected)
- Duplicates (when duplicate files are found)
- Encryption_Failed (when encryption issues occur)
- Errored (when processing errors happen)
- Grade (during authentication processes)
- Imported (after successful imports)
- Limbo (when authentication is uncertain)
- Lockered (when using RAIDA locker features)
- Pending (during processing operations)
- Sent (after successful transfers)
- Suspect (when suspicious coins are found)
- Withdrawn (after withdrawal operations)

## Validation Requirements

### For Wallet Recognition
A directory is considered a valid wallet if it contains:
1. **transactions.csv** file
2. **config.toml** file  
3. **Bank** folder
4. **Fracked** folder

### For Wallet Operations
For full wallet functionality, all folders should exist or be creatable by the application.

## Coin File Movement Rules

### Coin Lifecycle Flow
```
Import → Pending → Grade → (Bank | Fracked | Counterfeit | Limbo)
                           ↓
Export ← Sent ← (Bank | Fracked)
                           ↓
Lockered ↔ (Bank | Fracked)
                           ↓
Withdrawn → Import (for re-processing)
```

### Error Handling Flow
```
Any Stage → (Corrupted | Errored | Encryption_Failed)
Import → Duplicates (if duplicate detected)
Any Stage → Trash (if permanently rejected)
```

## Best Practices

### File Management
- **Never delete folders**: Create all folders even if empty
- **Move, don't delete**: Files are moved between folders, never deleted
- **Maintain structure**: Always preserve the standard folder structure
- **Log movements**: Record all file movements in transaction logs

### Performance Considerations
- **Index frequently used folders**: Bank and Fracked folders accessed most often
- **Batch operations**: Process multiple files together when possible
- **Clean up periodically**: Archive old receipts and transaction logs if needed

### Security Considerations
- **Protect Bank and Fracked**: These folders contain active coins
- **Secure config.toml**: Contains sensitive wallet settings
- **Backup transactions.csv**: Critical for transaction history

## Implementation Notes

### For Command Developers
- Always validate wallet structure before operations
- Create missing folders as needed during operations
- Follow the coin movement rules strictly
- Update transactions.csv for all coin movements

### For Wallet Management
- Use this structure for wallet creation (create-wallet command)
- Validate structure during wallet loading (list-wallets command)
- Maintain structure integrity during all operations

This standardized structure ensures that all CloudCoin wallets are consistent, predictable, and fully functional across all implementations and platforms.
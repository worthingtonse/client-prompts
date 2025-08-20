# Locations File Format Specification

This document defines the format and structure of location configuration files used by CloudCoin Pro to manage data storage locations. This specification ensures consistency across all location management functions and enables proper functionality of location management commands.

## File Overview

CloudCoin Pro uses multiple files to track and manage data locations within the installation directory:

```
D:/CloudCoin/Pro/
├── locations.csv               # Primary location configuration
├── last-export-folder-locations-dropdown.txt  # Recent export folders
├── Wallets/                    # Wallet storage locations
├── program-config.txt          # Main program configuration
├── guardians.csv               # Guardian server list
├── root-hints.csv              # DNS root hint servers
├── raidas-ips.csv              # RAIDA server IP configuration
└── [other configuration files...]
```

## Primary Location File

### locations.csv (Simplified Format)

**Format**: CSV with headers  
**Encoding**: UTF-8  
**Purpose**: Simple location configuration with only essential, non-calculated data

```csv
path,type
D:\CloudCoin\Pro\Wallets,local
C:\Users\User\Documents\CloudCoin\Backup,local
E:\USB_Backup\CloudCoin\Data,usb
\\NetworkDrive\CloudCoin\Shared,network
```

#### CSV Column Definitions

| Column | Type | Required | Description |
|--------|------|----------|-------------|
| path | string | Yes | Absolute file system path |
| type | enum | No | Location type for future use (optional) |

#### Required CSV Structure
- **Header row**: Must contain column names as specified above
- **Path column**: First column must be the absolute file system path
- **Type column**: Optional, for future use
- **Order matters**: First location in file is the default/primary location

#### Cross-Platform Path Examples
```csv
path,type
# Windows paths
D:\CloudCoin\Pro\Wallets,local
C:\Users\%USERNAME%\Documents\CloudCoin\Backup,local
\\server\share\CloudCoin\Data,network

# Linux paths  
/home/$USER/cloudcoin/wallets,local
/mnt/usb/cloudcoin/backup,usb
/media/external/cloudcoin,usb

# Mac paths
/Users/$USER/CloudCoin/Wallets,local
/Volumes/USB/CloudCoin/Data,usb
/Volumes/NetworkDrive/CloudCoin,network

# Universal paths (using environment variables)
%USERPROFILE%\Documents\CloudCoin\Wallets,local
$HOME/cloudcoin/wallets,local
```

### last-export-folder-locations-dropdown.txt

**Format**: Plain text file with one folder per line  
**Purpose**: Track recently used export folder locations

```
C:\Users\User\Documents\CloudCoin\Exports
C:\Users\User\Desktop\CloudCoin_Backup
D:\CloudCoin\Exports
E:\USB_Exports\CloudCoin
```

#### Format Rules
- **One folder per line**: Each line contains a single export folder path
- **Most recent first**: First line is the most recently used folder
- **Maximum entries**: Typically limited to 10 most recent folders
- **Absolute paths**: All paths should be absolute
- **Auto-cleanup**: Invalid paths may be automatically removed

## Location Types (Future Use)

### Location Type Enums
| Type | Description | Detection Method |
|------|-------------|------------------|
| **local** | Local file system path | Auto-detected by path analysis |
| **usb** | USB drive or removable media | Auto-detected by mount point |
| **network** | Network share or mapped drive | Auto-detected by UNC/network path |
| **cloud** | Cloud storage mount point | Auto-detected by known cloud paths |

**Note**: Type field is optional and for future use. The `list-locations` function will auto-detect types regardless of what's stored in the CSV.

## Cross-Platform Path Handling

### Environment Variable Support
| Platform | Variable | Example |
|----------|----------|---------|
| Windows | `%USERPROFILE%` | `%USERPROFILE%\Documents\CloudCoin` |
| Windows | `%USERNAME%` | `C:\Users\%USERNAME%\CloudCoin` |
| Linux/Mac | `$HOME` | `$HOME/cloudcoin/wallets` |
| Linux/Mac | `$USER` | `/home/$USER/cloudcoin` |

### Platform-Specific Defaults

#### Windows Default
```csv
path,type
D:\CloudCoin\Pro\Wallets,local
%USERPROFILE%\Documents\CloudCoin\Backup,local
```

#### Linux Default
```csv
path,type
/opt/cloudcoin/wallets,local
$HOME/cloudcoin/backup,local
```

#### Mac Default
```csv
path,type
/Applications/CloudCoin/Wallets,local
$HOME/CloudCoin/Backup,local
```

## Validation Rules

### CSV Format Validation
- **Header required**: CSV must have proper column headers
- **Path uniqueness**: No duplicate paths allowed
- **Path format**: Must be valid file system paths

### Path Validation
- **Absolute paths required**: All paths must be absolute file system paths
- **Environment variables**: Support platform-specific environment variables
- **Reserved characters**: Handle platform-specific reserved characters appropriately

### Data Type Validation
- **Path field**: UTF-8 encoded strings, platform-appropriate separators
- **Type field**: Optional enum values (case insensitive)

## Default Configuration Creation

### When No Configuration Exists
Create `locations.csv` with platform-appropriate default:

#### Windows
```csv
path,type
D:\CloudCoin\Pro\Wallets,local
```

#### Linux
```csv
path,type
/opt/cloudcoin/wallets,local
```

#### Mac
```csv
path,type
/Applications/CloudCoin/Wallets,local
```

## Error Handling

### Missing Files
- **No locations.csv**: Create default configuration automatically
- **Corrupted CSV**: Attempt to parse valid rows, create backup of corrupted file
- **Permission denied**: Report specific permission error with guidance

### Invalid Data
- **Malformed CSV**: Skip invalid rows, log warnings, continue with valid entries
- **Invalid paths**: Skip invalid paths, log warnings
- **Missing required columns**: Use default values for missing optional columns

## CSV File Operations

### Reading Configuration
1. Check if locations.csv exists
2. Parse CSV headers and validate required columns
3. Process each row and validate path format
4. Return ordered list of locations (first = primary)

### Writing Configuration
1. Create temporary CSV file
2. Write header row with required columns
3. Write each location row with proper escaping
4. Atomically replace original file
5. Verify written file can be read back

### Backup Strategy
- **Pre-modification backup**: Create `locations.csv.bak` before changes
- **Atomic writes**: Write to `locations.csv.tmp`, then rename
- **Validation**: Verify written file can be parsed correctly

## Best Practices

### File Management
- **Keep it simple**: Store only essential, non-calculated data
- **Order matters**: First location is primary/default
- **Cross-platform**: Use environment variables when possible
- **No calculated fields**: Let functions calculate accessibility, size, etc.

### CSV Handling
- **Proper escaping**: Escape commas and quotes in path strings
- **UTF-8 encoding**: Always use UTF-8 encoding for international characters
- **Line endings**: Handle both LF and CRLF line endings
- **Minimal columns**: Keep only path and optional type

### Performance Considerations
- **Lightweight file**: Minimal data means fast parsing
- **No file updates**: File doesn't change during normal operations
- **Real-time calculation**: All dynamic data calculated by functions

## Integration Notes

### For Location Management Commands
- Always validate CSV structure before operations
- Read locations.csv from D:/CloudCoin/Pro/ directory
- Create default configuration if none exists
- Handle CSV parsing errors gracefully
- Calculate all dynamic data (accessibility, size, etc.) in real-time

### For list-locations Function
- Read simple CSV with path and optional type
- Calculate all dynamic information:
  - Active status (based on current usage)
  - Last used (from file system timestamps)
  - Accessibility (by attempting access)
  - Size (by scanning directories)
  - Label (from folder name)
  - Detailed type detection (auto-detect regardless of CSV type)

### Separation of Concerns
- **CSV file**: Static configuration only
- **Functions**: Dynamic calculations and status
- **GUI**: Displays combined static + calculated data

This simplified format ensures that the locations.csv file contains only essential, non-calculated data while allowing the list-locations function to provide rich, real-time information by calculating dynamic data on demand.
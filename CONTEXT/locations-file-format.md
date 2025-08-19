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

### locations.csv (Primary Format)

**Format**: CSV with headers  
**Encoding**: UTF-8  
**Purpose**: Primary location configuration with metadata and active location tracking

```csv
path,active,type,label,last_used,accessible,size_mb,description
D:\CloudCoin\Pro\Wallets,true,local,Default Location,2025-01-15T10:30:00Z,true,1250.5,Primary wallet storage
C:\Users\User\Documents\CloudCoin\Backup,false,local,Backup Location,2025-01-14T15:20:00Z,true,850.2,Backup wallet location
E:\USB_Backup\CloudCoin\Data,false,usb,USB Backup,2025-01-13T09:15:00Z,false,0,External USB drive
\\NetworkDrive\CloudCoin\Shared,false,network,Network Share,2025-01-10T14:30:00Z,true,2100.8,Shared network storage
```

#### CSV Column Definitions

| Column | Type | Required | Description |
|--------|------|----------|-------------|
| path | string | Yes | Absolute file system path |
| active | boolean | Yes | Whether this is the active location |
| type | enum | No | Location type: local, usb, network, cloud |
| label | string | No | Human-readable location name |
| last_used | datetime | No | Last access timestamp (ISO 8601) |
| accessible | boolean | No | Whether location is currently accessible |
| size_mb | float | No | Storage size in megabytes |
| description | string | No | Location description |

#### Required CSV Structure
- **Header row**: Must contain column names as specified above
- **Path column**: First column must be the absolute file system path
- **Active column**: Second column must be boolean indicating active status
- **Additional columns**: Optional but recommended for enhanced functionality

#### Path Format Examples
```csv
path,active,type,label,last_used,accessible,size_mb,description
# Windows local paths
D:\CloudCoin\Pro\Wallets,true,local,Primary Location,2025-01-15T10:30:00Z,true,1250.5,Main wallet storage
C:\Users\username\Documents\CloudCoin\Backup,false,local,Backup Storage,2025-01-14T15:20:00Z,true,850.2,Backup location

# Windows network paths
\\server\share\CloudCoin\Data,false,network,Network Storage,2025-01-13T09:15:00Z,true,2100.8,Shared network drive
\\192.168.1.100\cloudcoin\shared,false,network,IP Share,2025-01-12T14:30:00Z,false,0,Direct IP network share

# Unix/Linux paths
/home/username/cloudcoin/wallets,true,local,Home Directory,2025-01-15T10:30:00Z,true,500.3,User home storage
/mnt/usb/cloudcoin/backup,false,usb,USB Backup,2025-01-14T08:45:00Z,false,0,External USB storage

# Mac paths
/Users/username/CloudCoin/Wallets,true,local,User Wallets,2025-01-15T10:30:00Z,true,750.8,Main wallet folder
/Volumes/USB/CloudCoin/Data,false,usb,USB Drive,2025-01-13T16:20:00Z,false,0,External USB volume
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

## Location Types and Classification

### Location Types
| Type | Description | Detection Criteria |
|------|-------------|-------------------|
| **local** | Local file system path | Local drive letters (C:\, D:\) or home directories |
| **usb** | USB drive or removable media | Removable media paths or mount points |
| **network** | Network share or mapped drive | UNC paths (\\server\share) or network mounts |
| **cloud** | Cloud storage mount point | Cloud service mount directories |

### Automatic Type Detection
| Path Pattern | Detected Type | Examples |
|-------------|---------------|----------|
| `C:\`, `D:\`, etc. | `local` | `C:\Users\user\Wallets` |
| `\\server\share` | `network` | `\\fileserver\cloudcoin\data` |
| `/mnt/`, `/media/` | `usb` or `network` | `/mnt/usb/cloudcoin` |
| `/Volumes/` | `usb` | `/Volumes/USB/CloudCoin` |

## Required Files and Validation

### Location Validation Requirements
A location is considered valid if it:
1. **Path exists**: The directory exists on the file system
2. **Readable**: Application has read permissions
3. **Writable**: Application has write permissions (for active location)
4. **Contains wallets**: Contains valid wallet folder structures

### Active Location Rules
- **Single active**: Only one location can be marked as active (active=true)
- **Must be accessible**: Active location must be currently accessible
- **Auto-fallback**: If active location becomes inaccessible, switch to first available

## Default Configuration Creation

### When No Configuration Exists
Create `locations.csv` with default location based on platform:

#### Windows Default
```csv
path,active,type,label,last_used,accessible,size_mb,description
C:\Users\%USERNAME%\cloudcoin_desktop\Wallets,true,local,Default Location,2025-01-15T10:30:00Z,true,0,Default wallet storage location
```

#### Linux Default
```csv
path,active,type,label,last_used,accessible,size_mb,description
/home/$USER/cloudcoin/wallets,true,local,Default Location,2025-01-15T10:30:00Z,true,0,Default wallet storage location
```

#### Mac Default
```csv
path,active,type,label,last_used,accessible,size_mb,description
/Users/$USER/CloudCoin/Wallets,true,local,Default Location,2025-01-15T10:30:00Z,true,0,Default wallet storage location
```

## Validation Rules

### CSV Format Validation
- **Header required**: CSV must have proper column headers
- **Path uniqueness**: No duplicate paths allowed
- **Boolean consistency**: Boolean fields must use consistent format
- **DateTime format**: Timestamps must be in ISO 8601 format

### Path Validation
- **Absolute paths required**: All paths must be absolute file system paths
- **Path accessibility**: Paths should be accessible with appropriate permissions
- **Reserved characters**: Handle platform-specific reserved characters appropriately

### Data Type Validation
- **Boolean fields**: Accept `true`, `false`, `1`, `0`, `yes`, `no` (case insensitive)
- **DateTime fields**: Must use ISO 8601 format (`YYYY-MM-DDTHH:MM:SSZ`)
- **Numeric fields**: Must be valid positive numbers
- **Enum fields**: Must match predefined values (case insensitive)

### Active Location Validation
```csv
# Valid: Single active location
path,active,type,label
C:\Users\user\Wallets,true,local,Primary
D:\Backup\Wallets,false,local,Backup

# Invalid: Multiple active locations (will use first active)
path,active,type,label
C:\Users\user\Wallets,true,local,Primary
D:\Backup\Wallets,true,local,Backup  # This will be set to false
```

## Error Handling

### Missing Files
- **No locations.csv**: Create default configuration automatically
- **Corrupted CSV**: Attempt to parse valid rows, create backup of corrupted file
- **Permission denied**: Report specific permission error with guidance

### Invalid Data
- **Malformed CSV**: Skip invalid rows, log warnings, continue with valid entries
- **Invalid paths**: Mark as inaccessible, retain in configuration for potential recovery
- **Multiple active locations**: Use first active location, mark others as inactive
- **Missing required columns**: Use default values for missing optional columns

### Network and Media Issues
- **Network timeouts**: Mark network locations as temporarily inaccessible (accessible=false)
- **USB not mounted**: Mark USB locations as offline until reconnected
- **Permission changes**: Re-validate permissions and update accessibility status

## CSV File Operations

### Reading Configuration
```csv
# Example reading logic pseudo-code:
# 1. Check if locations.csv exists
# 2. Parse CSV headers and validate required columns
# 3. Process each row and validate data types
# 4. Identify active location
# 5. Return structured location data
```

### Writing Configuration
```csv
# Example writing logic:
# 1. Create temporary CSV file
# 2. Write header row with all columns
# 3. Write each location row with proper escaping
# 4. Atomically replace original file
# 5. Verify written file can be read back
```

### Backup Strategy
- **Pre-modification backup**: Create `locations.csv.bak` before changes
- **Atomic writes**: Write to `locations.csv.tmp`, then rename
- **Validation**: Verify written file can be parsed correctly

## Best Practices

### File Management
- **Never delete entries**: Mark inaccessible locations rather than removing them
- **Preserve user data**: Maintain user-configured labels and descriptions
- **Regular validation**: Periodically check location accessibility
- **Backup configurations**: Keep backup copies of configuration files

### CSV Handling
- **Proper escaping**: Escape commas and quotes in path strings
- **UTF-8 encoding**: Always use UTF-8 encoding for international characters
- **Line endings**: Handle both LF and CRLF line endings
- **Empty fields**: Handle empty optional fields gracefully

### Performance Considerations
- **Cache validation results**: Avoid repeated file system checks
- **Async validation**: Check accessibility in background when possible
- **Batch operations**: Process multiple location checks together
- **Timeout limits**: Set reasonable timeouts for network location checks

### Security Considerations
- **Path sanitization**: Validate and sanitize all file paths
- **Permission checking**: Verify read/write permissions before use
- **Network security**: Be cautious with network path credentials
- **Access logging**: Log location access for security auditing

## Integration Notes

### For Location Management Commands
- Always validate CSV structure before operations
- Read locations.csv from D:/CloudCoin/Pro/ directory
- Create default configuration if none exists
- Handle CSV parsing errors gracefully
- Update accessibility status during operations

### For Wallet Operations
- Use location configuration to find wallet directories
- Validate wallet structure within each location
- Update location usage timestamps during operations
- Handle location switching gracefully

This standardized format ensures that all CloudCoin Pro installations can consistently manage data locations across different platforms and storage types while maintaining compatibility with existing configurations.
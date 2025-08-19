# List Locations

This function takes no arguments and returns a list of all configured data locations for the CloudCoin Pro application.

The primary purpose of this function is to read and display all configured data locations from the locations configuration file, showing which location is currently active and providing details about each configured path.

## Function Requirements

### 1. Location File Reading
The function must read the locations configuration file from the CloudCoin Pro installation:
- Primary locations file: `locations.csv`
- Fallback to default location if no configuration exists

### 2. Location Data Processing
Parse and organize location data to identify:
- All configured data locations
- Currently active location (marked with asterisk or active flag)
- Location accessibility and validation status
- Path types (local, network, USB, cloud storage)

### 3. Structured Output Format
Return location information in a clear, organized format showing:
- List of all configured locations
- Active location indicator
- Path validation status
- Location metadata (type, accessibility, size, etc.)

### 4. Return Value
The function must return a structured object containing all location information with validation status and accessibility details.

## Input
- **No parameters required** - Function reads from standard CloudCoin Pro configuration

## Output
(object): Comprehensive list of all configured data locations with status information

## File Structure
Your code will interact with the following CloudCoin Pro location files:

```
D:/CloudCoin/Pro/
├── locations.csv               # Primary location configuration
├── last-export-folder-locations-dropdown.txt  # Recent export folders
└── Wallets/                   # Individual wallet locations
    ├── [wallet_name]/         # Each wallet is a location
    └── [other_wallets]/
```

## Location File Formats

### 1. locations.csv (Primary Format)
```csv
path,active,type,label,last_used,accessible,size_mb,description
D:\CloudCoin\Pro\Wallets,true,local,Default Location,2025-01-15T10:30:00Z,true,1250.5,Primary wallet storage
C:\Users\User\Documents\CloudCoin\Backup,false,local,Backup Location,2025-01-14T15:20:00Z,true,850.2,Backup wallet location
E:\USB_Backup\CloudCoin\Data,false,usb,USB Backup,2025-01-13T09:15:00Z,false,0,External USB drive
\\NetworkDrive\CloudCoin\Shared,false,network,Network Share,2025-01-10T14:30:00Z,true,2100.8,Shared network storage
```

**Format Rules:**
- CSV format with required headers
- Active location marked with `active=true`
- Absolute file system paths
- Support for local, network, and USB paths

### 3. last-export-folder-locations-dropdown.txt (Recent Folders)
```
C:\Users\User\Documents\CloudCoin\Exports
C:\Users\User\Desktop\CloudCoin_Backup
D:\CloudCoin\Exports
E:\USB_Exports\CloudCoin
```

## Location Types and Validation

### Location Types
| Type | Description | Validation Required |
|------|-------------|-------------------|
| **local** | Local file system path | Check directory exists and writable |
| **usb** | USB drive or removable media | Check drive mounted and accessible |
| **network** | Network share or mapped drive | Check network connectivity and permissions |
| **cloud** | Cloud storage mount point | Check cloud service connection |

### Validation Checks
- **Existence**: Path exists on file system
- **Accessibility**: Read/write permissions available
- **Space**: Available disk space
- **Type Detection**: Automatically determine location type
- **Wallet Structure**: Contains valid wallet folders

## Detailed Logic Flow

### 1. Read Location Configuration
- Read locations.csv file from D:/CloudCoin/Pro/
- Parse CSV data according to format specification
- Handle missing or corrupted configuration files

### 2. Validate Each Location
- Test path existence and accessibility
- Check read/write permissions
- Calculate storage usage if accessible
- Determine location type (local/usb/network/cloud)
- Validate wallet structure if applicable

### 3. Identify Active Location
- Find location marked as active in configuration
- Verify active location is accessible
- Fallback to first accessible location if active is unavailable

### 4. Scan Wallet Locations
- Enumerate wallet folders in each location
- Count wallets and calculate total storage
- Validate wallet structure integrity

### 5. Read Recent Export Folders
- Parse last-export-folder-locations-dropdown.txt from D:/CloudCoin/Pro/
- Include recent export destinations in output
- Mark which recent folders are still accessible

### 6. Return Structured Data
- Organize all location information
- Include validation status and metadata
- Provide clear active location indication

## Example Function Call

```bash
list-locations
# Reads from D:/CloudCoin/Pro/locations.csv
```

## Configuration Output Structure

```json
{
  "locations_info": {
    "timestamp": "2025-01-15T10:30:00Z",
    "total_locations": 4,
    "active_location": "D:\\CloudCoin\\Pro\\Wallets",
    "config_source": "locations.csv",
    
    "locations": [
      {
        "path": "D:\\CloudCoin\\Pro\\Wallets",
        "active": true,
        "type": "local",
        "label": "Default Location",
        "accessible": true,
        "exists": true,
        "writable": true,
        "last_used": "2025-01-15T10:30:00Z",
        "storage": {
          "total_size_mb": 1250.5,
          "available_space_gb": 45.2,
          "wallet_count": 3
        },
        "validation": {
          "status": "valid",
          "warnings": [],
          "errors": []
        }
      },
      {
        "path": "C:\\Users\\User\\Documents\\CloudCoin\\Backup",
        "active": false,
        "type": "local",
        "label": "Backup Location",
        "accessible": true,
        "exists": true,
        "writable": true,
        "last_used": "2025-01-14T15:20:00Z",
        "storage": {
          "total_size_mb": 850.2,
          "available_space_gb": 120.5,
          "wallet_count": 2
        },
        "validation": {
          "status": "valid",
          "warnings": [],
          "errors": []
        }
      },
      {
        "path": "E:\\USB_Backup\\CloudCoin\\Data",
        "active": false,
        "type": "usb",
        "label": "USB Backup",
        "accessible": false,
        "exists": false,
        "writable": false,
        "last_used": "2025-01-13T09:15:00Z",
        "storage": {
          "total_size_mb": 0,
          "available_space_gb": 0,
          "wallet_count": 0
        },
        "validation": {
          "status": "error",
          "warnings": [],
          "errors": ["Drive not accessible", "Path does not exist"]
        }
      },
      {
        "path": "\\\\NetworkDrive\\CloudCoin\\Shared",
        "active": false,
        "type": "network",
        "label": "Network Share",
        "accessible": true,
        "exists": true,
        "writable": true,
        "last_used": "2025-01-10T14:30:00Z",
        "storage": {
          "total_size_mb": 2100.8,
          "available_space_gb": 500.0,
          "wallet_count": 5
        },
        "validation": {
          "status": "valid",
          "warnings": ["Network latency detected"],
          "errors": []
        }
      }
    ],
    
    "recent_export_folders": [
      {
        "path": "C:\\Users\\User\\Documents\\CloudCoin\\Exports",
        "accessible": true,
        "last_used": "2025-01-15T09:45:00Z"
      },
      {
        "path": "C:\\Users\\User\\Desktop\\CloudCoin_Backup",
        "accessible": true,
        "last_used": "2025-01-14T16:20:00Z"
      },
      {
        "path": "D:\\CloudCoin\\Exports",
        "accessible": true,
        "last_used": "2025-01-13T11:30:00Z"
      },
      {
        "path": "E:\\USB_Exports\\CloudCoin",
        "accessible": false,
        "last_used": "2025-01-12T14:15:00Z"
      }
    ],
    
    "summary": {
      "total_accessible_locations": 3,
      "total_inaccessible_locations": 1,
      "total_wallets_across_locations": 10,
      "total_storage_used_mb": 4201.5,
      "locations_with_errors": 1,
      "locations_with_warnings": 1
    }
  }
}
```

## Human-Readable Format Option

The function can also return information in a human-readable text format:

```
====================================================
CLOUDCOIN PRO DATA LOCATIONS
====================================================
Generated: January 15, 2025 at 10:30 AM
Configuration Source: locations.csv

ACTIVE LOCATION
====================================================
📁 D:\CloudCoin\Pro\Wallets
   Type: Local Drive
   Status: ✅ Accessible
   Storage: 1,250.5 MB used, 45.2 GB available
   Wallets: 3 wallets found
   Last Used: January 15, 2025 at 10:30 AM

ALL CONFIGURED LOCATIONS
====================================================

1. 📁 D:\CloudCoin\Pro\Wallets [ACTIVE]
   Type: Local Drive
   Status: ✅ Accessible and writable
   Storage: 1,250.5 MB used, 45.2 GB available
   Wallets: 3 wallets found
   Last Used: January 15, 2025 at 10:30 AM

2. 📁 C:\Users\User\Documents\CloudCoin\Backup
   Type: Local Drive  
   Status: ✅ Accessible and writable
   Storage: 850.2 MB used, 120.5 GB available
   Wallets: 2 wallets found
   Last Used: January 14, 2025 at 3:20 PM

3. 💾 E:\USB_Backup\CloudCoin\Data
   Type: USB Drive
   Status: ❌ Not accessible (Drive not mounted)
   Storage: Unknown (drive offline)
   Wallets: Unknown
   Last Used: January 13, 2025 at 9:15 AM

4. 🌐 \\NetworkDrive\CloudCoin\Shared
   Type: Network Share
   Status: ⚠️ Accessible with warnings (Network latency detected)
   Storage: 2,100.8 MB used, 500.0 GB available
   Wallets: 5 wallets found
   Last Used: January 10, 2025 at 2:30 PM

RECENT EXPORT FOLDERS
====================================================
• C:\Users\User\Documents\CloudCoin\Exports ✅
• C:\Users\User\Desktop\CloudCoin_Backup ✅
• D:\CloudCoin\Exports ✅
• E:\USB_Exports\CloudCoin ❌

SUMMARY
====================================================
Total Locations: 4
Accessible: 3
Inaccessible: 1
Total Wallets: 10 across all locations
Total Storage Used: 4,201.5 MB
Locations with Issues: 2 (1 error, 1 warning)

RECOMMENDATIONS
====================================================
⚠️ USB drive E:\ is not accessible - check if drive is connected
⚠️ Network location has latency issues - consider local backup
✅ Active location is healthy and accessible
```

## Error Handling

| Error Condition | Response Action |
|-----------------|-----------------|
| No configuration file found | Create default configuration with current directory |
| Configuration file corrupted | Use default location and log warning |
| Active location inaccessible | Switch to first accessible location |
| All locations inaccessible | Return error with troubleshooting guidance |
| Permission denied | Report specific permission issues |
| Network location timeout | Mark as inaccessible with timeout error |

## Location Path Validation

### Path Format Support
- **Windows**: `C:\path\to\location`, `\\server\share\path`
- **Linux/Mac**: `/path/to/location`, `/mnt/network/path`
- **Relative**: `./wallets`, `../backup/wallets`

### Drive Type Detection
```ini
# Local drives
C:\, D:\, E:\ = local
# Network paths  
\\server\share = network
# Mounted drives
/media/usb = usb
/mnt/cloud = cloud
```

## Default Location Configuration

When no configuration exists, create default:

```csv
path,active,type,label,last_used,accessible,size_mb,description
C:\Users\[username]\cloudcoin_desktop\Wallets,true,local,Default Location,[current_time],true,0,Default wallet storage location
```

## Integration Notes

- Works with all CloudCoin Pro installations following standard structure
- Compatible with both simple and enhanced location configuration formats
- Supports local, network, USB, and cloud storage locations
- Can be used for location management and troubleshooting
- Provides foundation for location switching functionality
- Useful for backup and recovery planning
- References configuration-files-format.md for validation rules
- Integrates with wallet management system
- Compatible with export folder history tracking
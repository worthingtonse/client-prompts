# List Locations

This function takes no arguments and returns a list of all configured data locations for the CloudCoin Pro application with real-time calculated information.

The primary purpose of this function is to read the simple locations configuration file and enhance it with calculated data including accessibility, size, usage information, and detailed metadata.

## Function Requirements

### 1. Location File Reading
The function must read the simplified locations configuration file:
- Primary locations file: `locations.csv` (simplified format with path and optional type)
- Fallback to default location if no configuration exists

### 2. Real-Time Data Calculation
Calculate all dynamic information for each location:
- **Accessibility**: Test if location is currently accessible
- **Size and usage**: Calculate storage used and available space
- **Last used**: Determine from file system timestamps
- **Label**: Extract from folder name
- **Type detection**: Auto-detect location type regardless of CSV value
- **Wallet enumeration**: Count and validate wallet structures

### 3. Primary Location Logic
- **First location in CSV**: Treated as primary/default location
- **No "active" flag**: All locations can be used simultaneously
- **Order matters**: File order determines priority

### 4. Return Value
The function must return enhanced location information with all calculated data while keeping the CSV file simple.

## Input
- **No parameters required** - Function reads from standard CloudCoin Pro configuration

## Output
(object): Comprehensive list with calculated information for all configured locations

## File Structure
Your code will interact with the following CloudCoin Pro location files:

```
D:/CloudCoin/Pro/
├── locations.csv               # Simple location configuration (path, type)
├── last-export-folder-locations-dropdown.txt  # Recent export folders
└── Wallets/                   # Individual wallet locations
    ├── [wallet_name]/         # Each wallet location
    └── [other_wallets]/
```

## Simplified Location File Format

### locations.csv (Simplified Format)
```csv
path,type
D:\CloudCoin\Pro\Wallets,local
C:\Users\User\Documents\CloudCoin\Backup,local
E:\USB_Backup\CloudCoin\Data,usb
\\NetworkDrive\CloudCoin\Shared,network
```

**Format Rules:**
- **Minimal data**: Only path and optional type
- **No calculated fields**: No active, last_used, accessible, size_mb
- **Order matters**: First location is primary/default
- **Cross-platform paths**: Support environment variables

## Detailed Logic Flow

### 1. Read Simple Configuration
- Read locations.csv file from D:/CloudCoin/Pro/
- Parse minimal CSV with path and optional type
- Handle missing or corrupted configuration files
- Use first location as primary/default

### 2. Calculate Accessibility for Each Location
- Test path existence and accessibility
- Check read/write permissions
- Determine if location is currently available
- Handle network timeouts and USB drive detection

### 3. Calculate Storage Information
- Calculate storage used if accessible
- Determine available disk space
- Handle inaccessible locations gracefully

### 4. Determine Last Used Times
- Read file system timestamps from location directories
- Check wallet modification times
- Calculate most recent activity

### 5. Generate Labels from Folder Names
- Extract folder name from path
- Use folder name as label
- Handle special cases (root drives, network shares)

### 6. Auto-Detect Location Types
- Analyze path patterns for type detection
- Override CSV type with calculated type
- Support cross-platform detection

### 7. Scan and Validate Wallets
- Enumerate wallet folders in each accessible location
- Count wallets and validate structure
- Calculate total storage across wallets

### 8. Read Recent Export Folders
- Parse last-export-folder-locations-dropdown.txt
- Calculate accessibility for recent folders
- Include in output with status

### 9. Return Enhanced Data
- Combine simple CSV data with calculated information
- Provide comprehensive location details
- Include validation status and metadata

## Example Function Call

```bash
list-locations
# Reads simple CSV and calculates all dynamic data
```

## Enhanced Output Structure

```json
{
  "locations_info": {
    "timestamp": "2025-01-15T10:30:00Z",
    "total_locations": 4,
    "primary_location": "D:\\CloudCoin\\Pro\\Wallets",
    "config_source": "locations.csv",
    
    "locations": [
      {
        "path": "D:\\CloudCoin\\Pro\\Wallets",
        "is_primary": true,
        "order_index": 0,
        "csv_type": "local",
        "calculated_data": {
          "label": "Wallets",
          "detected_type": "local",
          "accessible": true,
          "exists": true,
          "writable": true,
          "last_used": "2025-01-15T10:30:00Z",
          "storage": {
            "total_size_mb": 1250.5,
            "available_space_gb": 45.2,
            "wallet_count": 3
          }
        },
        "validation": {
          "status": "valid",
          "warnings": [],
          "errors": []
        }
      },
      {
        "path": "C:\\Users\\User\\Documents\\CloudCoin\\Backup",
        "is_primary": false,
        "order_index": 1,
        "csv_type": "local",
        "calculated_data": {
          "label": "Backup",
          "detected_type": "local",
          "accessible": true,
          "exists": true,
          "writable": true,
          "last_used": "2025-01-14T15:20:00Z",
          "storage": {
            "total_size_mb": 850.2,
            "available_space_gb": 120.5,
            "wallet_count": 2
          }
        },
        "validation": {
          "status": "valid",
          "warnings": [],
          "errors": []
        }
      },
      {
        "path": "E:\\USB_Backup\\CloudCoin\\Data",
        "is_primary": false,
        "order_index": 2,
        "csv_type": "usb",
        "calculated_data": {
          "label": "Data",
          "detected_type": "usb",
          "accessible": false,
          "exists": false,
          "writable": false,
          "last_used": "2025-01-13T09:15:00Z",
          "storage": {
            "total_size_mb": 0,
            "available_space_gb": 0,
            "wallet_count": 0
          }
        },
        "validation": {
          "status": "error",
          "warnings": [],
          "errors": ["Drive not accessible", "Path does not exist"]
        }
      },
      {
        "path": "\\\\NetworkDrive\\CloudCoin\\Shared",
        "is_primary": false,
        "order_index": 3,
        "csv_type": "network",
        "calculated_data": {
          "label": "Shared",
          "detected_type": "network",
          "accessible": true,
          "exists": true,
          "writable": true,
          "last_used": "2025-01-10T14:30:00Z",
          "storage": {
            "total_size_mb": 2100.8,
            "available_space_gb": 500.0,
            "wallet_count": 5
          }
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
        "calculated_data": {
          "accessible": true,
          "last_used": "2025-01-15T09:45:00Z"
        }
      },
      {
        "path": "E:\\USB_Exports\\CloudCoin",
        "calculated_data": {
          "accessible": false,
          "last_used": "2025-01-12T14:15:00Z"
        }
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

## Cross-Platform Type Detection

### Automatic Type Detection Logic
```javascript
function detectLocationType(path) {
  // Windows detection
  if (path.match(/^[A-Z]:\\/)) return "local";
  if (path.match(/^\\\\[^\\]+\\/)) return "network";
  
  // Linux/Mac detection  
  if (path.match(/^\/home\/|^\/Users\//)) return "local";
  if (path.match(/^\/mnt\/|^\/media\//)) return "usb";
  if (path.match(/^\/Volumes\//)) return "usb";
  
  // Network mounts
  if (path.match(/^\/mnt\/.*network|^\/media\/.*network/)) return "network";
  
  return "local"; // default
}
```

## Human-Readable Format Option

```
====================================================
CLOUDCOIN PRO DATA LOCATIONS
====================================================
Generated: January 15, 2025 at 10:30 AM
Configuration Source: locations.csv (simplified)

PRIMARY LOCATION
====================================================
📁 D:\CloudCoin\Pro\Wallets (Wallets)
   Type: Local Drive (auto-detected)
   Status: ✅ Accessible
   Storage: 1,250.5 MB used, 45.2 GB available
   Wallets: 3 wallets found
   Last Used: January 15, 2025 at 10:30 AM

ALL CONFIGURED LOCATIONS
====================================================

1. 📁 D:\CloudCoin\Pro\Wallets (Wallets) [PRIMARY]
   Type: Local Drive
   Status: ✅ Accessible and writable
   Storage: 1,250.5 MB used, 45.2 GB available
   Wallets: 3 wallets found
   Last Used: January 15, 2025 at 10:30 AM

2. 📁 C:\Users\User\Documents\CloudCoin\Backup (Backup)
   Type: Local Drive  
   Status: ✅ Accessible and writable
   Storage: 850.2 MB used, 120.5 GB available
   Wallets: 2 wallets found
   Last Used: January 14, 2025 at 3:20 PM

3. 💾 E:\USB_Backup\CloudCoin\Data (Data)
   Type: USB Drive
   Status: ❌ Not accessible (Drive not mounted)
   Storage: Unknown (drive offline)
   Wallets: Unknown
   Last Used: January 13, 2025 at 9:15 AM

4. 🌐 \\NetworkDrive\CloudCoin\Shared (Shared)
   Type: Network Share
   Status: ⚠️ Accessible with warnings (Network latency detected)
   Storage: 2,100.8 MB used, 500.0 GB available
   Wallets: 5 wallets found
   Last Used: January 10, 2025 at 2:30 PM

CALCULATION DETAILS
====================================================
• All accessibility, size, and usage data calculated in real-time
• Labels generated from folder names
• Location types auto-detected regardless of CSV values
• Primary location determined by order in CSV file
• No calculated data stored in configuration files
```

## Error Handling

| Error Condition | Response Action |
|-----------------|-----------------|
| No configuration file found | Create default configuration with single location |
| Configuration file corrupted | Use default location and log warning |
| All locations inaccessible | Return error with troubleshooting guidance |
| Permission denied | Report specific permission issues |
| Network location timeout | Mark as inaccessible with timeout error |

## Default Location Configuration

When no configuration exists, create platform-appropriate default:

### Windows
```csv
path,type
D:\CloudCoin\Pro\Wallets,local
```

### Linux
```csv
path,type
/opt/cloudcoin/wallets,local
```

### Mac
```csv
path,type
/Applications/CloudCoin/Wallets,local
```

## Integration Notes

- **Simplified CSV**: Stores only essential path and optional type data
- **Real-time calculation**: All dynamic data calculated during function execution
- **No file updates**: CSV file remains static during normal operations
- **Cross-platform**: Supports environment variables and platform-specific paths
- **Primary location**: First location in CSV is treated as primary/default
- **Multiple usage**: All locations can be used simultaneously
- **Type override**: Auto-detected types override CSV type values
- **Label generation**: Folder names used as labels automatically
- **Performance**: Lightweight CSV parsing with on-demand calculations

This approach separates static configuration (CSV) from dynamic data (calculated by function), ensuring the configuration file remains simple and accurate while providing rich information to the application.
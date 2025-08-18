# Configuration Files Format Specification

This document defines the format, location, and structure of all configuration files used by CloudCoin Pro applications. This specification ensures consistency across all configuration management functions and provides validation rules for configuration data.

## File Locations and Structure

All configuration files are located within the CloudCoin Pro installation directory:

```
D:/CloudCoin/Pro/
├── program-config.txt          # Main program configuration
├── user-preferences.ini        # User interface preferences (optional)
├── raidas.csv                  # RAIDA server configuration
├── guardians.csv               # Guardian server list
├── root-hints.csv              # DNS root hint servers
├── locations.csv               # Location and export preferences
├── last-echo-log.json          # Recent RAIDA echo results
├── last-export-folder-locations-dropdown.txt  # Export folder history
├── simple-log.txt              # Simple activity log
├── main-log.txt                # Detailed application log
├── Client Server Keys/         # Server authentication keys
│   ├── server.somedomain.com port 607623.txt
│   ├── 143.74.11.42 port 80.txt
│   └── company.org port 8892.txt
├── Themes/
│   └── [active_theme]/Theme.txt # Active theme configuration
├── Wallets/
│   └── [wallet_name]/config.toml # Individual wallet configurations
├── Receipts/                   # Global receipt storage
├── Coin Images/                # Coin denomination images
├── Drivers/                    # Application dependencies (DLLs, etc.)
├── Zipped Logs/               # Archived log files
│   └── main-[timestamp].log.zip
└── Performance Statistics/
    ├── echos.csv               # Echo performance data
    ├── get-tickets.csv         # Ticket performance data
    ├── fixes.csv               # Fix operation performance
    └── powns.csv               # POWN operation performance
```

## Configuration File Formats

### 1. program-config.txt (Main Program Configuration)

**Format**: INI-style configuration  
**Encoding**: UTF-8  
**Purpose**: Core application settings and preferences

```ini
# CloudCoin Pro Main Configuration
title = "CloudCoin Desktop"
help = "support@cloudcoin.global"

[main]
http_timeout = 3
domain = ""
max_notes_to_send = 1000
export_background = "#02203D"
brand_color = "#7FA8FF"
maximum_coins_allowed = 500000
require_usb = true
protocol = "auto"
serial_mode = false
http_mode = false
default_timeout_mult = 100
echo_timeout_mult = 100
change_server_sn = 2
encryption_disabled = true
use_local_raidas = false
use_parallel_requests = true
admin_key = ""
coin_id = 6

[theme]
active_theme = "default"
auto_switch_theme = false
theme_path = "Themes/default"

[security]
auto_lock_timeout = 30
backup_encryption = true
secure_delete = false

[performance]
cache_enabled = true
max_cache_size = "100MB"
auto_cleanup = true
log_level = "info"
max_log_files = 5
```

#### Configuration Key Definitions

| Section | Key | Type | Default | Description |
|---------|-----|------|---------|-------------|
| [root] | title | string | "CloudCoin Desktop" | Application display title |
| [root] | help | string | "support@cloudcoin.global" | Support contact information |
| [main] | http_timeout | integer | 3 | HTTP request timeout in seconds |
| [main] | max_notes_to_send | integer | 1000 | Maximum coins per transaction |
| [main] | maximum_coins_allowed | integer | 500000 | Total coin limit in wallet |
| [main] | require_usb | boolean | true | Require USB drive for operation |
| [main] | protocol | enum | "auto" | Network protocol: auto, TCP, UDP |
| [main] | use_parallel_requests | boolean | true | Send parallel RAIDA requests |
| [main] | encryption_disabled | boolean | true | Disable coin encryption |
| [main] | coin_id | integer | 6 | CloudCoin identification number |

### 2. user-preferences.ini (User Interface Preferences)

**Format**: INI configuration  
**Purpose**: User-specific interface and behavior settings  
**Note**: Optional file - preferences may be stored in program-config.txt if this file doesn't exist

```ini
[interface]
language = "English"
date_format = "MM/DD/YYYY"
window_size = "1024x768"
show_tooltips = true
enable_animations = true
auto_backup = true

[export]
last_export_folder = "C:/Users/User/Documents/CloudCoin/"
default_export_format = "bin"
include_receipts = true

[display]
theme_preference = "auto"
high_contrast = false
large_fonts = false
```

### 3. raidas.csv (RAIDA Server Configuration)

**Format**: CSV with headers  
**Purpose**: RAIDA server list and status information

```csv
server_id,hostname,port,protocol,status,last_echo,response_time,region
0,raida0.cloudcoin.global,443,https,active,2025-01-15T10:25:00Z,234,us-east
1,raida1.cloudcoin.global,443,https,active,2025-01-15T10:25:01Z,156,us-west
2,raida2.cloudcoin.global,443,https,down,2025-01-15T10:20:00Z,0,eu-central
```

#### CSV Column Definitions

| Column | Type | Description |
|--------|------|-------------|
| server_id | integer | RAIDA server identifier (0-24) |
| hostname | string | Server hostname or IP address |
| port | integer | Server port number |
| protocol | string | Connection protocol (http, https) |
| status | enum | Server status: active, down, maintenance |
| last_echo | datetime | Last successful echo timestamp |
| response_time | integer | Last response time in milliseconds |
| region | string | Geographic region identifier |

### 4. guardians.csv (Guardian Server List)

**Format**: CSV with headers  
**Purpose**: Guardian server configuration and backup priorities

```csv
guardian_id,hostname,port,region,backup_priority,status,last_check
g1,raida-guardian-tx.us,443,us-central,1,active,2025-01-15T10:25:00Z
g2,g2.cloudcoin.asia,443,asia-pacific,2,active,2025-01-15T10:25:01Z
g3,guardian.ladyjade.cc,443,eu-west,3,active,2025-01-15T10:25:02Z
```

### 5. root-hints.csv (DNS Root Hint Servers)

**Format**: CSV with headers  
**Purpose**: DNS root hint servers for network resolution

```csv
server_name,ip_address,port,region,priority,status
cloudflare,1.1.1.1,53,global,1,active
google,8.8.8.8,53,global,2,active
quad9,9.9.9.9,53,global,3,active
```

#### CSV Column Definitions

| Column | Type | Description |
|--------|------|-------------|
| server_name | string | DNS server identifier |
| ip_address | string | Server IP address |
| port | integer | DNS port (usually 53) |
| region | string | Geographic region |
| priority | integer | Server priority (1=highest) |
| status | enum | Server status: active, inactive |

### 6. locations.csv (Location and Export Preferences)

**Format**: CSV with headers  
**Purpose**: Location preferences and export folder history

```csv
location_type,path,last_used,favorite,description
export,C:/Users/User/Documents/CloudCoin/,2025-01-15T10:20:00Z,true,Default export location
import,C:/Users/User/Downloads/,2025-01-15T09:30:00Z,false,Download folder
backup,D:/CloudCoin/Backups/,2025-01-14T18:00:00Z,true,USB backup location
```

### 7. last-echo-log.json (Recent Echo Results)

**Format**: JSON  
**Purpose**: Store recent RAIDA echo test results

```json
{
  "timestamp": "2025-01-15T10:25:00Z",
  "total_raidas": 25,
  "successful_echoes": 23,
  "failed_echoes": 2,
  "average_response_time": 245,
  "results": [
    {
      "raida_id": 0,
      "hostname": "raida0.cloudcoin.global",
      "success": true,
      "response_time": 234,
      "error": null
    },
    {
      "raida_id": 2,
      "hostname": "raida2.cloudcoin.global", 
      "success": false,
      "response_time": 0,
      "error": "Connection timeout"
    }
  ]
}
```

### 8. Client Server Keys

**Format**: Text files  
**Purpose**: Server authentication keys  
**Location**: `Client Server Keys/` folder  
**Naming**: `[server] port [port].txt`

```
server.somedomain.com port 607623.txt
143.74.11.42 port 80.txt
company.org port 8892.txt
```

Each file contains the authentication key for connecting to that specific server.

### 9. Performance Statistics CSV Files

**Location**: `Performance Statistics/` folder  
**Format**: CSV with headers for each operation type

#### echos.csv
```csv
timestamp,raida_id,response_time,success,error_code,total_bytes
2025-01-15T10:25:00Z,0,234,true,,128
2025-01-15T10:25:01Z,1,156,true,,128
2025-01-15T10:25:02Z,2,0,false,timeout,0
```

#### powns.csv  
```csv
timestamp,raida_id,coin_count,success_count,fail_count,total_time,average_time
2025-01-15T10:20:00Z,0,10,8,2,2340,234
2025-01-15T10:20:01Z,1,10,10,0,1560,156
```

## Configuration Validation Rules

### Data Type Validation
- **boolean**: true, false (case insensitive)
- **integer**: Positive integers, specific ranges where applicable
- **string**: UTF-8 encoded strings, length limits where applicable
- **enum**: Predefined values only (case insensitive)
- **datetime**: ISO 8601 format (YYYY-MM-DDTHH:MM:SSZ)
- **color**: Hex format (#RRGGBB) or named colors

### Value Constraints
```ini
# Numeric ranges
http_timeout = 1-300              # 1 second to 5 minutes
max_notes_to_send = 1-1000000     # 1 to 1 million coins
maximum_coins_allowed = 1-10000000 # 1 to 10 million coins
coin_id = 1-255                   # Valid coin identifiers

# String constraints  
protocol = ["auto", "TCP", "UDP"] # Case insensitive
log_level = ["debug", "info", "warn", "error"]
language = ["English", "Spanish", "French", "German"]

# Boolean values
require_usb = [true, false, "true", "false", "yes", "no", 1, 0]
```

### File Format Rules
- **Encoding**: All text files must be UTF-8 encoded
- **Line endings**: LF or CRLF acceptable
- **Comments**: Lines starting with # or ; in INI files
- **Case sensitivity**: Keys are case-insensitive, values may be case-sensitive
- **Whitespace**: Leading/trailing whitespace trimmed from values

## Default Configuration Values

### Program Defaults
```ini
title = "CloudCoin Pro"
help = "support@cloudcoin.org"
http_timeout = 5
max_notes_to_send = 1000
maximum_coins_allowed = 1000000
require_usb = false
protocol = "auto"
use_parallel_requests = true
encryption_disabled = false
coin_id = 6
```

### Theme Defaults
```ini
active_theme = "default"
auto_switch_theme = false
export_background = "#FFFFFF"
brand_color = "#007BFF"
```

### Security Defaults
```ini
auto_lock_timeout = 30
backup_encryption = true
secure_delete = false
```

## Configuration File Interactions

### Priority Order
1. **User-modified settings** (highest priority)
2. **Program-config.txt** settings
3. **Theme-specific** settings
4. **System defaults** (lowest priority)

### Theme Integration
- Theme colors override program-config.txt colors
- Theme fonts override system defaults
- Brand colors from themes update export_background
- Theme switching updates active_theme in program-config.txt

### Wallet Integration
- Individual wallet config.toml files override global settings for that wallet
- Wallet-specific timeouts and preferences
- Per-wallet backup and security settings

## Error Handling

### Missing Files
- Use default values for missing configuration files
- Log warnings for missing optional files
- Create default files with standard values when possible

### Invalid Values
- Validate all configuration values on load
- Use default values for invalid entries
- Log errors for invalid configurations
- Continue operation with defaults when possible

### Corrupted Files
- Attempt to parse partially corrupted files
- Use backup configurations if available
- Recreate files with defaults if severely corrupted
- Maintain operation with minimal configuration

## Configuration Management Best Practices

### Reading Configurations
- Parse files in dependency order
- Cache parsed configurations for performance
- Validate all values after parsing
- Apply inheritance and overrides correctly

### Writing Configurations
- Preserve user comments when possible
- Maintain file formatting and structure
- Create atomic writes (temp file + rename)
- Backup existing configurations before modification

### Performance Considerations
- Cache frequently accessed configurations
- Use file modification timestamps to detect changes
- Minimize configuration file reads during operation
- Batch configuration updates when possible

This specification ensures consistent configuration handling across all CloudCoin Pro functions and provides clear guidelines for configuration file management.
# Show Configuration Info

This is used to create a function called `show-config-info(config_path: string)`. This function takes one argument: the file path to the CloudCoin Pro installation directory.

The primary purpose of this function is to read and display comprehensive configuration information including program settings, theme configuration, RAIDA settings, and system preferences in a structured, human-readable format.

## Function Requirements

### 1. Configuration File Reading
The function must read multiple configuration files from the CloudCoin Pro installation:
- Main program configuration file (program-config.txt or config.toml)
- User preferences (user-preferences.ini if exists, otherwise from program-config.txt)
- Active theme configuration (from current theme)
- RAIDA configuration settings
- DNS and network configuration
- Server authentication keys

### 2. Configuration Data Processing
Parse and organize configuration data into logical categories:
- General program settings
- Network and RAIDA settings  
- DNS and root hints configuration
- Theme and appearance settings
- Security and performance settings
- User interface preferences
- Authentication and server keys
- Asset availability

### 3. Structured Output Format
Return configuration information in a clear, organized format that's easy to read and understand.
Include both current values and descriptions of what each setting controls.

### 4. Return Value
The function must return a structured object containing all configuration information with clear categorization and formatting.

## Input
- **config_path** (string): The path to the CloudCoin Pro installation directory (e.g., "D:/CloudCoin/Pro/")

## Output
(object): Comprehensive configuration information organized by category

## File Structure
Your code will interact with the following CloudCoin Pro directory structure:

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
│   ├── default/
│   │   └── Theme.txt          # Theme configurations
│   └── [current active theme]/
├── Wallets/                    # Individual wallet folders
│   └── [wallet_name]/
│       ├── config.toml         # Wallet-specific configuration
│       ├── transactions.csv    # Wallet transaction history
│       ├── Bank/              # Authenticated coins
│       ├── Fracked/           # Partially authenticated coins
│       └── [other wallet folders per wallet-folder-structure.md]
├── Receipts/                   # Global receipt storage
├── Coin Images/                # Coin denomination images
├── Drivers/                    # Application dependencies (DLLs, etc.)
├── Zipped Logs/               # Archived log files
│   └── main-[timestamp].log.zip
└── Performance Statistics/
    ├── echos.csv              # Echo performance data
    ├── get-tickets.csv        # Ticket performance data
    ├── fixes.csv              # Fix performance data
    └── powns.csv              # POWN performance data
```

## Configuration Categories

### 1. General Program Settings
```ini
[general]
title = "CloudCoin Desktop"
help = "support@cloudcoin.global"
version = "2.1.0"
max_notes_to_send = 1000
maximum_coins_allowed = 500000
require_usb = true
coin_id = 6
```

### 2. Network and Protocol Settings
```ini
[network]
protocol = "auto"              # auto, TCP, or UDP
http_timeout = 3
http_mode = false
serial_mode = false
use_parallel_requests = true
default_timeout_mult = 100
echo_timeout_mult = 100
encryption_disabled = true
use_local_raidas = false
```

### 3. RAIDA Configuration
```ini
[raida]
change_server_sn = 2
admin_key = ""
guardians = [
  "raida-guardian-tx.us",
  "g2.cloudcoin.asia", 
  "guardian.ladyjade.cc",
  # ... full guardian list
]
private_raidas = []
```

### 4. DNS and Root Hints Configuration
```ini
[dns]
root_hints_configured = true
primary_dns = "1.1.1.1"
dns_servers = [
  "1.1.1.1",
  "8.8.8.8",
  "9.9.9.9"
]
```

### 5. Theme and Appearance Settings
```ini
[theme]
active_theme = "dark"
theme_path = "D:/CloudCoin/Pro/Themes/dark"
export_background = "#02203D"
brand_color = "#7FA8FF"
background_color = "#2C303D"
text_color = "#D4D4D4"
primary_button_color = "#AB0000"
```

### 6. User Interface Settings
```ini
[interface]
last_export_folder = "C:/Users/User/Documents/CloudCoin/"
window_size = "1024x768"
auto_backup = true
show_tooltips = true
enable_animations = true
```

## Detailed Logic Flow

### 1. Validate Input Parameters
- Check if config_path exists and is accessible
- Verify it points to a valid CloudCoin Pro installation
- Check read permissions for configuration files

### 2. Read Main Program Configuration
- Locate and read primary configuration file (program-config.txt)
- Parse configuration format (INI, TOML, or custom format)
- Extract general program settings

### 3. Read User Preferences
- Check for user-preferences.ini file
- If not found, extract user preferences from program-config.txt
- Read UI preferences and settings
- Extract export/import folder settings
- Read backup and security preferences

### 4. Read Theme Configuration
- Determine active theme from settings or default
- Read active theme's Theme.txt file
- Extract theme colors, fonts, and appearance settings
- Include theme metadata (name, author, version)

### 5. Read RAIDA Configuration
- Read raidas.csv for RAIDA server list
- Read guardians.csv for guardian server configuration
- Extract network and protocol settings
- Read last echo results if available

### 6. Read DNS Configuration
- Read root-hints.csv for DNS server list
- Extract DNS server priorities and status
- Include network resolution settings

### 7. Read Location Preferences
- Read locations.csv for location preferences
- Read last-export-folder-locations-dropdown.txt for recent folders

### 8. Read Authentication Configuration
- Scan Client Server Keys/ folder for server authentication files
- Extract server authentication information
- Count available keys

### 9. Read Asset Information
- Check Coin Images/ folder for denomination assets
- Verify Drivers/ folder for dependencies
- Review Zipped Logs/ for archived information
- Check Receipts/ folder status

### 10. Read Wallet Summary
- Scan Wallets/ folder for available wallets
- Read individual wallet config.toml files
- Validate wallet structure according to wallet-folder-structure.md
- Extract wallet transaction summaries

### 11. Organize Configuration Data
- Group settings by logical categories
- Add descriptions for each setting
- Include current values and defaults
- Format for easy reading

### 12. Return Structured Configuration Object
- Return complete configuration information
- Include metadata about configuration sources
- Provide timestamps and version information

## Example Function Call

```bash
show-config-info "D:/CloudCoin/Pro/"
```

## Configuration Output Structure

```json
{
  "configuration_info": {
    "timestamp": "2025-01-15T10:30:00Z",
    "cloudcoin_pro_version": "2.1.0",
    "config_path": "D:/CloudCoin/Pro/",
    
    "general": {
      "application_title": "CloudCoin Desktop",
      "support_help": "support@cloudcoin.global",
      "support_url": "https://CloudCoin.com/support",
      "coin_id": 6,
      "maximum_coins_allowed": 500000,
      "max_notes_to_send": 1000,
      "require_usb": true
    },
    
    "network": {
      "protocol": "auto",
      "protocol_description": "Automatically choose between TCP and UDP",
      "http_timeout": 3,
      "http_mode": false,
      "serial_mode": false,
      "use_parallel_requests": true,
      "parallel_description": "Send requests to multiple RAIDAs simultaneously",
      "default_timeout_mult": 100,
      "echo_timeout_mult": 100,
      "encryption_disabled": true,
      "use_local_raidas": false
    },
    
    "raida": {
      "change_server_sn": 2,
      "admin_key": "",
      "total_guardians": 26,
      "guardians": [
        "raida-guardian-tx.us",
        "g2.cloudcoin.asia",
        "guardian.ladyjade.cc",
        "watchdog.guardwatch.cc",
        "g5.raida-guardian.us"
      ],
      "private_raidas": [],
      "last_echo_status": "success",
      "last_echo_time": "2025-01-15T10:25:00Z"
    },
    
    "dns": {
      "root_hints_configured": true,
      "total_dns_servers": 3,
      "primary_dns": "1.1.1.1",
      "dns_servers": [
        {
          "name": "cloudflare",
          "ip": "1.1.1.1",
          "priority": 1,
          "status": "active"
        },
        {
          "name": "google",
          "ip": "8.8.8.8",
          "priority": 2,
          "status": "active"
        },
        {
          "name": "quad9",
          "ip": "9.9.9.9",
          "priority": 3,
          "status": "active"
        }
      ]
    },
    
    "theme": {
      "active_theme_name": "EthBold",
      "active_theme_title": "EthBold Wallet",
      "active_theme_path": "D:/CloudCoin/Pro/Themes/ethbold",
      "theme_author": "EthBold Team",
      "theme_version": "1.0.0",
      "export_background": "#02203D",
      "brand_color": "#7FA8FF",
      "background_color": "#2C303D",
      "header_background_color": "#1C1F28",
      "main_text_color": "#D4D4D4",
      "primary_button_color": "#AB0000",
      "error_color": "#FF0000",
      "main_font": "Montserrat-Regular.otf"
    },
    
    "interface": {
      "last_export_folder": "C:/Users/User/Documents/CloudCoin/",
      "auto_backup": true,
      "show_tooltips": true,
      "enable_animations": true,
      "window_size": "1024x768",
      "language": "English",
      "date_format": "MM/DD/YYYY"
    },
    
    "authentication": {
      "client_server_keys": 3,
      "key_files": [
        "server.somedomain.com port 607623.txt",
        "143.74.11.42 port 80.txt",
        "company.org port 8892.txt"
      ]
    },
    
    "assets": {
      "coin_images_available": true,
      "total_coin_images": 15,
      "drivers_folder_size": "45.2MB",
      "archived_logs": 5,
      "receipts_folder_active": true
    },
    
    "wallets_summary": {
      "total_wallets": 3,
      "wallets": [
        {
          "name": "MyWallet",
          "path": "D:/CloudCoin/Pro/Wallets/MyWallet",
          "structure_valid": true,
          "config_exists": true,
          "last_transaction": "2025-01-15T10:20:00Z",
          "total_coins": 1250
        },
        {
          "name": "TestWallet",
          "path": "D:/CloudCoin/Pro/Wallets/TestWallet",
          "structure_valid": true,
          "config_exists": true,
          "last_transaction": "2025-01-14T15:30:00Z",
          "total_coins": 500
        },
        {
          "name": "EmptyWallet",
          "path": "D:/CloudCoin/Pro/Wallets/EmptyWallet",
          "structure_valid": true,
          "config_exists": true,
          "last_transaction": null,
          "total_coins": 0
        }
      ]
    },
    
    "performance": {
      "cache_enabled": true,
      "max_cache_size": "100MB",
      "auto_cleanup": true,
      "log_level": "info",
      "max_log_files": 5
    },
    
    "security": {
      "encryption_enabled": false,
      "backup_encryption": true,
      "secure_delete": false,
      "auto_lock_timeout": 30
    }
  },
  
  "validation": {
    "config_files_found": 10,
    "config_files_missing": 0,
    "theme_valid": true,
    "raida_config_valid": true,
    "dns_config_valid": true,
    "wallets_valid": 3,
    "warnings": [],
    "errors": []
  }
}
```

## Human-Readable Format Option

The function can also return information in a human-readable text format:

```
====================================================
CLOUDCOIN PRO CONFIGURATION INFORMATION
====================================================
Generated: January 15, 2025 at 10:30 AM
CloudCoin Pro Version: 2.1.0
Installation Path: D:/CloudCoin/Pro/

GENERAL SETTINGS
====================================================
Application Title: CloudCoin Desktop
Support Contact: support@cloudcoin.global
Support Website: https://CloudCoin.com/support
Maximum Coins Allowed: 500,000
Maximum Notes Per Send: 1,000
USB Required: Yes
Coin ID: 6

NETWORK & PROTOCOL SETTINGS
====================================================
Protocol: Automatic (TCP/UDP)
HTTP Timeout: 3 seconds
Parallel Requests: Enabled
Serial Mode: Disabled
HTTP Mode: Disabled
Default Timeout Multiplier: 100
Echo Timeout Multiplier: 100
Encryption: Disabled
Local RAIDAs: Disabled

RAIDA CONFIGURATION
====================================================
Change Server Serial Number: 2
Admin Key: [Not Set]
Total Guardian Servers: 26
Active Guardians: 
  • raida-guardian-tx.us
  • g2.cloudcoin.asia
  • guardian.ladyjade.cc
  • [... and 23 more]

Private RAIDAs: None configured
Last Echo Status: Success
Last Echo Time: January 15, 2025 at 10:25 AM

DNS & NETWORK RESOLUTION
====================================================
Root Hints Configured: Yes
Primary DNS Server: 1.1.1.1 (Cloudflare)
Total DNS Servers: 3
  • Cloudflare (1.1.1.1) - Priority 1 - Active
  • Google (8.8.8.8) - Priority 2 - Active  
  • Quad9 (9.9.9.9) - Priority 3 - Active

THEME & APPEARANCE
====================================================
Active Theme: EthBold Wallet
Theme Author: EthBold Team
Theme Version: 1.0.0
Theme Location: D:/CloudCoin/Pro/Themes/ethbold

Color Scheme:
  • Background: #2C303D (Dark Blue-Gray)
  • Header: #1C1F28 (Darker Blue-Gray)  
  • Text: #D4D4D4 (Light Gray)
  • Buttons: #AB0000 (Dark Red)
  • Brand: #7FA8FF (Light Blue)
  • Export Background: #02203D (Navy Blue)

Fonts:
  • Main Font: Montserrat-Regular.otf
  • Bold Font: Montserrat-Bold.otf

USER INTERFACE
====================================================
Last Export Folder: C:/Users/User/Documents/CloudCoin/
Auto Backup: Enabled
Tooltips: Enabled
Animations: Enabled
Window Size: 1024x768
Language: English
Date Format: MM/DD/YYYY

SERVER AUTHENTICATION
====================================================
Client Server Keys: 3 configured
  • server.somedomain.com port 607623
  • 143.74.11.42 port 80
  • company.org port 8892

ASSETS & RESOURCES
====================================================
Coin Images: Available (15 denominations)
Drivers Folder: 45.2MB
Archived Logs: 5 files
Receipts Folder: Active

WALLETS SUMMARY
====================================================
Total Wallets: 3
Active Wallets:
  • MyWallet - Valid structure, 1,250 coins
  • TestWallet - Valid structure, 500 coins
  • EmptyWallet - Valid structure, 0 coins

PERFORMANCE SETTINGS
====================================================
Cache: Enabled (Max 100MB)
Auto Cleanup: Enabled
Log Level: Information
Max Log Files: 5

SECURITY SETTINGS
====================================================
File Encryption: Disabled
Backup Encryption: Enabled
Secure File Deletion: Disabled
Auto Lock Timeout: 30 minutes
```

## Error Handling

| Error Condition | Response Action |
|-----------------|-----------------|
| Config path doesn't exist | Return error: "CloudCoin Pro installation not found" |
| Permission denied | Return error: "Unable to read configuration files" |
| Missing config files | Return partial config with warnings |
| Invalid config format | Return error with specific parsing issues |
| Corrupted theme | Return config with theme warnings |
| Missing RAIDA config | Return config with RAIDA warnings |
| Missing DNS config | Return config with DNS warnings |
| Invalid wallet structure | Return wallet summary with validation warnings |

## Configuration File Parsing

### INI Format Support
```ini
[section]
key=value
key2=value2
```

### TOML Format Support
```toml
[section]
key = "value"
key2 = 123
```

### CSV Format Support
```csv
guardian,url,port,status
g1,raida-guardian-tx.us,443,active
```

### JSON Format Support
```json
{
  "timestamp": "2025-01-15T10:25:00Z",
  "results": [...]
}
```

## Configuration Validation

The function must validate all configuration data according to the specifications in configuration-files-format.md:

### Data Type Validation
- **boolean**: true/false (case insensitive)
- **integer**: Positive integers within specified ranges
- **string**: UTF-8 encoded strings with length limits
- **enum**: Predefined values only (case insensitive)
- **datetime**: ISO 8601 format
- **color**: Hex format (#RRGGBB) or named colors

### Value Range Validation
```ini
# Validate numeric ranges
http_timeout = 1-300              # 1 second to 5 minutes
max_notes_to_send = 1-1000000     # 1 to 1 million coins
maximum_coins_allowed = 1-10000000 # 1 to 10 million coins

# Validate enum values
protocol = ["auto", "TCP", "UDP"] # Case insensitive
log_level = ["debug", "info", "warn", "error"]
```

## Default Values

When configuration values are missing or invalid, use these defaults:

```ini
# Program defaults
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

# Theme defaults
active_theme = "default"
export_background = "#FFFFFF"
brand_color = "#007BFF"

# Interface defaults
language = "English"
date_format = "MM/DD/YYYY"
window_size = "1024x768"
show_tooltips = true
enable_animations = true
auto_backup = true

# DNS defaults
primary_dns = "1.1.1.1"
dns_servers = ["1.1.1.1", "8.8.8.8"]
```

## Integration Notes

- Works with all CloudCoin Pro installations following standard structure
- Compatible with different configuration file formats (INI, TOML, CSV, JSON)
- Supports both built-in and custom themes
- Can be used for troubleshooting configuration issues
- Provides foundation for configuration management interfaces
- Useful for support and diagnostic purposes
- References configuration-files-format.md for validation rules and default values
- Integrates with theme system defined in theme-file-format.md
- Compatible with wallet configurations defined in wallet-folder-structure.md
- Includes comprehensive asset and resource inventory
- Provides DNS and network configuration visibility
- Supports server authentication key management
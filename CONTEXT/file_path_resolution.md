# Cross-Platform File Path Resolution

## Problem
Different deployment scenarios require different file path resolution strategies:
- Development: Files relative to source code
- Packaged executable: Files bundled with executable
- Installed application: Files in installation directory

## Solution Pattern

### Python Implementation
```python
import os
import sys

def resource_path(relative_path: str) -> str:
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        # Development mode - files relative to script location
        base_path = os.path.abspath(os.path.join(
            os.path.dirname(__file__), '..', '..'
        ))
    return os.path.join(base_path, relative_path)

# Usage
ip_file_path = resource_path('CONTEXT/raida-ips.csv')
```

### C# Implementation
```csharp
using System;
using System.IO;
using System.Reflection;

public static string ResourcePath(string relativePath)
{
    string baseDirectory;
    
    // Try to get executable directory
    try
    {
        baseDirectory = Path.GetDirectoryName(
            Assembly.GetExecutingAssembly().Location);
    }
    catch
    {
        // Fallback to current directory
        baseDirectory = Directory.GetCurrentDirectory();
    }
    
    return Path.Combine(baseDirectory, relativePath);
}

// Usage
string ipFilePath = ResourcePath("CONTEXT/raida-ips.csv");
```

### TypeScript/Node.js Implementation
```typescript
import * as path from 'path';
import { fileURLToPath } from 'url';

function resourcePath(relativePath: string): string {
    let baseDirectory: string;
    
    if (typeof __dirname !== 'undefined') {
        // CommonJS
        baseDirectory = path.join(__dirname, '..', '..');
    } else {
        // ES modules
        const __filename = fileURLToPath(import.meta.url);
        const __dirname = path.dirname(__filename);
        baseDirectory = path.join(__dirname, '..', '..');
    }
    
    return path.join(baseDirectory, relativePath);
}

// Usage
const ipFilePath = resourcePath('CONTEXT/raida-ips.csv');
```

## Required Configuration Files
All implementations must be able to locate these files:

### Required Files
- `CONTEXT/raida-ips.csv` - RAIDA server endpoints
- `CONTEXT/protocol.h` - Status code definitions (if available)

### Optional Files
- `CONTEXT/gardians.csv` - Guardian servers
- `CONTEXT/roothints.csv` - DNS hints

### Output Directories
Implementations should create these directories if they don't exist:
- `Logs/` - For echo.status file
- `Pro/` - For last-echo-log.json file

## Error Handling
```python
# Example error handling for missing files
try:
    with open(resource_path('CONTEXT/raida-ips.csv'), 'r') as f:
        # Parse file
        pass
except FileNotFoundError:
    print("CRITICAL ERROR: CONTEXT/raida-ips.csv not found.")
    print("This file is required for RAIDA network operation.")
    sys.exit(1)
except Exception as e:
    print(f"Error reading RAIDA IPs: {e}")
    sys.exit(1)
```

## Directory Structure
```
project_root/
├── CONTEXT/
│   ├── raida-ips.csv
│   ├── gardians.csv
│   └── roothints.csv
├── Logs/            # Created by application
│   └── echo.status  # Generated output
├── Pro/             # Created by application
│   └── last-echo-log.json  # Generated output
└── src/
    └── main.py      # Your application
```
# Coin File Format Specification

This document defines the binary format structure for CloudCoin files used to store coin data. This specification ensures consistency across all coin file operations and enables proper functionality of coin management commands.

## File Overview

CloudCoin files use a binary format with a fixed header followed by variable coin data:

```
coin_file.bin
├── File Header (32 bytes)          # Fixed header with metadata
├── Coin 1 Data (407+ bytes)        # First coin with header + body
├── Coin 2 Data (407+ bytes)        # Second coin (if multiple)
└── [Additional coins...]           # More coins if present
```

## File Header Structure (32 bytes)

The file header contains metadata about the coin file and encryption information:

```
Byte Position | Field Name | Size | Description | Values
-------------|------------|------|-------------|--------
0            | File Version | 1    | Coin file format version | 9 (current)
1            | Cloud ID | 1        | Cloud identification | 1 (default)
2-3          | Coin ID | 2         | Coin type identifier | 0-255
4            | Experimental | 1     | Reserved for app use | Any
5            | Encryption Type | 1  | Encryption method used | 0, 1, 4
6-7          | Token Count | 2      | Number of coins in file | 0-65535
8-14         | Password Hash | 7    | First 7 bytes of MD5 hash | Any
15           | State Flag | 1       | Coin state tracking | 0, 1, 2
16-31        | POWN/Task Data | 16  | Variable based on coin count | Various
```

### Critical Fields for Password Verification

| Field | Bytes | Purpose |
|-------|-------|---------|
| **Encryption Type** | 5 | Indicates if password verification is needed |
| **Password Hash** | 8-14 | Stores hash for password verification |

### Encryption Types

| Code | Encryption Method | Password Required |
|------|------------------|-------------------|
| 0 | No encryption | No |
| 1 | 128-bit AES CTR | Yes |
| 4 | 256-bit AES CTR | Yes |

### State Flags

| Value | State | Description |
|-------|-------|-------------|
| 0 | Current | Current passwords, suspect status |
| 1 | Pending | Contains both current and proposed passwords |
| 2 | Confirmed | Post-authentication with known status |

## Individual Coin Structure

Each coin within the file has its own header and body:

### Coin Header (7 bytes)
```
Byte | Field | Values | Description
-----|-------|--------|-------------
0    | Split | 0      | Future use for splits
1    | Shard | 0      | Future use for shards  
2    | Denomination | -8 to +11 | Binary denomination value
3-6  | Serial Number | Any | Unique coin identifier
```

### Coin Body Structure

| Condition | Size | Content |
|-----------|------|---------|
| Always | 400 bytes | 25 GUIDs (16 bytes each) - Original ANs |
| If Has PANs = 1 | +400 bytes | Proposed Authenticity Numbers |
| If Last Coin | +Padding | Padding to make divisible by 32 |

**Total Coin Size:**
- **Standard coin**: 7 bytes (header) + 400 bytes (body) = 407 bytes
- **With PANs**: 7 bytes (header) + 800 bytes (body) = 807 bytes

## Password Hash Implementation

### Hash Generation Process
1. **Input**: Plain text password (UTF-8 encoded)
2. **Algorithm**: MD5 hash generation
3. **Storage**: First 7 bytes of MD5 hash stored in header bytes 8-14
4. **Verification**: Compare first 7 bytes of password hash with stored hash

### Hash Storage Format
```c
// Example hash storage in header
unsigned char password_hash[7] = {0xA1, 0xB2, 0xC3, 0xD4, 0xE5, 0xF6, 0xA7};
```

### Verification Algorithm
```pseudocode
function verifyPassword(file, password):
    header = readHeader(file, 32)
    if header.encryption_type == 0:
        return "no_encryption_needed"
    
    stored_hash = header.password_hash[8:15]  // 7 bytes
    input_hash = md5(password)[0:7]           // First 7 bytes
    
    return secure_compare(stored_hash, input_hash)
```

## File Size Calculation

### For Single Coin Files
- Header: 32 bytes
- Coin: 407 bytes (without PANs) or 807 bytes (with PANs)
- **Total**: 439 bytes or 839 bytes

### For Multiple Coin Files
- Header: 32 bytes  
- Coins: 407 bytes × coin_count
- Padding: Variable (to make divisible by 32)
- **Total**: 32 + (407 × count) + padding

## File Naming Convention

CloudCoin files follow a specific naming pattern:

```
[denomination].[serial_number].bin

Examples:
1.12345.bin          # 1-denomination coin, serial 12345
25.67890.bin         # 25-denomination coin, serial 67890
250.11111.bin        # 250-denomination coin, serial 11111
```

## Denomination Values

| Binary Value | Denomination | Color Code |
|-------------|--------------|------------|
| -8 | 1/256 | Brown |
| -7 | 1/128 | Brown |
| -6 | 1/64 | Brown |
| -5 | 1/32 | Brown |
| -4 | 1/16 | Brown |
| -3 | 1/8 | Brown |
| -2 | 1/4 | Brown |
| -1 | 1/2 | Brown |
| 0 | 1 | White |
| 1 | 5 | Blue |
| 2 | 25 | Green |
| 3 | 100 | Red |
| 4 | 250 | Yellow |
| 5 | 1000 | Orange |
| 6 | 2500 | Purple |
| 7 | 5000 | Pink |
| 8 | 12500 | Teal |
| 9 | 25000 | Navy |
| 10 | 50000 | Lime |
| 11 | 100000 | Silver |

## File Validation Rules

### Header Validation
- **File Version**: Must be 9 for current format
- **Cloud ID**: Typically 1 for standard CloudCoin
- **Token Count**: Must match actual coins in file
- **Encryption Type**: Must be valid value (0, 1, or 4)

### Structure Validation
- **File size**: Must match calculated size based on token count
- **Coin headers**: Each coin must have valid 7-byte header
- **Serial numbers**: Must be unique within the same denomination
- **Padding**: Last coin must be properly padded

### Password Hash Validation
- **Length**: Must be exactly 7 bytes
- **Format**: Binary data, not text representation
- **Consistency**: Same hash across all encrypted files in wallet

## Error Conditions

### File Format Errors
| Error | Description | Resolution |
|-------|-------------|------------|
| Invalid header size | File too small for header | File corrupted, move to Corrupted folder |
| Wrong file version | Unsupported format version | Update software or convert format |
| Mismatched token count | Actual coins ≠ header count | File corrupted, attempt repair |
| Invalid encryption type | Unknown encryption code | File corrupted or unsupported |

### Password Hash Errors
| Error | Description | Resolution |
|-------|-------------|------------|
| Hash mismatch | Stored hash ≠ password hash | Wrong password or corrupted file |
| Missing hash | Encrypted file with no hash | File corrupted, move to Encryption_Failed |
| Hash format error | Invalid hash length/format | File corrupted, attempt repair |

## Security Considerations

### Password Protection
- **Hash storage**: Only store non-reversible hash, never plaintext
- **Hash algorithm**: Use consistent MD5 implementation
- **Comparison method**: Use timing-attack resistant comparison
- **Memory handling**: Clear passwords from memory after use

### File Integrity
- **Checksum validation**: Verify file structure integrity
- **Size verification**: Confirm file size matches expected format
- **Header validation**: Ensure all header fields are valid
- **Coin validation**: Verify each coin structure is correct

## Implementation Guidelines

### Reading Coin Files
```pseudocode
function readCoinFile(filename):
    file = open(filename, "rb")
    
    // Read and validate header
    header = file.read(32)
    validate_header(header)
    
    // Read coins based on token count
    coins = []
    for i in range(header.token_count):
        coin_header = file.read(7)
        coin_body = file.read(400)  // Basic AN data
        
        if header.has_pans:
            coin_body += file.read(400)  // PAN data
            
        coins.append({header: coin_header, body: coin_body})
    
    file.close()
    return {header: header, coins: coins}
```

### Writing Coin Files
```pseudocode
function writeCoinFile(filename, header, coins):
    file = open(filename, "wb")
    
    // Write header
    file.write(header_to_bytes(header))
    
    // Write coins
    for coin in coins:
        file.write(coin.header)
        file.write(coin.body)
    
    // Add padding if needed
    padding_size = calculate_padding(file.size())
    file.write(random_bytes(padding_size))
    
    file.close()
```

## Best Practices

### File Handling
- **Atomic operations**: Use temporary files for modifications
- **Backup creation**: Create backups before any modifications
- **Permission checking**: Verify read/write permissions
- **Error recovery**: Handle corrupted files gracefully

### Performance Considerations
- **Header-only reads**: Read only header for metadata operations
- **Buffered I/O**: Use appropriate buffer sizes for file operations
- **Memory management**: Avoid loading entire large files into memory
- **Concurrent access**: Handle multiple processes accessing files

This specification ensures consistent coin file handling across all CloudCoin Pro implementations and provides the foundation for reliable password verification and file management operations.
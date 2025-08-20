# Verify Password

This is used to create a function called `verify-password(wallet_path: string, password_hash: string)`. This function takes two arguments: the file path to a CloudCoin wallet directory and a pre-computed password hash to verify.

The primary purpose of this function is to verify that a given password hash matches the password hash stored in coin file headers by comparing the provided hash with the stored hash in encrypted coin files.

## Function Requirements

### 1. Coin File Reading
The function must read coin files from the wallet directory:
- Read coin files from Bank/ and Fracked/ folders (authenticated coins)
- Parse coin file headers to extract password hash information
- Handle different coin file formats and encryption types
- Support both single and multiple coin files

### 2. Password Hash Verification
Verify the password using direct hash comparison:
- Accept pre-computed SHA-256 hash from client
- Extract password hash from coin file headers (bytes 8-14)
- Compare hashes using secure comparison methods
- Validate against multiple coin files for accuracy

### 3. Coin File Format Support
Support the standard CloudCoin binary file format:
- Parse 32-byte file headers
- Handle different encryption types (0=none, 1=128 AES CTR, 4=256 AES CTR)
- Read password hash from header bytes 8-14 (7 bytes)
- Validate file structure and integrity

### 4. Return Value
The function must return a verification result with detailed status information including success/failure and any validation issues encountered.

## Input
- **wallet_path** (string): The path to the CloudCoin wallet directory (e.g., "D:/CloudCoin/Pro/Wallets/MyWallet")
- **password_hash** (string): The pre-computed SHA-256 hash (first 7 bytes as hex string)

## Output
(object): Password verification result with detailed status and validation information

## File Structure
Your code will interact with the following wallet directory structure:

```
wallet_name/
├── Bank/                       # Authenticated coins ready for use
├── Fracked/                    # Partially authenticated coins
├── Import/                     # New coins waiting to be processed
├── Exported/                   # Coins prepared for export
├── Corrupted/                  # Files that couldn't be read properly
├── Counterfeit/                # Coins that failed authentication
├── Duplicates/                 # Duplicate coin files
├── Encryption_Failed/          # Coins with broken encryption keys
├── Errored/                    # Coins that encountered processing errors
├── Grade/                      # Coins after grading/authentication
├── Imported/                   # Successfully processed imports
├── Limbo/                      # Coins with uncertain authentication status
├── Lockered/                   # Coins in RAIDA lockers
├── Pending/                    # Coins waiting for processing
├── Receipts/                   # Transaction receipt files
├── Sent/                       # Coins that have been sent
├── Suspect/                    # Coins with questionable authenticity
├── Trash/                      # Deleted or rejected files
├── Withdrawn/                  # Coins withdrawn from lockers
├── transactions.csv            # Transaction history log
└── config.toml                 # Wallet configuration file
```

## Coin File Format Specification

### File Header Structure (32 bytes)
| Bytes | Name | Description | Values |
|-------|------|-------------|---------|
| 0 | File Version | Version of coin file format | 9 (current) |
| 1 | Cloud ID | Cloud identification number | 1 (default) |
| 2-3 | Coin ID | Coin type identifier | 0-255 |
| 4 | Experimental | Reserved for app use | Any |
| 5 | Encryption Type | Type of encryption used | 0, 1, 4 |
| 6-7 | Token Count | Number of coins in file | 0-65535 |
| 8-14 | **Password Hash** | **First 7 bytes of SHA-256 hash** | **Any** |
| 15 | State Flag | Coin state tracking | 0, 1, 2 |
| 16-31 | POWN String/Task Data | Variable based on coin count | Various |

### Encryption Types
| Code | Meaning |
|------|---------|
| 0 | No encryption |
| 1 | 128-bit AES CTR |
| 4 | 256-bit AES CTR |

### Password Hash Location
- **Location**: Bytes 8-14 (7 bytes total)
- **Format**: First 7 bytes of SHA-256 hash of the encryption password
- **Purpose**: Non-reversible password verification

## Detailed Logic Flow

### 1. Validate Input Parameters
- Check if wallet_path exists and is accessible
- Verify wallet_path points to valid wallet directory
- Validate password_hash parameter is not empty and correct format
- Check read permissions for wallet folders

### 2. Locate Coin Files for Verification
- Scan Bank/ folder for authenticated coin files
- Scan Fracked/ folder for partially authenticated coins
- Filter for .bin files with valid coin file structure
- Prioritize files with encryption enabled (encryption type > 0)

### 3. Parse Password Hash Input
- Accept hash as hex string (14 characters = 7 bytes)
- Convert hex string to binary format for comparison
- Validate hash format and length

### 4. Read and Parse Coin File Headers
- Read first 32 bytes of each coin file (file header)
- Validate file format and version
- Extract encryption type from byte 5
- Extract password hash from bytes 8-14

### 5. Perform Hash Comparison
- Compare provided password hash with stored hash
- Use secure comparison to prevent timing attacks
- Test against multiple coin files for consistency
- Handle edge cases (no encrypted files, corrupted headers)

### 6. Validate File Integrity
- Verify file header structure is valid
- Check file size matches expected format
- Validate coin count and file structure
- Detect corrupted or invalid coin files

### 7. Return Verification Result
- Compile verification status and details
- Include information about files tested
- Report any inconsistencies or errors
- Provide debugging information if needed

## Example Function Call

```bash
verify-password "D:/CloudCoin/Pro/Wallets/MyWallet" "a1b2c3d4e5f6a7"
```

## Hash Format Requirements

### Input Hash Format
- **Length**: Exactly 14 hex characters (7 bytes)
- **Format**: Hex string representing first 7 bytes of SHA-256 hash
- **Example**: `"a1b2c3d4e5f6a7"` represents bytes [0xA1, 0xB2, 0xC3, 0xD4, 0xE5, 0xF6, 0xA7]

### Client-Side Hash Generation
```pseudocode
// Client responsibility - not part of verify-password function
function generatePasswordHash(password: string): string {
    // Convert password to UTF-8 bytes
    passwordBytes = utf8Encode(password)
    
    // Generate SHA-256 hash
    fullHash = sha256(passwordBytes)
    
    // Extract first 7 bytes and convert to hex string
    return bytesToHex(fullHash[0:7])
}
```

## Verification Output Structure

```json
{
  "password_verification": {
    "timestamp": "2025-01-15T10:30:00Z",
    "wallet_path": "D:/CloudCoin/Pro/Wallets/MyWallet",
    "verification_result": "success",
    
    "summary": {
      "hash_valid": true,
      "files_tested": 5,
      "files_matched": 5,
      "files_failed": 0,
      "encrypted_files_found": 3,
      "unencrypted_files_found": 2
    },
    
    "verification_details": {
      "provided_hash": "a1b2c3d4e5f6a7",
      "hash_method": "SHA-256 (first 7 bytes)",
      "comparison_method": "secure_compare",
      "consistency_check": "passed"
    },
    
    "files_analyzed": [
      {
        "filename": "1,000 CloudCoin #7998 'From Ron'.bin",
        "path": "Bank/1,000 CloudCoin #7998 'From Ron'.bin",
        "file_size": 439,
        "encryption_type": 1,
        "encryption_name": "128-bit AES CTR",
        "stored_hash": "a1b2c3d4e5f6a7",
        "hash_match": true,
        "file_valid": true,
        "coin_count": 1
      },
      {
        "filename": "0.001 CloudCoin #89269 ''.bin",
        "path": "Bank/0.001 CloudCoin #89269 ''.bin", 
        "file_size": 439,
        "encryption_type": 1,
        "encryption_name": "128-bit AES CTR",
        "stored_hash": "a1b2c3d4e5f6a7",
        "hash_match": true,
        "file_valid": true,
        "coin_count": 1
      },
      {
        "filename": "12,441.0000-034 CloudCoin #12 ''.bin",
        "path": "Fracked/12,441.0000-034 CloudCoin #12 ''.bin",
        "file_size": 5236,
        "encryption_type": 1,
        "encryption_name": "128-bit AES CTR", 
        "stored_hash": "a1b2c3d4e5f6a7",
        "hash_match": true,
        "file_valid": true,
        "coin_count": 12
      },
      {
        "filename": "Key CloudCoin #499 'IP 46.65.33.34 port 7099 app 25'.bin",
        "path": "Bank/Key CloudCoin #499 'IP 46.65.33.34 port 7099 app 25'.bin",
        "file_size": 439,
        "encryption_type": 0,
        "encryption_name": "No encryption",
        "stored_hash": null,
        "hash_match": "N/A",
        "file_valid": true,
        "coin_count": 1
      }
    ],
    
    "validation": {
      "wallet_structure_valid": true,
      "coin_files_found": true,
      "encrypted_files_available": true,
      "hash_consistency": "all_matches",
      "warnings": [],
      "errors": []
    }
  }
}
```

## Human-Readable Format Option

The function can also return information in a human-readable text format:

```
====================================================
CLOUDCOIN WALLET PASSWORD VERIFICATION
====================================================
Generated: January 15, 2025 at 10:30 AM
Wallet: D:/CloudCoin/Pro/Wallets/MyWallet

VERIFICATION RESULT
====================================================
Password Hash Status: ✅ VALID
Files Tested: 4 coin files
Hash Matches: 3/3 encrypted files
Consistency: All encrypted files match

VERIFICATION DETAILS
====================================================
Provided Hash: a1b2c3d4e5f6a7 (SHA-256, first 7 bytes)
Hash Method: Direct comparison (client-generated)
Encrypted Files: 3 found
Unencrypted Files: 1 found (no verification needed)

FILES ANALYZED
====================================================

✅ 1,000 CloudCoin #7998 'From Ron'.bin (Bank/)
   Encryption: 128-bit AES CTR
   Hash Match: ✅ Valid
   File Size: 439 bytes
   Coins: 1

✅ 0.001 CloudCoin #89269 ''.bin (Bank/)
   Encryption: 128-bit AES CTR  
   Hash Match: ✅ Valid
   File Size: 439 bytes
   Coins: 1

✅ 12,441.0000-034 CloudCoin #12 ''.bin (Fracked/)
   Encryption: 128-bit AES CTR
   Hash Match: ✅ Valid
   File Size: 5,236 bytes
   Coins: 12

ℹ️ Key CloudCoin #499 'IP 46.65.33.34 port 7099 app 25'.bin (Bank/)
   Encryption: None
   Hash Match: N/A (unencrypted)
   File Size: 439 bytes
   Coins: 1

SUMMARY
====================================================
✅ Password hash verification successful
✅ All encrypted files use consistent password
✅ Wallet structure is valid
ℹ️ 1 unencrypted file found (normal)
```

## Error Handling

| Error Condition | Response Action |
|-----------------|-----------------|
| Wallet path doesn't exist | Return error: "Wallet directory not found" |
| No coin files found | Return error: "No coin files available for verification" |
| No encrypted files found | Return warning: "No encrypted files to verify against" |
| Permission denied | Return error: "Unable to read coin files" |
| Invalid hash format | Return error: "Invalid hash format - must be 14 hex characters" |
| Hash mismatch | Return error: "Password hash does not match" |
| Invalid file format | Return error: "Invalid coin file format detected" |
| Empty hash | Return error: "Password hash cannot be empty" |

## Hash Processing Implementation

### Hash Format Validation
```pseudocode
function validateHashFormat(hash: string): boolean {
    // Check length (7 bytes = 14 hex characters)
    if hash.length != 14:
        return false
    
    // Check if all characters are valid hex
    for char in hash:
        if not isHexChar(char):
            return false
    
    return true
}
```

### Hash Conversion
```pseudocode
function hexStringToBytes(hexString: string): bytes[7] {
    bytes = []
    for i = 0 to 12 step 2:
        byte = parseInt(hexString[i:i+2], 16)
        bytes.append(byte)
    return bytes
}
```

### Secure Hash Comparison
```pseudocode
function secureCompare(hash1: bytes[7], hash2: bytes[7]): boolean {
    // Use constant-time comparison to prevent timing attacks
    result = 0
    for i = 0 to 6 {
        result |= hash1[i] XOR hash2[i]
    }
    return result == 0
}
```

## Client Integration Notes

### Client Responsibilities
- **Generate SHA-256 hash** of user password
- **Extract first 7 bytes** from the hash
- **Convert to hex string** format
- **Pass hex string** to verify-password function

### Function Responsibilities
- **Accept pre-computed hash** from client
- **Validate hash format** and length
- **Compare with stored hashes** in coin files
- **Return verification result** with detailed status

## Security Considerations

### Hash Handling
- **No password storage**: Function never receives plaintext passwords
- **Client flexibility**: Allows client to implement custom hashing
- **Secure comparison**: Uses constant-time comparison functions
- **Hash validation**: Verify hash format and length

### File Access Security
- **Read-only access**: Never modify coin files during verification
- **Permission checking**: Verify read permissions before access
- **Path validation**: Sanitize and validate file paths
- **Error handling**: Don't leak sensitive information in error messages

## Integration Notes

- Works with all CloudCoin wallet implementations following standard structure
- Compatible with different encryption types (none, 128-bit AES, 256-bit AES)
- Supports both single and multiple coin files with proper naming convention
- Can be used for wallet access control and security validation
- Provides foundation for password change and encryption management
- Useful for troubleshooting wallet access issues
- References wallet-folder-structure.md for wallet validation
- Integrates with coin file naming convention specifications
- Uses SHA-256 for quantum-safe hashing
- Allows client flexibility in hash generation methods
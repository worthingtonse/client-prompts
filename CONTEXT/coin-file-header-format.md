# Coin File Header Format

Coin files hold the data about coins and coin files will have a coin file header and then many coin chunks (one chunk per coin). Each coin has a coin header.

So there are Coin files. Coin Files have File Headers and an array of coins. Each coin has a coin header and a coin body.

Coin files have a naming convention that makes it easier for software to use them.

## File Header For All Tokens (32 Bytes Fixed)

The coin file header is exactly 32 bytes and contains metadata about the entire file:

```
Byte Position | Field Name | Size | Description | Values
-------------|------------|------|-------------|--------
0            | File Version | 1    | Coin file format version | 9 (current)
1            | Cloud ID | 1        | Cloud identification | 1 (default)
2-3          | Coin ID | 2         | Coin type identifier | 0-255
4            | Experimental | 1     | Reserved for app use | Any
5            | Encryption Type | 1  | Encryption method used | 0, 1, 4
6-7          | Token Count | 2      | Number of coins in file | 0-65535
8-14         | Password Hash | 7    | First 7 bytes of SHA-256 hash | Any
15           | State Flag | 1       | Coin state tracking | 0, 1, 2
16-31        | POWN/Task Data | 16  | Variable based on coin count | Various
```

## File Header Byte Explanation

| Index | Code | Bytes | Name | Possible Values | Description |
|-------|------|-------|------|-----------------|-------------|
| 00 | FT | 1 | File Version | 9 | We are on file version 9 now |
| 01 | CL | 1 | Cloud ID | 1 | If creating a new standalone cloud, choose an unused number |
| 02,03 | ID | 2 | Coin ID | 0-255 | This is if there are more than one coin on your cloud. Useful for NFTs, Stable Tokens, etc. |
| 04 | SP | 1 | Experimental | Any | App programmer can use this as they like |
| 05 | EN | 1 | Encryption Type | 0, 1, 4 | The type of encryption to be used (See Encryption Types table) |
| 06,07 | CC | 2 | Token Count | 0-65535 | How many notes are in the file. Not the total value but total count |
| 08-14 | HS | 7 | Password Hash | Any | First 7 bytes of the encryption key's SHA-256 Hash |
| 15 | FL | 1 | State Flag | 0, 1, 2 | Optional: Used as a way to track state if needed. See table below for meanings |

## State Table (Optional and for internal use)

| Value Dec | State | Value Binary | Description |
|-----------|-------|--------------|-------------|
| 0 | Current | 00000000 | This file contains passwords that are the last known good but not guaranteed. Therefore they are suspect. No Proposed Authenticity Numbers are present. Each coin uses 400 bytes and not 800 bytes. These files are found in the "Suspect" folder. |
| 1 | Pending | 00000001 | Used within a program during the pown process. In addition to the 400 bytes of the current authenticity numbers, each coin holds 400 bytes of pending passwords that are the PANs (Proposed Authenticity Numbers) that will be sent to the raida. |
| 2 | Confirmed | 00000010 | This coin has gone through pown process and the status of each AN is known (although the status of some maybe "Limbo" that describes that it is known that the state of the authenticity number is unknown). These coins are usually found in the "Grade" folder |
| 3-255 | Expansion | 00000011-11111111 | These bits are free for experimentation |

### Alternative to Track State
```
wallet-name/
├── Suspect/  (This is the current passwords that are thought to be good)
│   └── coinname.bin
└── Pending/ (This is a copy of the coin with just the proposed authenticity numbers) 
    └── coinname.bin
```

## Last 16 bytes of the header if the Coin File has many coins in it

| Index | Code | Bytes | Name | Possible Values | Description |
|-------|------|-------|------|-----------------|-------------|
| 17-31 | PS | 16 | Motto | "4C 69 76 65 20 46 72 65 65 20 4F 72 20 44 69 65" | This translates to "Live Free or Die" in ASCII. See [POWN String Codes](pown-string-codes.md) |

## Last 16 bytes of the header if the Coin File has only one coin in it

| Index | Code | Bytes | Name | Possible Values | Description |
|-------|------|-------|------|-----------------|-------------|
| 17-28.5 | PS | 12.5 | Pown String | 0x0,0xA,0xB,0xC,0xE,0xF | [POWN String Codes](pown-string-codes.md) |
| 29.5-30 | EX | 0.5 | Experimental | Any | App programmer can use this as they like |
| 30-31 | TI | 2 | Task ID | Any | Allows program to give coin a tracking number for accounting purposes |
| 32 | EX | 1 | Experimental | Any | App programmer can use this as they like |

## File Encryption Types

| Code | Meaning |
|------|---------|
| 0 | No encryption |
| 1 | 128 AES CTR |
| 4 | 256 AES CTR |

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

### Hash Generation Process (Client Responsibility)
1. **Input**: Plain text password (UTF-8 encoded)
2. **Algorithm**: SHA-256 hash generation
3. **Storage**: First 7 bytes of SHA-256 hash stored in header bytes 8-14
4. **Verification**: Compare first 7 bytes of password hash with stored hash

### Hash Storage Format
```c
// Example hash storage in header
unsigned char password_hash[7] = {0xA1, 0xB2, 0xC3, 0xD4, 0xE5, 0xF6, 0xA7};
```

### Verification Algorithm
```pseudocode
function verifyPasswordHash(file, providedHash):
    header = readHeader(file, 32)
    if header.encryption_type == 0:
        return "no_encryption_needed"
    
    stored_hash = header.password_hash[8:15]  // 7 bytes
    provided_hash_bytes = hexToBytes(providedHash)  // Convert hex string to bytes
    
    
# Coin File Naming Convention

By using a standard naming convention, applications and users can see how many coins a file holds and tag the coins with memos.

The binary files will have a common naming convention. There is one convention for files with a single note and another for files with many notes.

## Single Note File Names

We are accurate to one satoshi which represents a decimal, seven zeros, and a 1. However, for ease of human reading, we display fractions with a hyphen between every four digits. Trailing zeros are removed.

| Index | Part Name | Allowable Values | Description |
|-------|-----------|------------------|-------------|
| 0 | Denomination | See [Denominations](denominations.md) | Number formatted |
| 1 | Space Separator | ' ' | A space to separate index 0 and 1 |
| 2 | CoinName | "CloudCoin" | Name of the coin |
| 3 | Space Separator | ' ' | A space to separate index 2 and 3 |
| 4 | Prefix | '#' | Shows the next number will be a serial number |
| 5 | Serial Number | Any Four Bytes | The serial number of the coin formatted as an unsigned integer |
| 6 | Space Separator | ' ' | A space to separate index 5 and 6 |
| 7 | Tag | Any string allowable in all OS's filenames | Add an apostrophe at the front and end of the string |
| 8 | Extension | ".bin" | Short for binary. Allows binary readers to open it |

### Sample Single Note File Names:
```
1,000 CloudCoin #7998 'From Ron'.bin
Key CloudCoin #499 'IP 46.65.33.34 port 7099 app 25'.bin
0.001 CloudCoin #89269 ''.bin
0.000-0001 CloudCoin #879398 'j'.bin
```

## File Naming Convention For Files with Multiple Coins

If there are more than 1 token in the file, the sum of all the tokens will be in the name and so will the number of coins.

| Index | Part Name | Allowable Values | Description |
|-------|-----------|------------------|-------------|
| 0 | Total Value | Any value formatted with commas after each 3 digits in whole numbers and hyphens after each four digits for fractions. No zeros at the end | How much the coin file is worth |
| 1 | Space Separator | ' ' | A space to separate index 0 and 1 |
| 2 | CoinName | "CloudCoin" | Name of the coin |
| 3 | Space Separator | ' ' | A space to separate index 2 and 3 |
| 4 | Prefix | '#' | Shows the next number will be a number |
| 5 | Number of Notes | Any two Bytes | The number of coins in the coin file |
| 6 | Space Separator | ' ' | A space to separate index 5 and 6 |
| 7 | Tag | Any string allowable in all OS's filenames | Add an apostrophe at the front and end of the string |
| 8 | Extension | ".bin" | Short for binary. Allows binary readers to open it |

### Sample Multiple Coin File Names:
```
0.0830-01 CloudCoin #55 'From Ron'.bin
0.5016-7 CloudCoin #89 ''.bin
0.0040-0099 CloudCoin #2 ''.bin
12,441.0000-034 CloudCoin #12 ''.bin
```

## Formatting Rules

### Number Formatting
- **Whole numbers**: Use commas after every 3 digits (e.g., 1,000; 12,441)
- **Fractions**: Use hyphens after every 4 digits (e.g., 0.0000-0001; 0.5016-7)
- **Trailing zeros**: Remove trailing zeros from the end
- **Leading zeros**: Remove unnecessary leading zeros

### Tag Formatting
- **Apostrophes**: Surround the tag with single apostrophes
- **Empty tags**: Use '' for empty tags
- **OS compatibility**: Use only characters allowed in all operating system filenames
- **Special characters**: Avoid characters that conflict with file system restrictions

### Examples by Category

#### Small Denominations (Fractions)
```
0.000-0001 CloudCoin #123456 'micro payment'.bin
0.0001 CloudCoin #789012 'test coin'.bin
0.001 CloudCoin #345678 'fee payment'.bin
0.01 CloudCoin #901234 ''.bin
```

#### Standard Denominations
```
1 CloudCoin #567890 'daily allowance'.bin
5 CloudCoin #234567 'coffee money'.bin
25 CloudCoin #890123 'lunch fund'.bin
100 CloudCoin #456789 'grocery shopping'.bin
```

#### Large Denominations
```
1,000 CloudCoin #012345 'rent payment'.bin
10,000 CloudCoin #678901 'car payment'.bin
100,000 CloudCoin #234567 'house down payment'.bin
```

#### Multiple Coin Files
```
156.25 CloudCoin #8 'weekly savings'.bin
1,500.50 CloudCoin #15 'vacation fund'.bin
25,000.75 CloudCoin #100 'business investment'.bin
```

#### Special Purpose Coins
```
Key CloudCoin #499 'IP 46.65.33.34 port 7099 app 25'.bin
Token CloudCoin #888 'NFT metadata link'.bin
Certificate CloudCoin #777 'ownership proof'.bin
```

## Validation Rules

### File Name Validation
- **Required components**: All parts (denomination/value, "CloudCoin", serial/count, tag, extension) must be present
- **Proper spacing**: Exactly one space between each component
- **Correct formatting**: Numbers must follow formatting rules
- **Valid characters**: Only OS-compatible characters in tags
- **Extension**: Must end with ".bin"

### Parsing Guidelines
- **Split by spaces**: Use space as the primary delimiter
- **Identify type**: Single coin (has #serial) vs multiple coins (has #count)
- **Extract value**: Parse denomination or total value with proper number formatting
- **Extract identifier**: Get serial number or coin count
- **Extract tag**: Remove apostrophes from tag content
- **Validate extension**: Ensure ".bin" extension

### Error Handling
- **Invalid format**: Reject files that don't follow the naming convention
- **Missing components**: Flag files with missing required parts
- **Invalid characters**: Warn about problematic characters in tags
- **Number format errors**: Report incorrectly formatted values
- **Duplicate names**: Handle naming conflicts appropriately

## Implementation Notes

### File Creation
- Generate names automatically based on coin content
- Validate names before file creation
- Handle OS-specific filename restrictions
- Ensure uniqueness within directories

### File Reading
- Parse names to extract metadata
- Use naming convention to determine file type
- Extract value and count information from names
- Validate naming convention compliance

### Cross-Platform Compatibility
- Avoid OS-specific forbidden characters
- Handle case sensitivity differences
- Support Unicode characters where appropriate
- Test compatibility across Windows, Linux, and Mac

This naming convention ensures that CloudCoin files are self-describing, easily identifiable, and compatible across all platforms while providing essential metadata directly in the filename.


# Coin File Header Format

Coin files hold the data about coins and coin files will have a coin file header and then many coin chunks (one chunk per coin). Each coin has a coin header.

So Coin Files have two parts, the File Header and the coin array. Each coin in the coin array has a Coin header and a Coin body.

Coin files have a naming convention that makes it easier for software to use them.

## File Header For All Tokens (32 Bytes Fixed)

The coin file header is exactly 32 bytes and contains metadata about the entire file:


Byte Position | Field Name | Byte Size | Description | Values
-------------|------------|------|-------------|--------
0            | File Format | 1    | The format of the coin file | Format ID 9 (We are only using one file format now)
1            | Reserved | 1        | For future use | 1 is the default. Can be ignored
2-3          | Coin ID | 2         | There can be lots of coins besides CloudCoin | CloudCoin is 0x0006 Others should be rejected. 
4            | Experimental | 1     | Reserved for app use | Any
5            | Encryption Type | 1  | File Encryption method | 0,1 or 4
6-7          | Token Count | 2      | Number of coins in file | 0-65535
8-14         | Password Hash | 7    | First 7 bytes of the encryption key's SHA-256 Hash. This allows us to know if the user entered the wrong password to decrypt the coin array | 
15           | Future Use | 1       | For future use

<!--
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
-->
## Many Coins: Last 16 bytes of the header if the Coin File has many coins in it
We fill this space with a motto if there are more than one coin
| Index | Code | Bytes | Name | Possible Values | Description |
|-------|------|-------|------|-----------------|-------------|
| 16-31 | PS | 16 | Motto | "4C 69 76 65 20 46 72 65 65 20 4F 72 20 44 69 65" | This translates to "Live Free or Die" in ASCII. See [POWN String Codes](pown-string-codes.md) |

## One Coin: Last 16 bytes of the header if the Coin File has only one coin in it
We put the pown string here to tell us the results of the last authentication
| Index | Code | Bytes | Name | Possible Values | Description |
|-------|------|-------|------|-----------------|-------------|
| 16-28 | PS | 13 | Pown String 4 bits x 25 | 0x0,0xA,0xB,0xC,0xE,0xF | Last 4 bits are empty [POWN String Codes](pown-string-codes.md) |
| 28-31 | TI | 3| Task ID | Any | Program's tracking number. Number of .25 minutes (15 seconds) since start of year. |

# POWN String Codes

POWN (Password Ownership) codes are used throughout the CloudCoin client and server software to make it possible to track the status of coins. These codes can be expressed as strings of characters like "ppuppppfpppeppppppnppbpep" or in four bit binary such as here shown as hex "AA 0A AA AF AA AA AA AA AA CA AB AE A3". The last four bits are ignored and can be anything. 

After a coin is sent to the 25 Raidas to be checked for authenticty, there will idealy be 25 responses. To keep track of these responses we have a POWN string.
POWN means Password Own. 

These codes are placed in coin files that have only one coin in them. Otherwise, the motto is used instead of the pown string. 

##  Pown String In Files with Many Coins
If a coin file has more than one coin in it, there will be no pown string, task ID or experimental bytes. Instead, 
CloudCoin's moto will be used instead. The motto is "Live Free or Die".

Live free or die translates to hex: "4C 69 76 65 20 46 72 65 65 20 4F 72 20 44 69 65" in ASCII.

## Pown String with only one Coin
If a coin file only has one coin in it, it is probably because the coin file is inside of a program and the status of the coin needs to be tracked. There are
25 status codes that each require four bits. These are encoded into hexidecimal numbers that are easy to understand by the naked eye. 

Character Code | Hex Code | Name | Meaning 
---|---|---|---
u |0x0 | Untried/Unknown   | The raida failed to return an echo request so the client did not send that raida a pown request.
p | 0xA | Pass/Authentic | The raida responded that the coin was authentic. 
b | 0xB | Broke Encryption Key | The raida could not decrypt the request because the encryption key was not authentic.  
n | 0xC | No Reply/Clock Timeout | The raida did not respond in the expected timeframe. This is usally caused by lost packets while using the UPD protocol.
d | 0xD | Dropped |There was a network error that had nothing to do with the RAIDA
e | 0xE | Error |The raida responded with an error or the RAIDA refused the connection showing that the raida was there. 
f | 0xF | Failed/Counterfiet |The raida responded that the coin was counterfeit. 




## File Encryption Types

| Code | Meaning |
|------|---------|
| 0 | No encryption |
| 1 | 128 AES CTR |
| 4 | 256 AES CTR |

## Individual Coin Structure

Each coin within the file has its own header and body:

### Coin Header (7 bytes)

Byte | Field | Values | Description
-----|-------|--------|-------------
0    | Split | 0      | Future use for splits
1    | Shard | 0      | Future use for shards  
2    | Denomination | -7 to +11 | Binary denomination value
3-6  | Serial Number | Any | Unique coin identifier

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
```java
// Example hash storage in header
unsigned char password_hash[7] = {0xA1, 0xB2, 0xC3, 0xD4, 0xE5, 0xF6, 0xA7};
```

### Verification Algorithm
```c
function verifyPasswordHash(file, providedHash):
    header = readHeader(file, 32)
    if header.encryption_type == 0:
        return "no_encryption_needed"
    
    stored_hash = header.password_hash[8:15]  // 7 bytes
    provided_hash_bytes = hexToBytes(providedHash)  // Convert hex string to bytes
    
    
# File Format for Binary Files

## Coin Header
Each coin in the file has a header made up of 7 bytes. 

Index | Name | Allowable Values | Description
---|---|---|---
0 | Split | 0 | For future use if splits are implemented
1 |Shard | 0 | For future use if shards are implemented
2 | Denomination | -8 to +11 inclusive | The binary version of the denominations. See [Denominations](denominations.md)
3-6 | Serial Number | Any four bytes | Used together with the denomination to identify the coin. 

## Coin Body

Rules:

Condition | Bytes | explanation
---|---|---
Always | 400  | 25 GUIDs. 16 bytes per GUID (The original ANs before the call)
If index 15/State Flag in the file header is set to 1, include the PANs | +400 | The PANs that were sent to the server but no reply
NOTE: THIS WAS DELETED but is here incase it is somewhere in the code and no one knows why. If the Coin is the last coin | + Padding  | Add random bytes to make the entire coin body divisable by 32. The number of coins in the file is in the File Header (bytes 24-27)

<!--
If Coin Type is NFT | +128 | Add 128 Fixed Bytes for the file's Title.
If Coin Type is NFT | +128 | Add 128 Fixed Bytes for the file's Meta Information.
If Coin Type is NFT | + The File Size | The Variable bytes of the file
-->


Sample Coin Body:
```c
SP SH DN SN SN SN SN // Header for first coin
AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN  AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN  AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN   
AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN  AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN  AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN  
AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN  AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN  AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN  
AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN  AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN  AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN  
AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN  AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN  AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN  
AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN  AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN  AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN  
AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN  AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN  AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN  
AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN  AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN  AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN  
AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN
SP SH DN SN SN SN SN // Header for second coin
AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN  AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN  AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN   
AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN  AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN  AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN  
AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN  AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN  AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN  
AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN  AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN  AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN  
AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN  AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN  AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN  
AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN  AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN  AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN  
AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN  AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN  AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN  
AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN  AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN  AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN  
AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN  
PD PD PD PD PD PD PD PD PD // Padding for whole body 
```

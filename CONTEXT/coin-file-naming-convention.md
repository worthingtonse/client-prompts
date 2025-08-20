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
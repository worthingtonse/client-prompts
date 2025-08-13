
# Get Transaction Receipt Prompt

This is used to create a function called `get-transaction-receipt(wallet_path: string, receipt_filename: string)`. This function will take two arguments: the file path to a user's wallet folder and a receipt filename.

The primary purpose of this function is to locate and read a specific transaction receipt file from the Receipts folder and return its complete content as a text string without any processing or formatting. The receipt file contains pre-formatted transaction details that are ready for display.

## Function Requirements

### 1. Wallet and Receipt Validation
A "wallet" is a directory containing a transactions.csv file and subdirectories including Bank, Fracked, and Receipts.
The function must locate the receipt file within the Receipts subfolder using the provided receipt_filename.
The receipt_filename includes the full filename with extension (e.g., "2025-02-25_17-34-00.withdraw-to-locker.txt").

### 2. Receipt File Reading
The function needs to read the receipt file located at `{wallet_path}/Receipts/{receipt_filename}`.
The function must read the entire file content and return it as-is without any parsing, processing, or formatting.
Receipt files are pre-formatted text files created by the transaction commands and are ready for display.

### 3. Return Value
The function must return the complete content of the receipt file as a single text string, preserving all original formatting and content.

## Input
- **wallet_path** (string): The absolute or relative path to the wallet directory
- **receipt_filename** (string): The complete filename of the receipt including extension (e.g., "2025-02-25_17-34-00.withdraw-to-locker.txt")

## Output
(string): The entire content of the receipt file as a text string.

## File Structure
Your code will interact with the following directory and file structure:

```
/path/to/wallet_name/
|-- Bank/
|   |-- 1,000 CloudCoin #7998 'From Ron'.bin
|   `-- 0.001 CloudCoin #89269 'Task 231'.bin
|-- Fracked/
|   `-- 0.0000-001 CloudCoin #879398 'j'.bin
|-- Receipts/
|   |-- 2025-02-25_17-34-00.withdraw-to-locker.txt
|   |-- 2025-03-08_16-08-00.deposit-from-file.txt
|   `-- 2025-04-04_12-41-00.pown-authentication.txt
|-- transactions.csv
`-- main.log
```

The receipt files contain pre-formatted transaction details created by the transaction commands. The format and content are described in receipt-file-format.md in the CONTEXT folder.

## Detailed Logic Flow

### 1. Receive Parameters
The function is called with the `wallet_path` and `receipt_filename`.

### 2. Validate Wallet Structure
- Verify that `wallet_path` exists and is a directory
- Check that the Receipts subdirectory exists within the wallet
- If validation fails, return an error indicating the issue

### 3. Locate Receipt File
- Construct the receipt file path: `{wallet_path}/Receipts/{receipt_filename}`
- Verify that the receipt file exists
- If the file doesn't exist, return an error indicating receipt not found

### 4. Read Receipt File Content
- Open the receipt file for reading
- Read the entire file content into a string variable
- Close the file
- Return the complete file content as-is

## Receipt Filename Format

Receipt filenames follow this format: `YYYY-MM-DD_HH-MM-SS.transaction-type.txt`

Examples:
- `2025-02-25_17-34-00.withdraw-to-locker.txt`
- `2025-03-08_16-08-00.deposit-from-file.txt`
- `2025-04-04_12-41-00.pown-authentication.txt`
- `2025-01-15_09-22-30.break-coins.txt`
- `2025-06-20_14-55-15.join-coins.txt`

Where:
- **YYYY-MM-DD_HH-MM-SS**: Timestamp (also serves as Task ID)
- **transaction-type**: Descriptive name of the transaction type
- **.txt**: File extension

## Error Handling

The function should handle these error conditions:

| Error Condition | Response Action |
|-----------------|-----------------|
| Wallet path doesn't exist | Return error: "Wallet directory not found" |
| Receipts folder missing | Return error: "Receipts directory not found in wallet" |
| Receipt file doesn't exist | Return error: "Receipt file '{receipt_filename}' not found" |
| File permission issues | Return error: "Unable to read receipt file" |
| Empty receipt file | Return empty string |

## Best Practices Compliance

This function follows the established best practices:

- **Never Delete Files**: Only reads receipt files, never modifies or deletes them
- **Work Out of RAM**: Minimal memory usage for file reading
- **Consistent Folder Structure**: Uses standardized wallet directory layout
- **Data-Driven Approach**: Simple file reading without complex processing
- **Error Recovery**: Handles various failure scenarios gracefully

## Integration Notes

- This function is read-only and safe to call multiple times
- Receipt files are created by transaction commands (pown, deposit, withdraw, etc.)
- The receipt format and content standards are defined in receipt-file-format.md
- The function requires no knowledge of receipt content structure
- Can be used for displaying receipts, audit trails, and transaction history
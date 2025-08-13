# Receipt File Format Specification

This document defines the standard format for transaction receipt files created by multiple RAIDA commands. All transaction commands that process coins must create receipt files following this specification to ensure consistency across the system.

## File Naming Convention

Receipt files must follow this naming format:
```
YYYY-MM-DD_HH-MM-SS.transaction-type.txt
```

### Naming Components:

| Component | Description | Example |
|-----------|-------------|---------|
| YYYY-MM-DD | Date in ISO format | 2025-02-25 |
| HH-MM-SS | Time in 24-hour format | 17-34-00 |
| transaction-type | Descriptive transaction name | withdraw-to-locker |
| .txt | File extension | .txt |

### Common Transaction Types:

| Transaction Type | Filename Example |
|------------------|------------------|
| Deposit from file | `2025-02-25_17-34-00.deposit-from-file.txt` |
| Withdraw to file | `2025-02-25_17-34-00.withdraw-to-file.txt` |
| Withdraw to locker | `2025-02-25_17-34-00.withdraw-to-locker.txt` |
| Deposit from locker | `2025-02-25_17-34-00.deposit-from-locker.txt` |
| POWN authentication | `2025-02-25_17-34-00.pown-authentication.txt` |
| Break coins | `2025-02-25_17-34-00.break-coins.txt` |
| Join coins | `2025-02-25_17-34-00.join-coins.txt` |
| Fix coins | `2025-02-25_17-34-00.fix-coins.txt` |
| Find coins | `2025-02-25_17-34-00.find-coins.txt` |
| Echo test | `2025-02-25_17-34-00.echo-test.txt` |

## Receipt File Content Format

### Header Section
Every receipt file must start with a header containing:
1. Transaction summary information
2. Timestamp and task ID
3. Summary statistics

### Detail Section  
Following the header, list individual coin results with:
1. Serial number
2. Denomination
3. POWN string (RAIDA responses)
4. Final result/status

### Footer Section (Optional)
End with any additional information such as:
1. Error messages
2. Warnings
3. Next steps or recommendations

## Sample Receipt File Content

```
=================================================
CLOUDCOIN TRANSACTION RECEIPT
=================================================
Task ID: 2025-02-25_17-34-00
Transaction Type: POWN Authentication
Date & Time: February 25, 2025 at 5:34:00 PM
=================================================

SUMMARY STATISTICS:
Total Coins Processed: 5
├─ Bank Folder (Authentic): 3
├─ Fracked Folder: 1  
├─ Counterfeit: 1
└─ Limbo: 0

=================================================
COIN-BY-COIN RESULTS:
=================================================
Serial: 7395, Denomination: 1, Result: Authentic
POWN: uppnppppppppppppupppppppp
Final Location: Bank folder

Serial: 7404, Denomination: 1, Result: Authentic  
POWN: uppnppppppppppppupppppppp
Final Location: Bank folder

Serial: 8821, Denomination: 0, Result: Authentic
POWN: uppnppppppppppppupppppppp
Final Location: Bank folder

Serial: 9156, Denomination: 2, Result: Fracked
POWN: uppnpppppnppppppuppppppp
Final Location: Fracked folder

Serial: 5577, Denomination: 1, Result: Counterfeit
POWN: nnnnnnnnnnnnnnnnnnnnnnn
Final Location: Rejected (not stored)

=================================================
TRANSACTION COMPLETED SUCCESSFULLY
=================================================
```

## Receipt Content Guidelines

### 1. Formatting Standards
- Use clear section dividers (===== lines)
- Align text consistently
- Use descriptive labels
- Include proper spacing for readability

### 2. Required Information
- **Task ID**: Always include the timestamp as task ID
- **Transaction Type**: Clear description of operation performed
- **Summary Statistics**: Count of coins by final status
- **Individual Results**: Details for each coin processed

### 3. Status Terminology
Use consistent terminology for coin results:
- **Authentic**: Coin passed authentication → Bank folder
- **Fracked**: Coin partially authentic → Fracked folder  
- **Counterfeit**: Coin failed authentication → Rejected
- **Limbo**: Coin status uncertain → Limbo folder
- **Error**: Processing error occurred

### 4. POWN String Display
- Show complete 25-character POWN string
- Use consistent formatting
- Include explanation if helpful for user

### 5. Folder Destinations
Clearly indicate where each coin ended up:
- Bank folder (for authentic coins)
- Fracked folder (for partially authentic coins)
- Limbo folder (for uncertain status)
- Rejected (for counterfeit coins)
- Error folder (for processing errors)

## Implementation Notes

### For Command Developers
1. **Always create receipts**: Every transaction command must generate a receipt file
2. **Use timestamp as Task ID**: The filename timestamp serves as the unique task identifier
3. **Include summary statistics**: Calculate and display counts by result type
4. **Show individual results**: List each coin with its specific outcome
5. **Handle errors gracefully**: Include error information in receipt when appropriate

### For Utility Functions
A `create-receipt` utility function should be available that accepts:
- Timestamp/Task ID
- Transaction type
- Array of coin results (serial, denomination, pown string, result)
- Summary statistics
- Additional metadata

### File Storage
- All receipts stored in `{wallet_path}/Receipts/` folder
- Files are never deleted (following best practices)
- Receipts can be compressed periodically if needed
- Maintain chronological order for easy access

## Best Practices

1. **Consistency**: All commands use the same format
2. **Readability**: Receipts should be human-readable
3. **Completeness**: Include all relevant transaction details
4. **Timestamps**: Always use the same timestamp format
5. **Error Handling**: Include error details when transactions fail
6. **File Safety**: Never overwrite existing receipt files

This standardized format ensures that all transaction receipts across the system are consistent, readable, and contain all necessary information for auditing and user reference.
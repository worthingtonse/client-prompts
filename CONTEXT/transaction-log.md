# Format of the transactions.csv file

The file `transactions.csv` is located in the root of every wallet folder.
This file tracks the transactions such as deposit, withdraw, transfer so a person has a history of their activities. 
-----

## **File Structure**

Your code will interact with the following directory and file structure:

```
/path/to/wallet_name/
`-- transactions.csv
```

The `transactions.csv` file has the following columns: `Symbol`, `Task ID`, `Date & Time`, `Remarks`, `Deposit`, `Withdraw`, `Description`, `Balance`. This header row is always the first row. New transactions are always inserted under the header row and become the 2nd row

-----

## **Failed Transactions**
Even if transaction fails, it must be listed in the `transactions.csv` file. The remarks will say failed or success.  

-----

## **Record Column Formatting**

 Column      | Formatting Instructions 
 :---------- | :-----------------------
**Symbol** | These are either green or red unless they are a balance adjustment. See the types table below.
**Task ID** | If the event has a Task ID, it will go here in format "command date time microseconds timezone". Examples: `"deposit Aug-19-2025 2:24pm 2321 PST"`, `"withdraw Aug-19-2025 3:15pm 1847 PST"`, `"transfer Aug-19-2025 4:30pm 5692 EST"`. When coins are deposited, that task will get an ID.                                                                 
**Date & Time** | Use the user's local date and time. Enclose the entire string in double quotes (e.g., `"7/8/2025, 3:15 PM"`).                                                
**Remarks** | See about table below Create a descriptive string, such as `"150 coins missing"` or `"25 coins found"`, based on the adjustment amount.                           
**Deposit** | This will be the amount that was deposited or the amount that the wallet increased.                                                                              
**Withdraw** | This will be the amount that was withdrawn or the amount that the wallet decreased. See table below.
**Description** | Set this to the string to the default description `"Balance Adjusted"`. 
**Balance** | The true balance (total coins actually in the wallet). Format this as a string, using the user's locale for number formatting. For any fractional part, insert a hyphen after the fourth digit if there are more than four non-zero digits. Remove any trailing zeros from the fraction. For instance, `211150.79389913` becomes `"211,150.7938-9913"`. 

## **Deposit Types**
Symbols should be the color Green. 
| Deposit Symbol | Default Description | Default Remarks
| :----------- | :--------- | :--------- 
| 🡆| Deposited coin files | Success or Failed
| 🡇| Downloaded from locker | {Locker code} or Failed
| 🡆| Transferred In | Transferred from {wallet name}
| 🡇| Purchased from swap | Swapped with { currency code like BTC}
| 🡇| Delisted from sales | Success or Failed
| ⚠️| Balance Adjusted Up | `"25 coins found"`
| ⭿| Converted from CCv1 | Success or Failed
| ⭿| Convert from CCv2 | Success or Failed

## **Withdraw Types**
Symbol should be the color Red
| Withdraw Symbol | Default Description | Default Remarks
| :----------- | :--------- | :--------- 
| 🡄| Withdrawn to file | path/to/file/filename
| 🡅| Uploaded to locker | {Locker code} or Failed
| 🡄| Transferred Out | Transferred to {wallet name}
| 🡅| Listed for sale | Swap for { currency code like BTC}
| ⚠️| Balance Adjusted Down | `"150 coins missing"`

## **Sample Transaction Records**

Here are examples of how transactions should be recorded with the new task ID format:

### Successful Deposit
```csv
🡆,"deposit Aug-19-2025 2:24pm 2321 PST","8/19/2025, 2:24 PM","Success",100.0,,"Deposited coin files","1,250.0"
```

### Failed Withdrawal
```csv
🡄,"withdraw Aug-19-2025 3:15pm 1847 PST","8/19/2025, 3:15 PM","Failed",,50.0,"Withdrawn to file","1,250.0"
```

### Balance Adjustment
```csv
⚠️,,"8/19/2025, 4:30 PM","25 coins found",25.0,,"Balance Adjusted","1,275.0"
```

### Transfer Operation
```csv
🡄,"transfer Aug-19-2025 4:45pm 5692 EST","8/19/2025, 4:45 PM","Transferred to BusinessWallet",,200.0,"Transferred Out","1,075.0"
```
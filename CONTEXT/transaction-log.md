# Format of the transactions.csv file

The file `list_transactions` is located in the root of very wallet folder.
This file tracks the transactions such as deposit, withdraw, transfer so a person has a history of their activities. 
-----

## **File Structure**

Your code will interact with the following directory and file structure:

```
/path/to/wallet_name/
`-- transactions.csv
```

The `transactions.csv` file has the following columns: `Symbol`, `Task ID`, `Date & Time`, `Remarks`, `deposit`, `withdraw`, `discription`, `Balance`. This header row is always the first row. New transactions are always inserted under the header row and become the 2nd row

-----

## **Failed Transactions**
Even if transaction fails, it must be listed in the `transactions.csv` file. The remarks will say failed or success.  

-----

## **Record Column Formatting**

 Column      | Formatting Instructions 
 :---------- | :-----------------------
**Symbol** | These are either green or red unless they are a balance adjustment. See the types table below.
**Task ID** | If the event has a Task ID, it will go here. When coins are deposited, that task will get an ID.                                                                 
**Date & Time** | Use the user's local date and time. Enclose the entire string in double quotes (e.g., `"7/8/2025, 3:15 PM"`).                                                
**Remarks** | See about table below Create a descriptive string, such as `"150 coins missing"` or `"25 coins found"`, based on the adjustment amount.                           
**Deposit** | This will be the amount that was depositied or the amount that the wallet increased.                                                                              
**Withdraw** | This will be the amount that was withdrawn or the amount that the wallet decreased. See table below.
**Discription** | Set this to the string to the default description `"Balance Adjusted"`. 
**Balance** | The true balance (total coins actually in the wallet). Format this as a string, using the user's locale for number formatting. For any fractional part, insert a hyphen after the fourth digit if there are more than four non-zero digits. Remove any trailing zeros from the fraction. For instance, `211150.79389913` becomes `"211,150.7938-9913"`. 

## **Deposit Types**
Symbols should be the color Green. 
| Deposit Symbol | Default Description | Default Remarks
| :----------- | :--------- | :--------- 
| 🡆| Deposited coin files | Success or Failed
| 🡇| Downloaded from locker | {Locker code} or Faile
| 🡆| Transfered In | Transfered from {wallet name}
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
| 🡄| Transfered Out | Transfered to {wallet name}
| 🡅| Listed for sale | Swap for { currency code like BTC}
| ⚠️| Balance Adjusted Down | `"150 coins missing"`

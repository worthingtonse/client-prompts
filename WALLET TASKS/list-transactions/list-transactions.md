# List Transactions Prompt
This is used to create a function called `list-transactions(string path)`. This function will take one argument: the file path to a user's wallet folder.

The primary purpose of this function is to ensure the running balance in a `transactions.csv` file, located within the specified wallet folder, accurately reflects the true number of "coins" stored in that wallet. If there's a discrepancy, the function must add an "Adjustment" record to the `transactions.csv` file to correct the balance. Finally, it should return the entire, potentially updated, content of the `transactions.csv` file as a single string.

-----

## **Function Requirements**

### **1. Wallet and Coin Verification**

  * A "wallet" is a directory containing a `transactions.csv` file and two subdirectories: `Bank` and `Fracked`.
  * The function must calculate the "true balance" by summing the values of all coin files within the `Bank` and `Fracked` subfolders.
  * The value of each coin file is determined by reading the number at the very beginning of the file, from the first byte up to the first space character.

### **2. Balance Reconciliation**

  * The function needs to read the "last recorded balance" from the `transactions.csv` file. This value is located in the last column of the second row (the first data row after the header).
  * It will then compare the "true balance" with the "last recorded balance."

### **3. Handling Discrepancies**

  * If the balances do not match, an "Adjustment" transaction must be created and prepended as a new second row to the `transactions.csv` file (i.e., inserted immediately after the header row).
  * This adjustment record will bring the recorded balance in line with the true balance. For example, if the `transactions.csv` shows a balance of 500, but the actual coin count is 450, the adjustment amount will be -50.

### **4. Return Value**

  * Regardless of whether an adjustment was needed, the function must return the complete contents of the `transactions.csv` file as a single string.

-----

## **Input**

  * `wallet_path` (string): The absolute or relative path to the wallet directory.

-----

## **Output**

  * (string): The entire content of the `transactions.csv` file.

-----

## **File Structure**

Your code will interact with the following directory and file structure:

```
/path/to/wallet_name/
|-- Bank/
|   |-- 1,000 CloudCoin #7998 'From Ron'.bin
|   `-- 0.001 CloudCoin #89269 'Task 231'.bin
|-- Fracked/
|   `-- 0.0000-001 CloudCoin #879398 'j'.bin
`-- transactions.csv
```

The `transactions.csv` file has the following columns: `Task ID`, `Date & Time`, `About`, `Type`, `Memo`, `Amount`, `Balance`. New transactions are always added to the top, just below the header row.

-----

## **Detailed Logic Flow**

1.  **Receive Wallet Path**: The function is called with the `wallet_path`.
2.  **Calculate True Balance**:
      * Initialize a total coin count to zero.
      * Iterate through all files in the `Bank` and `Fracked` subdirectories of the `wallet_path`.
      * For each file, open it, read the initial numeric value (up to the first space), and add it to the total coin count.
3.  **Read Recorded Balance**:
      * Open the `transactions.csv` file located at the root of `wallet_path`.
      * Read the second line of the file.
      * Extract the value from the last column, which represents the last recorded balance.
4.  **Compare Balances**:
      * If the true balance and the recorded balance are equal, proceed to step 6.
5.  **Create and Prepend Adjustment Record (if needed)**:
      * If the balances differ, calculate the adjustment amount (`true_balance - recorded_balance`).
      * Construct a new transaction line as a list of strings, following the column formatting rules below.
      * Read all existing lines from `transactions.csv`.
      * Insert the newly created adjustment line at the second position in the list of lines (after the header).
      * Overwrite the `transactions.csv` file with the updated list of lines.
6.  **Return CSV Content**:
      * Read the entire (and possibly updated) `transactions.csv` file into a single string.
      * Return this string.

-----

## **Adjustment Record Column Formatting**

| Column      | Formatting Instructions                                                                                                                                                                                                                                                          |
| :---------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Task ID** | Leave this field empty.                                                                                                                                                                                                                                                          |
| **Date & Time** | Use the user's local date and time. Enclose the entire string in double quotes (e.g., `"7/8/2025, 3:15 PM"`).                                                                                                                                                                  |
| **About** | Create a descriptive string, such as `"150 coins missing"` or `"25 coins found"`, based on the adjustment amount.                                                                                                                                                                   |
| **Type** | Set this warning symbol to the string `"⚠️"`.                                                                                                                                                                                                                                           |
| **Memo** | Set this to the string `"Balance Adjusted"`.                                                                                                                                                                                                                                     |
| **Amount** | The calculated difference between the true balance and the recorded balance. This will be a negative number if coins are missing and positive if extra coins are found.                                                                                                        |
| **Balance** | The true balance (total coins actually in the wallet). Format this as a string, using the user's locale for number formatting. For any fractional part, insert a hyphen after the fourth digit if there are more than four non-zero digits. Remove any trailing zeros from the fraction. For instance, `211150.79389913` becomes `"211,150.7938-9913"`. |


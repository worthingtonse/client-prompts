# **Function Specification: Show Wallet Coins**

## **1\. Overview**

The Show Wallet Coins function returns detailed information about coins in a specified wallet including denomination counts, total balance, and folder distribution. It also performs balance reconciliation with the transaction log and creates adjustment records when necessary.

## **2\. External Dependencies**

The implementation of this function relies on specifications detailed in the following external documents. The AI must assume the formats and rules described in these files are available.

* denominations.md: Defines the denominations that need to be used to create a histogram.
* transaction-log.md: Defines the format for transaction adjustment records.
* wallet-folder-structure.md: Defines the standard wallet folder structure.

## **3\. Main Function:** Show Wallet Coins

### **3.1. Parameters**

| Name | Type | Description |
| :---- | :---- | :---- |
| path\_to\_wallet\_folder | string | The full path to the specific wallet folder (e.g., "C:/Users/User/CloudCoin_Pro/Wallets/MyWallet") containing Bank, Fracked, and Limbo folders. |

### **3.2. Return Value**

* **Type:** JSON object  
* **Description:** Complete wallet coin information for the specified wallet including denomination histogram, balance totals, and folder distributions.

### **3.3. Example Function Call**
```bash
show-wallet-coins "C:/Users/User/CloudCoin_Pro/Wallets/MyWallet"
```

### **3.4. Example JSON Output**
```json
{
  "denomination_count": {
    "0": 45,
    "1": 12,
    "2": 8,
    "3": 0,
    "4": 2,
    "5": 0,
    "6": 1,
    "7": 0,
    "8": 3,
    "9": 0,
    "10": 0,
    "11": 0
  },
  "total": 34343.776,
  "bank": 30000.5,
  "fracked": 4000.276,
  "limbo": 343.0,
  "balance_reconciled": true
}
```

## **4\. Execution Logic**

### **4.1. Initialization**

1. **Start Timer:** Record the start time to calculate the total execution duration later.  
2. **Initialize JSON Response Object:** Create response object with denomination_count, total, bank, fracked, limbo fields.
3. **Initialize Denomination Histogram:** Create denomination_count object with currency denomination keys: 0-6 (decimal codes 0, 1, 2, 3, 4, 5, 6) and key denomination keys: 7-11 (decimal codes 7, 8, 9, 10, 11) as defined in denominations.md, all values set to zero.
4. **Validate Path:** Check for the existence of path\_to\_wallet\_folder and the required folders: Bank, Fracked, and Limbo. If the wallet folder doesn't exist or any required folders are missing, return error JSON and terminate.

### **4.2. Coin Counting and Analysis**

5. **Process Bank Folder:** Read all .bin files from the 'Bank' folder:
   - Parse filename (number before first space) to get coin value
   - Add value to bank total
   - Determine denomination and increment denomination_count
   - Add to overall total

6. **Process Fracked Folder:** Read all .bin files from the 'Fracked' folder:
   - Parse filename (number before first space) to get coin value  
   - Add value to fracked total
   - Determine denomination and increment denomination_count
   - Add to overall total

7. **Process Limbo Folder:** Read all .bin files from the 'Limbo' folder:
   - Parse filename (number before first space) to get coin value
   - Add value to limbo total
   - Determine denomination and increment denomination_count
   - Add to overall total

### **4.3. Balance Reconciliation**

8. **Read Transaction Log:** Open and parse the wallet's transactions.csv file
9. **Get Last Recorded Balance:** Extract balance from the most recent transaction (second row, last column)
10. **Compare Balances:** Compare calculated total with recorded balance from the wallet's transaction log
11. **Create Adjustment Record:** If discrepancy exists:
    - If actual total < recorded balance: Create withdraw adjustment record
    - If actual total > recorded balance: Create deposit adjustment record
    - Insert adjustment record as new second row in the wallet's transactions.csv
    - Use balance adjustment symbols and format from transaction-log.md
12. **Set balance_reconciled flag:** true if no adjustment needed, false if adjustment was created

### **4.4. Return Results**

13. **Construct JSON Response:** Build final JSON object with all calculated values
14. **Return JSON:** Return the complete JSON response object

## **5. JSON Response Format**

The function returns a JSON object with the following structure:

```json
{
  "denomination_count": {
    "0": 45,
    "1": 12,
    "2": 8,
    "3": 0,
    "4": 2,
    "5": 0,
    "6": 1,
    "7": 0,
    "8": 3,
    "9": 0,
    "10": 0,
    "11": 0
  },
  "total": 34343.776,
  "bank": 30000.5,
  "fracked": 4000.276,
  "limbo": 343.0,
  "balance_reconciled": true
}
```

### **5.1. Field Descriptions**

| Field | Type | Description |
|-------|------|-------------|
| denomination_count | object | Count of coins by denomination (decimal codes 0-11 from denominations.md) |
| total | number | Total value of all coins (bank + fracked) |
| bank | number | Total value of coins in Bank folder |
| fracked | number | Total value of coins in Fracked folder |
| limbo | number | Total value of coins in Limbo folder |
| balance_reconciled | boolean | true if no adjustment needed, false if adjustment was created |

### **5.2. Additional JSON Response Examples**

**Example 1: Empty Wallet**
```json
{
  "denomination_count": {
    "0": 0, "1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0,
    "7": 0, "8": 0, "9": 0, "10": 0, "11": 0
  },
  "total": 0.0,
  "bank": 0.0,
  "fracked": 0.0,
  "limbo": 0.0,
  "balance_reconciled": true
}
```

**Example 2: Wallet with Balance Adjustment**
```json
{
  "denomination_count": {
    "0": 10, "1": 5, "2": 2, "3": 0, "4": 0, "5": 0, "6": 0,
    "7": 0, "8": 1, "9": 0, "10": 0, "11": 0
  },
  "total": 1205.5,
  "bank": 1000.0,
  "fracked": 200.5,
  "limbo": 5.0,
  "balance_reconciled": false
}
```

**Example 3: Large Wallet with Mixed Denominations**
```json
{
  "denomination_count": {
    "0": 100, "1": 50, "2": 25, "3": 10, "4": 5, "5": 2, "6": 1,
    "7": 0, "8": 5, "9": 2, "10": 1, "11": 0
  },
  "total": 2500750.12345,
  "bank": 2500000.0,
  "fracked": 750.12345,
  "limbo": 0.0,
  "balance_reconciled": true
}
```

## **6. Balance Adjustment Logic**

When discrepancies are found between actual coins and recorded balance:

### **6.1. Adjustment Record Format**
Follow the transaction-log.md specification for creating adjustment records:

**If actual total < recorded balance (coins missing):**
- Create withdraw adjustment record
- Use ⚠️ symbol
- Message: "Balance Adjusted Down"
- Remarks: "{difference} coins missing"

**If actual total > recorded balance (extra coins found):**
- Create deposit adjustment record  
- Use ⚠️ symbol
- Message: "Balance Adjusted Up"
- Remarks: "{difference} coins found"

### **6.2. Insertion Rules**
- Insert adjustment record as new second row (after header)
- Update balance to match actual coin total
- Use current timestamp for Date & Time field
- Leave Task ID empty for adjustment records

## **7. Error Handling**

When errors occur, return a JSON error object:

```json
{
  "error": "ERROR:CANNOT-FIND-WALLET-FOLDER",
  "message": "The specified wallet directory does not exist."
}
```

### **7.1. Error Codes**

| Error Code | Description |
| :---- | :---- |
| ERROR:CANNOT-FIND-WALLET-FOLDER | The specified wallet directory does not exist. |
| ERROR:CANNOT-READ-WALLET-FOLDER | The application lacks permissions to read the wallet directory. |
| ERROR:MISSING-REQUIRED-FOLDERS | Bank, Fracked, or Limbo folders are missing from the wallet. |
| ERROR:CANNOT-READ-BIN-FILE | A .bin file could not be read from the disk, possibly due to permissions. |
| ERROR:CANNOT-PARSE-FILE-NAME | The amount of coins in a .bin file name could not be found |
| ERROR:CANNOT-FIND-FILE | A file listed is no longer present. |
| ERROR:CANNOT-READ-TRANSACTIONS | Unable to read or parse transactions.csv file |
| ERROR:CANNOT-WRITE-TRANSACTIONS | Unable to write adjustment record to transactions.csv |
| ERROR:INVALID-WALLET-STRUCTURE | The wallet does not have the required structure as defined in wallet-folder-structure.md |

### **7.2. Error Response Examples**

**Missing Wallet Folder:**
```json
{
  "error": "ERROR:CANNOT-FIND-WALLET-FOLDER",
  "message": "The specified wallet directory 'C:/Users/User/CloudCoin_Pro/Wallets/NonExistentWallet' does not exist."
}
```

**Missing Required Folders:**
```json
{
  "error": "ERROR:MISSING-REQUIRED-FOLDERS",
  "message": "Required folders (Bank, Fracked, Limbo) are missing from the wallet directory."
}
```

**Permission Issues:**
```json
{
  "error": "ERROR:CANNOT-READ-WALLET-FOLDER",
  "message": "The application lacks permissions to read the wallet directory."
}
```

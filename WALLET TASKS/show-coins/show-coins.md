# **Function Specification: Show Coins**

## **1\. Overview**

The Show Coins function returns the number of coins that are in a specified wallet. The Show coins
Returns an array of values that are based on the amounts in the names of the files. 

## **2\. External Dependencies**

The implementation of this function relies on specifications detailed in the following external documents. The AI must assume the formats and rules described in these files are available.

* denominations.md: Defines the denominations that need to be used to create a histogram.

## **4\. Main Function:** Unpack

### **4.1. Parameters**

| Name | Type | Description |
| :---- | :---- | :---- |
| path\_to\_wallet\_folder | string | The full path to the folder containing Bank, Fracked and Limbo folders. |

### **4.2. Return Value**

* **Type:** string\[\] (Array of strings)  
* **Description:** An event log array containing a record of all significant actions, errors, and a final execution time summary.
* It should be pre-initialized to a size of 21 empty strings.

## **5\. Execution Logic**

#### **Initialization**

1. **Start Timer:** Record the start time to calculate the total execution duration later.  
2. **Initialize Event Array:** Create return\_event\_array as a string\[\] with 21 elements.
3. **Initialize Histogram Dictionary:** Create histogram\_array as a int\[\] with the keys being indexes 0 through 14 inclusive in the denomination.md file. All values are integers and should be set to zero.
4. **Validate Path:** Check for the existence of path\_to\_wallet\_folder and and the folders that are in that folder: Bank,Fracked and Limbo. If any are missing, add the corresponding translated error to the event array and terminate the function.  
5. **Get File List:** Read all file names from the 'Bank' folder into a string\[\] called filenames\_in\_bank\_folder.
6. **Get File List:** Read all file names from the 'Fracked' folder into a string\[\] called filenames\_in\_bank\_folder.
7. **Get File List:** Read all file names from the 'Limbo" into a string\[\] called filenames\_in\_limbo\_folder.
8. **Estimate Coin Total In The Bank Folder:** For each .bin file, attempt to parse the filename (before the first _). See if the results can be turned into a number. If successful, add this number to a total\_authentic\_coins counter. Also, add this number to a histogram. 
9. **Estimate Coin Total In The Fracked Folder:** For each .bin file, attempt to parse the filename (before the first .) as a number. If successful, add this number to a total\_authentic\_coins counter and add this number to a total\_fracked\_coins counter.
10. **Set the values of the histogram_array to the corresponding denomination key:** Count the number of times each denomination 
11. **Estimate Coin Total In The Limbo Folder:** For each .bin file, attempt to parse the filename (before the first .) as a number. If successful, add this number to total\_limbo\_coins counter.
12. **Set indexs 0 through 14 to the key values in the histogram\_dictionary set to a string.
13. **Set index 15:**  The return\_event\_array to "Total Authentic:" concatenated with total\_authentic\_coins.
14. **Set index 16:**  The return\_event\_array to "Total Authentic But Needs Fixing:" concatenated with total\_fracked\_coins.
15. **Set index 17:** The return\_event\_array to "Total in Limbo:" concatenated with total\_limbo\_coins.
16. **Set index 18:** "success" if not errors or put all errors in the return\_events into one string.
17. **Log the appropriate error**  Log the return\_event\_array to the log file.
18. **Set index 19:**  The timer's time.
19. **Print the return\_event\_array to the console**. 


### **6.2. Error Codes**

| Error Code | Description |
| :---- | :---- |
| ERROR:CANNOT-FIND-WALLET-FOLDER | The specified wallet directory does not exist. |
| ERROR:CANNOT-READ-WALLET-FOLDER | The application lacks permissions to read the wallet directory. |
| ERROR:CANNOT-READ-BIN-FILE | A .bin file could not be read from the disk, possibly due to permissions. |
| ERROR:CANNOT-PARSE-FILE-NAME | The amount of coins in a .bin file name could not be found |
| ERROR:CANNOT-FIND-FILE | A file listed is no longer present. |

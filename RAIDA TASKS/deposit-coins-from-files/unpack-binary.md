# **Function Specification: Unpack**

## **1\. Overview**

The Unpack function is designed to process binary container files (with a .bin extension) from an import folder. It extracts individual "coin" data structures from within these files, validates them, and saves each valid coin as a separate file in a suspect folder. The function also handles file management, moving processed and invalid files to designated folders, and provides detailed logging of its operations.

**Workflow:** Import Folder → Unpack → Suspect Folder & Pending Folder. Then Import → Folder Imported or Trash. 

## **2\. External Dependencies**

The implementation of this function relies on specifications detailed in the following external documents. The AI must assume the formats and rules described in these files are available.

* file\_header.md: Describes the 32-byte structure of the main .bin container file.  
* File\_Body\_Format.md: Describes the structure of individual coin data within the container's body, including headers and allowable values.  
* File\_Naming\_Format.md: Specifies the convention for naming the output coin files.  
* Headers.md: Defines the header format for the individual coin files written to the suspect folder.

## **3\. Prerequisite Helper Functions**

The following helper functions should be available for use within the Unpack function.

#### validate\_allowable\_bytes

* **Description:** Checks if a specific sequence of bytes exists within a larger byte array.  
* **Parameters:**  
  1. bytes\_to\_check: A byte\[\] array to be searched.  
  2. allowable\_bytes: A byte\[\] array containing the sequence to find.  
* **Returns:** A string: "valid" if the sequence is found, otherwise "invalid".

#### validate\_allowable\_range

* **Description:** Checks if the integer representation of a byte array falls within an inclusive numerical range.  
* **Parameters:**  
  1. bytes\_to\_check: A byte\[\] array representing a number.  
  2. min\_value: An integer for the minimum allowable value.  
  3. max\_value: An integer for the maximum allowable value.  
* **Returns:** A string: "valid" if the value is within the range (inclusive), otherwise "invalid".

## **4\. Main Function:** Unpack

### **4.1. Parameters**

| Name | Type | Description |
| :---- | :---- | :---- |
| path_to_wallet | string | The full path to the wallet folder. | 
| clear_text_password | string | An optional AES password. If not empty, it's used to verify the file's hash. |
| tracking_id | string | A unique identifier for this unpacking task, to be included in output files. |
| pans | string array | The proposed authenticity numbers. |

### **4.2. Return Value**

* **Type:** string\[\] (Array of strings)  
* **Description:** An event log array containing a record of all significant actions, errors, and a final execution time summary. It should be pre-initialized to a size of 100 empty strings.

## **5\. Execution Logic**

#### **Initialization**

1. **Start Timer:** Record the start time to calculate the total execution duration later.  
2. **Initialize Event Array:** Create return\_event\_array as a string\[\] with 100 elements.  
3. **Validate Paths:** Check for the existence of path_to_wallet. If missing, add the corresponding error to the event array and terminate the function.  
4. **Get File List:** Read all file names from the "Import" subfolder.  A string\[\] called filenames\_in\_import\_folder. If the folder is empty or cannot be read, log the appropriate error and terminate.

#### **File Pre-processing**

5. **Filter Files:** Iterate through filenames\_in\_import\_folder. Move any file that does **not** have a .bin extension to the "Trash" subfolder. If a file with the same name already exists in the trash folder, append a number (e.g., (2)) to the filename before the extension to avoid overwriting.  
6. **Estimate Coin Total:** For each .bin file, attempt to parse the filename (before the first .) as a number. If successful, add this number to a total\_coins counter.  
7. **Log Initial Count:** Print the total\_coins count to the console to inform the user.

#### **Main Processing Loop**

8. **Iterate Through** .bin **Files:** For each valid .bin file remaining in the import folder:  
   1. Read the entire file into memory as a byte array.
   3. Separate the file into a header (the first 32 bytes) and a body (all subsequent bytes).
   4. **Password Check:** If clear\_text\_password is not empty, calculate its AES 256 CTR hash and compare it to the hash bytes stored in the file's header. If they do not match, log a translated ERROR:BAD-PASSWORD, move the file to the trash folder, and continue to the next file.  
   5. **Header Validation:** Validate every field in the 32-byte header according to the rules in file\_header.md. If any byte is invalid, log ERROR:INVALID-BYTE-IN-HEADER, move the file to corrupt, and continue.  
   6. **Type Check:** Read the coin type from the header. If it is an NFT, log ERROR:NTF-NOT-SUPPORTED-YET, move the file to corrupt, and continue.  
   7. **Decryption:** If the header indicates the body is encrypted, decrypt it using 256-bit AES. *Prioritize using hardware-accelerated AES instructions if available on the processor.*  
   8. **Process Coins in Body:** Loop through the decrypted body to extract each coin:  
      * The size of each coin is determined by its FL flag byte: 407 bytes if FL is 0, or 807 bytes if FL is 1\.  
      * For each coin found:
        i. **Validate Coin Header:** Validate the coin's internal header based on the specifications in File\_Body\_Format.md. If any part is invalid, log the specific error and skip to the next coin in the body. However, if the file type is not 9, report that the file type is not supported and upgrade their software. 
        ii. **Generate Filename:** Create a filename for the coin using the convention from File\_Naming\_Format.md.
        iii. **Check for Duplicates:** If a file with this name already exists in path\_to\_suspect\_folder, modify the "tag" portion of the new filename (e.g., by appending a random number) and log ERROR:COIN-ALREADY-IN-SUSPECT-FOLDER and move the coin to the path\_to\_duplicates\_folder folder. 
        iv. **Write Coin File:** Create a new file in "Suspect" subfolder with the generated name.
        v. **Write Another Coin File:** Create a new file in "Pending" subfolder with the same generated name.
        vi. **Write Coin Data:** Write the coin's full byte sequence (407 bytes) into the new file. The file's header should be generated according to Headers.md, be unencrypted, include the current timestamp, and contain the tracking\_id passed into the function.
        vii. **Generate Random Bytes:** Generate 400 random bytes for the new passwords.  
        viii. **Write Pending Coin Data:** Write the coin's full byte sequence (407 bytes) into the new file except change the last 400 bytes to be the bytes generated. The file's header should be generated according to Headers.md, be unencrypted, include the current timestamp, and contain the tracking\_id passed into the function.
        
#### **Finalization**

9. **Move Processed Files:** After successfully processing a .bin file (i.e., iterating through all its coins), move it from the import folder to the "Imported" subfolder. Handle filename collisions as previously described.  
10. **Stop Timer:** Calculate the total\_time\_in\_ms from the start time.  
11. **Log Execution Time:** Add a final entry to the return\_event\_array: "Execution Time: \[total\_time\_in\_ms\]ms".  
12. **Return Event Array:** Return the return\_event\_array.

## **6\. Error Handling**

### **6.2. Error Codes**

| Error Code | Description |
| :---- | :---- |
| ERROR:CANNOT-FIND-IMPORT-FOLDER | The specified import directory does not exist. |
| ERROR:CANNOT-READ-IMPORT-FOLDER | The application lacks permissions to read the import directory. |
| ERROR:IMPORT-FOLDER-EMPTY | The import directory contains no files to process. |
| ERROR:CANNOT-READ-BIN-FILE | A .bin file could not be read from the disk, possibly due to permissions. |
| ERROR:CANNOT-FIND-FILE | A file listed is no longer present. |
| ERROR:BAD-PASSWORD | The MD5 hash of the provided password does not match the file's hash. |
| ERROR:CANNOT-FIND-SUSPECT-FOLDER | The specified suspect directory does not exist. |
| ERROR:CANNOT-WRITE-TO-SUSPECT | The application lacks permissions to write files to the suspect directory. |
| ERROR:NTF-NOT-SUPPORTED-YET | The file contains NFT data, which is not currently supported. |
| ERROR:INVALID-BYTE-IN-HEADER | A byte in the file's 32-byte header violates the specification. |
| ERROR:COIN-ALREADY-IN-SUSPECT | A coin with the same generated filename already exists in the destination. |



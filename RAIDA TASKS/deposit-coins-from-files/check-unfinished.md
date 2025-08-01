### **Function Specification: checkForUnfinished**

#### **1\. Function Purpose**

This function serves as a quick, preliminary check to determine if a specific directory contains any unprocessed binary files. It is intended to be called before a more resource-intensive operation (like an "unpack" process) to see if there is any work to be done.

The function scans a target folder for files with a .bin extension. Its return value signals whether such files are present, absent, or if an error occurred during the check.

#### **2\. Function Signature**

function checkForUnfinished(path: string): string

* **Function Name:** checkForUnfinished  
* **Input Parameter:**  
  * path (string): A string representing the absolute or relative path to the directory that needs to be checked.  
* **Return Value:**  
  * (string): The function returns one of three possible outcomes as a string:  
    * "true": If at least one file with a .bin extension is found in the directory.  
    * "false": If the directory contains no files with a .bin extension.  
    * A formatted error string: If any error occurs during the process.

#### **3\. Detailed Logic & Execution Flow**

1. **Normalize Path:** Upon receiving the path string, the first step is to normalize it to ensure it is a valid path for the host operating system (e.g., correctly handling / and \\ separators).  
2. **Access Directory:** Attempt to access and list the contents of the directory specified by the normalized path.  
3. **Iterate and Check:**  
   * Go through each item in the directory.  
   * For each item, determine if its name ends with the .bin file extension. This check should preferably be case-insensitive (i.e., it should match .bin, .BIN, .bIn, etc.).  
4. **Determine Outcome:**  
   * If the **very first** file ending in .bin is found, the function should immediately stop its search and return the string "true".  
   * If the function iterates through all the contents of the directory and finds no files matching the .bin extension, it should return the string "false".

#### **4\. Error Handling**

* The entire process of accessing the directory and checking its contents must be contained within an error-handling mechanism (such as a try...catch block).  
* If any exception occurs (e.g., the directory at path does not exist, the program lacks the necessary permissions to read the directory, or any other I/O error), the function must catch the exception.  
* Upon catching an error, the function must immediately stop and return a single formatted string containing the error details.  
* **Error String Format:** "Error, \<code\>, \<message\>"  
  * **Example:** "Error, ENOENT, No such file or directory"

#### **5\. Code Requirements**

* **Comments:** The implementation should include comments explaining the key parts of the logic: path normalization, directory iteration, the file check condition, and the error handling block.  
* **Variable Naming:** Use clear, descriptive, and self-documenting variable names (e.g., directoryPath, fileName, hasUnfinishedFiles).  
* **Documentation:** The function definition should be preceded by a standard documentation block (e.g., JSDoc, Python Docstring) that clearly explains its purpose, parameters, and all possible return values.

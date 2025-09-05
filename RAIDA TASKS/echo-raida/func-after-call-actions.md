# **Function Specification: after_call_actions() for final RAIDA echo wrap-up tasks**

This document specifies the after_call_actions() function, which executes the final wrap-up tasks after all RAIDA `echo` responses have been processed. This includes calling the final logging function and creating the two output files.

## **Function Signature:**

function after_call_actions(statuses: Array<string>, latencies: Array<float>): boolean | string

* **Input Parameters:**  
  * statuses (Array<string>): An array of 25 status strings representing the result of each RAIDA server's echo response (e.g., "Pass", "error:timeout:ms=3000", "error:failed_challenge").
  * latencies (Array<float>): An array of 25 floating-point latency values in milliseconds representing the response time for each RAIDA server.
* **Return Value:**  
  * A boolean indicating success/failure of the operations, or a string "failure" if critical errors occur.

## **Input Validation Requirements:**

* **Array Length:** Both arrays must contain exactly 25 elements (one per RAIDA server)
* **Status Values:** Only "Pass" is considered success; all other strings are failures
* **Latency Values:** Should be non-negative numbers; invalid values default to 0
* **Error Handling:** Handle missing or malformed input gracefully with appropriate defaults

## **Detailed Logic:**

### **1. Final Console Logging:**

* **Display RAIDA Echo Results:**
  * Call the `Echo Special Logging` function, passing the `statuses` array.
  * This will display the final results in the console using the standardized 5x5 grid format with detailed error information.
  * Ensure the logging function completes successfully before proceeding to file operations.

### **2. Echo Status File Creation:**

* **File Location and Naming:**
  * Create a file named `echo.status` in the `Logs` directory.
  * Full path: `Logs/echo.status`
  * If the file already exists, it should be overwritten completely.
  * Ensure the `Logs` directory exists; create it if necessary.

* **File Content Generation:**
  * The file must contain a single line of exactly 25 characters.
  * Iterate through the `statuses` array from index 0 to 24.
  * **Character Mapping:**
    * If the status string is exactly `"Pass"`, write the character `P`.
    * For any other status string (error conditions), write the character `F`.

* **Example Content:**
  ```
  PPPPPFPPPPPPPPPPPFPPPPP
  ```

### **3. JSON Log File Creation:**

* **File Location and Naming:**
  * Create a file named `last-echo-log.json` in the `Pro` directory.
  * Full path: `Pro/last-echo-log.json`
  * If the file already exists, it should be overwritten completely.
  * Ensure the `Pro` directory exists; create it if necessary.

* **JSON Object Structure:**
  The JSON file must contain an object with the following fields:

#### **JSON Field Specifications:**

* **`online` (integer):**
  * The total number of servers with a "Pass" status.
  * Count all occurrences where status string equals exactly "Pass".

* **`pownstring` (string):**
  * A 25-character string representation of server status.
  * Use lowercase `p` for each "Pass" status.
  * Use lowercase `f` for any failure/error status.
  * Example: `"pppppfpppppppppppfppppp"`

* **`pownarray` (array of integers):**
  * An array of 25 integers representing server status.
  * Use `1` for "Pass" status.
  * Use `0` for any failure/error status.
  * Example: `[1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1]`

* **`latencies` (array of integers):**
  * The array of latency values, rounded to the nearest integer.
  * Convert floating-point millisecond values to integers using standard rounding.
  * Maintain the original array order (RAIDA 0-24).
  * Example: `[150,200,75,300,125,0,180,95,220,160,140,185,110,175,205,190,145,165,0,155,170,195,135,210,180]`

#### **Example JSON Output:**
```json
{
  "online": 23,
  "pownstring": "pppppfpppppppppppfppppp",
  "pownarray": [1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1],
  "latencies": [150,200,75,300,125,0,180,95,220,160,140,185,110,175,205,190,145,165,0,155,170,195,135,210,180]
}
```

## **Implementation Details:**

### **4. Data Processing Logic:**

* **Status Classification:**
  ```
  for i in range(25):
      if statuses[i] == "Pass":
          echo_status_char = 'P'
          pown_char = 'p'
          pown_value = 1
      else:
          echo_status_char = 'F'
          pown_char = 'f'
          pown_value = 0
  ```

* **Latency Processing:**
  ```
  rounded_latencies = [round(latency) for latency in latencies]
  ```

### **5. File Writing Operations:**

* **Echo Status File:**
  * Write the 25-character string as a single line.
  * Ensure no additional characters (spaces, newlines, etc.) are added.
  * Use appropriate file writing methods for atomic operations.

* **JSON File:**
  * Format JSON with proper structure and indentation for readability.
  * Ensure proper JSON encoding and character escaping.
  * Validate JSON structure before writing to file.

## **Error Handling:**

* **Input Validation:**
  * Verify that both `statuses` and `latencies` arrays contain exactly 25 elements.
  * Handle null, undefined, or invalid array elements appropriately.
  * Default missing statuses to failure conditions.
  * Default missing latencies to 0 or appropriate error values.

* **File System Operations:**
  * Handle directory creation errors (permissions, disk space, etc.).
  * Handle file write errors (permissions, disk space, file locks, etc.).
  * Implement proper file closure and resource cleanup.
  * Handle potential race conditions if multiple processes access the same files.

* **Data Processing Errors:**
  * Handle invalid latency values (negative, NaN, infinity).
  * Process malformed or unexpected status strings safely.
  * Ensure JSON serialization handles all data types correctly.

## **Logging Requirements:**

* **Successful Operations:**
  * Log the start of after-call actions with input summary.
  * Log successful completion of console logging.
  * Log successful creation of both output files with file paths.
  * Example: INFO: After-call actions completed successfully. Files created: Logs/echo.status, Pro/last-echo-log.json

* **Error Logging:**
  * Log failures in console logging operations.
  * Log file system errors (directory creation, file write operations).
  * Log input validation errors with specific details.
  * Log JSON serialization errors.
  * Example: ERROR: Failed to create Pro directory. Reason: Permission denied.
  * Example: ERROR: Failed to write last-echo-log.json. Reason: Disk full.
  * Example: WARNING: Invalid latency value for RAIDA 15: -1.5ms. Using default: 0ms.

## **Performance Considerations:**

* **File Operations:**
  * Use efficient file I/O operations for both text and JSON files.
  * Minimize disk access through proper buffering.
  * Implement atomic write operations to prevent file corruption.

* **Data Processing:**
  * Optimize array processing and string operations.
  * Use efficient JSON serialization libraries.
  * Minimize memory allocation during processing.

## **General Considerations:**

* **Atomicity:** Ensure file write operations are atomic to prevent corruption if the process is interrupted.
* **Data Integrity:** Validate all data before writing to files to ensure consistency.
* **Cross-Platform Compatibility:** Ensure file path handling works correctly across different operating systems.
* **Backup Strategy:** Consider maintaining backup files or transaction logs for critical data operations.
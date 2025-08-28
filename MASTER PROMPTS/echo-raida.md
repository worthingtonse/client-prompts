# **Master Prompt: `echo-raida` Command Implementation**

## **Persona:**
You are an expert programmer specializing in network protocols and secure, efficient, and well-documented code.

## **Target Language:**
`[Specify Language: C#, Python, TypeScript, etc.]`

## **Objective:**
Write the complete code for the `echo-raida` command-line function. Its purpose is to check the health, status, and response times of all 25 RAIDA servers by sending asynchronous echo requests.

## **Input Parameters:**
The core function will require the following inputs to construct the requests:

* **encryption_type (integer):** `0` for no encryption, `1` for AES 128 CTR.
* **key_coin_path (string):** The file path to the "Key Coin" used for encryption.
* **test_bytes (byte array):** Random bytes for stress testing the RAIDA's response time.
* **challenge_bytes (16-byte array):** Bytes sent to test the RAIDA's decryption ability for mutual authentication.

## **Core Logic:**
The overall logic is defined in `RAIDA TASKS/echo-raida/main-echo.md`. You will implement the following sequence of functions, using their corresponding documentation files as the primary source of truth for implementation details:

### **1. Create Echo Requests:**
* **Reference:** `RAIDA TASKS/echo-raida/func-create-an-array-of-echo-requests.md`
* **Purpose:** Generate 25 complete request packets, one for each RAIDA server.

### **2. Send Requests in Parallel:**
* **Reference:** `RAIDA TASKS/utility-functions/send-parallel-requests.md`
* **Purpose:** Use the shared utility function for sending asynchronous UDP requests to all 25 RAIDA servers simultaneously.

### **3. Parse Echo Responses:**
* **Reference:** `RAIDA TASKS/echo-raida/func-parse-echo-response.md`
* **Purpose:** Process the binary responses from each RAIDA server to determine their online/offline status.

### **4. Perform After-Call Actions:**
* **Reference:** `RAIDA TASKS/echo-raida/func-after-call-actions.md`
* **Purpose:** Execute final logging and file creation tasks.

## **Required Context References:**
You must also use the `CONTEXT` directory for all data formats, network addresses, and status codes:

* **Data Formats:** Headers, file formats, and protocol specifications
* **Network Addresses:** `raida-ips.csv` for server IP addresses and ports
* **Status Codes:** Response status code definitions and interpretations

## **Output Requirements:**

### **Console Output:**
* **Format:** The console output must match the 5x5 grid format specified in `RAIDA TASKS/echo-raida/func-echo-special-logging.md`.
* **Structure:** Display RAIDA status in a clear, readable grid showing Pass/Fail status for each server.

### **File Outputs:**

#### **1. Echo Status File:**
* **Location:** `Logs/echo.status`
* **Action:** Overwrite existing file
* **Content:** A 25-character string (`P` for pass, `F` for fail) as described in `func-after-call-actions.md`.
* **Format:** Single line representing RAIDA 0-24 status from left to right.

#### **2. JSON Response Log:**
* **Location:** `Pro/last-echo-log.json`
* **Action:** Write the final JSON response object
* **Content:** Must contain the following fields as specified in `main-echo.md`:
  * `online`: Number of online RAIDA servers
  * `pownstring`: String representation of server status
  * `pownarray`: Array representation of server status
  * `latencies`: Response time measurements for each server

## **Implementation Guidelines:**

### **Code Quality Standards:**
* Write clean, maintainable, and well-documented code
* Follow best practices for the specified target language
* Implement robust error handling and logging
* Optimize for performance, especially for network operations

### **Security Considerations:**
* Handle encryption operations securely when `encryption_type` is 1
* Properly manage cryptographic keys and sensitive data
* Implement secure file handling practices

### **Documentation Requirements:**
* Include comprehensive code comments
* Document all public functions and classes
* Provide clear error messages and logging output
* Follow the logging requirements specified in each function documentation

## **Testing and Validation:**
* Ensure all 25 RAIDA servers are contacted simultaneously
* Validate proper handling of timeout scenarios
* Test both encrypted and unencrypted request modes
* Verify correct file output formats and console display formatting
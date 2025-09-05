# **Master Prompt: `echo-raida` Command Implementation**

## **Persona:**
You are an expert programmer specializing in network protocols and secure, efficient, and well-documented code.

## **Target Language:**
`[Specify Language: C#, Python, TypeScript, etc.]`

## **Objective:**
Write the complete code for the `echo-raida` command-line function. Its purpose is to check the health, status, and response times of all 25 RAIDA servers by sending asynchronous UDP echo requests.

## **Network Configuration:**
The implementation must load RAIDA server endpoints from `CONTEXT/raida-ips.csv` which contains exactly 25 entries in the format:
```
raida_id,ip_port
0,hostname:port
1,hostname:port
...
24,hostname:port
```

Parse this file to extract the hostname and port for each RAIDA server (0-24). All requests must be sent via UDP protocol to these endpoints simultaneously.

## **Core Logic:**
The overall logic is defined in `RAIDA TASKS/echo-raida/main-echo.md`. You will implement the following sequence of functions, using their corresponding updated documentation files as the primary source of truth.

## **Implementation Sequence:**

### **1. Create Echo Requests:**
* **Reference:** `CONTEXT/create_echo_requests_spec.md`
* **Purpose:** Generate 25 complete request packets and a corresponding list of the 16-byte challenge fields that were sent.
* **Return Value:** A tuple containing two lists: `(requests, sent_challenges)`
  * `requests`: Array of 25 complete request byte arrays (Header + Body + Termination Bytes)
  * `sent_challenges`: Array of 25 corresponding 16-byte challenge values used in each request
* **Key Features:**
  * Each request is uniquely constructed for its target RAIDA server (0-24)
  * Challenge bytes are tracked for later validation of responses
  * Requests include proper encryption if specified
  * All requests follow the standardized protocol format

### **2. Send Requests in Parallel:**
* **Reference:** `CONTEXT/parallel-requests-implementation.md`
* **Purpose:** Send all 25 requests concurrently over UDP to maximize efficiency.
* **Implementation Requirements:**
  * Asynchronous UDP transmission to all 25 RAIDA servers simultaneously
  * Proper timeout handling for unresponsive servers
  * Collection of response data and timing information
  * Error handling for network connectivity issues
* **Validation Logic:** For each response received, the validation logic must compare the received challenge against the correct `sent_challenges` value from the previous step.

### **3. Parse Echo Responses:**
* **Reference:** `CONTEXT/parse_echo_response_corrected_spec.md`
* **Purpose:** For each valid response, parse the header to determine if the command was successful.
* **Success Criteria:** A response is considered successful if the status code is `0`, `1`, or `250`.
* **Processing Steps:**
  * Validate response format and structure
  * Parse response header according to protocol specification
  * Extract and verify challenge response for authentication
  * Determine server health status based on status codes
  * Calculate response time metrics

### **4. Display Final Output:**
* **Reference:** `CONTEXT/echo_special_logging_updated_spec.md`
* **Purpose:** Display the final pass/fail status of all 25 servers in a formatted grid in the console.
* **Output Requirements:**
  * Clear visual representation of network health
  * 5x5 grid format showing RAIDA 0-24 status
  * Pass/Fail indicators for each server
  * Summary statistics (e.g., "24/25 Online")
  * Consistent formatting for easy readability

### **5. Create Log Files:**
* **Reference:** `CONTEXT/after_call_actions_updated_spec.md`
* **Purpose:** Create the `Logs/echo.status` and `Pro/last-echo-log.json` files with the final results.
* **File Output Requirements:**
  * **`Logs/echo.status`:** 25-character string (P for pass, F for fail)
  * **`Pro/last-echo-log.json`:** Complete JSON response object containing:
    * `online`: Number of online RAIDA servers
    * `pownstring`: String representation of server status
    * `pownarray`: Array representation of server status  
    * `latencies`: Response time measurements for each server

## **Required Context References:**
You must utilize the `CONTEXT` directory for all protocol specifications and configuration data:

* **Protocol Formats:** Request/response header structures and data formats
* **Network Configuration:** `raida-ips.csv` for server IP addresses and ports (CSV format: index,ip:port)
* **Status Codes:** Complete definitions of response status codes and their meanings
* **File Formats:** Specifications for log file structures and content

## **Critical Implementation Details:**

### **Network Protocol Specifications:**
* **Transport Protocol:** UDP (User Datagram Protocol) for all echo requests
* **Parallel Processing:** All 25 requests MUST be sent simultaneously using asynchronous/concurrent programming
* **Timeout Handling:** Individual timeout per request (default 3000ms), convert to seconds for most async libraries
* **Response Size:** Maximum expected response is 4096 bytes

### **File Path Resolution:**
* Implement cross-platform file path resolution for configuration files
* Support both development and packaged deployment scenarios
* Required files: `CONTEXT/raida-ips.csv` (25 RAIDA server endpoints)
* Create output directories: `Logs/` and `Pro/` if they don't exist

### **Challenge-Response Validation:**
* Each request includes a unique 16-byte challenge field
* Challenge construction: [12 random bytes] + [4-byte CRC32 checksum in big-endian]
* Response validation: Bytes 16-32 of response must match sent challenge exactly
* Failed challenge validation should return `error:failed_challenge`

### **RAIDA IP Configuration Format:**
Load RAIDA endpoints from `CONTEXT/raida-ips.csv`:
```csv
raida_id,ip_port
0,raida0.cloudcoin.global:443
1,raida1.cloudcoin.global:443
...
24,raida24.cloudcoin.global:443
```

### **Response Parsing Details:**
* Status code location: **Byte 2** of response header (not byte 4 as some docs suggest)
* Success status codes: 0, 1, or 250
* Response structure: 32-byte header + variable body
* Challenge echo location: Bytes 16-32 of response header

### **Error Message Standardization:**
* Timeout: `error:timeout:ms=<timeout_value>`
* Challenge failure: `error:failed_challenge`
* Network errors: `error:connection:<ExceptionType>`
* Server errors: `error:internal_server_fail_code_<status_code>`

### **Async Implementation Requirements:**
* Use language-appropriate async/await or promise patterns
* Implement proper UDP socket management
* Handle individual request timeouts
* Aggregate results from all 25 servers
* Measure latency from request start to response received

### **Output File Creation:**
* `Logs/echo.status`: 25-character string (P/F for each RAIDA)
* `Pro/last-echo-log.json`: Complete JSON with online count, pownstring, pownarray, latencies

### **Cross-Platform Considerations:**
* Handle different path separators (Windows vs Unix)
* Support both development and packaged executable deployments
* Implement proper error handling for missing configuration files
* Use appropriate random number generation for challenges

## **Additional Implementation Details from Python Reference:**

### **Configuration Loading:**
* **RAIDA IPs:** Load from `CONTEXT/raida-ips.csv`, parse IP:port pairs from second column
* **Resource Path Handling:** Use `resource_path()` function for cross-platform file access
* **Error Handling:** Handle FileNotFoundError for missing configuration files

### **Protocol-Specific Details:**
* **CRC32 Implementation:** Use `zlib.crc32()` or equivalent, pack as big-endian 4 bytes with `struct.pack('>I', crc)`
* **Challenge Location in Response:** Bytes 16-32 of response contain echoed challenge
* **Timeout Handling:** Convert milliseconds to seconds for async operations
* **Response Size:** Maximum expected response size is 4096 bytes

### **Error Message Format:**
Standardized error message patterns:
* `error:timeout:ms=<timeout_value>`
* `error:failed_challenge` 
* `error:connection:<ExceptionType>`
* `error:internal_server_fail_code_<status_code>`

### **Command Line Interface:**
* **Arguments:** --timeout (default 3000ms), --test-bytes (default 16), --encryption-type (default 0), --key-coin-path
* **Default Values:** Use constants for configuration (NUM_RAIDA_SERVERS=25, DEFAULT_TIMEOUT_MS=3000)

## **Implementation Guidelines:**

### **Code Quality Standards:**
* Write clean, maintainable, and well-documented code following industry best practices
* Implement comprehensive error handling and logging throughout all functions
* Use appropriate design patterns for network programming and asynchronous operations
* Follow the coding standards and conventions of the specified target language
* Ensure code is testable and includes appropriate unit test considerations

### **Security Considerations:**
* Handle encryption operations securely when required (AES 128 CTR mode)
* Properly manage cryptographic keys and sensitive authentication data
* Implement secure file handling practices for log file creation
* Validate all input data and responses to prevent security vulnerabilities
* Use secure random number generation for challenge bytes

### **Network Programming Requirements:**
* Implement robust UDP communication with proper socket management
* Handle network timeouts, packet loss, and connectivity issues gracefully
* Optimize for performance with efficient parallel request processing
* Implement proper resource cleanup and connection management
* Handle endianness and binary data serialization correctly

### **Documentation Requirements:**
* Include comprehensive inline code comments explaining complex logic
* Document all public functions, classes, and interfaces with clear descriptions
* Provide detailed error messages and logging output for troubleshooting
* Follow the logging requirements specified in each function documentation
* Include usage examples and configuration instructions

### **Performance Optimization:**
* Minimize latency through efficient parallel processing
* Optimize memory usage for handling multiple concurrent requests
* Implement efficient data structures for request/response management
* Use appropriate caching strategies where beneficial
* Profile and optimize critical code paths

## **Testing and Validation Requirements:**

### **Unit Testing:**
* Test individual functions in isolation with mock data
* Validate request packet construction and format correctness
* Test response parsing with various status codes and error conditions
* Verify file output format compliance

### **Integration Testing:**
* Test complete end-to-end workflow with live or simulated RAIDA servers
* Validate parallel request sending and response collection
* Test timeout handling and error recovery scenarios
* Verify correct challenge validation and authentication flow

### **Error Scenario Testing:**
* Network connectivity failures and timeouts
* Malformed or corrupted response data
* File system errors during log creation
* Invalid or missing configuration data
* Server unavailability and partial network failures

## **Success Criteria:**
The implementation is considered successful when:
* All 25 RAIDA servers are contacted simultaneously within acceptable timeouts
* Response validation correctly authenticates server responses using challenge comparison
* Console output matches the specified 5x5 grid format exactly
* Log files are created in the correct format and locations
* Error handling provides meaningful feedback for all failure scenarios
* Performance meets requirements for real-time network health monitoring
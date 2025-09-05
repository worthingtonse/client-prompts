# **Command Specification: `echo` - RAIDA Network Health Check**

This document specifies the `echo` command, which checks the health, status, and response times of all 25 RAIDA servers by sending parallel UDP echo requests.

## **Command Overview:**

**Command Name:** `echo`  
**Purpose:** Network health monitoring and status verification for the entire RAIDA network  
**Protocol:** UDP-based parallel requests with challenge-response validation  
**Output:** Console display, status files, and JSON logs

## **Network Protocol Details:**

**Transport Protocol:** UDP (User Datagram Protocol)
**Parallel Processing:** All 25 requests MUST be sent simultaneously using asynchronous/concurrent programming
**Response Size:** Maximum expected response is 4096 bytes
**Timeout Handling:** Individual timeout per request (default 3000ms)

**Challenge-Response Security:**
- Each request includes a unique 16-byte challenge field
- Challenge construction: [12 random bytes] + [4-byte CRC32 checksum in big-endian]
- Response validation: Bytes 16-32 of response must match sent challenge exactly
- Failed challenge validation should return `error:failed_challenge`

## **Description:**

The `echo` command performs a comprehensive health check of all 25 RAIDA servers in the network. It sends specially crafted UDP requests containing challenge data and validates the responses to ensure proper server functionality and network connectivity. The command provides real-time status information and creates detailed logs for monitoring and analysis purposes.

## **Detailed Workflow:**

### **1. Load Configuration:**

* **Configuration Source:** 
  * Load IP addresses and ports for all 25 RAIDA servers from `CONTEXT/raida-ips.csv`
  * Parse CSV file to extract network endpoint information for each RAIDA (0-24)
  * Validate configuration data for completeness and format correctness

* **Network Setup:**
  * Initialize UDP socket connections for parallel communication
  * Configure timeout values and retry parameters
  * Prepare network resources for concurrent operations

### **2. Generate Requests:**

* **Request Construction:**
  * For each of the 25 servers, construct a unique request packet
  * Create a standardized 32-byte header with server-specific routing information
  * Generate request body with specific structure including:
    * **Challenge Field:** 16-byte random challenge for response validation
    * **CRC32 Checksum:** Data integrity verification using first 12 bytes of challenge
    * **Test Bytes:** Additional random data for stress testing server response times

* **Packet Structure:**
  * **Header (32 bytes):** Contains routing, command, and encryption information
  * **Body (variable):** Challenge data, test bytes, and validation checksums
  * **Termination (2 bytes):** Fixed sequence marking end of request (0x3e3e)

### **3. Send Concurrently:**

* **Parallel Transmission:**
  * All 25 UDP requests are sent simultaneously to maximize efficiency
  * Utilize asynchronous networking to avoid blocking operations
  * Implement proper error handling for network connectivity issues

* **Response Collection:**
  * Wait for responses up to a specified timeout period (configurable)
  * Collect timing information for latency measurements
  * Handle partial responses and timeout scenarios gracefully

### **4. Validate Responses:**

Each received response undergoes comprehensive validation:

* **Challenge Verification:**
  * Check that the server echoed back the correct 16-byte challenge field
  * Verify challenge integrity using CRC32 checksum validation
  * Authenticate server response to prevent spoofing attacks

* **Status Code Analysis:**
  * Parse the response header to extract status code information
  * Success condition: Status code indicates success (`0`, `1`, or `250`)
    * `0` (NO_ERROR): Standard success response
    * `1` (REQUEST_PASS): Request validation and processing successful
    * `250` (STATUS_SUCCESS): Operation completed successfully
  * All other status codes indicate server errors or failures

* **Response Integrity:**
  * Validate response packet structure and length
  * Verify proper header format and required fields
  * Check for data corruption or transmission errors

### **5. Display and Log Results:**

* **Console Output:**
  * Display final status of all 25 servers in a 5x5 grid format
  * Show detailed error information for failed servers
  * Include summary statistics (e.g., "24/25 Online")

* **File Outputs:**
  * **`Logs/echo.status`:** Single-line status file with P/F indicators
  * **`Pro/last-echo-log.json`:** Comprehensive JSON log with detailed metrics

## **Output Files:**

### **Echo Status File (`Logs/echo.status`):**

* **Format:** Single line of 25 characters
* **Content:** `P` for pass (successful response), `F` for fail (error/timeout)
* **Example:** `PPPPFPPPPPPPPPPPPPPPPPPPP`

### **JSON Response Log (`Pro/last-echo-log.json`):**

The final JSON output file contains a detailed summary of the network health check with the following structure:

#### **Properties:**

* **`online` (integer):** 
  * The total number of RAIDA servers that are online and responded successfully
  * Range: 0-25
  * Calculated by counting servers with successful status validation

* **`pownstring` (string):** 
  * A 25-character string representing the pass/fail status for each RAIDA server
  * `p` indicates a pass (successful response)
  * `f` indicates a fail (timeout, error, or invalid response)
  * Characters represent RAIDAs 0-24 from left to right

* **`pownarray` (array<integer>):** 
  * An array of 25 integers where each element represents a RAIDA server status
  * `1` indicates a pass (online and functioning correctly)
  * `0` indicates a fail (offline, timeout, or error condition)
  * Array indices 0-24 correspond to RAIDA servers 0-24

* **`latencies` (array<integer>):** 
  * An array of 25 integers representing response times in milliseconds
  * Each value corresponds to the round-trip time for the respective RAIDA server
  * Failed/timeout responses typically show high values (e.g., timeout duration)
  * Successful responses show actual network latency measurements

## **Example JSON Output:**

```json
{
  "online": 24,
  "pownstring": "ppppfpppppppppppppppppppp",
  "pownarray": [
    1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1
  ],
  "latencies": [
    210, 215, 220, 205, 208, 3000, 218, 221, 214, 217, 219, 209, 211,
    213, 216, 222, 223, 225, 206, 207, 224, 226, 227, 228, 229
  ]
}
```

**Example Analysis:**
* **Network Health:** 24 out of 25 servers online (96% availability)
* **Failed Server:** RAIDA 5 is offline (indicated by `f` in position 5, `0` in array, high latency)
* **Performance:** Most servers responding in 200-230ms range
* **Problem Server:** RAIDA 5 shows 3000ms latency (likely timeout)

## **Implementation Requirements:**

### **Error Handling:**
* Graceful handling of network timeouts and connectivity issues
* Proper validation of malformed or corrupted responses
* Comprehensive logging of error conditions and recovery attempts

### **Performance Optimization:**
* Efficient parallel processing to minimize total execution time
* Optimized memory usage for handling concurrent requests
* Fast response validation and data processing

### **Security Considerations:**
* Secure challenge generation using cryptographic random numbers
* Proper validation of server responses to prevent spoofing
* Safe handling of network data and file operations

### **Monitoring and Diagnostics:**
* Detailed logging for troubleshooting network issues
* Performance metrics collection for trend analysis
* Error classification and reporting for operational insights

## **Usage Context:**

The `echo` command serves as a fundamental network diagnostic tool for:
* **System Health Monitoring:** Regular verification of RAIDA network status
* **Performance Analysis:** Latency measurement and trend tracking
* **Troubleshooting:** Identification of problematic servers or network segments
* **Operational Verification:** Confirmation of network readiness for critical operations
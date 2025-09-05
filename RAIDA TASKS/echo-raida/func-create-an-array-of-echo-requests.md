# **Function Specification: create_echo_requests() for generating RAIDA echo request packets**

This document specifies the create_echo_requests() function, which creates 25 complete, correctly formatted UDP request packets for the `echo` command and a corresponding list of the challenges sent.

## **Function Signature:**

function create_echo_requests(): Tuple<Array<byte[]>, Array<byte[]>>

* **Input Parameters:**  
  * None (function generates all required data internally)
* **Return Value:**  
  * A tuple containing two lists:
    1. `requests`: An array of 25 byte arrays, where each is a complete request packet.
    2. `sent_challenges`: An array of 25 byte arrays, where each is the 16-byte challenge field that was included in the corresponding request's body.

## **Detailed Logic:**

The function iterates through all 25 RAIDA servers (index `i` from 0 to 24) and constructs a unique request for each.

### **1. Request Body Construction:**

The body is constructed first, as its contents are needed for the header length calculation.

#### **Challenge Field Generation:**
* **Generate Random Challenge Data:**
  * Generate 16 bytes of cryptographically secure random data
  * Use the first 12 bytes for CRC32 calculation
  * Use secure random number generation (not pseudo-random)

* **Calculate CRC32 Checksum:**
  * Input: First 12 bytes of the random challenge data
  * Algorithm: Standard CRC32 (polynomial 0x04C11DB7)
  * Output: 4-byte checksum in big-endian byte order
  * **Implementation Example:** `crc_bytes = struct.pack('>I', zlib.crc32(challenge_data[:12]))`

* **Form the Final Challenge Field:**
  * Concatenate: [12 bytes random data] + [4 bytes CRC32 checksum]
  * Total length: Exactly 16 bytes
  * **Store for validation:** Save this complete 16-byte challenge for response validation
  * **Unique per request:** Each RAIDA gets a different challenge

* **Challenge Field Structure:**
  ```
  Bytes 0-11:  Random challenge data (12 bytes)
  Bytes 12-15: CRC32 checksum of bytes 0-11 (4 bytes, big-endian)
  ```

#### **Test Bytes Generation:**
* **Generate Test Data:**
  * Create a separate array of random bytes for stress testing.
  * Recommended size: 16 bytes (configurable based on requirements).
  * Use cryptographically secure random generation.

#### **Final Body Assembly:**
* **Construct Unencrypted Body:**
  * The final unencrypted body structure: `sent_challenge` + `test_bytes`
  * Total body length: 16 bytes (challenge) + test_bytes length

### **2. Request Header Construction (32 bytes):**

Create a standardized 32-byte header for each RAIDA server request.

#### **Routing Section (Bytes 0-3):**
* **Byte 0 (Routing BF):** Must be `1`
* **Byte 1 (Routing SP):** Must be `0`
* **Byte 2 (Routing RI):** The RAIDA ID, which is the loop index `i` (0-24)
* **Byte 3 (Routing SH):** `0`

#### **Command Section (Bytes 4-7):**
* **Byte 4 (Command Group):** `0`
* **Byte 5 (Command):** `0` for the `echo` command
* **Bytes 6 & 7 (Coin ID):** 
  * These two bytes form a 16-bit integer for Coin ID of `6`
  * **Byte 6:** `0`
  * **Byte 7:** `6`

#### **Presentation Section (Bytes 8-15):**
* **Bytes 8-13 (Presentation):** All `0`
* **Byte 14 (Packet Index `iii`):** `0` (first and only packet)
* **Byte 15 (Packet Array Length `lear`):** `1` (only one packet in this request)

#### **Encryption and Body Information (Bytes 16-31):**
* **Byte 16 (Encryption Type):** The specified encryption type (e.g., `0` for none)
* **Bytes 17-21:** All `0` for unencrypted requests
* **Bytes 22-23 (Body Length):** 
  * A 16-bit unsigned integer in big-endian format
  * Represents the total length of the `final_body` plus 2 termination bytes
  * Calculate as: (challenge_length + test_bytes_length + 2)
* **Bytes 24-31:** All `0` for unencrypted requests

### **3. Final Assembly:**

* **Complete Request Packet Structure:**
  * `header` + `final_body` + `termination_bytes`
  * Termination bytes: `0x3e3e` (two bytes: 0x3E, 0x3E)

* **Data Storage:**
  * Store the complete request packet in the `requests` array at index `i`
  * Store the corresponding `sent_challenge` in the `sent_challenges` array at index `i`

## **Implementation Details:**

### **4. Data Validation:**

* **Header Validation:**
  * Verify all header fields are set to correct values
  * Ensure body length calculation is accurate
  * Validate big-endian byte order for multi-byte fields

* **Challenge Validation:**
  * Verify CRC32 checksum calculation is correct
  * Ensure proper byte ordering for checksum
  * Validate challenge field construction

### **5. Memory Management:**

* **Efficient Array Handling:**
  * Pre-allocate arrays for optimal performance
  * Ensure proper cleanup of temporary data
  * Minimize memory fragmentation

## **Error Handling:**

* **Random Number Generation Failures:**
  * Handle failures in cryptographic random number generation
  * Provide fallback mechanisms or clear error reporting

* **Memory Allocation Errors:**
  * Handle insufficient memory conditions gracefully
  * Provide meaningful error messages for allocation failures

* **Checksum Calculation Errors:**
  * Validate CRC32 implementation correctness
  * Handle edge cases in checksum calculation

## **Logging Requirements:**

* **Successful Operations:**
  * Log the start and completion of request generation
  * Log summary information (e.g., "Generated 25 echo requests successfully")
  * Example: INFO: Created echo requests for 25 RAIDA servers. Total packet size: X bytes each.

* **Error Logging:**
  * Log any failures in random number generation
  * Log memory allocation errors
  * Log checksum calculation issues
  * Example: ERROR: Failed to generate random challenge data for RAIDA 5.
  * Example: ERROR: CRC32 checksum calculation failed for challenge data.

## **General Considerations:**

* **Performance:** Optimize for quick generation of all 25 requests simultaneously
* **Security:** Use cryptographically secure random number generation for all challenge data
* **Reliability:** Ensure consistent packet format across all generated requests
* **Thread Safety:** If used in multi-threaded environment, ensure thread-safe random number generation
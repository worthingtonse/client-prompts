## **Function: send_parallel_requests**

### **Purpose**
Concurrently sends up to 25 requests to a network of servers and collects their responses or reports on the connection status for each.

### **Parameters**

| Name | Type | Description |
| :--- | :--- | :--- |
| `requests` | **Array of Byte Arrays** | An array of 25 byte arrays. Each byte array is a complete, pre-formatted request to be sent. An empty byte array at an index signifies that no request should be sent for that server. |
| `ips` | **Array of Strings** | An array of 25 IP address strings (e.g., `"192.168.1.10"`), one for each target server. |
| `ports` | **Array of Integers** | An array of 25 integer port numbers, one for each target server. |
| `timeouts` | **Array of Integers** | An array of 25 integer values, each specifying the maximum time in **milliseconds** to wait for a response from the corresponding server. |
| `expected_challenges` | **Array of Byte Arrays** | An array of 25 byte arrays. Each array contains a 16-byte challenge GUID that is expected to be present in the corresponding server's response for validation. |
| `protocol` | **String** | The transport protocol to use. The value will be either `"TCP"` or `"UDP"`. |
| `max_response_size` | **Integer** | The maximum number of bytes allowed in a valid response from a server. |

### **Return Value**
The function must return an **Array** containing exactly 25 elements. Each element corresponds to the outcome of the request at the same index and will be one of two types:
1.  **Byte Array**: The raw response from the server if the request was successful.
2.  **String**: A formatted error or status message if the request failed or was not attempted.

### **Core Logic**
1.  Initialize a results array of 25 elements, with each element set to a default "not attempted" state.
2.  Launch up to 25 **concurrent** operations, one for each element in the `requests` array from index `0` to `24`.
3.  For each operation, if the `requests[index]` is empty, no action is needed. The result for this index should remain a status message indicating it was not attempted.
4.  If `requests[index]` is **not** empty, the concurrent operation must perform the following steps.

### **Individual Request Handling**
Each concurrent task must execute the following logic independently:

1.  **Start a Timer:** Record the start time.
2.  **Send Request:** Send the data from `requests[index]` to the server at `ips[index]
    `:`ports[index]` using the specified `protocol`.
3.  **Wait for Response:** Await a response from the server.

4.  **Process Outcome:**
    * **On Timeout:** If no response is received within the `timeouts[index]` duration, stop the operation. Place the formatted **timeout error string** into the `results[index]`.
    * **On Response:** If a response is received, stop the timer and perform the following checks in order:
        1.  **Check Size:** If the length of the received byte array is greater than `max_response_size`, place the formatted **response length error string** into `results[index]`.
        2.  **Check Challenge:** Extract the 16 bytes from the response starting at index 16. If these bytes do not exactly match the bytes in `expected_challenges[index]`, place the formatted **failed challenge error string** into `results[index]`.
        3.  **On Success:** If all checks pass, place the **raw, unmodified response byte array** into `results[index]`.

5.  **Finalize:** After all concurrent operations have completed (either successfully, with an error, or by timing out), return the final `results` array.

### **Status and Error Message Formats**
The formatted strings placed in the results array must follow these exact formats.

| Condition | Format | Example |
| :--- | :--- | :--- |
| Request not attempted | `status:not_attempted` | `status:not_attempted` |
| Request times out | `error:timeout:ms=<timeout>` | `error:timeout:ms=3000` |
| Response is too long | `error:response_length:max=<max> actual=<actual>` | `error:response_length:max=4096 actual=5120` |
| Response challenge fails | `error:failed_challenge` | `error:failed_challenge` |v

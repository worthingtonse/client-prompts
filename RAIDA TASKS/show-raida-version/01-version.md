# **Function Specification: create\_version\_requests()**

This document specifies the create\_version\_requests() function. This function is responsible for creating a batch of 25 requests to be sent in parallel to the RAIDA network to retrieve the software version of each server.

## **Core Concepts:**

* **RAIDA (Redundant Array of Independent Detection Agents):** A decentralized network of 25 servers that validate digital currency.  
* **CloudCoin:** A digital cash file. For the purposes of this function, we are interested in a special "Key Coin" used for encrypting requests.  
* **Authenticity Number (AN):** A 128-bit (16-byte) random GUID that acts as a password for a CloudCoin. There are 25 ANs per CloudCoin, one for each RAIDA server.

## **Function Signature:**

function create\_version\_requests(encryption\_type: integer, key\_coin\_path: string, challenge\_bytes: array of 16-byte arrays): Array\<byte\[\]\> | string

* **Input Parameters:**  
  * encryption\_type (integer): Specifies the type of encryption to be used for the request body.  
    * 0: No encryption.  
    * 1: AES 128 CTR encryption.  
  * key\_coin\_path (string): The file path to the "Key Coin" file. This parameter is only used when encryption\_type is 1\.  
  * challenge\_bytes (array of 16-byte arrays): An array containing 25 unique 16-byte challenges. The challenge at index i will be sent to the RAIDA server with ID i.  
* **Return Value:**  
  * An array of 25 complete, prepared byte arrays. Each byte array represents a full request (Header \+ Body \+ Termination Bytes) for one of the 25 servers.  
  * Returns the string "failure" if any significant, unrecoverable error occurs (e.g., file system access issues, invalid key coin, encryption failure).

## **Request Structure Overview:**

Each version request consists of three main parts, concatenated in order:

1. **Request Header (32 bytes):** Contains metadata about the request, such as the server ID and the command.  
2. **Request Body (16 bytes):** Contains a challenge for the RAIDA server.  
3. **Termination Bytes (2 bytes):** A fixed sequence (0x3E 0x3E) to mark the end of the request.

## **Detailed Logic:**

The function will construct 25 distinct requests, one for each server (Server ID 0 to 24).

### **1\. Data Extraction from Key Coin File (for Encryption Type 1):**

* If encryption\_type is 1, read the file located at key\_coin\_path and extract:  
  * Denomination (byte at index 34\)  
  * Serial Number (4 bytes at index 35\)  
  * An array of 25 Authenticity Numbers (ANs). Each AN is a 16-byte GUID. The ANs start at byte index 39\.

### **2\. Request Body Construction:**

* For each of the 25 requests, the body is simply the corresponding 16-byte challenge from the challenge\_bytes input array.  
* The body for server i is challenge\_bytes\[i\].  
* If encryption\_type is 1, this 16-byte body will be encrypted. Since the body is already a multiple of 16, no padding is required.

### **3\. Request Header Construction (32 bytes):**

Create a 32-byte header for each of the 25 servers.

* **Bytes 0-3:**  
  * Byte 0 (VR): 0x00  
  * Byte 1 (SP): 0x00  
  * Byte 2 (RI): **Server ID** (from 0x00 for server 0, up to 0x18 for server 24\)  
  * Byte 3 (SH): 0x00  
* **Bytes 4-5 (Command):**  
  * Byte 4 (CG): 0x00 (Command Group: Status)  
  * Byte 5 (CM): 0x01 (Command: version)  
* **Bytes 6-15:** All set to 0x00.  
* **Byte 16 (EN):** **Encryption Type** (from the encryption\_type parameter).  
* **Bytes 17-31:** Handled based on encryption\_type:  
  * **If encryption\_type is 0 (No Encryption):**  
    * Bytes 17-21: Set to 0x00.  
    * Bytes 22-23 (BL): The length of the body plus two termination bytes (16 \+ 2 \= 18). This will be 0x0012 (big-endian).  
    * Bytes 24-29: Set to 0x00.  
    * Bytes 30-31 (Echo): Two random bytes.  
  * **If encryption\_type is 1 (AES 128 CTR Encryption):**  
    * Byte 17 (DN): Denomination of the Key Coin.  
    * Bytes 18-21 (SN): Serial Number of the Key Coin.  
    * Bytes 22-23 (BL): The length of the encrypted body plus two termination bytes (16 \+ 2 \= 18). This will be 0x0012 (big-endian).  
    * Bytes 24-31 (NO): A randomly generated 8-byte **Nonce** to be used in the CTR encryption.  
* **Encryption Process (for Encryption Type 1):**  
  * Encrypt the 16-byte request body using AES 128 CTR mode.  
  * The encryption **key** for each server's request is the specific Authenticity Number (AN) from the Key Coin that corresponds to that server's ID. (For Server 0, use the 0th AN; for Server 1, use the 1st AN, etc.).  
  * The **nonce** used for encryption is the 8-byte random nonce generated for bytes 24-31 of the header.

### **4\. Termination Bytes:**

* After the header and the (potentially encrypted) body, append two fixed termination bytes: 0x3E 0x3E.

### **5\. Final Request Assembly:**

* For each of the 25 servers, concatenate the constructed Header, Body (encrypted if encryption\_type is 1), and Termination Bytes into a single byte array.  
* Return the array containing all 25 complete request byte arrays.

## **Logging and Error Handling:**

* **Success:** Log key milestones, such as the start of the function and its successful completion.  
* **Errors:**  
  * Log all errors encountered during file system operations (e.g., key\_coin\_path not found, permission denied, invalid file format).  
  * Log errors during encryption (e.g., invalid key, algorithm issues).  
  * Log entries should be descriptive, including the error type and the affected operation.  
  * Any error that prevents the successful creation of all 25 requests should cause the function to log the error and return the string "failure".

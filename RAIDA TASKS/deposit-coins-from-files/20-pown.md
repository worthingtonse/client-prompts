# **Function Specification: create\_pown\_requests() for CloudCoin Powning**

This document specifies the create\_pown\_requests() function, which is responsible for generating cryptographic requests to "pown" (password own) CloudCoin files. These requests are sent to a network of 25 servers to update the ownership of CloudCoins by changing their authenticity numbers (passwords).

## **Core Concepts:**

* **CloudCoin:** A digital cash file with a .bin extension. Each CloudCoin file contains a serial number and 25 unique 128-bit random GUIDs, which serve as passwords (authenticity numbers). Possession of these passwords signifies ownership.  
* **Powning:** The process of changing the 25 authenticity numbers (passwords) of a CloudCoin file on 25 different servers. This act transfers ownership to the party performing the pown.  
* **Authenticity Number (AN):** A 128-bit random GUID acting as a password for a CloudCoin. There are 25 ANs per CloudCoin.
* **Proposed Authenticity Number (PAN):** A 128-bit random GUID acting as the next passwords for a CloudCoin. There are 25 PANs per CloudCoin before Powning.

## **Function Signature:**

function create\_pown\_requests(encryption\_type: integer, path\_to\_suspect\_folder: string, key\_coin\_path: string): Array\<byte\[\]\> | string

* **Input Parameters:**  
  * encryption\_type (integer): Specifies the type of encryption to be used for the request body.  
    * 0: No encryption.  
    * 1: AES 128 CTR encryption.  
  * key\_coin\_path (string): The file path to the "Key Coin" file. This parameter is only relevant when encryption\_type is 1\.
  * path\_to\_suspect\_folder (string): The path to the folder that holds all the coins that will be powned.
  * challenge\_array (array of 25 GUIDs): Used as a decrytion challenges for mutual authenticiation. 
* **Return Value:**  
  * An array of 25 complete, prepared byte arrays, where each byte array represents a full request (Header \+ Body \+ Termination Bytes) for one of the 25 servers.  
  * Returns the string "failure" if any significant, unrecoverable error occurs (e.g., file system access issues, invalid key coin, encryption failure).

## **Folder Structure (Context):**

* Suspect/: The folder containing CloudCoin files that need to be "powned." The function will read these files to construct the request bodies.

## **Request Structure Overview:**

Each pown request consists of three main parts, concatenated in order:

1. **Request Header (32 bytes):** Contains metadata about the request.  
2. **Request Body (variable length):** Contains the challenge and CloudCoin information.  
3. **Termination Bytes (2 bytes):** A fixed sequence to mark the end of the request.

## **Detailed Logic:**

The function will iterate through all CloudCoin files in the Suspect/ folder, gather their information, and construct 25 distinct requests, one for each server (Server ID 0 to 24).

### **1\. Data Extraction from Key Coin File:**

* Read the file located at the key\_coin\_path and extract:  
  * Denomination (byte index 34)
  * Serial Number  (byte index 35 to 39 inclusive)
  * An array of Authenticity Numbers (ANs). This is an array of 25 GUIDs, each having 16 bytes that add up to 400 bytes (byte index 39 to the files end)
    

### **1.1\. Data Extraction from Suspect Folder:**

* Loop through each .bin file in the Suspect/ folder.  
* For each CloudCoin file, extract:  
  * Denomination (byte index 34)
  * Serial Number  (byte index 35 to 38 inclusive)
  * 25 Current Authenticity Numbers (ANs) bytes 39 to 439.
  * 25 Proposed Authenticity Numbers (new ANs) \- to replace the ANs on the servers. Bytes 439 to 839.
* Maintain a running count of the total number of CloudCoins processed across all requests.  
* **Maximum Coins per Request:** A single request body can include a maximum of 1800 CloudCoins. If the total number of coins exceeds this limit for any given request, the excess coins must be held over for a subsequent "round" of requests (i.e., this function will only prepare requests for the first 1800 coins, and subsequent calls would handle the rest).

### **2\. Request Body Construction:**

For each of the 25 requests (one per server):

* **Challenge (16 bytes):** A random 16-byte value used for mutual authentication. This must be generated uniquely for each request.  
* **Coin Information Array:**  
  * Following the challenge, append an array of coin information.  
  * Each coin's information is 37 bytes:  
    * Byte 0: Denomination (1 byte)  
    * Bytes 1-4: Serial Number (4 bytes)  
    * Bytes 5-20: Current Authenticity Number (16 bytes)  
    * Bytes 21-36: Proposed Authenticity Number (16 bytes)  
  * **Important:** For the 25 different requests (one per server), the Denomination and Serial Number for a given CloudCoin will remain the same. However, the Current Authenticity Number will be the one corresponding to that specific server, and the Proposed Authenticity Number will be a newly generated random GUID for that server.  
* **Padding:** After forming the complete body (Challenge \+ Coin Information Array), pad the body with null bytes (0x00) at the end until its total length is perfectly divisible by 16 bytes. This is a requirement for potential encryption.

### **3\. Request Header Construction (32 bytes):**

Create a 32-byte header for each of the 25 servers.

* **Fixed First 16 Bytes:**  
  * Byte 0 (0x00): 0x00  
  * Byte 1 (0x01): 0x00  
  * Byte 2 (0x02): **Server ID** (0x00 for server 0, up to 0x18 for server 24\)  
  * Byte 3 (0x03): 0x00  
  * Byte 4 (0x04): 0x01  
  * Byte 5 (0x05): 0x14  
  * Byte 6 (0x06): 0x00  
  * Byte 7 (0x07): 0x00  
  * Byte 8 (0x08): 0x00  
  * Byte 9 (0x09): 0x00  
  * Byte 10 (0x0A): 0x00  
  * Byte 11 (0x0B): 0x00  
  * Byte 12 (0x0C): 0x00  
  * Byte 13 (0x0D): 0x00  
  * Byte 14 (0x0E): 0x00  
  * Byte 15 (0x0F): 0x00  
  * Byte 16 (0x10): **Encryption Type** (taken from the encryption\_type parameter).  
* **Remaining 16 Bytes (Bytes 17-31):** Handled based on encryption\_type:  
  * **If encryption\_type is 0 (No Encryption):**  
    * All remaining bytes (17-31) must be set to 0x00, *except* for bytes 22 and 23\.  
    * Bytes 22 & 23: These two bytes together represent the 16-bit unsigned integer length of the *unencrypted* body (including the 16-byte challenge, coin information, and padding), *plus two termination bytes*.  
  * **If encryption\_type is 1 (AES 128 CTR Encryption):**  
    * **Key Coin Extraction:**  
      * Read the CloudCoin file located at key\_coin\_path.  
      * From this "Key Coin" file, extract its Denomination, Serial Number, and all 25 Authenticity Numbers. This Key Coin acts as a shared secret.  
    * **Header Bytes (17-31):**  
      * Byte 17: Denomination of the Key Coin (1 byte).  
      * Bytes 18-21: Serial Number of the Key Coin (4 bytes).  
      * Bytes 22-23: These two bytes together represent the 16-bit unsigned integer length of the *encrypted* body (including the 16-byte challenge, coin information, and padding), *plus two termination bytes*.  
      * Bytes 24-31: A randomly generated 8-byte **Nounce** (used in CTR mode).  
    * **Encryption Process:**  
      * Encrypt the *entire* request body (Challenge \+ Coin Information Array \+ Padding) using AES 128 CTR mode.  
      * The encryption key for each server's request will be the specific Authenticity Number of the Key Coin that corresponds to that server's ID (e.g., for Server 0, use the Key Coin's 0th authenticity number; for Server 1, use the 1st authenticity number, and so on, up to Server 24).  
      * If the system/processor supports AES encryption machine commands (e.g., AES-NI), those should be utilized for performance if available in the target programming language's standard libraries. Otherwise, a software implementation should be used.

### **4\. Termination Bytes:**

* After the header and (potentially encrypted) body, append two fixed termination bytes: 0x3E 0x3E.

### **5\. Final Request Assembly:**

* Concatenate the constructed Header, Body (encrypted if encryption\_type is 1), and Termination Bytes into a single byte array for each of the 25 requests.  
* Return the array containing all 25 complete request byte arrays.

## **Logging Requirements:**

* **Successful Operations:** Log key milestones, such as the start of the function, successful processing of CloudCoins, and final completion.  
* **Error Logging:**  
  * All errors encountered during file system operations (e.g., inability to read Suspect folder or Key Coin file, file not found, permission denied, invalid file format).  
  * Errors during encryption (e.g., invalid key, algorithm issues).  
  * Log entries should include the error type, a descriptive message, and the affected file/folder path or operation.  
  * Example: ERROR: Failed to read Key Coin file: /path/to/key.bin. Reason: File not found.  
  * Example: ERROR: Encryption failed for Server ID 5\. Reason: Invalid key size.

## **Error Handling Philosophy:**

* The function should be robust and handle common file system and cryptographic errors gracefully.  
* Any error that prevents the successful creation of all 25 requests (e.g., inability to access the Suspect folder, critical issues with the Key Coin when encryption type is 1, unrecoverable encryption errors) should cause the function to log the error and return "failure".  
* Minor issues might be logged but not necessarily stop the entire process if the core logic can continue for other coins/requests. For simplicity, assume any logged error could lead to a "failure" return if it impacts the ability to produce all valid requests.

## **General Considerations:**

* The function should be designed to be programming language agnostic. Focus on the logical steps and requirements.  
* Efficiency: Optimize for performance, especially concerning file I/O and cryptographic operations.

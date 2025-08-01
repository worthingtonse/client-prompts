# **Function Specification: create\_ticked\_request\_by\_sum() for CloudCoin Fixing**

This document specifies the create\_ticket\_requests\_by\_sum() function, which is responsible for generating cryptographic requests 
to get "tickets" from raida servers so these tickets can be given to other raida servers to prove authenticity and heal nodes that think a coin is counterfeit when it is not. 

## **Core Concepts:**

* **CloudCoin:** A digital cash file with a .bin extension. Each CloudCoin file contains a serial number and 25 unique 128-bit random GUIDs, which serve as passwords (authenticity numbers). Possession of these passwords signifies ownership.  
* **Powning:** The process of changing the 25 authenticity numbers (passwords) of a CloudCoin file on 25 different servers. This act transfers ownership to the party performing the pown.  
* **Authenticity Number (AN):** A 128-bit random GUID acting as a password for a CloudCoin. There are 25 ANs per CloudCoin.
* **Pan Authenticity Number (PAN):** A 128-bit random GUID that will become the new AN if the current AN is accepted to be authentic by the RAIDA server node. There are 25 PANs per CloudCoin.

## **Function Signature:**

function create\_ticket\_requests(encryption\_type: integer, path\_to\_fracked\_folder: string, encryption\_key: 16 bytes, coin\_id: coin_id array that varies in length: five bytes, challenge:16 bytes guid, AN Array: array of 16 bytes that varies in length but same length as the coin_id ): Array\<byte\[\]\> | string

* **Input Parameters:**  
  * encryption\_type (integer): Specifies the type of encryption to be used for the request body.  
    * 0: No encryption.  
    * 1: AES 128 CTR encryption.  
  * encryption\_key (16 bytes): This parameter is only relevant when encryption\_type is not zero\.
  * challenge (16 bytes): Used for mutual authenticiation.
  * coin\_id_array (array of 5-byte values) used to authenticate the coin.
  * AN\_array (array of GUIDs) used to create a sum that will authenticate the coins.
    
* **Return Value:**  
  * A complete request (Header \+ Body \+ Termination Bytes) for one of the raida servers.  
  * Returns the string "failure" if any significant, unrecoverable error occurs (e.g., file system access issues, invalid key coin, encryption failure).


## **Request Structure Overview:**

Each ticket request consists of three main parts, concatenated in order:

1. **Request Header (32 bytes):** Contains metadata about the request.  
2. **Request Body (variable length):** Contains the challenge and CloudCoin information.  
3. **Termination Bytes (2 bytes):** A fixed sequence to mark the end of the request.


### **2\. Request Body Construction:**


* **Challenge (16 bytes):** A random 16-byte value used for mutual authentication. This must be generated uniquely for each request.  
* **Coin Information Array:**  
  * Following the challenge, append an array of coin information by looping through the arrays of coin_id an AN_array.  
  * Each coin's information is 21 bytes:  
    * Byte 0-4: coin_id (5 byte)  
    * Bytes 5-20: Current Authenticity Number (16 bytes)  
* **Padding:** If the encryption type is not zero, After forming the complete body (Challenge \+ Coin Information Array), pad the body with null bytes (0x00) at the end until its total length is perfectly divisible by 16 bytes. This is a requirement for potential encryption.

### **3\. Request Header Construction (32 bytes):**

Create a 32-byte header for each of the 25 servers.

* **Fixed First 16 Bytes:**  
  * Byte  0 (0x00): 0x00  
  * Byte  1 (0x01): 0x00  
  * Byte  2 (0x02): **Server ID** (0x00 for server 0, up to 0x18 for server 24\)  
  * Byte  3 (0x03): 0x00  
  * Byte  4 (0x04): 0x02  
  * Byte  5 (0x05): 0x29
  * Byte  6 (0x06): 0x00  
  * Byte  7 (0x07): 0x00  
  * Byte  8 (0x08): 0x00  
  * Byte  9 (0x09): 0x00  
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


# GET TICKET BY SUM
The ANs are added up and put in one number. This reduces the amount of data that needs to be sent.

The sum is calculated as per these steps:
1. Each AN of every coin is converted to four 32 integers from a byte array
```
i0 = an[0] | an[1]<<8 | an[2]<<16 | an[3]<<24
i1 = an[4] | an[5]<<8 | an[6]<<16 | an[7]<<24
i2 = an[8] | an[9]<<8 | an[10]<<16 | an[11]<<24
i3 = an[12] | an[13]<<8 | an[14]<<16 | an[15]<<24
```
2. The integers are XOR-ed to the accumulator (XOR-ed sum). The initial value of the XOR-ed sum is zeroes
```
sum[0] ^= i0
sum[1] ^= i1
sum[2] ^= i2
sum[3] ^= i3
```
3. Steps #1 and #2 are repeated for every coin
4. The resulting sum is converted to a byte array (SU SU SU SU SU SU SU SU SU SU SU SU SU SU SU SU)
```
SU = sum[0]
SU = sum[0] >> 8
SU = sum[0] >> 16
SU = sum[0] >> 24
SU = sum[1]
SU = sum[1] >> 8
SU = sum[1] >> 16
SU = sum[1] >> 24
SU = sum[2]
SU = sum[2] >> 8
SU = sum[2] >> 16
SU = sum[2] >> 24
SU = sum[3]
SU = sum[3] >> 8
SU = sum[3] >> 16
SU = sum[3] >> 24
```

REQUEST: Example Request Body with four tokens:
```hex
CH CH CH CH CH CH CH CH CH CH CH CH CH CH CH CH
DN  SN SN SN SN  
DN  SN SN SN SN  
DN  SN SN SN SN 
DN  SN SN SN SN  
SU SU SU SU SU SU SU SU SU SU SU SU SU SU SU SU //Sum of all Authenticity Numbers as per the algorithm above
PD PD PD // Variable length of Padding Bytes if encrypted and needs to be divisable by 16. 
3E 3E //Not Encrypted
```

### **4\. Termination Bytes:**

* After the header and (potentially encrypted) body, append two fixed termination bytes: 0x3E 0x3E.

### **5\. Final Request Assembly:**

* Concatenate the constructed Header, Body (encrypted if encryption\_type is 1), and Termination Bytes into a single string of bytes.  
* Return the byte string containing the request.

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

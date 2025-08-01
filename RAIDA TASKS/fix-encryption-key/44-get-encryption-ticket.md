
# **Function Specification: create\_get\_encryption\_ticket\_requests()**

This document specifies the create\_get\_encryption\_ticket\_requests() function. This function is responsible for creating a batch of encrypted requests to be sent to "helper" RAIDA servers. The purpose is to take an 8-byte part of a key, have the helper RAIDA encrypt it using a key it shares with a "fracked" RAIDA, and return it as a 16-byte encrypted ticket.

## **Core Concepts:**

* **Helper RAIDA:** A RAIDA server with which the client has a valid, working shared secret (an authentic token).  
* **Fracked RAIDA:** A RAIDA server with which the client's token is "fracked" (counterfeit), preventing normal encrypted communication.  
* **Key Part:** An 8-byte portion of the full Authenticity Number (AN) that needs to be fixed on the fracked RAIDA.  
* **Encryption Ticket:** The 16-byte encrypted output from the helper RAIDA. It is the key part, padded and encrypted with a key known only to the helper and fracked RAIDA servers.

## **Function Signature:**

function create\_get\_encryption\_ticket\_requests(target\_raida\_key\_id: {denomination: byte, serial\_number: uint32}, key\_part: byte\_array, fracked\_token: {denomination: byte, serial\_number: uint32, an: byte\_array}, challenge\_bytes: array of 16-byte arrays, encryption\_coin: {denomination: byte, serial\_number: uint32, ans: array of 16-byte arrays}) : Array\<byte\[\]\> | string

* **Input Parameters:**  
  * target\_raida\_key\_id (object): The denomination and serial number of the key the helper RAIDA should use to encrypt the ticket. This key is shared between the helper and the fracked RAIDA.  
  * key\_part (8-byte array): The 8-byte portion of the fracked AN to be turned into a ticket.  
  * fracked\_token (object): The full details of the token that is fracked on the target RAIDA.  
    * denomination, serial\_number, an (16-byte array)  
  * challenge\_bytes (array of 16-byte arrays): An array of 25 unique 16-byte challenges.  
  * encryption\_coin (object): The coin used to encrypt the request itself. This coin must be authentic on the helper RAIDA(s).  
    * denomination, serial\_number, ans (an array of 25 16-byte ANs)  
* **Return Value:**  
  * An array of 25 complete, prepared, and encrypted byte arrays. Each byte array represents a full request. The client will select and send the appropriate requests to the chosen helper RAIDA servers.  
  * Returns the string "failure" if any significant, unrecoverable error occurs.

## **Request Structure Overview:**

Each request consists of three main parts, concatenated in order:

1. **Request Header (32 bytes):** Contains metadata, including the target server ID, command, and details for encrypting the request.  
2. **Request Body (50 bytes):** Contains the challenge and data needed by the helper RAIDA. This entire body will be encrypted.  
3. **Termination Bytes (2 bytes):** A fixed sequence (0x3E 0x3E) to mark the end of the request.

## **Detailed Logic:**

The function will construct 25 distinct requests, one for each potential helper server (Server ID 0 to 24).

### **1\. Request Body Construction (50 bytes):**

* The unencrypted body is constructed by concatenating the following parts in order:  
  * **Challenge (16 bytes):** The corresponding 16-byte challenge from the challenge\_bytes input array.  
  * **Target RAIDA Key ID (5 bytes):** The 1-byte denomination and 4-byte serial\_number from the target\_raida\_key\_id parameter.  
  * **Key Part (8 bytes):** The key\_part parameter.  
  * **Fracked Token SN (5 bytes):** The 1-byte denomination and 4-byte serial\_number from the fracked\_token parameter.  
  * **Fracked Token AN (16 bytes):** The 16-byte an from the fracked\_token parameter.

### **2\. Request Header Construction (32 bytes):**

Create a 32-byte header for each of the 25 servers. This function uses **Encryption Type 1**.

* **Bytes 0-3:**  
  * Byte 0 (VR): 0x00  
  * Byte 1 (SP): 0x00  
  * Byte 2 (RI): **Server ID** (from 0x00 for server 0, up to 0x18 for server 24\)  
  * Byte 3 (SH): 0x00  
* **Bytes 4-5 (Command):**  
  * Byte 4 (CG): 0x04 (Command Group: Healing Services For Keys)  
  * Byte 5 (CM): 0x2C (Command: Get Encryption Ticket, which is 44 in decimal)  
* **Bytes 6-15:** All set to 0x00.  
* **Byte 16 (EN):** 0x01 (Encryption Type: AES 128 CTR).  
* **Bytes 17-21 (Encryption Coin ID):**  
  * Byte 17: The denomination of the encryption\_coin.  
  * Bytes 18-21: The serial\_number of the encryption\_coin.  
* **Bytes 22-23 (BL):** The length of the encrypted body (50) plus two termination bytes (2), for a total of 52\. This will be 0x0034 (big-endian).  
* **Bytes 24-31 (Nonce):** A randomly generated 8-byte nonce.

### **3\. Encryption:**

* For each of the 25 requests, the entire 50-byte request body must be encrypted using AES 128 CTR mode.  
* The **encryption key** is the specific Authenticity Number from the encryption\_coin.ans array that corresponds to the server's ID (e.g., for Server ID i, use encryption\_coin.ans\[i\]).  
* The **nonce** is the 8-byte random nonce generated for bytes 24-31 of the header.

### **4\. Termination Bytes:**

* After the header and the encrypted body, append two fixed termination bytes: 0x3E 0x3E.

### **5\. Final Request Assembly:**

* For each of the 25 servers, concatenate the constructed Header, its corresponding encrypted Body, and the Termination Bytes into a single byte array.  
* Return the array containing all 25 complete request byte arrays.

## **Logging and Error Handling:**

* **Success:** Log key milestones, such as the start of the function and its successful completion.  
* **Errors:** Log any errors encountered during the process (e.g., invalid input parameters, encryption failures). Any error that prevents the successful creation of all 25 requests should cause the function to log the error and return the string "failure".

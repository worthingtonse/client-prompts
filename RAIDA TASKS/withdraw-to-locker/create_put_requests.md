### **Function Specification: createPutRequests**

#### **1\. Function Purpose**

The purpose of this function is to prepare a batch of 25 "put" requests. These requests are designed to store one or more digital coins into a single, secure "locker" on a distributed server network (RAIDA). All coins in the batch will be associated with a single, shared lockerCode, allowing them to be retrieved together by a third party who possesses that code.

#### **2\. Data Structures**

The function operates on the following data structure:

* **Coin Struct:** A 405-byte structure representing a single digital coin.  
  * authenticityNumbers (bytes, 400 bytes): An array of 25 elements, where each element is a 16-byte Authenticity Number (AN). authenticityNumbers\[i\] corresponds to the AN for RAIDA server i.  
  * denomination (byte, 1 byte): The value of the coin.  
  * serialNumber (bytes, 4 bytes): The unique serial number of the coin.

#### **3\. Function Signature**

function createPutRequests(  
    parentDirectory: string,  
    arrayOfFileNames: array\<string\>,  
    challenges: array\<byte\[16\]\>,  
    lockerCode: byte\[16\],  
    joinCoinsFirst: boolean  
): array\<byte\[\]\>

* **Input Parameters:**  
  * parentDirectory (string): The path to the directory where coin files are located.  
  * arrayOfFileNames (array of strings): An array of filenames for the coins to be included in the locker. This may be an empty array.  
  * challenges (array of 16-byte arrays): An array of 25 unique, 16-byte challenge strings, one for each RAIDA server.  
  * lockerCode (16-byte array): A 16-byte key used to secure and identify the locker on the RAIDA network.  
  * joinCoinsFirst (boolean): If true, the function must first call a join\_coins utility function, which may modify the arrayOfFileNames.  
* **Return Value:**  
  * An array of 25 byte arrays. Each byte array is a fully formed "put" request for a specific RAIDA server.

#### **4\. Input Validation**

Before processing, the function must validate the lockerCode:

1. The lockerCode must be exactly 16 bytes long.  
2. The last four bytes of the lockerCode **must** be 0xFF, 0xFF, 0xFF, 0xFF.  
3. If either of these conditions is not met, the function must throw an error with a message like: "Invalid Locker Code: Code must be 16 bytes and end with four 0xFF bytes."

#### **5\. Core Logic & Execution Flow**

1. **Validate lockerCode:** Perform the input validation as described above.  
2. **Join Coins (Optional):** If the joinCoinsFirst parameter is true, call the external join\_coins(arrayOfFileNames) function. The returned, potentially modified, array of filenames should be used for the subsequent steps.  
3. **Load Coins:** Iterate through the arrayOfFileNames. For each filename, call an external read\_coin(parentDirectory \+ fileName) function to read the file and load its contents into a Coin struct. Store all the resulting Coin structs in a list (e.g., listOfCoins).  
4. **Initialize Requests:** Create an array of 25 byte arrays, named putRequests.  
5. **Construct Requests (Outer Loop):** Loop from i \= 0 to 24\. Each iteration of this loop will build one of the 25 put requests.  
   a. **Initialize AN Sum:** Create a 16-byte array named aggregatedAN and initialize all its bytes to zero. This will act as the accumulator for the XOR sum.  
   b. Aggregate ANs (Inner Loop): Loop through each coin in the listOfCoins.  
   i. Take the i-th Authenticity Number from the current coin: currentAN \= coin.authenticityNumbers\[i\].  
   ii. Perform a 16-byte XOR operation between aggregatedAN and currentAN, storing the result back in aggregatedAN. (See XOR Sum Algorithm below).  
   c. Assemble Payload: Create the final byte array for the i-th request by concatenating the following components in order:  
   i. The i-th challenge: challenges\[i\] (16 bytes).  
   ii. The denomination from the first coin in the list: listOfCoins\[0\].denomination (1 byte).  
   iii. The serial number from the first coin in the list: listOfCoins\[0\].serialNumber (4 bytes).  
   iv. The calculated XOR sum: aggregatedAN (16 bytes).  
   v. The validated lockerCode (16 bytes).  
   d. **Store Request:** Assign the assembled payload to putRequests\[i\].  
6. **Return:** After the outer loop completes, return the putRequests array.

#### **6\. XOR Sum Algorithm**

To calculate the 16-byte aggregatedAN (the XOR sum), perform the following steps for each currentAN to be added:

1. **Convert to Integers:** Treat each 16-byte array (aggregatedAN and currentAN) as four consecutive 32-bit little-endian unsigned integers.  
   * agg\_i0 \= aggregatedAN\[0\] | aggregatedAN\[1\]\<\<8 | ...  
   * cur\_i0 \= currentAN\[0\] | currentAN\[1\]\<\<8 | ...  
2. **XOR Integers:** XOR the corresponding integers.  
   * sum\_i0 \= agg\_i0 ^ cur\_i0  
   * sum\_i1 \= agg\_i1 ^ cur\_i1  
   * ...and so on for all four integers.  
3. **Convert Back to Bytes:** Convert the four resulting sum integers back into a 16-byte array and update aggregatedAN with this new value.  
   * aggregatedAN\[0\] \= sum\_i0 & 0xFF  
   * aggregatedAN\[1\] \= (sum\_i0 \>\> 8\) & 0xFF  
   * ...and so on.

#### **7\. Dependencies**

This function relies on two external functions whose implementations are not defined here:

* join\_coins(arrayOfFileNames)  
* read\_coin(filePath)

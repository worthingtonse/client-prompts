CMD_PEEK (Command 63)
Description: Allows a client to check for messages without waiting (polling), or to fetch older messages since a timestamp.

Version A: With RKE/DRD (Current Code)
Auth: Session ID.

Request Structure (Decrypted Body):

Plaintext

| Byte Range | Field         | Size    | Description       |
| ---------- | ------------- | ------- | ----------------- |
| 0–7        | `SE ... SE`   | 8 bytes | Session ID        |
| 8–11       | `TS TS TS TS` | 4 bytes | “Since” Timestamp |

## RESPONSE STATUS
--------------------------------------------------------------------------------
```plaintext
[00]    ST                                               // Status Code (1 byte, 250=Success)
[01]    00                                               // CBDF Header Key
[02]    01                                               // CBDF Header Length
[03]    NP                                               // Number of Pairs (Files Found)
// --- Repeat NP Times ---
[..]    KY                                               // Key (1 byte): 100 + Index
[..]    L1 L2                                            // Length (2 bytes): File Size
[..]    DD DD ...                                        // File Data
```
explanation of response bytes :
## Response Structure Explanation

- **The Header (Bytes 01-03):**  
  The sequence starts with `00` (The "List" Tag) followed by `01` (telling the parser that the count field is 1 byte wide).  
  The next byte (`NP`) is the Item Count, representing exactly how many new email notifications were found (e.g., if you have 5 new emails, `NP` will be 5).

- **The Items (KLV Triplets):**  
  Following the count, the data is structured in repeating Key-Length-Value triplets for each file.

  - **Key (KY):**  
    A unique 1-byte ID for that specific message (starting at 100 and incrementing: 100, 101, 102...). This separates one message from the next.

  - **Length (L1 L2):**  
    A 2-byte integer specifying exactly how big the next file content is (e.g., 500 bytes). This tells the client "Read the next 500 bytes as one file."

  - **Data (DD...):**  
    The actual raw content of the `.meta` file.



meta files can be  present at /opt/raidax/mailboxes/500200/inbox/ where 500200 is the recivers identity

Version B: Standard RAIDA (New Architecture)
Auth: Receiver's Coin (Type 1 Header).

Request Structure (Decrypted Body):

Plaintext

| Byte Range | Field         | Size    | Description       |
| ---------- | ------------- | ------- | ----------------- |
| 0–3        | `TS TS TS TS` | 4 bytes | “Since” Timestamp |

Response Status:
```plaintext
// Same CBDF Structure as Option 1.
[00]    ST                                               // Status Code (1 byte, 250=Success)  /// STATUS_SUCCESS: Returns list of .meta files (binary or CBDF) found in /opt/raidax/mailboxes/<SN/DEN>/inbox/.
[01..]  CBDF Data...
```

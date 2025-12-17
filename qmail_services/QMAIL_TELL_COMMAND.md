# CMD_TELL

**Command Group:** 6
**Command Code:** 61
**Description:** Notifies the Beacon of a new message.

## Request Payload Structure (Decrypted)

**Total Common Preamble:** 49 Bytes (Offsets 0-48).

This is the body of the request. See other documents for how the header is organized.
| Offset | Size | Field Name | Description |
| :--- | :--- | :--- | :--- |
| **00-15** | 16 | **Challenge/CRC** | Random bytes or CRC. |
| **16-23** | 8 | **Session ID** | **Mode A:** Valid. **Mode B:** Zeros. Only used for encryption type 6, otherwise all zeros. |
| **24-25** | 2 | **Coin Type** | Fixed `00 06`. |
| **26** | 1 | **Denomination** | User's Denomination. Not used when using Encryption type 6 |
| **27-30** | 4 | **Serial Number** | User's Mailbox ID. This is for the user's ID. Not used when using Encryption type 6 |
| **31**    | 1  | **Device ID**        | 8-bit Device Identifier. User 0 for now for user's first desktop|
| **32-47**| 16 | **Authenticity (AN)**| **Mode A:** Zeros. **Mode B:** Valid AN. THe password for the DN SN SN SN mail box above|
| **48-63**| 16 | **File Group GUID**  | Unique 16-byte ID. |
| **64-71**| 8  | **Locker Code**      | Payment code. |
| **72-75**| 4  | **Timestamp**        | Client Time (Big Endian). |
| **76**   | 1  | **Tell Type**        | Type of notification. Use 0 for qmail |
| **77**   | 1  | **Address Count**    | Number of recipient addresses (AC) that will be listed below. |
| **78**   | 1  | **Server Count**     | Number of storage servers (QC) that will be listed below. |
| **79**   | 1  | **Reserved**         | 0. |
| **80**   | 1  | **Reserved**         | 0. |
| **81-87**| 7  | **Reserved**         | 0 |
| **88..** | Var| **Recipient List**   | `AC` items × 8 bytes each.<br>Item: `Type(1)+CoinID(2)+Denom(1)+SN(4)`. |
| **..**   | Var| **Stripe Map**       | `QC` items × 32 bytes each.<br>Item: `Index(1)+Total(1)+ServerID(1)+Reserved(29)`. |
| **End**  | 2  | **Terminator**       | Fixed `3E 3E` (Appended **after** last list item). |


### Receippient Types
Code | Name | Meaning
---|---|---
0 | To | Who the message is addessed to
1 | CC | copy sent to 
2 | BCC | Blind Carbon Copy
3 | Mass | Not implemented yet. 

### Server List Format

Name | bytes | Description
---|---|---
IP | 16 | Uses IP four but could use IPv6. IP 4 are the last four bytes of the 16
Port |2| The port that the Qmail server uses





### Address List Format
This is a list of all the addresses this tell is supposed to go to. Note that if there are addresses that are on different beacon servers, then a
tell must be sent out for each beacon server with different users. 



## Response Structure

**Note:** Status is returned in the Response Header. Payload is empty.

### Status Codes
| Code | Hex | Name | Meaning |
| :--- | :--- | :--- | :--- |
| **250** | `FA` | `STATUS_SUCCESS` | Notification created successfully. |
| **166** | `A6` | `ERROR_PAYMENT_REQUIRED`| Payment failed or locker empty. |
| **16** | `10` | `ERROR_INVALID_PACKET_LENGTH` | Malformed header or lists. |
| **194** | `C2` | `ERROR_FILESYSTEM` | Failed to write .meta file. |
| **18** | `12` | `ERROR_WRONG_RAIDA` | Recipient not found on this Beacon. |


## Tell File kept on RAIDA
| Offset | Size | Field Name | Description |
| :--- | :--- | :--- | :--- |
| **08-23** | 16 | **QMail GUID** | Unique ID of the file. |
| **08-23** | 8 | **Sender's Address** | CoinID, DN, SNs, extra byte  |
| **24-31** | 8 | **Locker Code** | Payment code (New code for receiver). |
| **32-35** | 4 | **Timestamp** | Client Timestamp. |
| **36** | 1 | **Tell Type** | Type of notification. |
| **..** | Var | **Server List** | `QC` items × 32 bytes each (Includes 2-byte RAID code). |
| **..** | Var | **Next Tell** | (If TS > 1, the next block repeats from Offset 08). |

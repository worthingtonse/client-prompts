# CMD_TELL

**Command Group:** 6
**Command Code:** 61
**Description:** Notifies the Beacon of a new message.

## Request Payload Structure (Decrypted)

**Total Common Preamble:** 49 Bytes (Offsets 0-48).


| Offset | Size | Field Name | Description |
| :--- | :--- | :--- | :--- |
| **00-15** | 16 | **Challenge/CRC** | Random bytes or CRC. |
| **16-23** | 8 | **Session ID** | **Mode A:** Valid. **Mode B:** Zeros. |
| **24-25** | 2 | **Coin Type** | Fixed `00 06`. |
| **26** | 1 | **Denomination** | User's Denomination. |
| **27-30** | 4 | **Serial Number** | User's Mailbox ID. |
| **31**    | 1  | **Device ID**        | 8-bit Device Identifier. |
| **32-47**| 16 | **Authenticity (AN)**| **Mode A:** Zeros. **Mode B:** Valid AN. |
| **48-63**| 16 | **File Group GUID**  | Unique 16-byte ID. |
| **64-71**| 8  | **Locker Code**      | Payment code. |
| **72-75**| 4  | **Timestamp**        | Client Time (Big Endian). |
| **76**   | 1  | **Tell Type**        | Type of notification. |
| **77**   | 1  | **Address Count**    | Number of recipients (AC). |
| **78**   | 1  | **Server Count**     | Number of storage servers (QC). |
| **79**   | 1  | **Reserved**         | (Was Subject Len). Set to 0. |
| **80**   | 1  | **Reserved**         | (Was Attach Count). Set to 0. |
| **81-87**| 7  | **Reserved**         | Padding bytes (Zeros). |
| **88..** | Var| **Recipient List**   | `AC` items × 8 bytes each.<br>Item: `Type(1)+CoinID(2)+Denom(1)+SN(4)`. |
| **..**   | Var| **Stripe Map**       | `QC` items × 32 bytes each.<br>Item: `Index(1)+Total(1)+ServerID(1)+Reserved(29)`. |
| **End**  | 2  | **Terminator**       | Fixed `3E 3E` (Appended **after** last list item). |


Receippient Types

Code | Name | Meaning
---|---|---
0 | To | Who the message is addessed to
1 | CC | copy sent to 
2 | BCC | Blind Carbon Copy
3 | Mass | Not implemented yet. 


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

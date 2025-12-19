# CMD_UPLOAD

**Command Group:** 6
**Command Code:** 60
**Description:** Uploads a binary data blob (stripe) to the storage server.

## Request Payload Structure (Decrypted)

**Total Common Preamble:** 49 Bytes (Offsets 0-48).


| Offset | Size | Field Name | Description |
| :--- | :--- | :--- | :--- |
| **00-15** | 16 | **Challenge/CRC** | Random bytes or CRC. |
| **16-23** | 8 | **Session ID** | **Mode A:** Valid. **Mode B:** Zeros. |
| **24-25** | 2 | **Coin Type** | Fixed `00 06`. |
| **26** | 1 | **Denomination** | User's Denomination. |
| **27-30** | 4 | **Serial Number** | Sender's Mailbox ID (Identity SN). |
| **31**    | 1 | **Device ID**        | 8-bit Device Identifier. |
| **32-47**| 16| **Authenticity (AN)**| Sender's Mailbox AN for that RAIDA **Mode A:** Zeros. **Mode B:** Valid AN. |
| **48-63**| 16| **File Group GUID**  | Unique 16-byte ID. |
| **64-71**| 8 | **Locker Code**      | Payment code. |
| **72-73**| 2 | **Reserved**         | Padding. |
| **74**   | 1 | **Reserved**         | (Was File Type). Set to 0. |
| **75**   | 1 | **Storage Duration** | Duration code. |
| **76-79**| 4 | **Reserved**         | Padding. |
| **80-83**| 4 | **Data Length**      | Size of binary data (Big Endian). |
| **84..** | N | **Binary Data**      | The actual file content. |
| **End**  | 2 | **Terminator**       | Fixed `3E 3E` (Appended **after** binary data). |


## Response Structure

**Note:** Status is returned in the Response Header. The Payload is empty on success.

### Status Codes
| Code | Hex | Name | Meaning |
| :--- | :--- | :--- | :--- |
| **250** | `FA` | `STATUS_SUCCESS` | File saved successfully. |
| **166** | `A6` | `ERROR_PAYMENT_REQUIRED`| Locker code invalid or insufficient funds. |
| **16** | `10` | `ERROR_INVALID_PACKET_LENGTH` | Payload too short or malformed. |
| **194** | `C2` | `ERROR_FILESYSTEM` | Server failed to write to disk. |
| **18** | `12` | `ERROR_WRONG_RAIDA` | User is not assigned to this server. |

## File Types

Type | Meaning
---|---
0 | Meta data about the email. Includes the subjects and id's of the attachments. 
1 | qmail. The styling and body of the qmail. 
2 | Reserved (could be web page, instant message, CloudCoin, crypto key, etc. 
10 | first attachment
11 | second attachment.
12 | attachments indexed to 255. 



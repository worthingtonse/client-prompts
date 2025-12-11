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
| **31-32** | 2 | **Device ID** | 16-bit Device Identifier. |
| **33-48** | 16 | **Authenticity (AN)** | **Mode A:** Zeros. **Mode B:** Valid AN. |
| **49-64** | 16 | **File Group GUID** | Unique 16-byte ID. |
| **65-72** | 8 | **Locker Code** | Payment code. |
| **73-76** | 4 | **Timestamp** | Client Time (Big Endian). |
| **77** | 1 | **Tell Type** | Type of notification. |
| **78** | 1 | **Address Count** | Number of recipients (AC). |
| **79** | 1 | **Server Count** | Number of storage servers (QC). |
| **80** | 1 | **Reserved** | (Was Subject Len). Set to 0. |
| **81** | 1 | **Reserved** | (Was Attach Count). Set to 0. |
| **82-88** | 7 | **Reserved** | Padding bytes (Zeros). |
| **89..** | Var | **Recipient List** | `AC` items × 8 bytes each.<br>Item: `Type(1)+CoinID(2)+Denom(1)+SN(4)`. |
| **..** | Var | **Stripe Map** | `QC` items × 32 bytes each.<br>Item: `Index(1)+Total(1)+ServerID(1)+Reserved(29)`. |
| **End** | 2 | **Terminator** | Fixed `3E 3E` (Appended **after** last list item). |

Receippient Types

Code | Meaning
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

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
| **27-30** | 4 | **Serial Number** | User's Mailbox ID (Identity SN). |
| **31-32** | 2 | **Device ID** | 16-bit Device Identifier. |
| **33-48** | 16 | **Authenticity (AN)** | **Mode A:** Zeros. **Mode B:** Valid AN. |
| **49-64** | 16 | **File Group GUID** | Unique 16-byte ID. |
| **65-72** | 8 | **Locker Code** | Payment code. |
| **73-74** | 2 | **Reserved** | Padding. |
| **75** | 1 | **Reserved** | (Was File Type). Set to 0. |
| **76** | 1 | **Storage Duration** | Duration code. |
| **77-80** | 4 | **Reserved** | Padding. |
| **81-84** | 4 | **Data Length** | Size of binary data (Big Endian). |
| **85..** | N | **Binary Data** | The actual file content. |
| **End** | 2 | **Terminator** | Fixed `3E 3E` (Appended **after** binary data). |

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

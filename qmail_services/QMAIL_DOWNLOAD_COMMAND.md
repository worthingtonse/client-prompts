# CMD_DOWNLOAD

**Command Group:** 6
**Command Code:** 64
**Description:** Retrieves a specific file blob from the storage server.

## Request Payload Structure (Decrypted)

**Total Common Preamble:** 49 Bytes.
**Command Data Starts:** Byte 49.

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
| **65** | 1 | **File Type** | Type of file requested. |
| **66** | 1 | **Version** | Version requested. |
| **67** | 1 | **Bytes Per Page** | Page size code (0=Max, 1=1KB, 2=8KB, 3=64KB). |
| **68** | 1 | **Page Number** | Page index to retrieve. |
| **69-70** | 2 | **Terminator** | Fixed `3E 3E` (Appended **after** parameters). |

## Response Payload Structure


| Offset | Size | Field Name | Description |
| :--- | :--- | :--- | :--- |
| **00** | 1 | **File Type** | Echoed back from request. |
| **01** | 1 | **Version** | Echoed back. |
| **02** | 1 | **Bytes Per Page** | Echoed back. |
| **03** | 1 | **Page Number** | Echoed back. |
| **04-07** | 4 | **Data Length** | Length of binary data following (Big Endian). |
| **08..** | N | **Binary Data** | The requested file chunk. |

### Status Codes
| Code | Hex | Name | Meaning |
| :--- | :--- | :--- | :--- |
| **250** | `FA` | `STATUS_SUCCESS` | File found and retrieved. |
| **202** | `CA` | `ERROR_FILE_NOT_EXIST` | GUID or Stripe not found. |
| **198** | `C6` | `ERROR_INVALID_PARAMETER` | Page Number exceeds file size. |
| **16** | `10` | `ERROR_INVALID_PACKET_LENGTH` | Malformed request. |
| **18** | `12` | `ERROR_WRONG_RAIDA` | User not authorized on this server. |

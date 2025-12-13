# CMD_PEEK

**Command Group:** 6
**Command Code:** 63
**Description:** Checks inbox for messages since a timestamp without waiting. Returns full details of new messages.

## Request Payload Structure (Decrypted)

**Total Common Preamble:** 49 Bytes.

| Offset | Size | Field Name | Description |
| :--- | :--- | :--- | :--- |
| **00-15** | 16 | **Challenge/CRC** | Random bytes or CRC. |
| **16-23** | 8 | **Session ID** | **Mode A:** Valid. **Mode B:** Zeros. |
| **24-25** | 2 | **Coin Type** | Fixed `00 06`. |
| **26** | 1 | **Denomination** | User's Denomination. |
| **27-30** | 4 | **Serial Number** | User's Mailbox ID. |
| **31**    | 1  | **Device ID**        | 8-bit Device Identifier. |
| **32-47**| 16 | **Authenticity (AN)**| **Mode A:** Zeros. **Mode B:** Valid AN. |
| **48-51**| 4  | **Since Timestamp**  | Unix Epoch (Big Endian). |
| **52-53**| 2  | **Terminator**       | Fixed `3E 3E` (Appended after timestamp). |


## Response Payload Structure (Tell Array)

| Offset | Size | Field Name | Description |
| :--- | :--- | :--- | :--- |
| **00** | 1 | **Tell Count (TS)** | How many tells are in this response packet. |
| **01-02** | 2 | **Total Tells (TT)**| How many tells remain on the beacon. |
| **03-07** | 5 | **Reserved** | Padding/Alignment bytes. |
| QMail Array | 0 | QMail index[n] | The following can be repeated for every qmail|
| **08-23** | 16 | **QMail GUID** | Unique ID of the qmail . |
| **24-31** | 8 | **Locker Code** | Payment code. |
| **32-35** | 4 | **Timestamp** | Client Timestamp. |
| **36** | 1 | **Tell Type** | Type of notification. |
| **37** | 1 | **Address Count** | Number of recipients (AC). |
| **38** | 1 | **Server Count** | Number of storage servers (QC). |
| **39** | 1 | **Reserved** | (Was Subject Len). |
| **40** | 1 | **Reserved** | (Was Attach Count). |
| **41-47** | 7 | **Reserved** | Padding. |
| **48..** | Var | **Address List** | `AC` items × 8 bytes each. |
| **..** | Var | **Server List** | `QC` items × 32 bytes each (Includes 2-byte RAID code). |
| **..** | Var | **Next Tell** | (If TS > 1, the next block repeats from Offset 08). |

### Status Codes
| Code | Hex | Name | Meaning |
| :--- | :--- | :--- | :--- |
| **250** | `FA` | `STATUS_SUCCESS` | Request successful (Check TS for count). |
| **16** | `10` | `ERROR_INVALID_PACKET_LENGTH` | Malformed request. |
| **165** | `A5` | `STATUS_AUTH_FAILED` | Session or Identity Invalid. |

# CMD_PING

**Command Group:** 6
**Command Code:** 62
**Description:** Establishes a long-polling connection to wait for new "Tells". Returns full details of new messages.

## Request Payload Structure (Decrypted)

**Total Size:** 51 Bytes.

| Offset | Size | Field Name | Description |
| :--- | :--- | :--- | :--- |
| **00-15** | 16 | **Challenge/CRC** | Random bytes or CRC. |
| **16-23** | 8 | **Session ID** | **Mode A:** Valid. **Mode B:** Zeros. |
| **24-25** | 2 | **Coin Type** | Fixed `00 06`. |
| **26** | 1 | **Denomination** | User's Denomination. |
| **27-30** | 4 | **Serial Number** | User's Mailbox ID. |
| **31**    | 1  | **Device ID**        | 8-bit Device Identifier. |
| **32-47**| 16 | **Authenticity (AN)**| **Mode A:** Zeros. **Mode B:** Valid AN. |
| **48-49**| 2  | **Terminator**       | Fixed `3E 3E` (Appended at end). |


## Response Payload Structure (Tell Array)

This payload follows the Response Header (which contains the Status Code).

| Offset | Size | Field Name | Description |
| :--- | :--- | :--- | :--- |
| **00** | 1 | **Tell Count (TS)** | How many tells are in this response packet. |
| **01-02** | 2 | **Total Tells (TT)**| How many tells remain on the beacon (Big Endian). |
| **03-07** | 5 | **Reserved** | Padding/Alignment bytes. |
| **08-23** | 16 | **File GUID** | Unique ID of the email. |
| **24-31** | 8 | **Locker Code** | blank |
| **32-35** | 4 | **Timestamp** | Beacon Timestamp. |
| **36** | 1 | **Tell Type** | Type of notification. |
| **37** | 1 | **Reserved** | blank |
| **38** | 1 | **Server Count** | Number of storage servers (QC). |
| **39-48** | 1 | **Reserved** | blank |
| **..** | Var | **Server List** | `QC` items × 32 bytes each (Includes 2-byte RAID code). |
| **..** | Var | **Next Tell** | (If TS > 1, the next block repeats from Offset 08). |

### Status Codes
| Code | Hex | Name | Meaning |
| :--- | :--- | :--- | :--- |
| **250** | `FA` | `STATUS_SUCCESS` | New mail found. |
| **17** | `11` | `ERROR_UDP_FRAME_TIMEOUT` | No mail found (Connection timed out). |
| **16** | `10` | `ERROR_INVALID_PACKET_LENGTH` | Malformed request. |
| **165** | `A5` | `STATUS_AUTH_FAILED` | Session or Identity Invalid. |

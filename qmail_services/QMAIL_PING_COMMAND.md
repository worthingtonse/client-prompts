CMD_PING (Command 62)
Description: Sent by the Receiver to the Beacon (R13). It opens a long-polling connection to wait for new mail notifications.

Version A: With RKE/DRD (Current Code)
Auth: Session ID.

Request Structure (Decrypted Body):

Plaintext

| Byte Range | Field                     | Size     | Description                        |
| ---------- | ------------------------- | -------- | ---------------------------------- |
| 0-15 | CH CH CH CH CH CH CH CH CH CH CH CH CH CH CH CH  | 16 bytes | Challenge/CRC |
| 0–7        | `SE SE SE SE SE SE SE SE` | 8 bytes  | Session ID                         |
| 0–7        | `3E 3E` | 2 bytes  | Termination bytes                        |

## RESPONSE STATUS
--------------------------------------------------------------------------------
```plaintext
// Immediate: None (Socket held open).
// On Event (New Mail): Returns file content.
// On Error:
[00]    ST                                               // Status Code (1 byte)
                                                         // 254 (0xFE): ERROR_INVALID_PACKET_LENGTH
                                                         // 241 (0xF1): STATUS_SESSION_TIMEOUT
```

## Response Body
This is basically the same information the Tell send to the Beacon.

| Byte Range | Field         | Size          | Description           |
| ---------- | ------------- | ------------- | --------------------- |
| 8–23       | `GG ... GG`   | 16 bytes      | File GUID             |
| 24–31      | `LC ... LC`   | 8 bytes       | Locker Code (payment) |
| 32–35      | `TT TT TT TT` | 4 bytes       | Client Timestamp      |
| 36         | `TY`          | 1 byte        | Tell Type             |
| 37         | `AC`          | 1 byte        | Address Count         |
| 38         | `QC`          | 1 byte        | QMail Server Count    |
| 39         | `SL`          | 1 byte        | Reserved         |
| 40         | `AT`          | 1 byte        | Reserved   |
| 41–47      | `RS ... RS`   | 7 bytes       | Reserved              |
| 48..       | `AD ...`      | AC × 8 bytes  | Address List   |
| ..         | `SV ...`      | QC × 32 bytes | Server List  that includes the two byte RAID code          |


Response Status:

| Status                            | Meaning                                |
| --------------------------        | -------------------------------------- |
| **STATUS_SUCCESS (0)** (250)      | Meta file created in recipient inboxes |
| **ERROR_PAYMENT_REQUIRED** (253)  | Locker code empty or invalid           |


Version B: Standard RAIDA (New Architecture)
Auth: Sender's Coin (Type 1 Header).

Behavior: Runs on Beacon (R13). processes payment (Import/Split/Export) and creates .meta file.

Request Structure (Decrypted Body):

Plaintext
| Byte Range | Field         | Size     | Description                              |
| ---------- | ------------- | -------- | ---------------------------------------- |
| 0–15       | `GG ... GG`   | 16 bytes | File GUID                                |
| 16–23      | `LC ... LC`   | 8 bytes  | Locker Code (payment)                    |
| 24–27      | `TT TT TT TT` | 4 bytes  | Client Timestamp                         |
| 28         | `AC`          | 1 byte   | Address Count                            |
| 29         | `SL`          | 1 byte   | Subject Length                           |
| 30..       | `AD ...`      | variable | Address List (Target SNs)                |
| ..         | `SB ...`      | SL bytes | Subject String                           |
| ..         | `LO ...`      | variable | Location Map (e.g., “Stripe 0: RAIDA 5”) |

Response Status:

STATUS_SUCCESS (0)



Version B: Standard RAIDA (New Architecture)
Auth: Receiver's Coin (Type 1 Header).

Identity: Server reads SN and denomination from Packet Header or a separate identity can be sent within the payload .

Request Structure (Decrypted Body):

Plaintext

(Empty Body)
// The user identity is fully contained in the encrypted Packet Header or we can include it in the body.
## RESPONSE STATUS
--------------------------------------------------------------------------------
```plaintext
// Immediate: None (Socket held open).
// On Event: Returns file content.
```

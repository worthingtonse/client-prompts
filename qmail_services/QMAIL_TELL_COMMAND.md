CMD_TELL (Command 61)
Description: Sent by the Sender to the Beacon (R13). It notifies the system that a file has been uploaded, provides metadata, and pays the fee.

Version A: With RKE/DRD (Current Code)
Auth: Session ID.

Request Structure (Decrypted Body):

Plaintext

| Byte Range | Field         | Size          | Description           |
| ---------- | ------------- | ------------- | --------------------- |
| 0–7        | `SE ... SE`   | 8 bytes       | Session ID            |
| 8–23       | `GG ... GG`   | 16 bytes      | File GUID             |
| 24–31      | `LC ... LC`   | 8 bytes       | Locker Code (payment) |
| 32–35      | `TT TT TT TT` | 4 bytes       | Client Timestamp      |
| 36         | `TY`          | 1 byte        | Tell Type             |
| 37         | `AC`          | 1 byte        | Address Count         |
| 38         | `QC`          | 1 byte        | QMail Server Count    |
| 39         | `SL`          | 1 byte        | Subject Length        |
| 40         | `AT`          | 1 byte        | Attachment Count      |
| 41–47      | `RS ... RS`   | 7 bytes       | Reserved              |
| 48..       | `AD ...`      | AC × 8 bytes  | Address List          |
| ..         | `SV ...`      | QC × 32 bytes | Server List           |
| ..         | `SB ...`      | SL bytes      | Subject String        |

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

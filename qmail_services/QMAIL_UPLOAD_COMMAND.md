CMD_UPLOAD (Command 60)
Description: Uploads a file stripe (chunk) to the  qmail server. The server saves it to a nested directory structure based on the file's GUID.

Version A: With RKE/DRD (Current Code)
Auth: Relies on a pre-established Session key and session ID.

Encryption: Type 6 (AES-256 using Session Key).

Request Structure (Decrypted Body):

Plaintext

| Byte Range | Field         | Size     | Description               |
| ---------- | ------------- | -------- | ------------------------- |
| 0–7        | `SE ... SE`   | 8 bytes  | Session ID                |
| 8–23       | `GG ... GG`   | 16 bytes | File GUID                 |
| 24–31      | `LC ... LC`   | 8 bytes  | Locker Code (Payment)     |
| 32–33      | `RS RS`       | 2 bytes  | Reserved                  |
| 34         | `FT`          | 1 byte   | File Type                 |
| 35         | `SD`          | 1 byte   | Storage Duration          |
| 36–39      | `RS ... RS`   | 4 bytes  | Reserved                  |
| 40–43      | `LL LL LL LL` | 4 bytes  | Data Length               |
| 44–45      | `RR RR`       | 2 bytes  | RAID Header (Index/Total) |
| 46..       | `DD ...`      | variable | File Data (Chunk content) |

Response Status:

| Status                     | Meaning                        |
| -------------------------- | ------------------------------ |
| **STATUS_SUCCESS (0)**     | File saved successfully        |
| **ERROR_PAYMENT_REQUIRED** | Locker code invalid or missing |
| **ERROR_SESSION_TIMEOUT**  | Session expired or not found   |


Version B: Standard RAIDA (New  proposed Architecture) 
Auth: Standard RAIDA Type 1 Header (Uses Coin SN/AN).

Encryption: Type 1 (AES-128 using Coin AN).

Diff: No Session ID, lighter payload. Payment is usually handled at the "Tell" stage (Beacon), but if per-upload payment is needed, it stays here.

Request Structure (Decrypted Body):

Plaintext

// Note: User Identity is derived from the Coin used to encrypt.

| Byte Range | Field    | Size     | Description               |
| ---------- | -------- | -------- | ------------------------- |
| 0–1        | `RR RR`  | 2 bytes  | RAID Header (Index/Total) |
| 2..        | `DD ...` | variable | File Data (Chunk content) |

(Note: If the simplified flow moves Payment to the Beacon, the UPLOAD command just needs the data. If specific metadata like Duration/Type is needed here for naming, it is prepended).

Response Status:

STATUS_SUCCESS (0)

ERROR_WRONG_RAIDA (If user is not assigned to this server in user.txt)
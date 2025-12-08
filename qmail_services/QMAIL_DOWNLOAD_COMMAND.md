CMD_DOWNLOAD (Command 64)
Description: Sent by Receiver to qmail Server (e.g., R5). Retrieves a specific file chunk based on GUID.

Version A: With RKE/DRD (Current Code)
Auth: Session ID.

Request Structure (Decrypted Body):

Plaintext

| Byte Range | Field                     | Size     | Description                        |
| ---------- | ------------------------- | -------- | ---------------------------------- |
| 0–7        | `SE SE SE SE SE SE SE SE` | 8 bytes  | Session ID                         |
| 8–23       | `GG ... GG`               | 16 bytes | File GUID                          |
| 24         | `FT`                      | 1 byte   | File Type                          |
| 25         | `VR`                      | 1 byte   | Version                            |
| 26         | `BP`                      | 1 byte   | Bytes-Per-Page Code                |
| 27         | `PN`                      | 1 byte   | Page Number (used for large files) |

Response Status:

| Status                   | Meaning                      |
| ------------------------ | ---------------------------- |
| **STATUS_SUCCESS**       | Followed by file binary data |
| **ERROR_FILE_NOT_EXIST** | GUID or stripe not found     |

storage path example : /opt/raidax/public_uploads/a1/b2/<GUID>/stripe05-25_type0_v0.qmail


Version B: Standard RAIDA (New Architecture)
Auth: Receiver's Coin (Type 1 Header).

Logic: Server checks if User (SN/DENOM from Header or info from payload) is authorized to download (optional), then fetches file by GUID.

Request Structure (Decrypted Body):

Plaintext

| Byte Range | Field       | Size     | Description         |
| ---------- | ----------- | -------- | ------------------- |
| 0–15       | `GG ... GG` | 16 bytes | File GUID           |
| 16         | `FT`        | 1 byte   | File Type           |
| 17         | `VR`        | 1 byte   | Version             |
| 18         | `BP`        | 1 byte   | Bytes-Per-Page Code |
| 19         | `PN`        | 1 byte   | Page Number         |

Response Status:

STATUS_SUCCESS: Followed by file binary data (Server looks in /opt/raidax/public_uploads/...).

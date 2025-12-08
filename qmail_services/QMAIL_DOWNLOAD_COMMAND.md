CMD_DOWNLOAD (Command 64)
Description: Sent by Receiver to Storage Server (e.g., R5). Retrieves a specific file chunk based on GUID.

Version A: With RKE/DRD (Current Code)
Auth: Session ID.

Request Structure (Decrypted Body):

Plaintext

[00-15] SE SE SE SE SE SE SE SE                          // Session ID (8 bytes)
[16-31] GG GG GG GG GG GG GG GG GG GG GG GG GG GG GG GG  // File GUID (16 bytes)
[32]    FT                                               // File Type (1 byte)
[33]    VR                                               // Version (1 byte)
[34]    BP                                               // Bytes Per Page Code (1 byte)
[35]    PN                                               // Page Number (1 byte - for large files)
Response Status:

STATUS_SUCCESS: Followed by file binary data. from /opt/raidax/public_uploads/a1/b2/<GUID>/stripe05-25_type0_v0.qmail

ERROR_FILE_NOT_EXIST: GUID/Stripe not found.

Version B: Standard RAIDA (New Architecture)
Auth: Receiver's Coin (Type 1 Header).

Logic: Server checks if User (SN/DENOM from Header or info from payload) is authorized to download (optional), then fetches file by GUID.

Request Structure (Decrypted Body):

Plaintext

[00-15] GG GG GG GG GG GG GG GG GG GG GG GG GG GG GG GG  // File GUID (16 bytes)
[16]    FT                                               // File Type
[17]    VR                                               // Version
[18]    BP                                               // Bytes Per Page Code
[19]    PN                                               // Page Number
Response Status:

STATUS_SUCCESS: Followed by file binary data (Server looks in /opt/raidax/public_uploads/...).
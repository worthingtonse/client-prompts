CMD_UPLOAD (Command 60)
Description: Uploads a file stripe (chunk) to the  qmail server. The server saves it to a nested directory structure based on the file's GUID.

Version A: With RKE/DRD (Current Code)
Auth: Relies on a pre-established Session key and session ID.

Encryption: Type 6 (AES-256 using Session Key).

Request Structure (Decrypted Body):

Plaintext

[00-15] SE SE SE SE SE SE SE SE                          // Session ID (8 bytes)
[16-31] GG GG GG GG GG GG GG GG GG GG GG GG GG GG GG GG  // File GUID (16 bytes)
[32-39] LC LC LC LC LC LC LC LC                          // Locker Code (8 bytes - Payment)
[40-41] RS RS                                            // Reserved (2 bytes)
[42]    FT                                               // File Type (1 byte)
[43]    SD                                               // Storage Duration (1 byte)
[44-47] RS RS RS RS                                      // Reserved (4 bytes)
[48-51] LL LL LL LL                                      // Data Length (4 bytes)
[52-53] RR RR                                            // RAID Header (2 bytes: Index/Total)
[54..]  DD DD DD ...                                     // File Data (Chunk content)
Response Status:

STATUS_SUCCESS (0): File saved successfully.

ERROR_PAYMENT_REQUIRED: Locker code invalid or empty.

ERROR_SESSION_TIMEOUT: Session ID not found.

Version B: Standard RAIDA (New  proposed Architecture) 
Auth: Standard RAIDA Type 1 Header (Uses Coin SN/AN).

Encryption: Type 1 (AES-128 using Coin AN).

Diff: No Session ID, lighter payload. Payment is usually handled at the "Tell" stage (Beacon), but if per-upload payment is needed, it stays here.

Request Structure (Decrypted Body):

Plaintext

// Note: User Identity is derived from the Coin used to encrypt.

[00-01] RR RR                                            // RAID Header (2 bytes: Index/Total)
[02..]  DD DD DD ...                                     // File Data (Chunk content)
(Note: If the simplified flow moves Payment to the Beacon, the UPLOAD command just needs the data. If specific metadata like Duration/Type is needed here for naming, it is prepended).

Response Status:

STATUS_SUCCESS (0)

ERROR_WRONG_RAIDA (If user is not assigned to this server in user.txt)
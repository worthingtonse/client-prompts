CMD_TELL (Command 61)
Description: Sent by the Sender to the Beacon (R13). It notifies the system that a file has been uploaded, provides metadata, and pays the fee.

Version A: With RKE/DRD (Current Code)
Auth: Session ID.

Request Structure (Decrypted Body):

Plaintext

[00-15] SE SE SE SE SE SE SE SE                          // Session ID (8 bytes)
[16-31] GG GG GG GG GG GG GG GG GG GG GG GG GG GG GG GG  // File GUID (16 bytes)
[32-39] LC LC LC LC LC LC LC LC                          // Locker Code (8 bytes - Payment)
[40-43] TT TT TT TT                                      // Client Timestamp (4 bytes)
[44]    TY                                               // Tell Type (1 byte)
[45]    AC                                               // Address Count (1 byte)
[46]    QC                                               // QMail Server Count (1 byte)
[47]    SL                                               // Subject Length (1 byte)
[48]    AT                                               // Attachment Count (1 byte)
[49-55] RS RS RS RS RS RS RS                             // Reserved (7 bytes)
[56..]  AD AD ...                                        // Address List (AC * 8 bytes)
[..]    SV SV ...                                        // Server List (QC * 32 bytes)
[..]    SB SB ...                                        // Subject String (SL bytes)
Response Status:

STATUS_SUCCESS (0): Meta file created in recipient inboxes.

ERROR_PAYMENT_REQUIRED: Locker code empty/invalid.

Version B: Standard RAIDA (New Architecture)
Auth: Sender's Coin (Type 1 Header).

Behavior: Runs on Beacon (R13). processes payment (Import/Split/Export) and creates .meta file.

Request Structure (Decrypted Body):

Plaintext

[00-15] GG GG GG GG GG GG GG GG GG GG GG GG GG GG GG GG  // File GUID (16 bytes)
[16-23] LC LC LC LC LC LC LC LC                          // Locker Code (8 bytes - Payment)
[24-27] TT TT TT TT                                      // Client Timestamp
[28]    AC                                               // Address Count
[29]    SL                                               // Subject Length
[30..]  AD AD ...                                        // Address List (Target User SNs)
[..]    SB SB ...                                        // Subject String
[..]    LO LO ...                                        // Location Map (e.g. "Stripe 0: RAIDA 5")
Response Status:

STATUS_SUCCESS (0)
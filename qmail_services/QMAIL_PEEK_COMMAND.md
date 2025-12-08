CMD_PEEK (Command 63)
Description: Allows a client to check for messages without waiting (polling), or to fetch older messages since a timestamp.

Version A: With RKE/DRD (Current Code)
Auth: Session ID.

Request Structure (Decrypted Body):

Plaintext

[00-15] SE SE SE SE SE SE SE SE                           // Session ID (8 bytes)
[16-19] TS TS TS TS                                      // Since Timestamp (4 bytes)
Response Status:

STATUS_SUCCESS: Returns CBDF payload containing list of .meta files found. which are present at /opt/raidax/mailboxes/500200/inbox/

Version B: Standard RAIDA (New Architecture)
Auth: Receiver's Coin (Type 1 Header).

Request Structure (Decrypted Body):

Plaintext

[00-03] TS TS TS TS                                      // Since Timestamp (4 bytes)
Response Status:

STATUS_SUCCESS: Returns list of .meta files (binary or CBDF) found in /opt/raidax/mailboxes/<SN/DEN>/inbox/.
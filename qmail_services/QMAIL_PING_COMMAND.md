CMD_PING (Command 62)
Description: Sent by the Receiver to the Beacon (R13). It opens a long-polling connection to wait for new mail notifications.

Version A: With RKE/DRD (Current Code)
Auth: Session ID.

Request Structure (Decrypted Body):

Plaintext

[00-15] SE SE SE SE SE SE SE SE   // Session ID (8 bytes)
Response Status:

(No immediate response - Socket held open).

On Data: Returns CBDF payload of .meta file.

STATUS_SESSION_TIMEOUT: If Session invalid.

Version B: Standard RAIDA (New Architecture)
Auth: Receiver's Coin (Type 1 Header).

Identity: Server reads SN and denomination from Packet Header or a separate identity can be sent within the payload .

Request Structure (Decrypted Body):

Plaintext

(Empty Body)
// The user identity is fully contained in the encrypted Packet Header or we can include it in the body.
Response Status:

(Socket held open).

On Data: Returns raw content of .meta file.

STATUS_SUCCESS: If no mail (after timeout).
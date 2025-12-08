CMD_PING (Command 62)
Description: Sent by the Receiver to the Beacon (R13). It opens a long-polling connection to wait for new mail notifications.

Version A: With RKE/DRD (Current Code)
Auth: Session ID.

Request Structure (Decrypted Body):

Plaintext

| Byte Range | Field                     | Size     | Description                        |
| ---------- | ------------------------- | -------- | ---------------------------------- |
| 0–7        | `SE SE SE SE SE SE SE SE` | 8 bytes  | Session ID                         |

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

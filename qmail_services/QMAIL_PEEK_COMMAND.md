CMD_PEEK (Command 63)
Description: Allows a client to check for messages without waiting (polling), or to fetch older messages since a timestamp.

Version A: With RKE/DRD (Current Code)
Auth: Session ID.

Request Structure (Decrypted Body):

Plaintext

| Byte Range | Field         | Size    | Description       |
| ---------- | ------------- | ------- | ----------------- |
| 0–7        | `SE ... SE`   | 8 bytes | Session ID        |
| 8–11       | `TS TS TS TS` | 4 bytes | “Since” Timestamp |

Response Status:

| Status             | Meaning                                               |
| ------------------ | ----------------------------------------------------- |
| **STATUS_SUCCESS** | Returns CBDF payload containing list of `.meta` files |

meta files can be  present at /opt/raidax/mailboxes/500200/inbox/ where 500200 is the recivers identity

Version B: Standard RAIDA (New Architecture)
Auth: Receiver's Coin (Type 1 Header).

Request Structure (Decrypted Body):

Plaintext

| Byte Range | Field         | Size    | Description       |
| ---------- | ------------- | ------- | ----------------- |
| 0–3        | `TS TS TS TS` | 4 bytes | “Since” Timestamp |

Response Status:

STATUS_SUCCESS: Returns list of .meta files (binary or CBDF) found in /opt/raidax/mailboxes/<SN/DEN>/inbox/.
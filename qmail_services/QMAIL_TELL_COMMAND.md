# CMD_TELL

**Command Group:** 6
**Command Code:** 61
**Description:** Notifies the Beacon of a new message.

## Authorization

**IMPORTANT:** Authorization is via AN (Authenticity Number) ONLY.
- Recipients do NOT need to be listed in a directory to receive mail
- The AN proves ownership of the sender's coin/mailbox
- Diectories such as the stopgap `users.php` is for optional profile data only (name, avatar, fees)

## Request Payload Structure (Decrypted)

**Total Common Preamble:** 48 Bytes (Offsets 0-47).

This is the body of the request. See other documents for how the header is organized.
| Offset | Size | Field Name | Description |
| :--- | :--- | :--- | :--- |
| **00-15** | 16 | **Challenge/CRC** | Random bytes or CRC. |
| **16-23** | 8 | **Session ID** | **Mode A:** Valid. **Mode B:** Zeros. Only used for encryption type 6, otherwise all zeros. |
| **24-25** | 2 | **Coin Type** | Fixed `00 06`. |
| **26** | 1 | **Denomination** | Sender's Denomination. Not used when using Encryption type 6 |
| **27-30** | 4 | **Serial Number** | Sender's Mailbox ID. This is for the user's ID. Not used when using Encryption type 6 |
| **31**    | 1  | Reserved      |  |
| **32-47**| 16 | **Authenticity (AN)**| **Mode A:** Zeros. **Mode B:** Valid AN. The password for the DN SN SN SN mail box above |
| **48-63**| 16 | **Email ID GUID**  | Unique 16-byte ID. |
| **64-71**| 8  | **Reserved**     |  |
| **72-75**| 4  | **Timestamp**        | Client Time (Big Endian). |
| **76**   | 1  | **Tell Type**        | Type of notification. Use 0 for qmail |
| **77**   | 1  | **Address Count**    | Number of recipient addresses (AC) that will be listed below. |
| **78**   | 1  | **Server Count**     | Number of storage servers (QC) that will be listed below. |
| **79-86** | 8  | **Beacon Payment Locker** | Optional 8-byte locker code for anti-DDOS payment to beacon. Zeros if no payment. |
| **87**   | 1  | **Reserved**         | |
|  | Var| **Recipient List**   | `AC` Recipients × 32 bytes each.<br>Item: `Type(1)+CoinID(2)+Denom(1)+DomainID(1)+SN(3)+LockerPaymentKey(16)+Reserved(8)`. |
|  | Var| **QMail Server**       | `QC` Servers × 32 bytes each.<br>Item: `StripeIndex(1)+StripeType(1)+LockerCode(8)+IP(16)+Port(2)+Reserved(4)`. |
| **End**  | 2  | **Terminator**       | Fixed `3E 3E` (Appended **after** last list item). Not encrypted |


### Receipient Types
Code | Name | Meaning
---|---|---
0 | To | Who the message is addessed to
1 | CC | copy sent to 
2 | BCC | Blind Carbon Copy
3 | Mass | Not implemented yet. 

### Server List Format (32 bytes each)
Each server that the messages are striped on is described here.

| Name | Bytes | Description |
|---|---|---|
| Stripe Index | 1 | Order in which this server array must be lined up. Starts at zero. |
| Stripe Type | 1 | 0=Data Stripe, 1=Parity, 2=Mirror |
| Locker Code | 8 | Locker code for this stripe (allows recipient to derive decryption key) |
| IP Address | 16 | IPv4 in last 4 bytes (first 12 bytes are zeros for IPv4) |
| Port | 2 | The port that the QMail server uses (Big Endian) |
| Reserved | 4 | Reserved for future use |

### Recipient Address Format (32 bytes each)

| Name | Bytes | Description |
|---|---|---|
| Address Type | 1 | 0x00=To, 0x01=CC, 0x02=BCC, 0x03=Mass Mailer |
| Coin ID | 2 | Example: 0x0006 (6 means CloudCoinV3) |
| Denomination | 1 | The denomination of the coin the user has staked for the email address |
| Domain ID | 1 | Top Level Domain (high byte of 4-byte serial). Use 0x01 for now. |
| Serial Number | 3 | The serial number of the mailbox (lower 3 bytes) |
| Locker Payment Key | 16 | Payment locker code for THIS recipient |
| Reserved | 8 | Reserved for future use | 



### Tell Types

| Type ID | Name | Description |
|---------|------|-------------|
| 0 | QMAIL | Primary email message file |
| 1 | QTEXT | Reserved for future text processing |
| 2 | QCHAT | Reserved for future chat functionality |
| 3 | PEER_TO_PEER_SECRET_CBDF | Private user identification data |
| 4 | GROUPS_SECRET_CBDF | Private group identification data |
| 5 | QPACKET | Reserved for future packet management |
| 6 | QDATA | File management for QData servers |
| 10-255 | Attachment N | File attachments (10 = first attachment, etc.) |

## Response Structure

**Note:** Status is returned in the Response Header. Payload is empty.

### Status Codes
| Code | Hex | Name | Meaning |
| :--- | :--- | :--- | :--- |
| **250** | `FA` | `STATUS_SUCCESS` | Notification created successfully. |
| **166** | `A6` | `ERROR_PAYMENT_REQUIRED`| Payment failed or locker empty. |
| **16** | `10` | `ERROR_INVALID_PACKET_LENGTH` | Malformed header or lists. |
| **194** | `C2` | `ERROR_FILESYSTEM` | Failed to write .meta file. |

**Note:** Recipients are NOT validated against `user.php`. All TELLs to this beacon are accepted.
The beacon delivers to the recipient's inbox directory based on their address.




# QMail Services
This coveres the servics that run on the Qmail servers for Phase I


### File Types

| Type ID | Name | Description |
|---------|------|-------------|
| 0x00 | QMAIL | Primary email message file |
| 0x01 | QTEXT | Reserved for future text processing |
| 0x02 | QCHAT | Reserved for future chat functionality |
| 0x03 | PEER_TO_PEER_SECRET_CBDF | Private user identification data |
| 0x04 | GROUPS_SECRET_CBDF | Private group identification data |
| 0x05 | QPACKET | Reserved for future packet management |
| 0x06 | QDATA | File management for QData servers |
| 0x07 | Contact | Standard Contact File|
| 0x08 | Calendar Item | Stardard Calendar Item |
| 0x09 | ToDo Item | For Assigining someone a ToDo item |
| 0x10-0xFF | Attachment N | File attachments (0x10 = first attachment, etc.) |

### Storage Duration
Files can be stored for varying durations based on the storage code:

| Code | Duration | Calculation | Description |
|------|----------|-------------|-------------|
| 0x00 | Server-dependent | N/A | Free storage, server decides deletion time |
| 0x01-0x06 | 1-6 days | Code × 1 day | Daily storage |
| 0x07-0x0A | 1-4 weeks | (Code - 6) × 7 days | Weekly storage |
| 0x0B-0x16 | 1-12 months | (Code - 10) × 30 days | Monthly storage |
| 0x17-20 | 1-10 years | (Code - 22) × 365 days | Yearly storage |

**Note**: Longer storage periods incur higher fees as specified in the server's DRD.


## Share File (Send Email and attachements)
Command Group: 6

Command Code: 60

Note that each file that is uploaded must have the same GUID but a different File Type/Index

These services generally use [Encryption Type 6](https://github.com/worthingtonse/client-prompts/blob/main/CONTEXT/request-header-format-for-256-bit-encryption.md#encryption-type-6) . However, if the QMail server is located on a RAIDA, it is possible that any encryption type could be used. Because off this, a key exchange must occure between the client and QMNail server before commands like this can be issued. 

Sample Request:
Note that everything is Big Endian
```
CH CH CH CH CH CH CH CH CH CH CH CH CH CH CH CH // Challenge
SE SE SE SE SE SE SE SE SE SE SE SE SE SE SE SE // Session ID
ID ID ID ID ID ID ID ID ID ID ID ID ID ID ID ID  // Email's GUID
LC LC LC LC LC LC LC LC LC LC LC LC LC LC LC LC   // Locker Code for payment to QMail server (All zeros if empty)
MY MY MY MY MY MY MY MY MY MY MY MY MY MY MY MY   // GUID of MyContact File (All zeros if empty)
FT // File type
RH RH // RAID Header
TS TS TS TS //Time stamp
RS // Number of Addresses Below (Up to 255)
AD AD AD AD AD AD AD AD // Adddress (Address type, Coin Coin Type, Denomination, Serial Numbers, 
BL BL BL BL // Number of Bytes in the Data below (Big Endian)
BI BI BI BI ..... Binary File Data
E3 E3 //Not encrypted
```

## Address Format:
Index Number | Name & Description
---| ---
0 Type (See above)
1 & 2 | Coin Code (0x0006)
3 | Denominator
4,5,67 | Serial Number


Response Status Codes
```C
STATUS_SUCCESS = 250
ERROR_FEW_COINS_IN_LOCKER = 153,
ERROR_LOCKER_EMPTY_OR_NOT_EXISTS = 179,
ERROR_INVALID_PARAMETER = 198,

```


## PING Command
Command Group: 6

Command Code: 61

The PING service allows the client to create a session with the QMail server so that the QMail server can instantly  inform the user should the QMail server receive an email from the user. This service must always use TCP and not UDP to allow the timeout to last more than 2 minutes. The ping is a keep alive and must be reissued from time to time. 

The qmail sender will send their messages to many QMail servers at the same time. It is not necessary for all the QMail servers to push warning to the client. The client controls which QMail server should be the one that informs it of new messages. To reduce the amount of RAM needed by QMail servers to track sessions, the client should make a list of the four QMail servers that are closest to it (in milliseconds) and then choose from these QMail servers randomly to distribute the load. 

Sample Request:
```
CH CH CH CH CH CH CH CH CH CH CH CH CH CH CH CH // Challenge
SE SE SE SE SE SE SE SE SE SE SE SE SE SE SE SE // Session key
Send Qmail CBD File
PD PD PD ... ? // Padding to make all body bytes (except for the E3 E3 ) divisable by 32.
E3 E3 //Not encrypted
```

The client will then wait for the QMail server to send it a message:

Response Status Codes
```C
STATUS_YOU_GOT_MAIL = 11
STATUS_SESSION_TIMEOUT = 12
```
With this response, the client should call the PEEK Mail service. 

## PEEK Mail
Command Group: 6

Command Code: 62

The user must first log in to get a session key. 

After getting a session key, the user can download all the meta data up to a certain amount of data. See the [Meta Data CBD File Format](meta-file-format.md )

Sample Request:
```
CH CH CH CH CH CH CH CH CH CH CH CH CH CH CH CH // Challenge
SE SE SE SE SE SE SE SE SE SE SE SE SE SE SE SE // Session key
PD PD PD ... ? // Padding to make all body bytes (except for the E3 E3 ) divisable by 32.
E3 E3 //Not encrypted
```





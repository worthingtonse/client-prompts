# QMail Services
This coveres the servics that run on the Qmail servers for Phase I

Commands: 

[Upload](#upload)

[Tell](#tell)

[Peek](#peek)

[Download](#download)

[Ping](#ping)

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
| 0x0A | My Public File | File that others will be allowed to see about you. Usually avatar|
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


## UPLOAD
Command Group: 6  Command Code: 60 0x063C

Note that each file that is uploaded must have the same GUID but a different File Type/Index

These services generally use [Encryption Type 6](https://github.com/worthingtonse/client-prompts/blob/main/CONTEXT/request-header-format-for-256-bit-encryption.md#encryption-type-6) . However, if the QMail server is located on a RAIDA, it is possible that any encryption type could be used. Because off this, a key exchange must occure between the client and QMNail server before commands like this can be issued. 

Sample Request:
Note that everything is Big Endian
```
CH CH CH CH CH CH CH CH CH CH CH CH CH CH CH CH // Challenge
SE SE SE SE SE SE SE SE SE SE SE SE SE SE SE SE // Session ID
ID ID ID ID ID ID ID ID ID ID ID ID ID ID ID ID  // File Group GUID ( All zerors if not in a file group)
LC LC LC LC LC LC LC LC LC LC LC LC  // Locker Code. Payment to QMail server without four 0xFF (All zeros if empty)
RS RS  // 2 byes reserved for future use
FT // File Type (See table above)
SD // Storage Duration (See table above)
RS RS RS RS  // 4 byes reserved for future use
BL BL BL BL // Number of Bytes in the Data below (Big Endian)
BI BI BI BI ..... Binary File Data
E3 E3 //Not encrypted
```

## TELL 
Command Group: 6  Command Code: 61 0x063D

The Tell command is only sent to one QMail server that is registered as the user's Beacon server. A beacon server tells the user when they get mail. So, if a user is sending email out to 20 people, this TELL command must be sent to 20 different Beacon servers so each person can get the Tell. 

Tell, tells the RAIDA to inform all the address owners of the existance of a file (email) so they can peek at the meta information and download it. It does this by creating a .meta file in all the addressies Email folder. 
```c
CH CH CH CH CH CH CH CH CH CH CH CH CH CH CH CH // Challenge
SE SE SE SE SE SE SE SE SE SE SE SE SE SE SE SE // Session ID
ID ID ID ID ID ID ID ID ID ID ID ID ID ID ID ID  // Email's File Group GUID Should be same as file group for emails
LC LC LC LC LC LC LC LC LC LC LC LC  // Locker Code. Payment to QMail server without four 0xFF (All zeros if empty)
TS TS TS TS // Time stamp
TT // Tell Type. 0x00 for QMail sent
AC // Address count. The number of 8 bytes addresses that follow.
QM // QMail server Count. How many Qmail server information follows.
SJ // Bytes in Subject
AT // Number of attachments associated with the email. 
RS RS RS RS RS RS RS // 7 bytes reserved for future use. 
AD AD AD AD AD AD AD AD // Adddress (Address type, Coin Coin Type, Denomination, Serial Number)
ST ST ST ST ST ST ST ST ST ST ST ST ST ST ST ST // Qmail server information
ST ST ST ST ST ST ST ST ST ST ST ST ST ST ST ST
SJ SJ SJ SJ ... // The subject of the email // UTF-8
E3 E3 //Not encrypted
```
## Stripe Data
Index ID | Name & Description
---|---
0 & 1 | RAID Header
2 & 3 | QMail Server's port
4 to 17 | IP address (Last four are IPv4) 
18 to 31 | Reserved for future use and Phase II like verification?.  


### User Address Format:
Index Number | Name & Description
---| ---
0 Type (See below)
1 & 2 | Coin Code (0x0006)
3 | Denominator
4,5,6 & 7 | Serial Number

### Address Types
Code | Meaning
---|---
0x00 | Mass Mailer
0x01 | Verification Server (Where people can go to see if the email is verified. )
0x02 | To
0xCC | CC
0xBC | BCC



Response Status Codes
```C
STATUS_SUCCESS = 250
ERROR_FEW_COINS_IN_LOCKER = 153,
ERROR_LOCKER_EMPTY_OR_NOT_EXISTS = 179,
ERROR_INVALID_PARAMETER = 198,

```


## PING
Command Group: 6  Command Code: 62 0x063E

The PING service allows the client to create a session with the QMail server so that the QMail server can instantly  inform the user should the QMail server receive an email from the user. This service must always use TCP and not UDP to allow the timeout to last more than 2 minutes. The ping is a keep alive and must be reissued from time to time. 

The qmail sender will send their messages to many QMail servers at the same time. It is not necessary for all the QMail servers to push warning to the client. The client controls which QMail server should be the one that informs it of new messages. To reduce the amount of RAM needed by QMail servers to track sessions, the client should make a list of the four QMail servers that are closest to it (in milliseconds) and then choose from these QMail servers randomly to distribute the load. 

Sample Request:
```
CH CH CH CH CH CH CH CH CH CH CH CH CH CH CH CH // Challenge
SE SE SE SE SE SE SE SE SE SE SE SE SE SE SE SE // Session key
E3 E3 //Not encrypted
```

The client will then wait for the QMail server to send it a message:

Response Status Codes
```C
STATUS_YOU_GOT_MAIL = 11
PING_TIMEOUT = 12
STATUS_SESSION_TIMEOUT = 13
```
With this response, the client should call the PEEK Mail service. 

## PEEK Mail
Command Group: 6  Command Code: 63 0x063F

The user must first log in to get a session key. 

After getting a session key, the user can download all the meta data up to a certain amount of data. See the [Meta Data CBD File Format](meta-file-format.md )

Sample Request:
```
CH CH CH CH CH CH CH CH CH CH CH CH CH CH CH CH // Challenge
SE SE SE SE SE SE SE SE SE SE SE SE SE SE SE SE // Session key
DT DT DT DT // Date and Time since meta data was last checked. 
E3 E3 //Not encrypted
```

## DOWNLOAD FILE
Allows the user to go and get the file. There will probably be a limit to how many times a person can download a file. It will be genourse like ten times. The idea is the user needs to download it once per device. 

```c
CH CH CH CH CH CH CH CH CH CH CH CH CH CH CH CH // Challenge
SE SE SE SE SE SE SE SE SE SE SE SE SE SE SE SE // Session ID
ID ID ID ID ID ID ID ID ID ID ID ID ID ID ID ID  // Email's File Group GUID Should be same as file group for emails
FT // File Type
VS // Version (optional)
BP  // Byes per page (zero means the whole thing
PN  // Page number (Zero means first page)
E3 E3 //Not encrypted
```


Sample Response
```c
FT // File Type
VS // Version (optional)
BP  // Byes per page (zero means the whole thing
PN  // Page number (Zero means first page)
BL BL BL BL // How many bytes are in the response below:
BI BI BI .....
E3 E3 //Not encrypted
```

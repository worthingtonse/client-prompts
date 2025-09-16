## Distributed Resource Directory
1. The DRD allows users to post information about themselves so that others can find them. 
2. Users can get a user ID by obtaining a certicate that has their user id on it.
3. Users can get tickets by authenticating with RAIDA servers.
4. Users can give their tickets to a DRD server who will confirm that they are authentic with the RAIDA servers.
5. Authenticated Users can associate their user ID with data that they put into the DRD. 
6. Users can delete their entire record in the DRD or update it. 
7. DRD records are kept in a SQLight Databased on the DRD server
7. There should be no empty fields in the user's DRD records.
8. The DRD servers also contain files such as the user's avatar.
9. Everything in the DRD is public information.
10. The client may register the same information with multiple DRD servers for redundancy.
11. DRD servers may syncronize themselves. 
12. DRD Servers use the same request and response format as the raida.
13. DRD servers must exchange AES keys with the client computers using the Distributed Key Exchange protocol.
14. DRD servers communicate with clients using encryption type 6.
15. DRD servers use session keys.
16. DRD servers provide the following DRD Services:
   
[INSERT UPDATE DELETE DRD](#insert-update-delete-drd)

[SEARCH DIRECTORY](#search-directory)

## DRD's Entity Relationship Diagram
```mermaid
---
title: PHASE I DLD (Distributed Resource Directory)
---
erDiagram

    USER {
        int UserID PK "Coin ID, denomination and serial number"
        string PublicAlias "The client determines what they will be called"
        string PublicDescription "The client determines what is their description"
        string PathToAvatarFile "The public image file used by the user"
        int SendingPrice "The price the sender must pay for this user to receive"
        datetime StartDateTime "The time the user account was created"
    }

    SESSION {
        int SessionKey PK "The session key"
        int UserID "The expected UserID of the session"
        int MinuntesUntilTimeout "How many minutes before the session key timesout"
        datetime StartDateTime "The time the session started"
    }

    USER_MAILSERVER {
        int UserID FK "Denomination and Serial Number"
        int QMailID FK "Denomination and Serial Number"
    }

    MAILSERVER {
        int QMailID PK "Denomination and Serial Number"
        string PublicAlias "Name of QMail server"
        string PublicDescription "Description of server"
        string FQDN "DNS domain name"
        double flatFee "The denomination the MailServer charges to recieve an email from a sender"
        datetime FirstRegistrationDate "The day the record was created"
        datetime LastUpdateData "The datetime the records information was updated"
    }

    USER ||--o{ USER_MAILSERVER : "has"
    USER_MAILSERVER ||--o{ MAILSERVER : "contains"

```

##
```
/directory_root/
└── users/
    └── 000634FC89A4E6/
        ├── .avatar.png
        ├── devices/
        │   ├── D_A1B2C3D4.json
        │   └── D_E5F6G7H8.json
        └── policies/
            └── P_Default.json
```


## Insert Update Delete DRD

Sample Request:
```c
CH CH CH CH CH CH CH CH CH CH CH CH CH CH CH CH
SE SE SE SE SE SE SE SE SE SE SE SE SE SE SE SE
Update CBD file
E3 E3
```

Directory Update CBDF Fixed Fields: Note: All data is in binary. Strings are UTC-8 Encoded.
Key Code | Value Bytes | Name & Description
---|---|---
0 | 1 | Number of Key-value pairs
1 | 2 | Payment Coin Code. 0006 for Cloudcoin.
2 | 16 | Payment Locker Code
3 | varies (max 255)| "Display Name/Alias". Primary display name or chosen alias for the user encoded in UTF-8
4 | varies (max 255) | "Self Description" Public info about self
5 | 3 | Amount that senders must pay reciever. Coin type (2 bytes) and Denomination ( 0x0000  Cloudcoin by default)
6 | varies | Avatar file name
7 | varies (255x100)| Avatar file
10 | 8 | QMail[0] CT CT IP IP IP IP PT PT  // coin id, ip address, port
11 | 8 | QMail[1] CT CT IP IP IP IP PT PT  // coin id, ip address, port
12-40 | 8 | QMail[2-40] CT CT IP IP IP IP PT PT  // coin id, ip address, port
41 | 8 | QMail[31] CT CT IP IP IP IP PT PT  // coin id, ip address, port


Return Status Codes
```C
STATUS_SUCCESS = 250
ERROR_FEW_COINS_IN_LOCKER = 153,
ERROR_LOCKER_EMPTY_OR_NOT_EXISTS = 179,
ERROR_INVALID_PARAMETER = 198,
```

Nothing in Response Body
```
E3 E3
```

## Search Directory
This allows the user to search for a person in the directory. It will only warn people if they are blacklisted. 

```C
CH CH CH CH CH CH CH CH CH CH CH CH CH CH CH CH
SE SE SE SE SE SE SE SE SE SE SE SE SE SE SE SE
Search Directory CBDF
E3 E3
```
Directory Search CBDF
Directory Update CBDF Fixed Fields: Note: All data is in binary. Strings are UTC-8 Encoded.
Key Code | Value Bytes | Name & Description
---|---|---
0 | 1 | Number of Key-value pairs
1 | 2 | Payment Coin Code. 0006 for Cloudcoin.
2 | 16 | Payment Locker Code
3 | Varies | Return Key IDs (columns) One byte per resource in the Resource Table CDFD Key Table above in the Update Directory Service above. 
4 | 1 | Limit in KB.  
5 | 1 | Page. Default is 0
6 | 3 | Where Clause. Directory Key, Comparison Operator ( 0= Not Equal To, 1= Equal To, 2 = Greater than, 3 = Less Than, 4 = Contains, 5 = Does Not Contain), Number (0) or Text (1) field, Number or Text (length varies)
7 | 3 | AND Where Clause. Directory Key, Comparison Operator ( 0= Not Equal To, 1= Equal To, 2 = Greater than, 3 = Less Than, 4 = Contains, 5 = Does Not Contain), Number (0) or Text (1) field, Number or Text (length varies)
8 | 3 | OR Where Clause. Directory Key, Comparison Operator ( 0= Not Equal To, 1= Equal To, 2 = Greater than, 3 = Less Than, 4 = Contains, 5 = Does Not Contain), Number (0) or Text (1) field, Number or Text (length varies)

Response Status Codes
```C
STATUS_SUCCESS = 250
ERROR_FEW_COINS_IN_LOCKER = 153,
ERROR_LOCKER_EMPTY_OR_NOT_EXISTS = 179,
ERROR_INVALID_PARAMETER = 198,
ERROR_DATABASE_RETURNED_ZERO_RECORDS = 9,
ERROR_DATABASE_REPORTED_AN_ERROR = 10,
```

Response Body:
```C
CBDF File
E3 E3
```

Directory Search Results CBDF
Fixed Key | Bytes | Description
---|---|---
Number of rows returned| 2 | How many rows where returned up to 65,535.
Columns Per Row | 1 |  Up to 255|

Variable Fields. Note that in the case of it returning more than one row, we will see the IDs repeat.
The following shows three rows being returned: 
```
01 10 ca8d0787f2a84b4babf1ef9f3d118b16
02 0F 4b4babfca8d0787f2a81ef9f3d118b
06 03 1ef9f3
01 0E 4babf1ef9f3d11ca8d0787f2a84b
02 0E 81ef9f3d114b4babfca8d0787f2a
06 02 1ef9
01 10 ca8d0787f2a84b4babf1ef9f3d118b16
02 0F 4b4babfca8d0787f2a81ef9f3d118b
06 03 1ef9f3
```

ID | Field Name | Example | Description
---|---|---|---
1 |"Display Name/Alias" | Varies |"TechWizard" | Primary display name or chosen alias for the user encoded in UTF-8
2 |"Self Description" | Varies |"I'm a nice guy" | Public info about self
6 | Amount that senders must pay reciever | 0x0000v 08 | 3 bytes. Coin type (2 bytes) and Denomination ( 0x0000  Cloudcoin by default) Phase I will just use 0x00 which means 1. 
7 | Thumbnail Stripe| 00 00 18 77 Data  | Data Type (0 for thumbnaile) RAID type, Stripe number, Total Stripes, Data rounded to 100. Up to 
10 |"Email Server 0" | 00 00 8E 82 89 mail.server.com | Raida ID (0-255) First 2 Byte: Coin type, Three Bytes: Port Number, Variable Bytes: Server Name or IP max 250 bytes.
11 |"Email Server 11" | - - -  | There is a different ID for each raida that the receiver uses to receive.  
12 to 34| "Email server N" | - - -  | - - - 
35 |"Email Server 35" | 00 00 8E 82 89 mail2.server.com | First Byte: Coin type, Three Bytes: Port Number, Variable Bytes: Server Name or IP max 250 bytes



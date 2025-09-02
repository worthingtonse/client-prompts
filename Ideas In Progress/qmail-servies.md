@ QMail Services
This coveres the actual servics used by Qmail starting with Phase I

## Note about Compact Binary Document Format
Many of the QMail services use the the CBDF to reduce the size of the request to its minium. Here are the 
specifications of the CBDF: 

** Directory CBDF File Format **
| Field                     | Size (Bytes) | Description                                                                 |
|---------------------------|--------------|-----------------------------------------------------------------------------|
| Fixed Fields     | Depends on CBDF File   | This is a header that contains all the fields that are not optional and have a fixed length  |
| Number of Key-Value Pairs | 1            | Unsigned integer (0–255) indicating the number of key-value pairs that follow. |
| Key-Value Pair(s)         | Variable     | Repeated for each pair (as specified by Number of Key-Value Pairs):         |
| &nbsp;&nbsp;Key           | 1            | Unsigned integer (0–255) representing a predefined key (e.g., 0 = "name").  |
| &nbsp;&nbsp;Value Length  | 1            | Unsigned integer (0–255) specifying the length of the value in bytes.       |
| &nbsp;&nbsp;Value         | 0–255        | Binary data for the value (length as specified by Value Length).            |



## Update Director
This uploads information into the director. Every Raida has a compy of the directory so this is uploaded 25 different times. 
It isa whole file designed so everyone can see it. However, it does allow for some permissions. 

* Permissions. White list can see everything. Blacklist can see nothing, light gray list can see
* somethings, dark gray list can
* see less. 

The direcotry can be complicated so we use the Compact Binary Document Format. 

```C
CH CH CH CH CH CH CH CH CH CH CH CH CH CH CH CH
CBDF
E3 E3 //end of body
```

### Resource Key Table Version 0
This is for phase I. There is a much larger list available for phase II. 

Directory Update CBDF Fixed Fields:
Name | Bytes | Description
---|---|---
Resource Table Version | 1 | Allows for many different listed key tables (Default is zero) 

Note: All strings are UTC-8 Encoded.

** Resource Table Version 0 **
ID | Field Name | Example | Description
---|---|---|---
6 |Update Payment Coin Code | 1 | What coin is being used for payment (00 is CloudCoin)
3 | Update Payment Locker Code | ca8d0787f2a84b4babf1ef9f3d118b16 | Locker code for the payment type
3 |"Display Name/Alias" | Varies |"TechWizard" in binary | Primary display name or chosen alias for the user
3 |"Self Description" | Varies |"I'm a nice guy" | Public info about self
2 |"Memo to self" | Varies | This is not read by other people but allows the user to remember why they made updates to the Directory
0 | Allow User List | 00 A3 67 98 E6 72 | Don't need to pay. An array of coin type (Cloudcoin is zero), Denomination, Serial Number 
0 | Deny User List | 00 A3 67 98 E6 72 | Cannot Send. An array of coin type (Cloudcoin is zero), Denomination, Serial Number 
0 | Locker Code Payment for Receiving | 00 08 | 2 bytes. Coin type and Denomination
4 |"Email Server 0" |00 8E 82 89 mail.server.com& | First Byte: Coin type, Three Bytes: Port Number, Variable Bytes: FQDN. Ampersam seperates servers. 
4 | Thumbnail Stripe| 00 18 77 Data  | RAID type, Stripe number of Total Stripes. 




5 |"Acknowledgment Number"
6| "email guid"
7| "version"

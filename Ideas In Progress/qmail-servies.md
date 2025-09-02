@ QMail Services
This coveres the actual servics used by Qmail starting with Phase I


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

Directory CBDF File Format
| Field                     | Size (Bytes) | Description                                                                 |
|---------------------------|--------------|-----------------------------------------------------------------------------|
| Sender ID                   | 5            | Unique identifier for the user (binary-encoded, fixed length).              |
| Number of Key-Value Pairs | 1            | Unsigned integer (0–255) indicating the number of key-value pairs that follow. |
| Key-Value Pair(s)         | Variable     | Repeated for each pair (as specified by Number of Key-Value Pairs):         |
| &nbsp;&nbsp;Key           | 1            | Unsigned integer (0–255) representing a predefined key (e.g., 0 = "name").  |
| &nbsp;&nbsp;Value Length  | 1            | Unsigned integer (0–255) specifying the length of the value in bytes.       |
| &nbsp;&nbsp;Value         | 0–255        | Binary data for the value (length as specified by Value Length).            |


### Resource Key Table Version 0
This is for phase I. There is a much larger list available for phase II. 

ID | Field Name | Example | Description
---|---|---
1 | Resource Table Version | 0 | This is so there can be many different listed key tables. 
2 |"Memo to self" | Varies | This is not read by other people but allows the user to remember why they made updates. 
0 | Updated White List | 
4 |"Email Servers" |ca8d0787f2a84b4babf1ef9f3d118b16 | Pays the Directory server 1 Coin
3 |"Display Name/Alias" | Varies |"TechWizard" in binary | Primary display name or chosen alias for the user UT8- Encoded

5 |"Acknowledgment Number"
6| "email guid"
7| "version"

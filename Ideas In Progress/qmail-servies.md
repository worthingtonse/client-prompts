@ QMail Services
This coveres the actual servics used by Qmail starting with Phase I


## Update Director
This uploads information into the director. Every Raida has a compy of the directory so this is uploaded 25 different times. 
It isa whole file designed so everyone can see it. However, it does allow for some permissions. 

* Permissions. White list can see everything. Blacklist can see nothing, light gray list can see
* somethings, dark gray list can
* see less. 

The direcotry can be complicated so we use the Compact Binary Document Format. 

```json
CH CH CH CH CH CH CH CH CH CH CH CH CH CH CH CH
CBDF
E3 E3 //end of body
```

CBDF File Format
| Field                     | Size (Bytes) | Description                                                                 |
|---------------------------|--------------|-----------------------------------------------------------------------------|
| Sender ID                   | 5            | Unique identifier for the user (binary-encoded, fixed length).              |
| Number of Key-Value Pairs | 1            | Unsigned integer (0–255) indicating the number of key-value pairs that follow. |
| Key-Value Pair(s)         | Variable     | Repeated for each pair (as specified by Number of Key-Value Pairs):         |
| &nbsp;&nbsp;Key           | 1            | Unsigned integer (0–255) representing a predefined key (e.g., 0 = "name").  |
| &nbsp;&nbsp;Value Length  | 1            | Unsigned integer (0–255) specifying the length of the value in bytes.       |
| &nbsp;&nbsp;Value         | 0–255        | Binary data for the value (length as specified by Value Length).            |

Key Table

Key | Name
---|---
1: |"Memo to self"
2: |""
3: |"coin"
4: |"Acknowledgment Number"
5:| "email guid"
6:| "version"

# Qmail File Format

This is the actual qmail file. It uses the CBD (Compace Binary Document) format.

# Fixed part of file (Phase I)

Code | Bytes | Name & Description | Required?
---|---|---|---
0 | 1 | Number of Key Pairs | Required 
1 | 1 | version / formatting type | 0=plain text, 1 = Formatted Qmail CBD file (0 for Phase I| Required 
2 | varies | Message. The actuall text of the message UTF-8 | Required 

Phase I just has plain text messages. 

Sample Qmail CBD File (13 bytes total):
```javascript
0x00 0x01 0x03 // Key: Number of key pairs, Length of Value: one byte, Value: Three key pairs
0x01 0x01 0x00  // Key: Version, Length of Value: one byte, Value: Version 0
0x02 0x0B 0x48 0x65 0x6c 0x6c 0x6f 0x20 0x57 0x6f 0x72 0x6c 0x64   // Key: Message, Length of Value: 11, Value: Hello world
```
Qmail CBD File Shown as a Table:

Key | Length of Value | Value
---|---|---
0x00 | 0x01 | 0x03 
0x01 | 0x01 | 0x00  
0x02 | 0x0B | 0x48 0x65 0x6c 0x6c 0x6f 0x20 0x57 0x6f 0x72 0x6c 0x64  

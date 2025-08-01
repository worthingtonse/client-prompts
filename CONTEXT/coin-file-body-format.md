# File Format for Binary Files

## Coin Header
Each coin in the file has a header made up of 7 bytes. 

Index | Name | Allowable Values | Description
---|---|---|---
0 | Split | 0 | For future use if splits are implemented
1 |Shard | 0 | For future use if shards are implemented
2 | Denomination | -8 to +11 inclusive | The binary version of the denominations. See [Denominations](denominations.md)
3-6 | Serial Number | Any four bytes | Used together with the denomination to identify the coin. 

## Coin Body

Rules:

Condition | Bytes | explanation
---|---|---
Always | 400  | 25 GUIDs. 16 bytes per GUID (The original ANs before the call)
If Has PANs set to 1 (byte 16 of the file header) | +400 | The PANs that were sent to the server but no reply
If the Coin is the last coin | + Padding  | Add random bytes to make the entire coin body divisable by 32. The number of coins in the file is in the File Header (bytes 24-27)

<!--
If Coin Type is NFT | +128 | Add 128 Fixed Bytes for the file's Title.
If Coin Type is NFT | +128 | Add 128 Fixed Bytes for the file's Meta Information.
If Coin Type is NFT | + The File Size | The Variable bytes of the file
-->


Sample Coin Body:
```c
SP SH DN SN SN SN SN // Header for first coin
AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN  AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN  AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN   
AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN  AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN  AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN  
AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN  AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN  AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN  
AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN  AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN  AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN  
AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN  AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN  AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN  
AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN  AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN  AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN  
AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN  AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN  AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN  
AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN  AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN  AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN  
AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN
SP SH DN SN SN SN SN // Header for second coin
AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN  AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN  AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN   
AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN  AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN  AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN  
AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN  AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN  AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN  
AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN  AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN  AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN  
AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN  AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN  AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN  
AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN  AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN  AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN  
AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN  AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN  AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN  
AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN  AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN  AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN  
AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN  
PD PD PD PD PD PD PD PD PD // Padding for whole body 
```

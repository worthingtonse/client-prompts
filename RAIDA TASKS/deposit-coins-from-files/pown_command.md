# Authentication Services (Command Group 1)

These services check the authenticty of tokens and allow change of ownership.

Key Terms: 

AN: Authenticity Number. A 16 byte password that they coin has. Usually shown as 32 hexidecimal characters. 

SN: Serial Number. Every coin has a unique 4 byte serial number .

PAN or PN: Proposed Authenticity Number. The new AN that the client wants to repace the old AN with. 

POWN: Password Own. To ask the RAIDA to change the AN to the PAN.

Fracked: When a coin has one or more RAIDA that think it is counterfeit but more than 13 that think it is authentic. 

Command Group | Command Code | Service  | Description
---|--- | --- |---
1|20 | [Pown](#pown)| Changes AN 

## Code meanings
Code | Meaning | Sample in HEX | Description
---|---|---|---
RD | Random | 6 | A random byte
DN | Denomination | 1 | A denomination code (See Request Header Denominations)
SN | Serial Number | FFFFFFFF | Four bytes of serial numbers
AN | Authenticity Number | F5DD153926DA42E8A062A915AD763DF0 | The token's password
PN | Proposed Authenticity Number | 6A3C3E384566483A9EE629D6BB38BCB9 | The new password
CH | Challenge | 84566483A9EE629D6BB38BCB96A3C3E3 | A random number that they RAIDA unencrypt 

# POWN 
POwn means "Password Own". The client sends the Serial Number, Authenticity Number and the Proposed Authenticity Number. The AN and PAN must be different or an error 
will be returned with a status that the ANs and PANs matched. The server checks to see if the AN that the client sent matches the AN in the table.
If it matches, the AN in the table is replaced with the PAN provided by the client and the "pass" status is returned. 
If multiple tokens are sent then the server may return "all pass" or "all fail" status. 
If some of the tokens are found authentic and some are found counterfeit, then the "mixed" status is returned along with a bitfield. 
The bitfield has one bit per token. A bit set to '1' is a pass and each bit set to '0' is a fail. Zeros are padded to the byte. 
Since the server only returns whole bytes, the client must know when to stop reading the bitfield based on how many tokens were sent.

Like all services, the pown allows the client to send a 16 byte challenge. 
The server returns the first four bytes of an MD5 hash of this challenge in the response header. 
This allows the client to be certain that the response came from the RAIDA since only the RAIDA would be able to decrypt the challenge.

REQUEST: DN (Denomination) is one byte. SN(Serial Number) is 4 bytes
```hex
CH CH CH CH CH CH CH CH CH CH CH CH CH CH CH CH
DN  SN SN SN SN  AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN  PN PN PN PN PN PN PN PN PN PN PN PN PN PN PN PN
DN  SN SN SN SN  AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN  PN PN PN PN PN PN PN PN PN PN PN PN PN PN PN PN
DN  SN SN SN SN  AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN  PN PN PN PN PN PN PN PN PN PN PN PN PN PN PN PN 
DN  SN SN SN SN  AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN  PN PN PN PN PN PN PN PN PN PN PN PN PN PN PN PN
3E 3E  //Not Encrypted
```
Reponse body if all passed | Reponse body if all failed: | Response body if mixed with passes and fails:
---|---|---
no response body | no response body | MT MT MT MT MS  //The MT are just zeros. 0x00 00 00 00. They are for future use in case we want to return master tickets.

MS means Mixed Status. Each bit returned represents the status of one token. If the bit is a zero then that token has failed. If the bit is a 1 then that token is authentic. 

Response Status | Code
---|---
All Pass | 241
All Fail | 242
Mixed | 243


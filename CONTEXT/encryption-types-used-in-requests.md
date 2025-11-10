# Encryption Types used in the Request Headers

### ENCRYPTION RULES All SERVICES
To make if more difficult for quantum computers to know when they have decrypted a Request Body, the Request Headers are not encrypted. Padding must often be added to the end of a body (before the terminating bytes) to make the body encryptable. Most documentation leaves this padding out of the protocol description but it should be there. Newer descriptions show the padding. 

## Encryption rules about different parts of the request:

Request Part | Encryption Rules | Length in bytes
---|---|---
 Request Headers | Not encrypted | 32 bytes if body uses encryption type 0,1,2 or 3. Encryptoin type 4 and above use 64 bytes fixed. Includes the ID's of shared secret
 Request Bodies | Encrypted using the shared secret identified in thje request header | Varries but padded to be divisable by 16 if using encryption type 1,2 or 3. Padded to 32 bytes if encryption type 4 and above. No padding if encryption type 0. 
 Terminating Bytes | Not encrypted. | 2 bytes (0xE3E3 ) Magic numbers.   

## ENCRYPTION
Code | Type | Description | Bytes after EN
---|---|-----|---
0 | No encryption | Clear Text | Bytes 17 to 21 in the request header are zeros
1 | 128 bit AES CTR | Shared Secret |   Byte at index 17 in the request header is the Denomination (DN) and bytes 18,19,20 and 21 are the serial number (SN)
2 | 128 bit AES CTR | Uses Locker Code for encryption | Byte 17 to 21 in the request header are the first five bytes in the locker code. Used mostly by the PEEK command that is in command group 8, command code 84.
3 | 128 AES CTR | RAIDA Key Exchange | Allows RAIDA's to exchange keys. Bytes 17 through 21 of the header are the key ID shared between the RAIDA and other RAIDAs.
4 | 256 bit AES CTR | Shared Secret | Just like Encryption type 2 except uses a 256 bit key. This changes the Request Header size from 32 bytes to 48 bytes fixed. Primarily used for client - server communication. 
5 | 256 bit AES CTR | Double Key | Bytes 24, 25, 26, 27 and 28 are used to identify a second key (DN,SN,SN,SN,SN) as well as be part of the nounce. Byte 24 is the denomination of the second key and bytes 25 though 28 are the four byte serial number of the second key. 
6 | 256 bit AES CTR  | RAIDA Key Exchange + Session Keys | Uses 256-bit session keys from RAIDA Key Exchange. Header is 32 bytes. Bytes 1–2 = body length, 3–7 = session key ID, 8–31 bytes 8-31 are 24-byte nonce field. Designed for secure client-server tunnels with persistent session key storage.     
7 | 256 bit AES CTR | RAIDA Key | Bytes 17 is the sending RAIDA. Bytes 18, 19, 20 and 21 are the shared RAIDA Key ID|


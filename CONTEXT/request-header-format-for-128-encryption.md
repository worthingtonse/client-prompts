# Second 16 Bytes of the Request Headers For 128 Bit AES Encryption. 
This specification is for when the client is sending requests encrypted in 128 bit AES. 

# Encryption Type 1, 2 and 3
Encryption types 1, 2 and 3 have the same structure. The only thing that is different is how the numbers are calculated for the bytes in 17 through 21 (inclusive)

```mermaid
---
title: "RAIDA Protocol Header 128 bit Encryption"
---
packet-beta
+8: "Encryption Type EN"
+8: "Denomination DN"
+32: "Serial No"
+16: "Body Length including two terminating bytes"
+64: "Nounce"
```


### Request Header Byte by Byte Code Meanings

Index | Group | Code | Name | Notes
---|---|---|---|---
16 | Encryption | EN  | [Encryption](https://github.com/worthingtonse/client-prompts/blob/main/CONTEXT/encryption-types-used-in-requests.md) Type  |  0x00 means no encryption. See encryption codes table.
17 | Encryption | DE | [Denomination](https://github.com/worthingtonse/client-prompts/blob/main/CONTEXT/denominations.md) | Denomination of the token used to encrypt the request body.
18 | Encryption | SN | Encryption token SN 0| Serial Number of the token used to encrypt the body. HOB
19 | Encryption | SN |  Encryption token SN 1 | 2nd Highest Order Byte
20 | Encryption | SN |  Encryption token SN 2 |  
21 | Encryption | SN |  Encryption token SN 3| Lowest Order Byte
22 | Encryption | BL u16| Body Length | Length in bytes of the entire body including the last 2 terminating bytes. 
23 | Encryption | BL u16| Body Length| LOB. if more than 65,535 bytes are sent, then bytes 22 and 23 will be FF FF and bytes 24, 25, 26 and 27 will be the body length. 
24 | Nonce | NO |  Nonce 0 | The nonce used in the encryption and should never be used twice. 
25 | Nonce | NO |  Nonce 1 | 
26 | Nonce | NO |  Nonce 2 |
27 | Nonce | NO |  Nonce 3 | 
28 | Nonce | NO |  Nonce 4 | 
29 | Nonce | NO |  Nonce 5 | 
30 | Nonce | NO |  Nonce 6 / Echo 0 | Serves two purposes. These bytes are always echoed back to the client.
31 | Nonce | NO |  Nonce 7 / Echo 1 | 

* Nounce can do two jobs. Bytes 30, 31 are used as an Echo also.
* The nounce is also a challenge. The RKE (RAIDA Key Exchange) server must decrypt this and place it in the response if RKE is enabled. 


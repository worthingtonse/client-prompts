# POWN String Codes

POWN (Password Ownership) codes are used throughout the CloudCoin client and server software to make it possible to track the status of coins. These codes can be expressed as strings of characters like "ppuppppfpppeppppppnppbpep" or in four bit binary such as here shown as hex "AA 0A AA AF AA AA AA AA AA CA AB AE A3". The last four bits are ignored and can be anything. 

After a coin is sent to the 25 Raidas to be checked for authenticty, there will idealy be 25 responses. To keep track of these responses we have a POWN string.
POWN means Password Own. 

These codes are placed in coin files that have only one coin in them. Otherwise, the motto is used instead of the pown string. 

##  Pown String In Files with Many Coins
If a coin file has more than one coin in it, there will be no pown string, task ID or experimental bytes. Instead, 
CloudCoin's moto will be used instead. The motto is "Live Free or Die".

Live free or die translates to hex: "4C 69 76 65 20 46 72 65 65 20 4F 72 20 44 69 65" in ASCII.

## Pown String with only one Coin
If a coin file only has one coin in it, it is probably because the coin file is inside of a program and the status of the coin needs to be tracked. There are
25 status codes that each require four bits. These are encoded into hexidecimal numbers that are easy to understand by the naked eye. 

Character Code | Hex Code | Name | Meaning 
---|---|---|---
u |0x0 | Untried   | The raida failed to return an echo request so the client did not send that raida a pown request.
p | 0xA | Pass/Authentic | The raida responded that the coin was authentic. 
b | 0xB | Broke Encryption Key | The raida could not decrypt the request because the encryption key was not authentic.  
n | 0xC | No Reply/Clock Timeout | The raida did not respond in the expected timeframe. This is usally caused by lost packets while using the UPD protocol.
e | 0xE | Error |The raida responded with an error. Could be an issue with the RAIDA software. 
f | 0xF | Failed/Counterfiet |The raida responded that the coin was counterfeit. 



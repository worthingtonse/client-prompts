# POWN (Password Own) String Codes

After a coin is sent to the 25 Raidas to be checked for authenticty, there will idealy be 25 responses. To keep track of these responses we have a POWN string. These codes can be either in binary or as strings. 

These codes are placed in coin files that have only one coin in them. Otherwise, the motto is used instead of the pown string. 

These codes are also placed in receit files and are returned through API calls. 

##  Pown String In Binary Coin Files 
If a coin file has more than one coin in it, there will be no pown string, task ID or experimental bytes. Instead, 
CloudCoin's moto will be used instead. The motto is "Live Free or Die".

Live free or die translates to hex: "4C 69 76 65 20 46 72 65 65 20 4F 72 20 44 69 65" in ASCII.

If a coin file only has one coin in it, it is probably because the coin file is inside of a program and the status of the coin needs to be tracked. There are
25 status codes that each require four bits. These are encoded into hexidecimal numbers that are easy to understand by the naked eye. 

String | Binary | Name | Meaning 
--|---|---|---
U | 0x0 | Untried   | The client did not send that raida a pown request because an earlier echo request showed that the raida was not reachable.
P | 0xA | Authentic/Pass | The raida responded that the coin was authentic. 
B | 0xB | Broke Encryption Key | The raida could not decrypt the request because the encryption key that was used was not authentic.  
N | 0xC | Clock Timeout/No Response | The raida did not respond in the expected timeframe. This is usally caused by lost packets while using the UPD protocol, a workplace firewall blocking outgoing traffic or network issues like a roaming cell phone. 
E | 0xE | Error |The raida responded with an error. Could be an issue with the RAIDA software. 
F | 0xF | Failed |The raida responded that the coin was counterfeit. 





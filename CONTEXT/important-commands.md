# Command Groups and Commands
Each request to the raida will cointain two bytes (index 4 and 5) that describe the command group code and a command code. 
The purpose of these is to tell the raida how to treat the request. 


## ESSENTIAL COMMAND CODES
Each command is made up of two bytes. The first byte is sometimes called the command group. 
                                   
Command Group & Code (Hex) | Group Name | Command | Description
---|---|---|---
0x0000 | Status | 🟢echo | Sends a request for a response.
0x0003 | Status | count | Shows how many coins are in the RAIDA
0x010a | Authentication | 🟢detect | Compares authenticity numbers but does not change them.
0x010b | Authentication | 🟢detect-by-sum | Compares authenticity numbers by adding them all together. Does not change them.
0x0114 | Authentication | 🟢p-own | Password Own. Changes ANs (Authenticity Numbers) with PANs (Proposed Authenticity Numbers). 
0x0115 | Authentication | 🟢p-by-sum | Checks the sums of all ANs sent at once and changes them if good.
0x0228 | Healing | 🟢get-ticket | Returns proof that the tokens are good. 
0x0232 | Healing | validate-ticket | raida checks to see if another raida's ticket is valid. 
0x023c | Healing | find | Checks last two ANs to see if there is a match. 
0x0250 | Healing | 🟢fix | Accepts a bunch of tickets to ensure they are good.
0x042c | Key Exchange | Encrypt Ticket | Returns an encrypted key part that can be used as a shared secret. 
0x042d | Key Exchange | Fix Encryption | Accepts tickets from many RAIDA to created a shared secret from many "key parts". 
0x0852 | Locker | put | Puts token in a locker that can be opened by a key.
0x0853 | Locker | peek | See what coins are in a locker
0x0854 | Locker | remove | Removes tokens from locker and destroys locker.
0x095b | Change | 🟢get-available-sns | Asks the RAIDA what SNs are available for use. 
0x095c | Change | break | Breaks token into ten smaller tokens. 
0x095d | Change | join | Joins smaller tokens into one larger token.


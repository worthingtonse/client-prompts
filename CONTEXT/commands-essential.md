# Command Groups and Commands
Each request to the raida will cointain a command group code and a command code. The purpose of these is to tell the raida how to treat the request. 

## COMMAND GROUPS
The Command Group is a way of grouping commands that are simular in nature. This gives us the ability to have large amounts of commands. 
The Command Groups are numbered 0 to 255 and taken from byte 9 of the request header. 

Code | Name | Description
--- | --- | ---
0 | Status | Status, Errors that have nothing to do with commands but usually with headers
1 | Authentication | Services that authenticate tokens.
2 | Healing | Services that make all RAIDA agree on the authenticity of tokens.
4 | Key Exchange | Service that exchange cryptographic keys with other machines
8 | Locker Services | Services that place and retrieve tokens from "RAIDA Lockers."
9 | Money Changing | Breaks 100s into 10s or joins 10s to make 100s. Works with all monetary denominations.

## COMMAND CODES
Each Command Group has its own command code. However, in an attempt to make things less confusing, each command has a seperate command number. This will work
until we have more than 255 commands. 

Group ID | Group Name | Command Code (Decimal) | Command | Description
---|--- | --- | --- |---
0 | Status |00 |  echo | Sends a request for a response.
0 | Status |03 | count | Shows how many coins are in the RAIDA
1 | Authentication | 10 |  detect | Compares authenticity numbers but does not change them.
1 | Authentication | 11 |  detect-by-sum | Compares authenticity numbers by adding them all together. Does not change them.
1 | Authentication | 20 | p-own | Password Own. Changes ANs (Authenticity Numbers) with PANs (Proposed Authenticity Numbers). 
1 | Authentication | 21 | p-by-sum | Checks the sums of all ANs sent at once and changes them if good.
2 | Healing |  40 | get-ticket | Returns proof that the tokens are good. 
2 | Healing | 50 | validate-ticket | raida checks to see if another raida's ticket is valid. 
2 | Healing | 60 |find|  Checks last two ANs to see if there is a match. 
2 | Healing | 80 | fix | Accepts a bunch of tickets to ensure they are good.
4 | Key Exchange |44 | Encrypt Ticket | Returns an encrypted key part that can be used as a shared secret. 
4 | Key Exchange |45 | Fix Encryption | Accepts tickets from many RAIDA to created a shared secret from many "key parts". 
8 | Locker | 82 | put | Puts token in a locker that can be opened by a key.
8 | Locker | 83 | peek | See what coins are in a locker
8 | Locker | 84 | remove | Removes tokens from locker and destroys locker.
9 | Change | 91 | get-available-sns | Asks the RAIDA what SNs are available for use. 
9 | Change | 92 | break | Breaks token into ten smaller tokens. 
9 | Change | 93 | join | Joins smaller tokens into one larger token. 


Code | Name | Description
--- | --- | ---
0 | Status | Status, Errors that have nothing to do with commands but usually with headers
6 | Messaging | QMail, QTXT, QChat, QCalendar, QTasks, etc
12 | RPC | Allows people to send command to other servers. 
13 | File System | Allows people to store files on the raida. 
18 | DRD |Distributed Resource Director


Phase II
Group ID | Group Name | Command Code (Decimal) | Command | Description
---|--- | --- | --- |---
4 | Key Exchange | 41 | post | Puts a key on the raida
4 | Key Exchange | 43 | get | downloads a key from the raida. 
6 | Chat | 60 | Send Mail
6 | Chat | 61 | PING (Used so the client can receive push requests from the QMail servers)
6 | Chat | 62 | Get Meta
6 | Chat | 63 | Get File
12 | RPC | 120 | nslookup | issues the nslookp command on the raida and returns the results to the client 
13 | Files | 134 | Put Object | Uploads a file
13 | Files | 135 | Get Object | Downloads a file
13 | Files | 136 | Remove Object | Deletes a file
18 | DRD | 180 | Create, Update and Delete Directory User Listing
18 | DRD | 181 | Search Directory
18 | DRD | 182 | List User's Mail Servers
18 | DRD | 183 | Read User's Avatar
18 | DRD | 184 | Create, Update and Delete Directory QMail server Listing
18 | DRD | 185 | Create, Update and Delete Directory RAIDA server Listing
18 | DRD | 186 | Create, Update and Delete Directory DLD server Listing
18 | DRD | 187 | Create, Update and Delete Directory DKE server Listing


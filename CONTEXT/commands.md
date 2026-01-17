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
3 | Administration | Services that add or subtrack tokens from the raida.
4 | Key Exchange | Service that exchange cryptographic keys with other machines
5 | Banking | Services that store money for people
6 | Messaging | QMail, QTXT, QChat, QCalendar, QTasks, etc
7 | Blockchain | Services that allow people to make changes to the raida blockchain
8 | Locker Services | Services that place and retrieve tokens from "RAIDA Lockers."
9 | Money Changing | Breaks 100s into 10s or joins 10s to make 100s. Works with all monetary denominations.
10 | Sharding | Allow people to move coins from one raida to another. 
11 | Swap | Services that allow people to change CloudCoin to Bitcoin or another currency
12 | RPC | Allows people to send command to other servers. 
13 | File System | Allows people to store files on the raida. 
15 | DKE | Distributed Key Exchange
18 | DRD |Distributed Resource Director



## COMMAND CODES
Each Command Group has its own command code. However, in an attempt to make things less confusing, each command has a seperate command number. This will work
until we have more than 255 commands. 

🟥 Means the service may not be implemented

Group ID | Group Name | Command Code (Decimal) | Command | Description
---|--- | --- | --- |---
0 | Status |00 |  echo | Sends a request for a response.
0 | Status |01 | version | Returns the version of the RAIDA Software
0 |Status |02 | show-stats | Shows information about requests to the RAIDA
0 | Status |03 | count | Shows how many coins are in the RAIDA
1 | Authentication | 10 |  detect | Compares authenticity numbers but does not change them.
1 | Authentication | 11 |  detect-by-sum | Compares authenticity numbers by adding them all together. Does not change them.
1 | Authentication | 20 | p-own | Password Own. Changes ANs (Authenticity Numbers) with PANs (Proposed Authenticity Numbers). 
1 | Authentication | 21 | p-by-sum | Checks the sums of all ANs sent at once and changes them if good.
2 | Healing |  40 | get-ticket | Returns proof that the tokens are good. 
2 | Healing | 50 | validate-ticket | raida checks to see if another raida's ticket is valid. 
2 | Healing | 60 |find|  Checks last two ANs to see if there is a match. 
2 | Healing | 80 | fix | Accepts a bunch of tickets to ensure they are good.
🟥2 |Healing | 51  | get-ticket by Sum | Returns proof that the tokens are good based on a sum of ANs. 
4 |Healing |  44 | get-encryption-ticket | Returns proof that the tokens are good. 
4 |Healing |  45 | fix-encryption-key | Returns proof that the tokens are good based on a sum of ANs. 
3 | Treasury | 120 | Get Available SNs| Shows available serial numbers. 
3 | Treasury |130 | Create tokens| Adds more tokens to the total tokens on the RAIDA.
3 | Treasury |140 | Delete tokens| Removes tokens from the RAIDA.
3 | Treasury |150 | Unfreeze coins | Frees coins that are locked. Tells RAIDA to release lock on reserved SNs. 
🟥3 | Treasury | 151 | Set Fee for Swaps | Allows Treasure to set the fee swap rate 
🟥?3 | Treasury |160 | Get All SNs | Allows RAIDA to syncronize their serial numbers. 
4 | Key Exchange | 41 | post | Puts a key on the raida
🟥4 | Key Exchange | 42 | key alert | tells another machine that there is a key on the raida for it. 
4 | Key Exchange | 43 | get | downloads a key from the raida. 
4 | Key Exchange |44 | Encrypt Ticket | Returns an encrypted key part that can be used as a shared secret. 
4 | Key Exchange |45 | Fix Encryption | Accepts tickets from many RAIDA to created a shared secret from many "key parts". 
6 | Chat | 60 | Send Mail
6 | Chat | 61 | PING (Used so the client can receive push requests from the QMail servers)
6 | Chat | 62 | Get Meta
6 | Chat | 63 | Get File
8 | Locker | 81 | peek-for-sale | Shows what coins are for sale in a sales locker
8 | Locker | 82 | put | Puts token in a locker that can be opened by a key.
8 | Locker | 83 | peek | See what coins are in a locker
8 | Locker | 84 | remove | Removes tokens from locker and destroys locker.
8 | Locker | 85 | put-for-sales | puts coins in a sales locker so they can be sold
8 | Locker | 86 | lockers-for-sale | returns lockers for sale
8 | Locker | 87 | buy | Allows purchasing crypto with cloudcoin
8 | Locker | 88 | put-muli-sum |Allows a person to create many lockers
8 | Locker | 89 | remove=locker-for-sale| Remove coins from a sales locker
9 | Change | 91 | get-available-sns | Asks the RAIDA what SNs are available for use. 
9 | Change | 92 | break | Breaks token into ten smaller tokens. 
9 | Change | 93 | join | Joins smaller tokens into one larger token. 
10 | Shard | 170 | Switch  |Move coins to another raida
10 | Shard | 171 | pickup | People can get new coins that were switched from old ones.
10 | Shard | 172 | get-sns | See what serial numbers are available for swithing
10 | Shard | 173 | rollback | Rollback a switch if something goes wrong
10 | Shard | 174 | switch-sum |switch that has a smaller footprint
11 | Swap | 110 | reserve | reserves a locker for the caller so radia can put coins in it after swap
11 | Swap | 111 | check| checks a depository
11 | Swap | 112 | withdaw | withdraws coins from a depository
11 | Swap | 114 | rate | the exchange rate 
12 | RPC | 120 | nslookup | issues the nslookp command on the raida and returns the results to the client 
🟥13 | Files | 101 | Create Folder | Creates a folder on the RAIDA
🟥13 | Files | 102 | Show Folder Contents | Shows list of files and folders
🟥13 | Files | 103 | Remove Folder | Removes a folder
13 | Files | 134 | Put Object | Uploads a file
13 | Files | 135 | Get Object | Downloads a file
13 | Files | 136 | Remove Object | Deletes a file
🟥13 | Files | 107 | Show Any Folder Contents | Used by KYC officers to see list of files
🟥13 | Files | 108 | Get Any Object | Used by KYC officers to see files
15 | DKE | 1 | Upload Master Secret (Content Server)
15 | DKE | 2 | Get Key Parts (Client)
18 | DRD | 180 | Create, Update and Delete Directory User Listing
18 | DRD | 181 | Search Directory
18 | DRD | 182 | List User's Mail Servers
18 | DRD | 183 | Read User's Avatar
18 | DRD | 184 | Create, Update and Delete Directory QMail server Listing
18 | DRD | 185 | Create, Update and Delete Directory RAIDA server Listing
18 | DRD | 186 | Create, Update and Delete Directory DLD server Listing
18 | DRD | 187 | Create, Update and Delete Directory DKE server Listing






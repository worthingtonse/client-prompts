# QMail Format For Phase I
The QMail is made up of three parts. Each part seperatd by the FS control character (ASCII 28 0x1C). FS means File Seperator

## Hello World QMail
The following is an actual qmail file consisting of three files (Meta, Styles, Markup Text)
```c
06 The number of key/value pairs in the meta file (#6)
01 ▪ 10 ▪ BF 7B 94 B3 91 A2 46 B5 8E 48 54 5D D8 F1 31 01   // Key 1(Email GUID) Value Length: 16. Value: GUID)
02 ▪ 0B ▪ 49 20 6C 6F 76 65 20 79 6F 75 21  // KeyID: 2(Subject Text) Value Length: 11 Value: "I love you!"
0B ▪ 01 ▪ 04 //KeyID: 12( Number of Attachments) Value Length: 1. Value: 4 attachments
0D ▪ 0E ▪ {{ 00 06, 02, 00 02 3F 98 },{ 00 06, 02, 00 04 67 2E }} // KeyID: 13(To Array) Value Length: 14. Value: Two mailbox IDs {{6,2,147352},{6,2,288558}} 
FF ▪ 04 ▪ 68 CF B6 AD  // KeyID: 255(Timestamp) Value Length: 4. Value: 1758443181 = "Sunday, September 21, 2025 8:26:21 AM"
13 ▪ 07 ▪ 00 06  02  03 E8 78 A0 // KeyID: 19(From Mailbox) Value Length: 7. Coin Code 00 06: CloudCoin, Denomination 02: 100cc, Serial Number 03 E8 78 A0: 65566880
1C  // End of Meta Data. Start of Styles Tables 
    // No Style Tables for Phase I. Client will use its default style. 
1C  // Start of Markup. End of the Styles Tables
01  // Next byte will be the status code. Defaults to zero. See Status Code Table below 
00  // Print status message 0 that says "Program: Waiting for your command to download this qmail's content"
02  // Start of text
48 65 6C 6C 6F 20 57 6F 72 6C 64 21 // These 12 bytes encode "Hello World!"
```

## Overall Structure
This is the structure of a QMail file for Phase I that is just for sending a text message

| Control Character | Name | Meaning | Description |
|---|---|---|---|
|n/a| [Meta Data File](meta-file.md)| This is seperat file|Concatinated to the next character |
|FS| File Seperator |ASCII 0x1C| The first FS begins the styles tables |
|FS| File Seperator |ASCII 0x1C| The Second FS begins the formatted text of the qmail |
|SOH| Start of Status |ASCII 0x01| Shows the status of the email (See Status Table)|
|STX| Start of Text |ASCII 0x02| Email Text |

## Meta Data Key Table
These are the ones available for Phase I but many optional 
| Key ID | Name | Size | Description | (Required) Δ(Added by Raida) Σ(Added by user) | Phase |
|---|---|---|---|---|---|
| 1 | Qmail ID | 16 | The GUID the sender assigned to this email | * | 1 |
| 2 | Subject | 1 | The UTF-8 encoded text of the subject line  | | 1 |
| 12| "Number of Attachments" | 1 | How many files are associated with the qmail. Limit 255| Δ | 2 |
| 13| "To Array" | 2 | An array of "To:" 7 byte mailbox addresses. | Δ| 1 |
| 14| "CC Array" | 2 | An array of "CC:" 7 byte mailbox addresses | Δ| 1 |
| 19| "From Mailbox" | 1| Cloudcoin (0x0006), Denomination (1 byte), Serial Number (4 bytes)| | 1 |
| 250 | "Timestamp" | 4 | Description to come | * | 1 |



## Status Table
While the email is loading, there will be a status bar on the top of the email that changes as the email is downloaded. 
People will first download the Meta file. The Style Tables and Marked up. The default status is "Waiting for download command" 
that shows the user that they are just looking at the downloaded meta data but the actual email is not downloading. 

Status Code | Text encoded as UTF-8
---|---
0 | Program: Waiting for your command to download this qmail's content
1 | Program: Decrypting qmail stripes
2 | Program: Assembling qmail file stripes
3 | Program: Recovering corrupted stripe
4 | QKey: Resolving QMail Servers' Key Exchange Server's IP addresses and port numbers
5 | QKey: Contacting Servers to exchange quantum safe keys
6 | RAIDA: Echoing Servers
7 | RAIDA: Checking Encryption Keys
8 | RAIDA: Getting Kerberose Tickets
9 | RAIDA: Repairing Encryption Keys
10 | RAIDA: Fixing Mailbox Certificate
11 | Qmail: Echoing Mail Servers
12 | QMail: Creating sessions
13 | QMail: Resolving QMail Servers' IP addresses and port numbers
14 | QMail: Exchanging keys with servers
15 | QMail: Creating Sessions
16 | QMail: Pinging servers
17 | QMail: Downloading qmail file
18 | QMail: Downloading User's Avatar
19 | QMail: Downloading 1st attachment
20 | QMail: Downloading 2nd attachment
21 | QMail: Downloading 3rd attachment
22 | QMail: Downloading 4th attachment
23 | QMail: Downloading 5th attachment
24 | QMail: Downloading 6th attachment
25 | QMail: Downloading 7th attachment
26 | QMail: Downloading 8th attachment
27 | QMail: Downloading 9th attachment
28 | QMail: Downloading 10th attachment
29 | QMail: Downloading another attachment
30 | QMail: Downloading last attachment
31 | QMail: Finnished downloading qmail with data loss
32 | QMail: Finnished downloading qmail with no errors
33 | QMail: Finnished downloading attachments with data loss.
34 | QMail: Finnished downloading qmail with no errors
35 | Total download progress: 00% ⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
36 | Total download progress: 00% 🡇⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
37 | Total download progress: 05% ⬛🡇⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
38 | Total download progress: 10% ⬛⬛🡇⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
39 | Total download progress: 15% ⬛⬛⬛🡇⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
40 | Total download progress: 20% ⬛⬛⬛⬛🡇⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
41 | Total download progress: 25% ⬛⬛⬛⬛⬛🡇⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
42 | Total download progress: 30% ⬛⬛⬛⬛⬛⬛🡇⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
43 | Total download progress: 35% ⬛⬛⬛⬛⬛⬛⬛🡇⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
44 | Total download progress: 40% ⬛⬛⬛⬛⬛⬛⬛⬛🡇⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
45 | Total download progress: 45% ⬛⬛⬛⬛⬛⬛⬛⬛⬛🡇⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
46 | Total download progress: 50% ⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛🡇⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
47 | Total download progress: 55% ⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛🡇⬜⬜⬜⬜⬜⬜⬜⬜⬜
48 | Total download progress: 60% ⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛🡇⬜⬜⬜⬜⬜⬜⬜⬜
49 | Total download progress: 65% ⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛🡇⬜⬜⬜⬜⬜⬜⬜
50 | Total download progress: 70% ⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛🡇⬜⬜⬜⬜⬜⬜
51 | Total download progress: 75% ⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛🡇⬜⬜⬜⬜⬜
52 | Total download progress: 80% ⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛🡇⬜⬜⬜⬜
53 | Total download progress: 85% ⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛🡇⬜⬜⬜
54 | Total download progress: 90% ⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛🡇⬜⬜
55 | Total download progress: 95% ⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛🡇⬜
56 | Total download progress: 100 ⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛🡇
57 | Total download progress: 100 ⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
255 |  // empty message



```c
  [Meta Data File](meta-file.md)
FS
  Styles
FS
  STX (Start of Text ASCII Control Character. Decimal 28. Hex 0x1C.
The text starts here and keeps going until there are is no more writing.
```


  



# QMail Format For Phase I
The QMail is made up of three parts:
1. Meta Data: Includes the Email ID, Subject text, Number of attachments, To:[], Date & Time Sent and From:
2. Styles: Not used in phase I but the starting byte 0x1C and ending byte 0x1C still need to be shown 
3. Binary Markup Text: Shows status message until email is downloaded.

## Phase I QMail File Structure
Here is a general look at the file structure. 
```c
    META DATA
FS (File Seperator)
    STYLES (empty in phase I)
FS (File Seperator)
    SOH (Start of Header)
        Shows a message here based on 1 byte status code.
    STX (Start of Text)
        The text starts here and keeps going until there are is no more writing.
```

## Hello World QMail (Phase I example)
The following is an actual qmail file used in Phase I. The message is simply "Hello World!". It can show some status messages.

All the values are shown in hex. This email is 86 bytes in length. 

```c
06    // The number of key/value pairs in the meta file. Here there are 6 key/value pairs
01 ▪ 10 ▪ BF 7B 94 B3 91 A2 46 B5 8E 48 54 5D D8 F1 31 01     // Key 1(Email GUID) Value Length: 16. Value: GUID)
02 ▪ 0B ▪ 49 20 6C 6F 76 65 20 79 6F 75 21    // KeyID: 2(Subject Text) Value Length: 11. Value: "I love you!"
0B ▪ 01 ▪ 04    // KeyID: 12( Number of Attachments) Value Length: 1. Value: 4 attachments
FB 0D ▪ 00 02 ▪ 07 ▪ {{ 00 06, 02, 00 02 3F 98 },{ 00 06, 02, 00 04 67 2E }}    // KeyID: 251 13(To: Array) Element Count: 2.  Element Length: 7. Value: Two mailbox IDs {{6,2,147352},{6,2,288558}} 
19 ▪ 04 ▪ 68 CF B6 AD  // KeyID: 25(Timestamp) Value Length: 4. Value: 1758443181 = "Sunday, September 21, 2025 8:26:21 AM"
13 ▪ 07 ▪ 00 06  02  03 E8 78 A0    // KeyID: 19(From Mailbox) Value Length: 7. Coin Code 00 06: CloudCoin, Denomination 02: 100cc, Serial Number 03 E8 78 A0: 65566880
1C    // End of Meta Data. Start of Styles Tables 
      // No Style Tables for Phase I. Client will use its default style. No characters between the two FSs.  
1C    // Start of Markup. End of the Styles Tables
01    // Next byte will be the status code. Defaults to zero. See Status Code Table below 
00    // Print status message 0 that says "Program: Waiting for your command to download this qmail's content"
02    // Start of text
48 65 6C 6C 6F 20 57 6F 72 6C 64 21    // These 12 bytes encode "Hello World!"
```

## Overall Structure
This is the structure of a QMail file for Phase I that is just for sending a text message

| ASCII Control Character (Hex) | Name | Meaning | Description |
|---|---|---|---|
| 1 byte int| Key/Value Pair Count | There will be a line of bytes below for every key/value | Just one byte with 0 to 255 pairs possible|
| Meta Key/Value Pairs | Key, Value Length, Value| [Meta Data Key Table](#meta-data-key-table)| There are up to 255 keys each with its own code.| 
| 0x1C| FS (File Seperator) |Seperates the Meta Part and the Styles Part| The first 0x1C ends the meta and begins the styles tables |
| 0x1C| FS (File Seperator) |Seperates the Styles Part and the Markup Part| The Second FS begins the formatted text of the qmail and ends the styles |
| 0x01 |SOH (Start of Header) |Shows the status of the email while it is loading | See [Status Table](#status-table)|
| 0x02 |STX| Start of Text |  This text is marked up with control characters | We will not start marking this up until Phase II |

## Meta Data Key Table
These are the ones available for Phase I but many optional 
| Key ID | Name | Size | Description | (Required) Δ(Added by Raida) Σ(Added by user) | Phase |
|---|---|---|---|---|---|
| 1 | Qmail ID | 16 | The GUID the sender assigned to this email | * | 1 |
| 2 | Subject | 1 | The UTF-8 encoded text of the subject line  | | 1 |
|12| "Number of Attachments" | 1 | How many files are associated with the qmail. Limit 255| Δ | 2 |
|251 13| "To Array" | 2 * 1 | 251(array) 13(To:s). Next 2 bytes = number of elements. 3rd Byte describes number of bytes per element. 7 bytes per mailbox address. | Δ| 1 |
| 14| "CC Array" | {2,1} | An array of "CC:" 7 byte mailbox addresses | Δ| 1 |
| 19| "From Mailbox" | 1| Cloudcoin (0x0006), Denomination (1 byte), Serial Number (4 bytes)| | 1 |
| 25 | "Timestamp" | 4 | Value: 1758443181 = "Sunday, September 21, 2025 8:26:21 AM" | * | 1 |
| 250 | "Escape to Array" | 1 Byte of array elements. 1 Byte of length per element | Multiplication by byte | * | 1 |
| 251 | "Escape to Array" | 2 Byte of array elements. 1 Byte of length per element  | Multiplication by byte  | * | 1 |


## Markup Contol Characters
In Phase I, we only use six of them:

| Index | Hex | Symbol | Description | New Use |
|-------|-----|---------|-------------|------------|
| 1 | 01 | SOH | Start of Heading | Status Code Follows |
| 2 | 02 | STX | Start of Text | Markup Text Follows
| 9 | 09 | HT | Horizontal Tab | Tab is used (unlike HTML)
| 10 | 0A | LF | Line Feed | Line Break (Unix) is used (unlike HTML which uses <br>)
| 13 | 0D | CR | Carriage Return | Line Break (Windows) is used (unlike HTML  which uses <br>)
| 28 | 1C | FS | File Separator | Seperates parts of the document


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
35 | Total download progress: 00% CRLF ⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
36 | Total download progress: 00% CRLF 🡇⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
37 | Total download progress: 05% CRLF ⬛🡇⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
38 | Total download progress: 10% CRLF ⬛⬛🡇⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
39 | Total download progress: 15% CRLF ⬛⬛⬛🡇⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
40 | Total download progress: 20% CRLF ⬛⬛⬛⬛🡇⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
41 | Total download progress: 25% CRLF ⬛⬛⬛⬛⬛🡇⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
42 | Total download progress: 30% CRLF ⬛⬛⬛⬛⬛⬛🡇⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
43 | Total download progress: 35% CRLF ⬛⬛⬛⬛⬛⬛⬛🡇⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
44 | Total download progress: 40% CRLF ⬛⬛⬛⬛⬛⬛⬛⬛🡇⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
45 | Total download progress: 45% CRLF ⬛⬛⬛⬛⬛⬛⬛⬛⬛🡇⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
46 | Total download progress: 50% CRLF ⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛🡇⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
47 | Total download progress: 55% CRLF ⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛🡇⬜⬜⬜⬜⬜⬜⬜⬜⬜
48 | Total download progress: 60% CRLF ⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛🡇⬜⬜⬜⬜⬜⬜⬜⬜
49 | Total download progress: 65% CRLF ⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛🡇⬜⬜⬜⬜⬜⬜⬜
50 | Total download progress: 70% CRLF ⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛🡇⬜⬜⬜⬜⬜⬜
51 | Total download progress: 75% CRLF ⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛🡇⬜⬜⬜⬜⬜
52 | Total download progress: 80% CRLF ⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛🡇⬜⬜⬜⬜
53 | Total download progress: 85% CRLF ⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛🡇⬜⬜⬜
54 | Total download progress: 90% CRLF ⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛🡇⬜⬜
55 | Total download progress: 95% CRLF ⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛🡇⬜
56 | Total download progress: 100 CRLF ⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛🡇
57 | Total download progress: 100 CRLF ⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
255 |  // empty message

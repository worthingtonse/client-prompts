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

| ASCII Index Decimal | Hex | Symbol | Description | Used For |
|-------|-----|---------|-------------|------------|
| 2 | 02 | STX | Start of Text | Indicator that Markup Text Follows
| 9 | 09 | HT | Horizontal Tab | Tab is used (unlike HTML). Adds a Tab character
| 10 | 0A | LF | Line Feed | Line Break (Unix) is used (unlike HTML which uses <br>)
| 13 | 0D | CR | Carriage Return | Line Break (Windows) is used (unlike HTML  which uses <br>)
| 28 | 1C | FS | File Separator | Seperates parts of the document


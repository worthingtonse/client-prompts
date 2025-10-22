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

## Meta Data
The meta data is the data about the email but not the email itself. The meta data is made up of two parts:
1. 16 bytes that are fixed
2. Other information that can varry but will show in chunks of 16 bytes each. 

## Meta Part Command Codes for Phase I
Command codes show what the bytes following the command code mean. The lenght of the bytes after a Meta Command code is fixed. 

Name | Code in Hex | Code in Decimal | Bytes including command code| Byte Meanings| Value if not included | Description 
---|---|---|---|---|---|---
Address | 0x02 | 2 | 16 | Address type To, CC, BCC, MM or From one byte, Coin ID 2 bytes, Denomination 1 bytes, Serial Number 4 bytes. | No CC | A mailbox address that the email was set to besides the receiver  |
Locker Code | 0x24 | 36 | 16 | Raida that sent the locker code, 14 bytes of locker code | The locker codes are missing the last two FF FF which are assumed to be there.| No Locker codes


## Body Part Command Codes for Phase I
These have a code followed by the length. The subject only uses one byte to describe the length. The text uses 2 bytes to describe the length of the text. 
Name | Code in Hex | Code in Decimal | Bytes that Follow| Byte Meanings| Value if not included | Description 
---|---|---|---|---|---|---
Subject | 0x01 | varies | Between 0 and 255  | index 1 says how many bytes follow.* | Subject bytes (UTF-8) up to 255 bytes.| No Subject  
Text | 0x02 | 2 | varies | Between 0 and 65584 | index 1 and 2 big endian says how many bytes will follow | UTF-8 | No Text|

## Hello World QMail (Phase I example)
The following is an actual qmail file used in Phase I. The message is simply "Hello World!". It can show some status messages.

All the values are shown in hex. This email is 86 bytes in length. 

```c
+// METADATA
+//-----------------------------------------------------------------------------
+// FIXED PART THAT IS ALWAYS THE SAME LENGTH AND ALL DATA IS REQUIRED. THE LENGTH IS ALWAY 16 BYTES
+// Address. 0x00 = To, 0x01 = cc, 0x02 = BCC, 0x03 = Mass Mailing, 0x04 = From, 0x05 = group
+04  00 00 06  03  00 4C D8 88 
+                       
+// Year -2000  UTC 
+19  
+
+// Month
+01
+
+// Day
+01
+
+// Minute
+01
+
+// Second
+01
+
+// Random Number 1 just to make sure the ID is unique 
+9A
+
+
+// Number of attachments
+00
+// VARIABLE PART OF THE META DATA THAT IS NOT REQUIRED. ALWAYS IN GROUPS OF 16 BYTES.
+// Locker Code $ followed by RAIDA ID and 16 byte GUID minus the 2 FF FFs that are assumed //
+24  0B  CE EC F2 28 7D 6A 4C 37 B3 21 DF 59 FF FF  // Code 24 (locker code) from RAIDA 11 (0x0B). Locker codes (14 bytes) always end in FF FF FF FF so last 2 bytes are assumed to be FF FF 
+
+24  01  DF 5D DD 5C 6A 72 4A 40 BC AE 55 B5 FF FF // Locker Code for Raida 1
+
+24  10  BE 8F E2 F4 26 E6 4E B4 B8 CA A6 20 FF FF  // Locke code from RAIDA 16
+
+//  Addresses 0x00 = To, 0x01 = cc, 0x02 = BCC, 0x03 = Mass Mailing, 0x04 = From, 0x05 = group
+02  00 00 06  03  00 4C D8 88  00 00 00 00 00 00 00 // Last seven bytes are reserved for future use. 
+
+02  00 00 06  04  00 B8 CA A6  00 00 00 00 00 00 00 // Last seven bytes are reserved for future use. 
+
+// CC Address 
+02  01 06  05  00 DD 5C 6A  00 00 00 00 00 00 00 // Last seven bytes are reserved for future use. 
+
+// SEPARATORS
+//-----------------------------------------------------------------------------
+1c                                      // FS: End of Metadata, Start of Styles. In Phase I, Styles is empty. 
+//-----------------------------------------------------------------------------
+1c                                      // FS: End of Styles, Start of Markup
+
+01  // Key ID 1 (Subject)
+05  // Value Length: 5 bytes
+48 65 6c 6c 6f           // Value: "Hello"
+
+02                                      // STX: Start of Text
+0C                                      // Number of bytes in the text tha follows: 12
+48 65 6c 6c 6f 20 57 6f 72 6c 64 21                // Body: "Hello World!"

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
| 14| "CC Array Member" | 7 | An array of "CC:" 7 byte mailbox addresses | Δ| 1 |
| 19| "From Mailbox" | 1| Cloudcoin (0x0006), Denomination (1 byte), Serial Number (4 bytes)| | 1 |
| 25 | "Timestamp" | 4 | Value: 1758443181 = "Sunday, September 21, 2025 8:26:21 AM" | * | 1 |

## Markup Contol Characters
In Phase I, we only use six of them:

| ASCII Index Decimal | Hex | Symbol | Description | Used For |
|-------|-----|---------|-------------|------------|
| 2 | 02 | STX | Start of Text | Indicator that Markup Text Follows
| 9 | 09 | HT | Horizontal Tab | Tab is used (unlike HTML). Adds a Tab character
| 10 | 0A | LF | Line Feed | Line Break (Unix) is used (unlike HTML which uses <br>)
| 13 | 0D | CR | Carriage Return | Line Break (Windows) is used (unlike HTML  which uses <br>)
| 28 | 1C | FS | File Separator | Seperates parts of the document

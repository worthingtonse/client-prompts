# QMail Format For Phase I
The QMail is made up of three parts:
1. Meta Data: Includes the Email ID, Subject text, Number of attachments, To:[], Date & Time Sent and From:
2. Styles: Not used in phase I but the starting byte 0x1C and ending byte 0x1C still need to be shown 
3. Binary Markup Text

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
The meta data is the data about the email but not the email itself. The meda data is put together by the client by assemplying data that it has gotting by downloading email stripes from QMail servers. The meta data is made up of two parts:
1. 32 bytes that are fixed
2. Other information that can varry but will show in chunks of 16 bytes each. 

## Meta Part Command Codes for Phase I
Command codes show what the bytes following the command code mean. The lenght of the bytes after a Meta Command code is fixed. 

Name | Code in Hex | Code in Decimal | Bytes including command code| Byte Meanings| Value if not included | Description 
---|---|---|---|---|---|---
Address | 0x40 | 64 | 16 | Address type 0x02 = To, 0xCC = CC, 0xBC = BCC, 0x00 = Mass Mailer. One byte, Coin ID 2 bytes, Denomination 1 bytes, Serial Number 4 bytes. | No other addresses such as To, CC  and BCC | A mailbox address that the email was set to besides the receiver  |
Stripe Info | 0x23 | 35 | 32 | [RAID Header](https://github.com/worthingtonse/client-prompts/blob/main/Ideas%20In%20Progress/QMAIL/raid-codes.md#raid-metadata-header-standard) ( 2 Bytes), Mail Server Port (2 bytes), For Future Use (11 bytes), QMail Server IP (16 bytes. Last four are the IPv4) | | Error

<!--
Locker Code | 0x24 | 36 | 16 | Raida that sent the locker code, 14 bytes of locker code | The locker codes are missing the last two FF FF which are assumed to be there.| No Locker codes
Shuffle Shard information | 0x3F | 63 | 32 | One row of the shuffle table. This will be between 2 and 32 characters long | | Error
-->

## Styles Part Command Codes for Phase I
The Styles Part will be left empty. 

## Body Part Command Codes for Phase I
These have a code followed by the length. The subject only uses one byte to describe the length. The text uses 2 bytes to describe the length of the text. 
Name | Code in Hex | Code in Decimal | Bytes that Follow| Byte Meanings| Value if not included | Description 
---|---|---|---|---|---|---
Subject | 0x01 | varies | Between 0 and 255  | index 1 says how many bytes follow.* | Subject bytes (UTF-8) up to 255 bytes.| No Subject  
Text | 0x02 | 2 | varies | Between 0 and 65584 | index 1 and 2 big endian says how many bytes will follow | UTF-8 | No Text|

## Hello World QMail (Phase I example)
The following is an actual qmail file used in Phase I. The message is simply "Hello World!". It can show some status messages.

All the values are shown in hex. This email is 310 bytes in length. It has been downloaded from five different QMail Servers. 

```c
11 E3 8F 8D 56 8C 4D 70 A7 F9 C5 0D B7 16 02 CD
40 F0 00 06 03 00 4C D8 88 19 01 01 01 01 00 00
02 00 00 06 03 00 4C D8 88 00 00 00 00 00 00 00 
02 00 00 06 04 00 B8 CA A6 00 00 00 00 00 00 00 
02 01 00 06 05 00 DD 5C 6A 00 00 00 00 00 00 00
23 38 80 C3 51 00 00 00 00 00 00 00 00 00 00 00 
00 00 00 00 00 00 00 00 00 00 00 00 56 A7 13 C5
23 38 80 C3 51 00 00 00 00 00 00 00 00 00 00 00 
00 00 00 00 00 00 00 00 00 00 00 00 FB 4F 0F B8 
23 38 80 C3 51 00 00 00 00 00 00 00 00 00 00 00 
00 00 00 00 00 00 00 00 00 00 00 00 B9 AE 42 EE 
23 38 80 C3 51 00 00 00 00 00 00 00 00 00 00 00 
00 00 00 00 00 00 00 00 00 00 00 00 A8 4A 88 5D 
23 38 80 C3 51 00 00 00 00 00 00 00 00 00 00 00 
00 00 00 00 00 00 00 00 00 00 00 00 23 27 C6 6E
1C 1C 01 05 48 65 6c 6c 6f 02 0C 48 65 6c 6c 6f
20 57 6f 72 6c 64 21     
```
Meaning of bytes:

```c
+// METADATA
+//-----------------------------------------------------------------------------
+// FIXED PART THAT IS ALWAYS THE SAME LENGTH AND ALL DATA IS REQUIRED. THE LENGTH IS ALWAY 16 BYTES
+
+// EMAIL GUID
+ 11 E3 8F 8D 56 8C 4D 70 A7 F9 C5 0D B7 16 02 CD
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
+// Reserved for future use
+00
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
+02  01 00 06  05  00 DD 5C 6A  00 00 00 00 00 00 00 // Last seven bytes are reserved for future use. 
+
+// Strip information
+23 38 80 C3 51 00 00 00 00 00 00 00 00 00 00 00 // RAID Header, Port Number, 11 for future use
 00 00 00 00 00 00 00 00 00 00 00 00 56 A7 13 C5 // IP Address

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
| 0x1C| FS (File Seperator) |Seperates the Meta Part and the Styles Part| The first 0x1C ends the meta and begins the styles tables |

## Markup Contol Characters
In Phase I, we only use 3 of them:

| ASCII Index Decimal | Hex | Symbol | Description | Used For |
|-------|-----|---------|-------------|------------|
| 9 | 09 | HT | Horizontal Tab | Tab is used (unlike HTML). Adds a Tab character
| 10 | 0A | LF | Line Feed | Line Break (Unix) is used (unlike HTML which uses <br>)
| 13 | 0D | CR | Carriage Return | Line Break (Windows) is used (unlike HTML  which uses <br>)


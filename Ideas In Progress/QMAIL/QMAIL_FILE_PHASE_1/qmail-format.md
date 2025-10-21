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
1. The RAIDA Report: data from the RAIDA that is confirmed and reliable. This is of fixed length and does not change.
2. The User Report: data from the user that may not be true. 

## Hello World QMail (Phase I example)
The following is an actual qmail file used in Phase I. The message is simply "Hello World!". It can show some status messages.

All the values are shown in hex. This email is 86 bytes in length. 

```c
+// METADATA
+//-----------------------------------------------------------------------------
+// FIXED PART
+// Coin Group
+00                                    
+
+// Coin ID
+06                            
+
+// From Denomination
+04                       
+
+// From Addres 1st Octet
+00                                    
+
+// From Addres 2nd Octet
+5C                                   
+
+// From Addres 3rd Octet
+14                                 
+
+// From Addres 4th Octet
+B8                                   
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
+// Reserved for future use.
+0B
+
+// Number of attachments
+00
+
+//-----------------------------------------------------------------------------
+1D                                      // GS: End of Server Report, start of User Report. The fize of this part will vary and depends
+
+// Locker Code $ followed by RAIDA ID and 16 byte GUID //
+24 0B 41 42 43 44 45 46 47 41 42 43 44 45 46 47 77 72
+
+// Locker Code $ followed by RAIDA ID and 16 byte GUID
+24 0B 41 42 43 44 45 46 47 41 42 43 44 45 46 47 77 72
+
+// Locker Code $ followed by RAIDA ID and 16 byte GUID
+24 0B 41 42 43 44 45 46 47 41 42 43 44 45 46 47 77 72
+
+// TO Address
+12 03 00 4C D8 88 
+
+// CC Address  Device Contorl Two
+13 03 00 4C D8 88 
+
+// BCC Address 
+14 03 00 4C D8 88 
+
**
+// SEPARATORS
+//-----------------------------------------------------------------------------
+1c                                      // FS: End of Server Report, start of Metadata
+//
+//
+// Number of key/value pairs
+06
+
+// Pair 1: QMail ID (GUID)
+01                                      // Key ID: 1
+10                                      // Value Length: 16 bytes
+bf7b94b391a246b58e48545dd8f13101        // Value: The GUID
+
+// Pair 2: Subject
+02                                      // Key ID: 2
+0c                                      // Value Length: 12 bytes
+48656c6c6f20576f726c6421                // Value: "Hello World!"
+
+// Pair 3: Number of Attachments
+0c                                      // Key ID: 12
+01                                      // Value Length: 1 byte
+04                                      // Value: 4
+
+// Pair 4: To Array
+fb0d                                    // Key ID: 251, 13 (Array of To:)
+0200                                    // Element Count: 2 (little-endian)
+07                                      // Element Length: 7 bytes
+060002983f0200                          // Element 1: Mailbox {6, 2, 147352}
+0600022e670400                          // Element 2: Mailbox {6, 2, 288558}
+

+// SEPARATORS
+//-----------------------------------------------------------------------------
+1c                                      // FS: End of Metadata, Start of Styles
+1c                                      // FS: End of Styles, Start of Markup
+
+// BODY
+//-----------------------------------------------------------------------------
+02                                      // STX: Start of Text
+48656c6c6f20576f726c6421                // Body: "Hello World!"

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

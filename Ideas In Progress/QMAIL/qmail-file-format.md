# Qmail File Format

This is the actual qmail file. It uses the CBD (Compace Binary Document) format.

# Fixed part of file (Phase I)

Code | Bytes | Name & Description | Required?
---|---|---|---
0 | 1 | Number of Key Pairs | Required 
1 | 1 | version / formatting type | 0=plain text, 1 = Formatted Qmail CBD file (0 for Phase I| Required 
2 | varies | Plain Text Message. Only used if version = 0. The actuall text of the message UTF-8 | Required 

Phase I just has plain text messages. 

Sample Qmail CBD File (13 bytes total):
```javascript
0x00 0x01 0x03 // Key: Number of key pairs, Length of Value: one byte, Value: Three key pairs
0x01 0x01 0x00  // Key: Version, Length of Value: one byte, Value: Version 0
0x02 0x0B 0x48 0x65 0x6c 0x6c 0x6f 0x20 0x57 0x6f 0x72 0x6c 0x64   // Key: Message, Length of Value: 11, Value: Hello world
```
Qmail CBD File Shown as a Table:

Key | Length of Value | Value
---|---|---
0x00 | 0x01 | 0x03 
0x01 | 0x01 | 0x00  
0x02 | 0x0B | 0x48 0x65 0x6c 0x6c 0x6f 0x20 0x57 0x6f 0x72 0x6c 0x64  


# Fixed part of file (Phase II)

Code | Bytes | Name & Description | Required?
---|---|---|---
0 | 1 | Number of Key Pairs | Required 
1 | 1 | version / formatting type | 0=plain text, 1 = Formatted Qmail CBD file (0 for Phase I| Required 
2 | varies | Plain Text Message. Only used if version = 0. The actuall text of the message UTF-8 | Required 
3 | 1 | Template (4 bits) and Corner Modifier (4 bits). See graphics table. 
100 | Varies but divisable by 4 | Panels ID, Panel Type, Panel Texture, Panel Color, Panel Corners, Boarder, Boarder Color, Padding, Margin, 4 bits (Sub Box Identifier 0-3), 
100 | Main Panel Formatting | Max Rows, Max Columns, Number of Containers used, Header 100, 8, 8, 64 (8 bits, 3 bits, 3 bits, 6 bits) 22 bits for spaces. 
101 | Header Panel Formatting
102 | Left Aside Panel Formatting
103 | Right Aside Panel Formatting
104 | Footer Panel Formatting

Panel IDs

ID in Hex| Name
---|---
Header, c    
  Space 0001 Rows Occupied 0000 0000 Columns Occumpied 0000 0000 ( 6 bits, 8 bits, 8 bits) Format Type, Format
Header, Sub Panel Layout 0000  Row 0000, Col 0000 

Header, Sub Panel Layout 0001  Row 0000, Col 0000 
Header, Sub Panel Layout 0001  Row 0001, Col 0000

Header, Sub Panel Layout 0010  Row 0000, Col 0000 
Header, Sub Panel Layout 0010  Row 0001, Col 0000 
Header, Sub Panel Layout 0010  Row 0010, Col 0000 

Header, Sub Panel Layout 0011  Row 0000, Col 0000 
Header, Sub Panel Layout 0011  Row 0000, Col 0001 

Header, Sub Panel Layout 0100  Row 0000, Col 0000 
Header, Sub Panel Layout 0100  Row 0000, Col 0001 
Header, Sub Panel Layout 0100  Row 0001, Col 0000 
Header, Sub Panel Layout 0100  Row 0001, Col 0001 

Header, Sub Panel Layout 0101  Row 0000, Col 0000 
Header, Sub Panel Layout 0101  Row 0000, Col 0001 
Header, Sub Panel Layout 0101  Row 0001, Col 0000 
Header, Sub Panel Layout 0101  Row 0001, Col 0001 
Header, Sub Panel Layout 0101  Row 0010, Col 0000 
Header, Sub Panel Layout 0101  Row 0010, Col 0001 

Header, Sub Panel Layout 0110  Row 0000, Col 0000 
Header, Sub Panel Layout 0110  Row 0000, Col 0001 
Header, Sub Panel Layout 0110  Row 0000, Col 0010

Header, Sub Panel Layout 0111  Row 0000, Col 0000 
Header, Sub Panel Layout 0111  Row 0000, Col 0001 
Header, Sub Panel Layout 0111  Row 0000, Col 0010
Header, Sub Panel Layout 0111  Row 0001, Col 0000 
Header, Sub Panel Layout 0111  Row 0001, Col 0001 
Header, Sub Panel Layout 0111  Row 0001, Col 0010


Panel Types: 
Code | Type
0 | Plain
1 | Tabs
2 | Accordian

Container Formatting

Code | Name | Bits | Notes
---|---|---|---
0 | container type | 4 bits | Continer types include plain, tabs, stacks, canvas, image, table, svg, form
1 | Max Rows | 8 bits | There are a maxiumum of 256 rows but only 4 for Phase I
2 | Max Columns | 8 bits |  There are a maxiumum of 256 rows but only 4 for Phase I



Sub-Container Formatting
Type Included | Name | Bytes | Notes
---|---|---|---
0 | Format Type | 1 | 16 types
1 | BG-Color |  2 | R5B5G5 (Default 1 white) Zero is translusent.
2 | Margin Top,Right,Bottom,Left | 2 | In percentages 0 to 16%. Margin,Border,Padding, Egg must all add up to 100%. (default 5%)
3 | Padding Top,Right,Bottom,Left | 2 | In percentages 0 to 16%. Hese four must all add up to 100% (Margin + Border + Padding + Egg = 100%) (default 5%)
4 | Egg | 1 | In percentages 1 to 100 (default 89%)
5 | Border Color | 2 | R5B5G5 (default middle gray #808080) 
6 | Border Thickness, Top,Right,Bottom,Left | 2 | In .5 % 0 to 8% (reduces the padding and margin by half the percentage. ( default 0% )
7 | Corner roundness, UL,UR,LL,LR | 3 (6 bits each | 0% to 50%. 50% is a circle. (Default 0%)
9 | Shaddow color | 2 | R5B5G5 (Default #808080)
10 | Shaddow X, Y, Diffusion | 2 | 6 + 6 + 4 bits. -32*.5% to +32*.5%, -32*.5% to +32*.5%, 0-15% 
12 | Image-byte | 1 | Used to chose one of the 255 built-in background images unless overwrite is specified.(Default 0 translucent) 
13 | Background Color Opacness | 1 | 0-100%. This goes over the Image. If 100% then the imgae will not show. (Default 100%. Covers all)

Egg 7
type 4
shad x 6
Shad y 6
Shad dff 4

Panel Format Types

0 All defaults. No other formatting
1 Group 1 only
2 Group 2 only
3 Group 3 only
4 Group 4 only
5 Group 1 and 2
6 Group 1 and 3
7 Group 1 and 4
8 Group 2 and 3
9 Group 2 and 4
10 Group 3 and 4
11 Group 1,2 and 3
12 Group 1,2 and 4
13 Group 1,3 and 4
14 Group 2,3 and 4 
15 Group All groups






All must be in percentage. Image ID, (16 bits, 8 bits, 5 bits, 5 bits, 16 bits, 4 bits, 4 bits, 4 bits, 16 bits, 5 bits, 5 bits, (Image-byte, BG-Color, Color Opacness)   


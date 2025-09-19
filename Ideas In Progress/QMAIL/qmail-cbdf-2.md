# **Qmail File Format v0.1 Specification**

## **1\. Overview**

The qmail Compact Binary Document Format (CBDF) is designed for the efficient storage and transmission of richly formatted documents. Its primary goals are to be significantly smaller than equivalent HTML/CSS files and to provide a consistent rendering experience within a closed ecosystem.

The format achieves its compactness through several key strategies:

* **Predefined Resource Tables:** Styles, layouts, links, and embedded objects are defined once in a file header and referenced by a small ID.  
* **Bit-Packed Structures:** Style definitions use bit-packing to minimize their size.  
* **Command-Based Body:** The document body uses a stream of text interspersed with single-byte command codes, eliminating the need for verbose opening and closing tags.

The standard character encoding for all text content is **UTF-8**.

## **2\. File Structure**

A CBDF file consists of two main sections: a **Fixed Header** followed by a **Variable Body**.

## **2.1 The Fixed Header**

Key | Bytes | Description
---|---|---
Version | 4 bits | Starts at zero
Formatting | 4 bits | 0 = plain text
Number of Key Pairs | 1 | Phase I will have zero and be a plain text document. 


Header Sections: Note: If the email will be shown as plain text, it should still work if control characters are removed. 
The file is broken up into different parts. Each part starts with the Starter Code and ends when a new Starter codes is shown. 
The email does not need to have all the sections and some of them can be skipped. 
Starter Code| In Hex | Name | Description
---|---|---
^0 | 5E 30 | Fixed Section | This is the fixed portion of the header
^1 | 5E 31 | Text Styles | This is the fixed portion of the header
^2 | 5E 32 | Events | What happens when ...
^3 | 5E 33 | Links | text of what happens ...
^4 | 5E 34 | Links | text of what happens ...
^5 | 5E 35 | Background Styles | Length depends on the template. Style includes Color, Img, Width%, Height%, Default will be golden ratio. 
^6 | 5E 36 | Containers Styles | This is the fixed portion of the header
^00000000 5E 00 | Heading / mail background?
^0100 0000 5E 40 | Footer
^0010 0000 5E 20 | Left Aside Top to Bottom
^0001 0000 5E 10 | Right Aside Top to Bottom


### **3.1. Layout Definition**

The first byte of the file defines which of the 255 predefined layouts to use. Each layout specifies the arrangement of content panes (e.g., header, main, footer) and has both a desktop and a mobile rendering mode.

* **Data Type:** 1 byte  
* **Example:** 0x03 selects Layout \#3 (e.g., Header, Navbar, Main, Footer).

# Figuring out the templates
There are 256 templates. All the templates have a "Main" section. Template 0 is just a main section. 
The byte of the templates is a bit field:

Template Types
bit | meaning
---|---
0 | Side to Side Heading exists
1 | Side to Side Footer exists
2 | Top to Bottom Left Aside exists
3 | Top to Bottom Right Aside exists
4, 5 | How many columns exist (1 to 4) 00=1 01=2 11=3
6, 7 | How many rows exist (1 to 4) 00=1 01=2 11=3

Container Types (For Phase II or QWeb)
bit | meaning
---|---
0 | Side to Side Heading exists
1 | Side to Side Footer exists
2 | Top to Bottom Left Aside exists
3 | Top to Bottom Right Aside exists
4, 5 | How many columns exist (1 to 4) 
6, 7 | How many rows exist (1 to 4) 


### **3.2. Style Table**

This table defines the visual styles used in the document.

* **Structure:** A count byte followed by a series of 6-byte style records.  
* **Style Record (6 bytes / 48 bits):**  
  * **font-family (6 bits):** ID for up to 64 predefined fonts.  
  * **font-size (7 bits):** Size in points (1-127pt).  
  * **flags (3 bits):** Bitmask for Bold, Italic, and Underline.  
  * **text-color (16 bits):** 16-bit "HighColor" (R5G6B5).  
  * **bg-color (16 bits):** 16-bit "HighColor" (R5G6B5).

### **3.3. Link Table**

This table contains all external URLs referenced in the document.

* **Structure:** A count byte followed by a series of URL entries.  
* **URL Entry:** A 2-byte integer specifying the length of the URL, followed by the UTF-8 encoded URL string.

### **3.4. Embedded Object Table**

This table contains binary data for embedded assets like images.

* **Structure:** A count byte followed by a series of object entries.  
* **Object Entry:** A 4-byte integer specifying the length of the binary data, followed by the raw data itself.

### **3.5. Text Direction**
Top Down, Left Right, Bottom Up. Right Left. 

### **3.6. Comment/meta**
Memo hidden in the header?

### **3.7. Return Address**
The place the mail was from

### **3.8. Time Stamp**
Raida Time stamp

### **3.9. Sending Raidas**
Addresses of all RAIDAs

### **3.10. Encryption Key ID**
Key used to decrypt maybe?

### **3.11. Subjects**
Do we need subjects anymore? no?

### **3.13. CloudCoin**
The payment for the email. A locker code.


## **4\. The Body & Command Codes**

The body has three layers. 
Layer Name | Discription
---|---
Background | This holds the everything that everything else is layed upon. May contain gradiants, images, solid colors. The user can override this. 
Containers | Containers must fit within the semantic spaces of the template. There are container templates that how how things can go in them. These containers can also be images, tables, gradiants, They may have shadows, glows, and may change on mouse over. These can also be "view boxes" where software code can be seen, videos, mermaid, svg, 
Text | This layer is only for text including links, lists, code, 

# Accessability. It be very easy for a blind person to navigate. 
* Title: "Message entitled How are you?"
* Page Description: There are four parts here: Heading, main, nav and aside.
* Main: The main box says Headline: "Time to live" text "Today it is time for us to live. Don't you know. 


The body contains the document's text content, interspersed with command codes. The 27 unused ASCII control characters (codes 0x01-0x08, 0x0B-0x0C, 0x0E-0x1A, and 0x1C-0x1F) are repurposed as command codes.

A parser reads the body byte by byte. If a byte is a standard UTF-8 character, it is rendered. If it is a command code, the parser performs the corresponding action.

### **Common Command Codes (Examples):**

Dec | Code (Hex) | Command | Description |  
---|---|---|---
0| 0x00 | Pane Seperator | These will be at the end of every section that the document has according to the template that has been choosen
1| 0x01 | Start / End Style | The next byte is a Style ID from the Style Table. All subsequent text will use this style until a new style is applied. |  2
2| 0x02 | Start / End Link | The next byte is a Link ID from the Link Table. All subsequent text is part of this link. | Link ID is  
3| 0x03 | Start / End Box | Draws a box around things | 
4| 0x04 | Insert Object Inline | The next byte is an Object ID f5rom the Embedded Object Table. The object is inserted at this position. |  
5| 0x05 | Start / End Table | The next byte specifies the number of columns. This is followed by column definition records. |  
6| 0x06 | Cell Separator | Marks the end of a cell within a table row. |  
7| 0x07 | Row Separator | Marks the end of a table row. |  
8| 0x08 | End Table | Terminates the current table definition. |  
9| 0x09 | Capitzlie word | Make the next letter capitalized.  
10| 0x0A | Add "ed"|  |  
11| 0x0B | Add "ing" |  |  
12| 0x0C | Add "'s"|  |  
13| 0x0D| "Th" |  |
14| 0x0E | Box S| |
15| 0x0F | Carraige Return  | This is special. If it is followed by another control character, it will not be added to the follower
16| 0x10 | Start / End List  | Followed by descriptor byte.  
17| 0x11 | Apply Style | The next byte is a Style ID from the Style Table. All subsequent text will use this style until a new style is applied. |  
18| 0x12 | Start Link | The next byte is a Link ID from the Link Table. All subsequent text is part of this link. |  
19| 0x13 | End Link | Terminates the current hyperlink. |  
20| 0x14 | Insert Object | The next byte is an Object ID from the Embedded Object Table. The object is inserted at this position. |  
21| 0x15 | Start Table | The next byte specifies the number of columns. This is followed by column definition records. |  
22| 0x16 | Cell Separator | Marks the end of a cell within a table row. |  
23| 0x17 | Row Separator | Marks the end of a table row. |  
24| 0x18 | End Table | Terminates the current table definition. |  
25| 0x19 | Pane Separator | Marks the end of content for the current layout pane (e.g., end of header content). |
26| 0x1A | Clickable | Can be clicked on |  
27| 0x1B | Form| Stuff that can be submitted |  
28| 0x1C | Input| Ways to input data |  
29| 0x1D| svg| image |
30| 0x1E | Mermaid| Mermaid diagrams |
31| 0x1F | Carraige Return  | Do not use this code because it is used as a line break. 


| 0x7F | Delete |

## **5\. Conceptual Example**

A simple document saying "**Hello** World" with "World" as a link might look like this conceptually:

1. **Header:**  
   * **Layout:** 0x01 (Single Pane)  
   * **Styles:** Count: 2\. Style 0x01 (Bold). Style 0x02 (Regular).  
   * **Links:** Count: 1\. Link 0x01 ("[http://example.com](http://example.com)").  
   * **Objects:** Count: 0\.  
2. **Body (Human-Readable):**  
   * \[ApplyStyle: 0x01\] Hello \[ApplyStyle: 0x02\] \[StartLink: 0x01\]World\[EndLink\]

This structure is highly efficient, defining resources once and using single-byte commands to apply them, resulting in a minimal file size.


# This is how meta files should look. Note that these files are designed to be downloaded without the user
needing to download the entire email and all of its attachments. 

# **Qmail Meta File Format v0.1 Specification**

## **1\. Overview**

The qmail Compact Binary Document Format (CBDF) is designed for the efficient storage and transmission of richly formatted documents. 
Its primary goals are to be significantly smaller than equivalent HTML/CSS files and to provide a consistent rendering experience 
within a closed ecosystem.

This is the format for the meta data about these .qmail file. These files should be stored on the server with a .meta extention. 

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
Number of Key Pairs | 1 | Phase I will have just a few. Some are mandatory


### Meta Option Table

| Key ID | Name | Size | Description | (Required) Δ(Added by Raida) Σ(Added by user) | Phase |
|---|---|---|---|---|---|
| 0 | Version | 1 | Starts at zero | * | 1 |
| 1 | Qmail ID | 16 | The number the sender assigned to it | * | 1 |
| 2 | Subject | Varies| The subject line that may include formatting | | 1 |
| 3 | Subject Formatting | 2 | 1 byte (style ID), 1 byte (Font), 1 byte (Decoration), 3 bytes(Color) 1 byte (Formatting seperator) | | 2 |
| 7 | "Payment Coin" | 16 | Description to come | Δ | 2 |
| 8 | "Payed Amount" | 16 | Description to come | Δ | 2 |
| 9 | "Acknowledgment Number" | 16 | Description to come | | 2 |
| 10| "Please Acknowledge" // No code | 16 | Description to come | | 2 |
| 11| "Embedded Object Table" | 16 | Description to come | | 1 |
| 12| "Attachment GUIDs" | 16 | Description to come | Δ | 2 |
| 13| "To Array" | 7xN | An array of To addresses. | Δ| 1 |
| 14| "CC Array" | 7xN | An array of CC addresses | Δ| 1 |
| 15| "Sender's Avatar" | 16 | Description to come | Δ | 1 |
| 16| "Senders signature" | 16 | Description to come | | 2 |
| 17| "Senders signature WebP" | 700+ | [Binary SVG Format](binary-svg.md) | | 2 |
| 18| "Senders Avatar Prompt" | 4K| [Avatar Prompt](#avatar-prompt) | | 2 |
| 19| "Senders Mailbox" | 7| Cloudcoin (0x0006), Denomination (1 byte), Serial Number (4 bytes)| | 1 |
| 24 | "Sub-subject" | Varies| The subject line that may include formatting | | 2 |
| 25 | "Sub-subject Formatting" | 16 | Description to come | | 2|
| 26 | "grouped" | 16 | Description to come | | 2 |
| 27| "Checksum" | 16 | Description to come | | 2 |
| 250 | "Timestamp" | 4 | Description to come | * | 1 |
| 251 | "read" | 16 | Description to come | Σ | 2 |
| 252 | "stared" | 16 | Description to come | Σ | 2 |
| 253 | "grouped" | 16 | Description to come | Σ | 2 |
| 254 | "Responded to" | 16 | Description to come | | 2 |
| 255 | "trashed" | 16 | Description to come | Σ | 2 |



### Subject Formatting Table
Total bytes: 8

Index Number |Name  | bytes/bits | Meaning
---|---|---|---
0 | Style Start Code      | 1      | (ASCII Non-printable characters are allowed) When this code is encoutered in the subject line, the following style will kick in. 
1 | font-family           | 1      | 0-255. See font table. 0 means download font from raida. Only one allowed
2 | color                 | 2      | 65K different colors
4 | background-color      | 2      | 65K different colors
5.0 | font-weight         | 2 bits | 0=normal, 1=light, 2= bold, 3 = ?
5.2| font-style           | 2 bits | 0=normal, 1=italic, 2=oblique
5.4 | text-decoration-line| 2 bits | 0=none, 1=underline, 2=overline, 3=line-through
5.6 | direction           | 2 bits | 0= Left Right, 1=Right Left, 2=Top Bottom, 3=Bottom Top
5.8| Style End Code       | 1      | (ASCII Non-printable characters are allowed) Puts the Style back into the last style. 

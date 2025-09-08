# **RAID Metadata Header Standard**

This document defines a 2-byte (16-bit) header for file chunks stored in a distributed, RAID-like system. The purpose of this header is to provide sufficient information for a client to correctly reassemble the original data from its constituent chunks, including handling various parity schemes.

## **Header Structure (16 bits)**

The header is designed to be compact and efficient, using bitwise operations for encoding and decoding.

**Visual Bitfield Layout:**

Bit: | 15 14 13 12 11 | 10  9  8  7  6 | 5  4  3 |    2    |  1  0  |  
---|----------------|----------------|---------|---------|-------|  
Field | TotalStripes (N)   |  StripeIndex(i)   | RAID Type   | IsParity? | Parity Type|  

## **Field Definitions**

Below are the detailed definitions for each field in the 16-bit header.

### **1\. TotalStripes (N)**

* **Bits:** 15-11 (5 bits)  
* **Description:** The total number of servers or stripes in the complete RAID set.  
* **Encoding:** This value is stored as N-1. This allows the 5 bits (0-31) to represent a total of 1 to 32 stripes.  
* Code Table:  
  | Encoded Value | Actual Number of Stripes (N) |  
  | :------------ | :--------------------------- |  
  | 00000 (0) | 1 |  
  | 00001 (1) | 2 |  
  | ... | ... |  
  | 11111 (31)| 32 |

### **2\. StripeIndex (i)**

* **Bits:** 10-6 (5 bits)  
* **Description:** The zero-based index of this specific file chunk within the stripe set. The index ranges from 0 to N-1.  
* Code Table:  
  | Encoded Value | Meaning |  
  | :------------ | :--------------------------- |  
  | 00000 (0) | This is the first chunk of the stripe (Stripe 0\) |  
  | 00001 (1) | This is the second chunk of the stripe (Stripe 1\) |  
  | ... | ... |  
  | 11111 (31)| This is the 32nd chunk of the stripe (Stripe 31\) |

### **3\. RAID Type**

* **Bits:** 5-3 (3 bits)  
* **Description:** Defines the RAID level or parity scheme being used for the stripe set.  
* Code Table:  
  | Encoded Value | RAID Scheme | Description |  
  | :------------ | :---------- | :---------- |  
  | 000 | RAID 0 | Simple striping with no parity. |  
  | 001 | RAID 1 | Mirroring. Data is duplicated. StripeIndex can be used to identify primary vs. mirror copy. |  
  | 010 | RAID 5 | Striping with single, rotating parity (Horizontal Parity). |  
  | 011 | RAID 6 | Striping with two independent parities (e.g., Horizontal and Vertical). |  
  | 100 | RAID-DP | Striping with two independent parities (e.g., Horizontal and Diagonal). |  
  | 101 | Grid Parity| A product code scheme with multiple parity types (e.g., Horizontal, Vertical, Diagonal). See Parity Type re-definition below. |  
  | 110-111 | Reserved | Reserved for future or custom schemes. |

### **4\. IsParity Flag**

* **Bits:** 2 (1 bit)  
* **Description:** A simple flag to indicate whether the chunk contains user data or calculated parity information.  
* Code Table:  
  | Encoded Value | Meaning |  
  | :------------ | :------ |  
  | 0 | Data Block |  
  | 1 | Parity Block|

### **5\. Parity Type**

* **Bits:** 1-0 (2 bits)  
* **Description:** If IsParity is set to 1, this field specifies the type of parity this block represents. It is ignored if IsParity is 0\.  
* Code Table (for RAID 0-DP):  
  | Encoded Value | Parity Type | Used In |  
  | :------------ | :---------- | :------ |  
  | 00 | None / Not Applicable | Used for all Data Blocks. |  
  | 01 | P Parity (Primary) | The primary parity calculation (e.g., horizontal XOR). Used in RAID 5, 6, DP. |  
  | 10 | Q Parity (Secondary) | The secondary, independent parity calculation. Used in RAID 6, DP. |  
  | 11 | Reserved | Reserved for a potential third parity block. |  
* Code Table (Re-defined for Grid Parity):  
  | Encoded Value | Parity Type | Description |  
  | :------------ | :---------- | :---------- |  
  | 00 | None / Not Applicable| Used for all Data Blocks. |  
  | 01 | Horizontal Parity| Parity calculated across a row of data. |  
  | 10 | Vertical Parity| Parity calculated down a column of data. |  
  | 11 | Diagonal Parity| Parity calculated across a diagonal of data. The StripeIndex differentiates between different diagonal sets. |

## **Examples**

### **Scenario 1, 2, 3... (Standard RAID levels remain the same)**

...

### **Scenario 4: Grid Parity (Maximum Fault Tolerance with 26 Servers)**

![26 Server Mega RAID](/IMG/s4.png?raw=true "For 26 servers")

* **Configuration:** A 5x5 grid of 25 servers, plus one additional server for a second diagonal parity, for a total of 26 servers. This scheme uses horizontal, vertical, and two diagonal parity calculations for extremely high fault tolerance.  
* **Constant Header Values:**  
  * TotalStripes: 26 \-\> Encoded as 25 (11001)  
  * RAID Type: Grid Parity \-\> 101

| Stripe Index (i) | Block Type | IsParity | ParityType | Final Hex Header |  
---|---|---|---|---
| 0 | Data | 0 | 0 (00) | 0xC828 |  
| 1 | Data | 0 | 0 (00) | 0xC868 |  
| 2 | Data | 0 | 0 (00) | 0xC8A8 |  
| 3 | Data | 0 | 0 (00) | 0xC8E8 |  
| 4 | Horizontal Parity | 1 | 1 (01) | 0xC92D |  
| 5 | Data | 0 | 0 (00) | 0xC968 |  
| 6 | Data | 0 | 0 (00) | 0xC9A8 |  
| 7 | Data | 0 | 0 (00) | 0xC9E8 |  
| 8 | Data | 0 | 0 (00) | 0xCA28 |  
| 9 | Horizontal Parity | 1 | 1 (01) | 0xCA6D |  
| 10 | Data | 0 | 0 (00) | 0xCAA8 |  
| 11 | Data | 0 | 0 (00) | 0xCAE8 |  
| 12 | Data | 0 | 0 (00) | 0xCB28 |  
| 13 | Data | 0 | 0 (00) | 0xCB68 |  
| 14 | Horizontal Parity | 1 | 1 (01) | 0xCBAD |  
| 15 | Data | 0 | 0 (00) | 0xCBE8 |  
| 16 | Data | 0 | 0 (00) | 0xCC28 |  
| 17 | Data | 0 | 0 (00) | 0xCC68 |  
| 18 | Data | 0 | 0 (00) | 0xCCA8 |  
| 19 | Horizontal Parity | 1 | 1 (01) | 0xCCED |  
| 20 | Vertical Parity | 1 | 2 (10) | 0xCD2E |  
| 21 | Vertical Parity | 1 | 2 (10) | 0xCD6E |  
| 22 | Vertical Parity | 1 | 2 (10) | 0xCDAE |  
| 23 | Vertical Parity | 1 | 2 (10) | 0xCDEE |  
| 24 | Diagonal Parity 1 | 1 | 3 (11) | 0xCE2F |  
| 25 | Diagonal Parity 2 | 1 | 3 (11) | 0xCE6F |

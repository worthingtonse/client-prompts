# **RAID Metadata Header Standard**

This document defines a 2-byte (16-bit) header for file chunks stored in a distributed, RAID-like system. The purpose of this header is to provide sufficient information for a client to correctly reassemble the original data from its constituent chunks, including handling various parity schemes.

## **Header Structure (16 bits)**

The header is designed to be compact and efficient, using bitwise operations for encoding and decoding.

**Visual Bitfield Layout:**

Bit: | 15 14 13 12 11 | 10  9  8  7  6 | 5  4  3 |    2    |  1  0  |  
     |----------------|----------------|---------|---------|-------|  
Field:  TotalStripes   |  StripeIndex   | RAID    | IsParity| Parity|  
     |      (N)       |      (i)       | Type    |         | Type  |

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
  | 100 | RAID-DP | Striping with two independent parities (e.g., Horizontal and Diagonal). Functionally similar to RAID 6 but may imply a different calculation method. |  
  | 101-111 | Reserved | Reserved for future or custom schemes. |

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
* Code Table:  
  | Encoded Value | Parity Type | Used In |  
  | :------------ | :---------- | :------ |  
  | 00 | None / Not Applicable | Used for all Data Blocks. |  
  | 01 | P Parity (Primary) | The primary parity calculation (e.g., horizontal XOR). Used in RAID 5, 6, DP. |  
  | 10 | Q Parity (Secondary) | The secondary, independent parity calculation (e.g., vertical, diagonal). Used in RAID 6, DP. |  
  | 11 | Reserved | Reserved for a potential third parity block (RAID-TP). |

## **Examples**

Let's illustrate with a few scenarios.

### **Scenario 1: RAID 0 (Striping)**

* **Configuration:** 8 servers, simple striping.  
* **Chunk:** The 3rd chunk (index 2\) of a file.  
* **Header Values:**  
  * TotalStripes: 8 \-\> Encoded as 7 (00111)  
  * StripeIndex: 2 (00010)  
  * RAID Type: RAID 0 \-\> 000  
  * IsParity: No \-\> 0  
  * ParityType: N/A \-\> 00  
* **Binary Header:** 00111 00010 000 0 00 \-\> 0011 1000 1000 0000  
* **Hex:** 0x3880

### **Scenario 2: RAID 5 (Horizontal Parity)**

* **Configuration:** 5 servers (4 data \+ 1 parity).  
* **Parity Location:** For this stripe, the parity block is on the last server (index 4).

**A) Header for a Data Block (e.g., the 1st chunk, index 0):**

* **Header Values:**  
  * TotalStripes: 5 \-\> Encoded as 4 (00100)  
  * StripeIndex: 0 (00000)  
  * RAID Type: RAID 5 \-\> 010  
  * IsParity: No \-\> 0  
  * ParityType: N/A \-\> 00  
* **Binary Header:** 00100 00000 010 0 00 \-\> 0010 0000 0001 0000  
* **Hex:** 0x2010

**B) Header for the Parity Block (chunk at index 4):**

* **Header Values:**  
  * TotalStripes: 5 \-\> Encoded as 4 (00100)  
  * StripeIndex: 4 (00100)  
  * RAID Type: RAID 5 \-\> 010  
  * IsParity: Yes \-\> 1  
  * ParityType: P Parity \-\> 01  
* **Binary Header:** 00100 00100 010 1 01 \-\> 0010 0001 0001 0101  
* **Hex:** 0x2115

### **Scenario 3: RAID 6 (Horizontal \+ Vertical Parity)**

* **Configuration:** 8 servers (6 data \+ 2 parity).  
* **Parity Location:** P parity is on index 6, Q parity is on index 7\.

**Header for the Q Parity Block (chunk at index 7):**

* **Header Values:**  
  * TotalStripes: 8 \-\> Encoded as 7 (00111)  
  * StripeIndex: 7 (00111)  
  * RAID Type: RAID 6 \-\> 011  
  * IsParity: Yes \-\> 1  
  * ParityType: Q Parity \-\> 10  
* **Binary Header:** 00111 00111 011 1 10 \-\> 0011 1001 1101 1110  
* **Hex:** 0x39DE
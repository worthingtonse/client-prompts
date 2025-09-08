# **RAID Metadata Header Standard**

This document defines a 2-byte (16-bit) header for file chunks stored in a distributed, RAID-like system. The purpose of this header is to provide sufficient information for a client to correctly reassemble the original data from its constituent chunks, including handling various parity schemes.
## Recommended RAID Usage
For maximum fault tolerance, it is recomended that you use grid RAID with either [ten](#ten-servers), [seventeen](#seventeen-servers), [twenty six](#twenty-six-servers) servers. You can also use Grid RAID by removing the Diagnal Parity and reduce the servers to eight, fifteen or twenty four. 

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
![RAID 5](IMG/s2.png?raw=true "RAID 5")
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
![RAID 5](IMG/s3.png?raw=true "RAID 6")
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

...

### **Scenario 4: Grid Parity (Maximum Fault Tolerance with 26 Servers)**
## Twenty Six Servers
![26 Server Mega RAID](IMG/s4.png?raw=true "For 26 servers")

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

## Seventeen Servers
| Stripe Index (i) | Block Type | IsParity | ParityType | Final Hex Header |  
---|---|---|---|---
| 0 | Data | 0 | 0 (00) | 0xC828 |  
| 1 | Data | 0 | 0 (00) | 0xC868 |  
| 2 | Data | 0 | 0 (00) | 0xC8A8 |  
| 3 |  Horizontal Parity | 1 | 1 (01) | 0xC92D |  
| 4 | Data | 0 | 0 (00) | 0xC968 |  
| 5 | Data | 0 | 0 (00) | 0xC9A8 |  
| 6 | Data | 0 | 0 (00) | 0xC9E8 |  
| 7 | Horizontal Parity | 1 | 1 (01) | 0xCA6D |  
| 8 | Data | 0 | 0 (00) | 0xCAA8 |  
| 9 | Data | 0 | 0 (00) | 0xCAE8 |  
| 10 | Data | 0 | 0 (00) | 0xCB28 |  
| 11 | Horizontal Parity | 1 | 1 (01) | 0xCBAD |  
| 12 | Vertical Parity | 1 | 2 (10) | 0xCD2E |  
| 13 | Vertical Parity | 1 | 2 (10) | 0xCD6E |  
| 14 | Vertical Parity | 1 | 2 (10) | 0xCDAE |  
| 15 | Diagonal Parity 1 | 1 | 3 (11) | 0xCE2F |  
| 16 | Diagonal Parity 2 | 1 | 3 (11) | 0xCE6F |


### **Scenario 5: Grid Parity (4x4 Grid \- 17 Servers)**

* **Configuration:** Based on a 4x4 grid, using 9 data servers (3x3), 3 horizontal parity, 3 vertical parity, and 2 diagonal parity servers for a total of 17\.  
* **Constant Header Values:**  
  * TotalStripes: 17 \-\> Encoded as 16 (10000)  
  * RAID Type: Grid Parity \-\> 101

| Stripe Index (i) | Block Type | IsParity | ParityType | Final Hex Header |
| :---- | :---- | :---- | :---- | :---- |
| 0 | Data | 0 | 0 (00) | 0x8028 |
| 1 | Data | 0 | 0 (00) | 0x8068 |
| 2 | Data | 0 | 0 (00) | 0x80A8 |
| 3 | **Horizontal Parity** | 1 | 1 (01) | 0x80ED |
| 4 | Data | 0 | 0 (00) | 0x8128 |
| 5 | Data | 0 | 0 (00) | 0x8168 |
| 6 | Data | 0 | 0 (00) | 0x81A8 |
| 7 | **Horizontal Parity** | 1 | 1 (01) | 0x81ED |
| 8 | Data | 0 | 0 (00) | 0x8228 |
| 9 | Data | 0 | 0 (00) | 0x8268 |
| 10 | Data | 0 | 0 (00) | 0x82A8 |
| 11 | **Horizontal Parity** | 1 | 1 (01) | 0x82ED |
| 12 | **Vertical Parity** | 1 | 2 (10) | 0x832E |
| 13 | **Vertical Parity** | 1 | 2 (10) | 0x836E |
| 14 | **Vertical Parity** | 1 | 2 (10) | 0x83AE |
| 15 | **Diagonal Parity 1** | 1 | 3 (11) | 0x83EF |
| 16 | **Diagonal Parity 2** | 1 | 3 (11) | 0x842F |

### **Scenario 6: Grid Parity (3x3 Grid \- 10 Servers)**

* **Configuration:** Based on a 3x3 grid, using 4 data servers (2x2), 2 horizontal parity, 2 vertical parity, and 2 diagonal parity servers for a total of 10\.  
* **Constant Header Values:**  
  * TotalStripes: 10 \-\> Encoded as 9 (01001)  
  * RAID Type: Grid Parity \-\> 101

| Stripe Index (i) | Block Type | IsParity | ParityType | Final Hex Header |
| :---- | :---- | :---- | :---- | :---- |
| 0 | Data | 0 | 0 (00) | 0x4828 |
| 1 | Data | 0 | 0 (00) | 0x4868 |
| 2 | **Horizontal Parity** | 1 | 1 (01) | 0x48AD |
| 3 | Data | 0 | 0 (00) | 0x48E8 |
| 4 | Data | 0 | 0 (00) | 0x4928 |
| 5 | **Horizontal Parity** | 1 | 1 (01) | 0x496D |
| 6 | **Vertical Parity** | 1 | 2 (10) | 0x49AE |
| 7 | **Vertical Parity** | 1 | 2 (10) | 0x49EE |
| 8 | **Diagonal Parity 1** | 1 | 3 (11) | 0x4A2F |
| 9 | **Diagonal Parity 2** | 1 | 3 (11) | 0x4A6F |





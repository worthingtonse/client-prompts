# RAID Type
RAID means a Redundant Array of Indpendent Disks and is different that RAIDA. RAID is used to make it possible for hard drives to crash without losing data. The Raida has the same
properties and there are many ways to spread data files over the Raida to keep from losing data. It is up to the client to decide how to write data
in ways that conservs server storage space vs take losses of data without losing emails and attachments. 


QMail supports multiple RAID types for data redundancy:

| RAID Type | ID | Description |
|-----------|----| ------------|
| Stripe | 0 | Data striped across multiple servers | Increases the odds of losing data greatly. 
| Mirror | 1 | Data mirrored across servers | Two raidas have the same data. Requiers two raida. It uses twice the amount of data to achieve fault tolerance and is inefficient. 
| Stripes with Parity | 5 | Striped with single parity | Uses one extra server to restor data should one of the other servers fail. 
| Stripe with Vertical Parity | 6 | Striped with vertical parity | This increases the number of servers dedicated to fault tolerance and allows more than one server to fail without data loss. 
| Stripe with H/V Parity | 7 | Horizontal and vertical parity | This radically increases the number of raida that can fail without dataloss. Military grade protection. 
| Stripe with H/V/D Parity | 8 | Horizontal, vertical, and diagonal parity | Even more protection than ID 7
| Mirrored Stripes | 10 | Combination of striping and mirroring | This is ID 0 that is mirrored. Needs and even number of servers. Half are mirrors of the other half. 

The following must be standard for sender and receiver. 

## Stripe ID 0
Adding more raida servers increases the risk of data loss. Data that is striped over 25 servers is 25 times more likely to loss data than if there was just one raida server. 
However, stripes are the fastest to read and write from. Stipes are high performance at the expense of fault tolernacne.

## Mirror ID 1
This requires two raida and is not secure since the whole unstriped documant is stored on two raidas where it can be read by the raida admin. This should not be used. 

## Stripes with Parity
A minimum of three stripes are needed.

RAID Code | Number of Servers | Data Stripes | Falt Tolerance (Parity) Stripes 
---|---|---|---
0 | N | N | 0
1 | 2 | 1 | 1
5 | N | N - 1 | 1
3 | 2 | 1 |
3 | 2 | 1 |




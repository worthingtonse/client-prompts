# QMail Overview
QMail incorporates a lot of new technologies including:
* [QKE](qkey.md) (Quantum Safe Key Exchange) a Distributed Key Exchange that is quantum safe
* [CCs](#cloudcoin.md) (CloudCoins) for mitrans (microtransactions) 
* [CBDF](#cbdf.md)(Compact Binary Document Format) for sending and receiving information
* [DRD](#drd.md) (Distributed Resource Directory) for locating users and other resources  
* [QMail](#qmail) Raida Protcol. 

To make things easier to understand, this document with include the hyperlinks above to a document that explains 
each of these components. 

## Work Flow
1. The QMail Server Admins registers* their servers with the Root RAIDA to place a record in the DRD (Distributed Resource Directory)
2. The QMail Users search* the DRD to find QMail Servers that  wants to use use to hire to store their email on.
3. The QMail Users use the QKE to exchange keys between their computers and the QMail servers that they hired.
4. The QMail Users register* themselves in the DRD (assuming they want to be found by others and use QMail's advanced functionality
5. The QMail Users exchange usernames or find* the usernames of others in the DRD.
6. The QMail Sender sends* CBDF email files and attachments to one or more other users between 800MB to 3.2TB maximum. 
7. The QMail Server Admins check the receiver's receiving rules in the DRD, processes the payment and stores the data.
8. The QMail Receiver  

* These operations cost CloudCoins in order to stop DDOS, Stop malevelent activity and pay the server administrators.
* The cost of sending mail and attachments depends on size. e.g. 800MB costs 32 CCs while 3.2 TB costs 128 CCs.
*  


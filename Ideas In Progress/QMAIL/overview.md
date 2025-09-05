# QMail Overview
QMail incorporates a lot of new technologies that make the system a bit more complicated to 
implement but easy enough for the users. The QMail system provides for true privacy and quantum safe 
transmission. QMail allows people to get paid for their attention through a system of tips. This allows famouse person could charge thousands of dollars to recieve an email and eliminates the ability of spammers and phishers to be able to operate. 

QMail server admins can take a cut of their customer's payments (Tips) and compete for customers ensuring the whole system is efficient and producitve. Admins can compete on price, quickness of replies, maximum email attachment size, screening of malevelon senders, level of trust, political juristictions, geolgraphical location and fault tolerance. In this way, QMail eliminmates the need for data centers to be run by tech giants and distributes the IT economy. Users can even choose to use QMail servers that are admistrated by their friends and families.

QMail radically reduces the size of emails by using the CBDF protocol. The CBDF is a novel alternative to HTML, CSS and JavaScript that may only be 1% of the bytes needed for an equivilant email used today. The QMail system nearly eliminates the bandwidth and storage space required to support spam and phishing. Emails sent to groups are stored securily in shared distributed storage eliminating the need for servers to save multiple copies of the same thing. The CBDF allows formatted emails to be filtered into plain text so that emails do not have to include both formatted and text version of the same email. Users can be required to download their emails to read them instead of keeping them on the servers. This massive reduction in needed system resources (bandwith, harddrives, RAM, processor power, electricity, physical space), allows the general public to host these QMail servers in their garages using old computers.

The system is inherintly secure because email messages are shred bit by bit into "Stripes" that can be distibued accross between 2 to 32 mail servers. Each stripe is encypted using its own 256 AES CTR encryption key. These keys are exchanged using the quantum safe QKE. Each stripe maybe routed through different networks so that tappers are less likely to be able to capture all the stipes needed to even attempt to dectypt. E.g. a sender could have internet access through Starlink satilite, T-Mobile cellular and Comcast Cable. Stripes could be spread out over these. The order in which the stripes are placed can be randomized so that it is unknown in which order they need to be put back together in and makes it impossible for a mail server admin to know what order they are in unless he is able to get the email from 
all 32 mail servers. Users who store just one QMail server in their house are vertually guaranteed privacy that this is impossible. 

The only data that can be understood from a message is some meta data. If the QVPN service (work in
progress) is used, then only the following can be know by anyone except the QMail Administrator. 

1. That users are using a VPN, but only If the tapper can associate the VPN origination IP to the user.

Regardless of the use of VPNs, the QMail Adminstrators would be able to know the additional meta information: 
1. The sender and receiver's 7-byte user ID which is psudo annonymous like a Bitcoin Addresses
2. The time the sender sent the message and the time that the receiver collected messages.
3. The IP addresses of the sender and receiver.
4. The number of bytes in a message can be infered. 

To fathum what it would be required for a QMail administrator to infire any meaning from a message, the administrator would need to: 
1. Capture up to 32 stripes of data that maybe traveling on many different networks.
2. Decrypt a quantum safe stripe of data that has 115,792,089,237,316,195,423,570,985,008,687,907,853,269,984,665,640,564,039,457,584,007,913,129,639,936 different combinations.
3. Repeat step 2 up to 32 times.
5. Decrypt the message's public key encryption using a quantum computer.
6. Unshuffle the transposition cipher that may have up to 263,130,836,933,693,530,167,218,012,160,000,000 different combinations. This cipher requires that the attacker decypt all of the stripes to infer any meaning. 

For QMail Administrators to be able to infer any information, they would need to:
1. Have access to all of the receiver's QMail server's hard drives to get all the message's stripes.
2. Decrypt the message's public key encryption using a quantum computer.
3. Decrypt all the stripes to decypt the transposition cipher that may have up to 263,130,836,933,693,530,167,218,012,160,000,000 different combinations.


## Glossary of QMail Terms
 Here are some terms that are useful to know:

* [QMail](#qmail) A protocol for sending and receing quantum-safe distributed messages.
* [qmail](#qmail) The lowercase version of QMail allows for people to differentiate between email and qmail. 
* [QKE](qkey.md) (Quantum-Safe Key Exchange) a Distributed 256 bit AEAS Key Exchange that is quantum safe.
* [Chips](#cloudcoin.md) Raida-based currency used to pay for services. These are true digial cash denominations that do not require a public ledger. The user is not required to have an account or password. 
* [Tip] A microtransaction paid in Chips. Often included in a request for service. 
* [CBDF](#cbdf.md)(Compact Binary Document Format) for sending and receiving information.
* [qmail File](#qmail-file.md) The CBDF used in qmails. Has a qmail extension like "MyMessage.qmail". 
* [DRD](#drd.md) (Distributed Resource Directory) a public CBDF file for QMail users to publish their presence and for locating users' QMail addresses and other network resources such as servers for RAIDA, Key Exchange and QMail.
* [CloudCoin](#CloudCoin)The first and default Chip used for QMail tips.
* [ACL](#acl.md) The receiver's Access Control List kept in the DRD that the reciever can use to add other uses to the built-in White List and Black List groups.   

To make things easier to understand, this document with include the hyperlinks above to a document that explains each of these components. 

## Work Flow
1. The QMail Server Admins registers* their servers with the Root RAIDA if they want to publish there IP address and other valuable information needed by the public.
2. The QMail Users search* the DRD to find QMail Servers they can hire to store their qmail on.
3. The QMail Users use the QKE to exchange keys between their computers and the QMail servers that they employ.
4. The QMail Users register* themselves in the DRD assuming they want to be found by others and use QMail's advanced functionality
5. The QMail Users exchange usernames or find* the usernames of others in the DRD.
6. The QMail Sender sends* qmail file and attachments to one or more other users. Byte limits depend on the QMail Server Administrators and may be between 800MB to 3.2TB maximum per message
7. * The cost of sending mail and attachments depends on size. e.g. 800MB costs 32 CCs while 3.2 TB costs 128 CCs.
8. The QMail Server Admins check the receiver's ACL (Access Control Lists) in the DRD, processes the payment and stores the data for the receiver.
9. The QMail Receiver downloads   

* These operations cost CloudCoins in order to stop DDOS, Stop malevelent activity and pay the server administrators.

*  


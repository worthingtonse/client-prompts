# QMail Overview

QMail is developed by the **Perfect Money Foundation**, an organization dedicated to engineering distributed information systems that champion strong user privacy and a decentralized internet economy (Web 3.0). Our mission is to foster a more equitable and resilient digital ecosystem, not controlled by a few tech giants or surveillance organizations.

Benefits of QMail
1. Possible to edit send qmails if it has not been read yet.
2. Quantum Safe Storage and Transmission
3. No Tech Giants
4. Better Naming Conventions
5. No servailance
6. Email files are 90% smaller.
7. Images embedded in qmain can be downloaded without
8. Terabytes attachments
9. Get paid for your attention
10. Messages are sent fastest

### Glossary of Terms

  * **[ACL](access-control-list.md) (Access Control List)**: A list stored in a user's DRD that the receiver uses to manage permissions by adding other users to built-in groups like a White List or Black List.
  * **[CBDF](compact-binary-document-format.md) (Compact Binary Document Format)**: The proprietary binary format used for structuring and sending information within the QMail protocol.
  * **[Chips](chips.md)**: A RAIDA-based digital currency used to pay for services. As a form of digital cash, it does not require a public ledger, accounts, or passwords.
  * **[CloudCoin](cloudcoin.md)**: The first and default implementation of **Chips** used for QMail tips.
  * **[DRD](distributed-resource-directory.md) (Distributed Resource Directory)**: A public directory file used to publish a user's presence and locate QMail addresses and other network resources, such as servers for RAIDA and **DKE**.
  * **[PMF](perfect-money-foundation.md) (Perfect Money Foundation)**: The organization that created and maintains the QMail standard and its related technologies.
  * **[DKE](quantum-safe-key-exchange.md) (Distributed Key Exchange)**: A distributed system for securely exchanging 256-bit AES encryption keys that is quantum-safe.
  * **[QMail](qmail-protocol.md)**: An open protocol for sending and receiving quantum-safe, distributed messages. A message sent via the protocol is often called a "qmail."
  * **[qmail file](qmail-file.md)**: A file with a `.qmail` extension that contains the message content in the **CBDF** format.
  * **[STC](shuffle-transposition-cipher.md) (Shuffle Transposition Cipher)**: A method of sharding a message so that all shards are required for decryption. This is designed to prevent partial information leaks, even if an attacker gains access to some of the shards.
  * **[Tip](tip.md)**: A microtransaction, paid in **Chips**, that is often included in a request for service.## QMail Open Standard

## Open Standard
The QMail protocol is an open standard for decentralized communication, free for any person or organization to implement.


### License

This specification document is licensed under the **Creative Commons Attribution-ShareAlike 4.0 International License (CC BY-SA 4.0)**.

> This means you are free to share and adapt this standard, even for commercial purposes, as long as you give appropriate credit and distribute any adaptations under the same license.

To view a copy of this license, visit:
[http://creativecommons.org/licenses/by-sa/4.0/](http://creativecommons.org/licenses/by-sa/4.0/)

The QMail service works with other PMF open standards that are being released at the same time such as Quantum Key Exchange, Distributed Resource Directory, Compact Binary Document Format, Compact Binary Mail Format and the Redundant Array of Independent Detection Agents. Other services being developed are QWeb, QText, QVPN and QData. 

## Open Source Software
In addition to the open standards, the PMF is releasing open source code and AI prompts that can be used to create and modify the software needed to make client and server software. This software is released with an MIT license.

## The Distributed Resource Directory

The Root Distributed Resource Directory (DRD), maintained by the PMF, serves as a public directory where users can publish information about their servers, contact details, and other network resources.

### Registration

While the registration of most resources like servers and QMail addresses is optional, the registration of **Chip IDs** is mandatory. This requirement is in place to ensure the fair allocation of the limited number of available IDs and to prevent squatting or unauthorized use.

The Root DRD maintains the definitive list of all registered Chip IDs.

### Registration Fees

To fund the ongoing development of the QMail ecosystem, the PMF charges modest fees for publishing resources in the Root DRD. Revenue from these fees directly supports the creation of new features and the maintenance of the open-source software.

Fees are required to register resources such as:

* **Server Endpoints**: Servers for QMail, QKE, RAIDA, address verification, and currency swaps.
* **Unique Identifiers**: QMail addresses and most Chip IDs (excluding the freely usable ID 127).
* **Public Documents**: CBDF standard definitions, document pointers, files, and text records.

### Benefits of QMail

The QMail system is designed to provide robust privacy and quantum-safe message transmission. It also introduces a novel economic model, allowing users to get paid for their attention through a system of 'tips'. For example, a high-profile individual could set a high tip fee to ensure the qmails they receive are substantive.

This same mechanism empowers all users to eliminate spam and phishing attempts by setting a prohibitive cost for unknown senders. Friends, family, and trusted contacts can be added to a whitelist, allowing them to send messages without a fee.

### System Administration

QMail server administrators can earn a percentage of the tip payments processed by their servers. This creates a competitive marketplace where admins are incentivized to provide efficient and reliable services. Admins can compete on a variety of factors, including:

* Price and fee structure
* Speed of message processing
* Maximum attachment size
* Screening of malicious senders
* Trust, political jurisdiction, and geographical location
* Fault tolerance and uptime

This model fosters a distributed IT economy, reducing the reliance on centralized data centers run by tech giants. Users can choose servers administered by anyone, from established businesses to trusted friends, and can distribute their messages across multiple servers for enhanced resilience. While using more servers improves security and reliability, it may also increase costs.

### QMail Efficiency

QMail radically reduces message size by using the Compact Binary Document Format (CBDF). As a novel alternative to HTML, a CBDF-formatted message can be as little as 1% of the size of an equivalent modern email. For example, instead of creating an email's layout using HTML and CSS, qmails have 255 unique layouts to choose from making it possible to create the qmail layout with one byte. Qmail layouts are made up of panels that can themselves be divided into sub panels using one byte. Each panel is described by a 16-byte code. Colors are reduced from 16,777,216 to 65,535 choices. The number of fonts possible are limited to 256. Since this is all encoded in binary, it is extreemly effficient. 

This efficiency nearly eliminates the bandwidth and storage required to handle spam. Furthermore, messages sent to groups are stored securely in shared distributed storage, removing the need for servers to hold multiple copies. This massive reduction in required system resources (bandwidth, storage, RAM, electricity) makes it feasible for individuals to host QMail servers on consumer-grade hardware.

### QMail Privacy

**Architectural Privacy**
QMail's security is inherent to its architecture. Messages are sharded into 2 to 32 encrypted "stripes," which can be distributed across multiple mail servers. Each stripe is encrypted with a unique AES-256 key, established using the quantum-safe QKE protocol.

These stripes can be routed through different physical networks (e.g., satellite, cellular, and cable), making it extraordinarily difficult for an attacker to intercept all the components of a single message. The storage order of the stripes on the servers can also be randomized, making reassembly impossible without the correct metadata.

**Metadata Considerations**
The only data an observer can glean from a message is the sender's ID. This ID is an alias and is psudo anonymous like the address of a Bitcoin user. Even so, if a VPN service is used, such as our upcomming Qvpn, an external observer can't even see the sender's ID.

The biggest threat are the QMail administrators themselves. QMail admins are able to see the folloing meta data:
* The sender and receiver's 7-byte pseudo-anonymous user ID.
* The IP addresses of the sender and receiver.
* The time when the message was sent and received.
* An approximation of the message's total size in bytes.

**Threat Model: Decryption Feasibility**
To comprehend the difficulty of compromising a QMail message, consider the steps an attacker would need to complete.

***An External Attacker or Malicious QMail Administrator would need to:***
1.  **Capture All Stripes:** Intercept up to 32 message stripes, which may be traveling across completely different global networks.
2.  **Break Public Key Encryption:** Decrypt the message's session key using a quantum computer.
3.  **Break AES-256 (x32):** Decrypt each of the individual stripes, each secured with AES-256 (a key space of $2^{256}$).
4.  **Break the Transposition Cipher:** Unshuffle the stripes, a task with up to 32! (over $2.6 \times 10^{35}$) combinations, which requires all stripes to be decrypted first.

### Securing the Client

Server-side encryption is ineffective if the user's device is compromised. To mitigate this risk, the QMail client is designed to run as a portable application from a USB drive, where all keys and CloudCoins are stored.

This data is encrypted with the user's password. For added security, the application will automatically log the user out and eject the USB drive after a period of inactivity.



# Development Phases

## Phase I: Foundational Workflow

In this initial phase, the core messaging functionality is established without a public directory.

1.  **Server Discovery**: The client downloads a basic, static directory to locate the initial beta QMail servers.
2.  **Key Exchange**: Users establish secure keys with their chosen QMail servers via the QKE protocol.
3.  **Contact Exchange**: Users must exchange their user IDs manually (e.g., over another secure channel).
4.  **Sending Messages**: Users can send plain-text qmails with small attachment limits. No tips or fees are implemented yet.
5.  **Receiving Messages**: The client periodically polls the QMail servers for new messages.
6.  **Message Download**: The receiver downloads their qmails and attachments for local storage and viewing.

## Phase II: Public Directory and Economy

This phase introduces the public DRD and the CloudCoin-based economy.

1.  **Server Registration***: Server admins register their services in the Root DRD to publish their IP addresses, fees, and other metadata.
2.  **Server Discovery***: Users can search the DRD to find and hire QMail servers that meet their needs.
3.  **Key Exchange**: Users perform the QKE with their hired servers.
4.  **User Registration***: Users can register in the DRD to be discoverable and access advanced features.
5.  **Contact Discovery***: Users can find each other by searching for usernames in the DRD.
6.  **Sending Messages***: Senders transmit qmails and attachments, with size limits and costs determined by the server admin.
    * *Cost Example: An 800 MB message might cost 32 CC, while a 3.2 GB message could cost 128 CC.*
7.  **Processing and Storage**: The destination server verifies the receiver's ACL, processes the tip payment, and stores the message.
8.  **Message Download**: The receiver is notified and can download the message.

***
*\*These operations require a small payment in CloudCoins to prevent DDoS attacks, deter malicious activity, and incentivize server administrators.*
***

## Phase III: Advanced Features

The third phase will focus on expanding functionality and decentralization.

1.  **Rich Content**: Implementation of message formatting using CBDF.
2.  **Advanced DRD**: Enhanced search capabilities and expanded data storage options within the directory.
3.  **Decentralized Administration**: Development of trust and registration systems for independent server administrators.

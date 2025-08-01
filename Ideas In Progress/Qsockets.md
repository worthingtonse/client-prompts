# QSocket 
QSocket is a quantum safe protocol that uses a new patent-pending key exchange system that does not need to be included in the diagrams.

## Requirements
1. Users can swap keys before hand to have a 256 bit encrypted session.
2. People can apply to have access to the QSocket server using the KYC prossess.
3. Must have mutual authentication.
4. There must be a white list and a black list.
5. There must be a list of resources.
6. Must be a list of users
7. List of User Groups
8. List of Resource Groups.
9. 

### Here is how the protocol works: 

The user's client application (such as a DNS service) wants to make a call to a server such as 1.1.1.1 to resolve an IP address. 

The client's request is sent to the QSocket Client software running locally.  

QSocket client takes the request and copies the IPv4 and TCP headers into 25 different request buffers. 

Then, QSocket Client takes the message encapsilated in the transport header and stripes it into 16 data stripes. These stipes are aranged logically as a 4x4 square. 

Then the QSocket Cient creates nine paratiy stipes to create horizontal, vertical and one diagnal parity stipe so that there is now a logical 5x5 grid: 16 data and 9 parity. These stipes are then added to the request buffers (one stripe per buffer).

The QSocket Client then encrypts each buffer using AES and encapcilates it int a QSocket request header. Each request is then sent to one server in an array of 25 servers called the "RAIDA". Each RAIDA server is located in a different part of the world. 

Each of the 25 RAIDA servers decrypt the message, read the IP header. Then encrypt the whole thing again using the DNS server's key. Then the requests are sent to the "QSocket Server that is runninig on the DNS server. 

The DNS server's QSocket Server is listening on 25 ports and assembles the message. The message is then dumped on the DNS server so that the DNS server gets the message and can respond back the the QSocket Server. The QSocket server then does the whole process in reverse sending the message back to the QSocket Client and then to the service doing the DNS call. 


## 0. Sankey Diagram
    
```mermaid
---
config:
  sankey:
    showValues: false
---

sankey-beta
QSocket_Client,RAIDA_0,1
QSocket_Client,RAIDA_1,1
QSocket_Client,RAIDA_2,1
QSocket_Client,RAIDA_3,1
QSocket_Client,RAIDA_4,1
QSocket_Client,RAIDA_5,1
QSocket_Client,RAIDA_6,1
QSocket_Client,RAIDA_7,1
QSocket_Client,RAIDA_8,1
QSocket_Client,RAIDA_9,1
QSocket_Client,RAIDA_10,1
QSocket_Client,RAIDA_11,1
QSocket_Client,RAIDA_12,1
QSocket_Client,RAIDA_13,1
QSocket_Client,RAIDA_14,1
QSocket_Client,RAIDA_15,1
QSocket_Client,RAIDA_16,1
QSocket_Client,RAIDA_17,1
QSocket_Client,RAIDA_18,1
QSocket_Client,RAIDA_19,1
QSocket_Client,RAIDA_20,1
QSocket_Client,RAIDA_21,1
QSocket_Client,RAIDA_22,1
QSocket_Client,RAIDA_23,1
QSocket_Client,RAIDA_24,1
RAIDA_0,QSocket_Server,1
RAIDA_1,QSocket_Server,1
RAIDA_2,QSocket_Server,1
RAIDA_3,QSocket_Server,1
RAIDA_4,QSocket_Server,1
RAIDA_5,QSocket_Server,1
RAIDA_6,QSocket_Server,1
RAIDA_7,QSocket_Server,1
RAIDA_8,QSocket_Server,1
RAIDA_9,QSocket_Server,1
RAIDA_10,QSocket_Server,1
RAIDA_11,QSocket_Server,1
RAIDA_12,QSocket_Server,1
RAIDA_13,QSocket_Server,1
RAIDA_14,QSocket_Server,1
RAIDA_15,QSocket_Server,1
RAIDA_16,QSocket_Server,1
RAIDA_17,QSocket_Server,1
RAIDA_18,QSocket_Server,1
RAIDA_19,QSocket_Server,1
RAIDA_20,QSocket_Server,1
RAIDA_21,QSocket_Server,1
RAIDA_22,QSocket_Server,1
RAIDA_23,QSocket_Server,1
RAIDA_24,QSocket_Server,1


```
</div>


## 1. System Context Diagram
This diagram shows the high-level context of the QSocket system, including the user's client application, the QSocket system, the RAIDA servers, and the DNS server.


```mermaid
classDiagram
    class User_Client_Application {
        +Makes DNS request
    }
    class QSocket_System {
        +Handles quantum-safe data transfer
    }
    class RAIDA_Servers {
        +25 geographically distributed servers
        +Decrypts and forwards requests
    }
    class DNS_Server {
        +Resolves IP addresses
    }

    User_Client_Application --> QSocket_System : Sends DNS request
    QSocket_System --> RAIDA_Servers : Sends 25 encrypted request buffers
    RAIDA_Servers --> DNS_Server : Forwards requests
    DNS_Server --> RAIDA_Servers : Sends response
    RAIDA_Servers --> QSocket_System : Returns response
    QSocket_System --> User_Client_Application : Delivers response

```
## 2. Container Diagram
This diagram breaks down the QSocket system into containers: QSocket Client, QSocket Server, RAIDA Servers, and the DNS Server, showing their interactions.


```mermaid
classDiagram
    class User_Client_Application {
        +DNS Client
    }
    class QSocket_Client {
        +Runs locally on client
        +Stripes data, encrypts buffers
    }
    class RAIDA_Servers {
        +25 servers worldwide
        +Decrypts, re-encrypts, forwards
    }
    class QSocket_Server {
        +Runs on DNS server
        +Listens on 25 ports, assembles message
    }
    class DNS_Server {
        +Handles DNS resolution
    }


    User_Client_Application --> QSocket_Client : Sends DNS request
    QSocket_Client --> RAIDA_Servers : Sends 25 encrypted buffers
    RAIDA_Servers --> QSocket_Server : Forwards requests with DNS key encryption
    QSocket_Server --> DNS_Server : Delivers assembled request
    DNS_Server --> QSocket_Server : Sends response
    QSocket_Server --> RAIDA_Servers : Sends 25 response buffers
    RAIDA_Servers --> QSocket_Client : Returns response buffers
    QSocket_Client --> User_Client_Application : Delivers response


```
## 3. Component Diagram
This diagram details the internal components of the QSocket Client and QSocket Server, focusing on the data striping, encryption, and message assembly processes.



```mermaid



classDiagram


    class RAIDA_Servers {
        +Decryptor
        +ReEncryptor
        +Forwarder
    }

    class QSocket_Client {
        +RequestBufferManager
        +DataStriper
        +ParityGenerator
        +AESEncryptor
        +QSocketHeaderEncapsulator
    }
    class RequestBufferManager {
        +Creates 25 request buffers
        +Copies IPv4/TCP headers
    }
    class DataStriper {
        +Stripes message into 16 data stripes
        +Arranges as 4x4 grid
    }
    class ParityGenerator {
        +Creates 9 parity stripes
        +Forms 5x5 grid
    }
    class AESEncryptor {
        +Encrypts each buffer with AES
    }
    class QSocketHeaderEncapsulator {
        +Adds QSocket request header
    }




    class QSocket_Server {
        +PortListener
        +MessageAssembler
        +ResponseProcessor
    }
    class PortListener {
        +Listens on 25 ports
    }
    class MessageAssembler {
        +Reconstructs 5x5 grid
        +Extracts original message
    }
    class ResponseProcessor {
        +Stripes and encrypts response
        +Sends via RAIDA
    }

    class DNS_Server {
        +DNSResolver
    }

    QSocket_Client --> RequestBufferManager : Uses
    QSocket_Client --> DataStriper : Uses
    QSocket_Client --> ParityGenerator : Uses
    QSocket_Client --> AESEncryptor : Uses
    QSocket_Client --> QSocketHeaderEncapsulator : Uses
    QSocket_Client --> RAIDA_Servers : Sends 25 buffers
    RAIDA_Servers --> QSocket_Server : Forwards requests
    QSocket_Server --> PortListener : Uses
    QSocket_Server --> MessageAssembler : Uses
    QSocket_Server --> ResponseProcessor : Uses
    QSocket_Server --> DNS_Server : Delivers request
    DNS_Server --> QSocket_Server : Sends response
    QSocket_Server --> RAIDA_Servers : Sends response buffers
    RAIDA_Servers --> QSocket_Client : Returns response

```

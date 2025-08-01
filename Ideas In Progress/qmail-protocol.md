# QMail Protocol
The QMail protocol is designed to replace the existing email system. 

## Requirments

1. Must to require a domain owener to give email.
2. Does not require a the sender or receiver to have a centralized email server
3. Has a decentralized directory to that people can publish, manage and unpublish their contact information.
4. Stop Spam by making it too expensive
5. Allow users to be paid when the accept emails.
6. Not allow emails to be sent unless they have been paid for.
7. Allow anyone to create a server and earn money by hosting email services.
8. Make email impossible to hack or lose.
9. Make emails quantum safe in transmission and storage.
10. Stop people from monitoring if their emails have been opened. 
11. Reduce storage space by having common server storage areas where data objects can be accessed by multiple people.
12. Make it faster to send and receive emails.
13. Be able to accept annonymous emails but also be able to turn them away.
14. Be able to have end to end encryption that is quantum safe and uses 256 bit AES CTR encryption.
15. Remove HTML, CSS and Javascript from emails and replace it with a much lighter formatting system. 
16. Remove attachments but instead use optional downloads.
17. Being able to send an email and prove your identity if you wish.
18. Allow people to vouch for the authenticity of the sender and receiver.

## Service

[Update Directory](#update-director)

[Post Master Key](#receiver-post-master-key)

[Get Receiver's Key](#get-receiver-key)

[Read Directory](#read-directory)

[Send To Many](#send-to-many)

[Send To One](#send-to-one)

[Send Associated File](#send-associated-file)

[Fetch Email](#fetch-email)

[Fetch Attachement](#fetch-attachement)

[Set Autoresponse](#set-autoresponse)

[Vouch For or Against Sender](#vouch-for-or-against-sender)

[Confirm Receipt](#confirm-receipt)

## Update Director
This service allows a receiver to tell people how to contact them, how much it costs to send email to them and weather a sender is free or blocked. 

ERD of the Directory

**Table User**

Datatype | Name | Description
---|---|---
int | ID | Primary Key. DN SN SN SN SN (Five bytes of the user's key that show the denomination and four byte serial number)
int | Alias | The name that the person want's to be called by 
string | description  | self discription 
timestamp  | date created   | Set by system
string | Key exchange servers  |  array of raida servers used to exchange keys (ip and port)
string | Email storage servers | array of raida servers used to exchange emails (ip and port  
int | annoyed in past month  | How many people send annoymnet reports 
int | hated in past month | How many people sent hate reports for this email.  
int | User's receiving fee  | How many coins the user needs in order to accept an email
       
## 


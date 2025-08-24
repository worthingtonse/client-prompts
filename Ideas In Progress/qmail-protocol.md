# QMail Protocol
The QMail protocol is designed to replace the existing email system. 

## RAIDA Mail Folder Structure
The all-folders folder holds all the user and public files. 

Each user is identified by a five byte identifier. Each user has a folder in the private folders that is based on their identifier. The user-folder folder has 256 sub folders
named after the first hexidecimal characters in the users ID. Then, there are four levels of subfolders so that the leaf folders are five folders deep. 

Each user has some standard folders. The user can create any folders that they want but there will always be a Mail folder. 
Within the mail folder there are two types of files, file stipes (.bin) and pointers (.lnk) to file stripes that are located in the public-files. 

```
00
--Mail
----c10d92f83091496d893f8e20f30372ea.0.bin // First Version of the file. 
----c10d92f83091496d893f8e20f30372ea.1.bin // File 0 after it haws been changed. 
----c10d92f83091496d893f8e20f30372ea.2.bin
----.c10d92f83091496d893f8e20f30372ea.3.bin // File after it has been deleted (has a . infont of it. Users can still see deleted files and undelete them)
----e08b3a6835c34716bad5bfe5a6d556cc.lnk // Link to a public file. 

```

Files have a GUID for a name.

```tree
all-folders
--public-folders
----00
------00
--user-folders
----00
----01
----02
----03
----00

```
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


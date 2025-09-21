# QMail File Types
There are several different file types that users can send. They must have a .qmail file that contains the text. 
Shared secret files help rudusing the possibility of spoofing (People pretending to be other people). The Avatar files are also unique to the person group receiving the email. Attachments are numbered. 

Code | Name | Description
---|---|---
0 | Meta | This is data about the email that can be quickly downloaded. Includes Subject, TO, FROM, Date, Email ID. See [Meta File Format](meta-file-format.md)
1 | qmail | the actual qmail CBDF file with a .qmail extention
2 | Shared Secret | a shared secret CDBF file that only the receivers will see and is not published in the DRD
3 | Avatar | Graphics file
4 | Attachment | attachment


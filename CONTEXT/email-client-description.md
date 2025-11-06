I have come up with a new way to encode email files so that they can be much smaller in size. 
I need to create an encoder decoder. 
I want to create a program in the C language that gives people a wusiwug to create the email file. 

The files are basically three files in one. The first file is for meta data and we don't have to worry about that part of the file here. 

Then there is a special ascii character 'FS' the File Seperator 0x1C and then the second file which is the Style definitions. 
Then another FS byte and then text that is marked up. 



The style of the background is included in the Style definitions.


Here are the features. 
The program has a white page by default. 
The page has some type of tabs that allow the user to switch from layer to layer. 
The layars are the background, the panels and the text boxes. 

Starting with the background. The program has a thousand images that can be choises for the emails background. The program uses a SQLight database to allow the user to search things. When they pick the image they want to use as the background image of their email, that image is encoded as a 2 byte integer. The person who opens the email using the same mail client will get the same image. 

The next part of background style is the background color. There are 65K colors that the user can choose from. The color will sit on top of the image. The user can configurte the opacity of the color and that will give the image behind it a tint. These will take three bytes. 

The second layer is the "Panel Layer" and the general layout of the Panel are are encoded in one byte. There are 255 differnt Panel layouts that are possible. The user can pick these from a dropdown box. The first four bits allows the user to describe the general layout and the next four bits allow the user to describe the way the corners of the pages look. These designs are reactive so they will change on cell phones in ways that would be expected. There can be up to five Panels: Header, Footer, Left Aside, Right Aside and Main. 

Each Panel will have a grid within it. within the program, The user can click on the Panel and have some popup that allows the user to specify how many columns and how many rows the panel's grid will be. The default is just one column and one row so that it is a single cell. The user will also specify how many 

The maxiumum number of rows and columns that are allowed is 60 by 60. this number can be divided into many fractions. In addition to how many rows and columns a cointainer has, the use must also 

Each  

Each 

Each 
 can have one "Container Style". 


   Questions Before I Proceed:

  1. Log Rotation: Should main.log have a size limit and rotate (e.g., main.log, main.log.1, main.log.2)?
  2. Timestamp Format: I see "October 23, 2025 3:16 PM Sec 34" - what does "Sec 34" mean? (Seconds? Or something else?)
  3. Task ID Format: Should we use the existing Task ID format (Oct-23-25_03-16-34-PM) or create a new simpler
  format for logs?
  4. Verbosity Levels: Do you want different log levels (e.g., summary vs detailed mode)?
  5. Performance Data: For timing charts - should we log network latency separately from processing time?
  6. Receipt References: When logging refers to receipts, should it show full path or relative path?
  7. Currency Format: I see "5450.8734-98" - what does the "-98" suffix mean?
  
  
  Answers to Questions:
  1. Main log has a limit of 1 MB. After that, the log should be zipped up and moved into the "Zipped Logs" folder that is in the "Data" file. Then a new main.log should be started. 
2.   October 23, 2025 3:16 PM Sec 34 is a good format. "Sec 34" means the 34th second of the minute. If there is a better way that is human readable that shows the seconds then that is fine. 

3. The major requirments for a Task ID is that it is unique, that it can be put into chronological order, that it shows the time that the command started, that it can be part of a file name on Linux and Windows without name violation and it is easy for humans to read. What is the easit time format for people to read that meets these requirments? Do not worry about what is easist for machines, databases or programmers to program or read. 

4. The logs should not be verbose exept in the case where there is an error with the servers or some problem that the a debugger would need more information about. 

5. Network latency needs to be tracked but we also are interested in knowing if a server is slow to process. So they should be logged seperatly. 

6. For receipts files the relitive path is fine. 

7. The -98 uses the hypen to make it eaiser for people to read so that they do not have to spend a lot of time understanding the precision of the fraction. 

Your suggested logging looks just about perfect. 

There was one major error, the denominations that cloudcoin version 3 uses are metric: 1000000, 100000, 10000, 1000, 100, 10, 1, .1, .01, .001, .0001, .0000-1, .0000-01, .0000-001, .0000-0001

Are you able to make a few changes and then implement it? or do we need to any additional coding first to make the logging work?

We need a command that is exactly like the Fix Fracked except: 

It only tries to fix coins that have a 0xB on them. It only uses Get Encrypted Ticket and Fix Encrypted commands and it does not put anything into the Graded folder. 

There is one more thing to keep in mind. Usability above security. If encryption cannot be achieved on a RAIDA, then the program should use no encryption

Remove from Make: 
rty/sqlite3"


=====================
We need to worry about encrypting and decrypting files and doing it in a way that is easy and unlikely to have errors. We have implemented some different commands for this. However, I would like to make it so when ever the Authenticity numbers of a coin file need to be read or updated, the program unenctpts them automatically. Then after the read or change, the files are decrypted automatically. 

I can imagine that we have two functions that read files. One is called Read Meta. This one is able to read the file name and all the header information. 

Then we would have another function called Read all Coin (Or something like that). This one would need to decrypt and encrypt. 

The fuction would try to read the file and if it sees that the encryption byte is set, it will then look for a password in RAM. If the password is not there, then the read fails. The user will then need to load their password. 

Any thoughts on this? Do we have some read coin functions that we could alter? Create a plan first and ask any questions. 



 the AN are decrypted and after the read is done, they are encrypted. 





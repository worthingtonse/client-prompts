# Best Practices For Client Applications. 
Over the years we have created the followin best practices to reduce problems. 

## Never Delete Files
We never delete files, we just move them into appropriat folders. 

## Work Out of RAM as Much as Possible
We move files from folder to folder in data pipelines to assure that if the computer crashes, the coins will not be lost. This is why we keep very little in 
RAM unless we can afford to lose the data. This is true in the Fix and Find commands. 

## Keep the Folder Structure the Same
We always use the same folder structure with the same names. This is good for backwards compatibility and it makes it easier to work with the files. 

## Keep many different logs. 
We have four logs. 
1. Summary.log: Tells what happened without going into detail. Log items may include "raida was echoed and 23 came back good." The summary.log will show errors too.
2. main.log: Tracks every detail of what happened. These logs can grow quite large and must be compressed from time to time.
3. Stats.csv: This log is created so that it can be imported into Pandas and used to train AI on how to create timeouts, recogniuze unusual activities, identify problems with raida servers, and see what features are used.
4. Data stores. These a files that keep track of variables that would usually go into RAM. These variables can persuis of many usages. The echo table is one of these and tracks the status of the raida. 

## Have Functions in Depth
Have functions that do a lot of work so the programmers don't have to. 

## Be Data Driven 
Stay away from object orientated programming and try to keep everything in data pipelines. This means we are trading code usability with easy code that is easy to understand. It also makdess it
so a change in one part of the program will not change everything else. 

## Use of Global Variables
Functions should have access to global varables such as the paths to folders, tha password to encrypt and decrypt files, location of encryption keys.

## Passing variables by reference and not be value. 
Functions should be able to transform data without needing to create new space in RAM. 

## Using assembly codes for encrytion
Whenn using AES encryption, use the commands that are built into the processors. 





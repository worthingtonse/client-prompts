Now I think it is time to create some composit commands. 

Sarting with the "Health Check" command. This command looks at all the coins in the Bank and Fracked folder and confirms their authenticity and fixing any issues. 

The workflow maybe something like this: 


1. Call the Decrypt Wallet Coins
2. Fix Broken keys (yet to be implemented)

Now we will work on encrypting network traffic. 

To do this, we will need to create a few commands first:
1. Pick Encryption Key

The Pick Encryption Key command.
Any CloudCoin file can be used as an encryption key because the ANs in the file are also on the RAIDA servers and act as shared secrets for 128 bit AES CTR encryption. 

When the client wants to make a request to the raida, it must choose one of these coins to use as a key. The Key picker will first look into the bank folder to see if there are coin files there. Otherwise it must look into the Fracked folder. If there are no coins, no encrypted calls can be made unless we are doing a Download locker but that is another issue. 

The key picker will check it's "prefered-key.txt" list to see if there are coins that were used successfully as keys last time. A key found in that file will be used first. 

When the key picker is done testing the key, it will enter this key into the prefered-key.txt file unless it is alreday there. 

Testing the key. The key picker will run the echo command to verify that the CloudCoin is not fracked and will encrypt properly on all RAIDA. 

If there are problems due to a 0x0B (Broken encryptoin) then the Coin file will be placed in the "Broken Key" folder. Then the Fix Encryption Keys command will be run againt it to see if the keys can be fixed. 

Once done, the Pick Encryption key will return a CloudCoin file name to the caller.  

Any questions about this new command?



It will chose a key denomination that is the least likly to be used. 


 will look at its encryption key table and see if there is an entry for a good key that was used last time for encryption. If an encryption key is used and it works, then this would be kept in the encyrption key memory file.

1. On second thought, instead of having a "prefered-key.txt" list, make it so that when a key becomes the prefered key, the memo in the file name will be changed from what ever its task ID was to the word "key". We only need one key but it would make things better if there was a key file in every wallet. However, any key can be used for any transaction. We will make it so that everytime money is withdrawn from the wallet, the Key Picker command will be called to prepare the next key in case the key was spent. This will speed up the next call because the key will already be keys that are ready and can be selected. Note that these keys will be coins in the Bank folders unless there are not coins in the Bank folder and coins from the Fracked folder are neccessary, 

2. 

3. If the prefered key fails testing, then every coin in the Bank should be tested until one is found that is good. If no good coins can be found, then the key fixgin process should go forward. 

7. The Broken Key folder is in the wallet folder along side Bank and Fracked. 

8. The Fix Encryption Keys command already exists. as Command 20. 

 
===========
I've changed my mind. This process will be much different. Nevermind about a Key Picker command, there will be a Key Provider command instead. 

Instead of the key picker returning a coin file, it will return a "key struct". This key struct needs to have 25 Denominations, 25 Serial Number and 25 ANs (16 bytes long).

Instead, there will be "Key Provider Modes" and each mode will fill the key struct in a different way. 

Decide what mode to work in:

If there are coins in the Bank folder use "Bank" mode.
Otherwise, if there are coins in the Fracked folder, use "Fracked" mode. 
Otherwise, if there are coin in the Suspect folder, use "Suspect" mode. 
Otherwiee return an empty struct and do not use encryption with a coin file. 



BANK MODE: 
Pick one key at random from Bank folder, load it into a Key Struct and return that Key Stuct to the caller. 

FRACKED MODE:
Since the coins are fracked, it means that many coins will need to be opened and the good parts of them need to be combined with the good parts of others to create a Key Struct. So if a coin with serial number #7726 is fracked on RAIDA 7 and a Coin with serial number #28933 is fracked on RAIDA 11 then all of coin #7726 would be used except that its Authenticity Number for RAIDA 7 would be replaced with the Authenticity number of coin #28933. Return this Key struct to the caller. If any member of the Key stuct cannot be filled because a good authenticity number cannot be found, return the stuct with that element set to all zeros.

SUSPECT MODE: 
In suspect mode, an empty Key struct is created. Then the first coin in the susect folder is sent to the Echo Encrypted command. We don't have this yet so make a stub. Everytime the Echo Encrypted returns with no encryption errors, that part goes into the Key Struct. A loop of all the keys continue until either all members of the key stuct are filled or all the coins in the Suspect folder are exhasted.  The Key Struct is then returned to the caller.   

Answers to question: 
1. No prefered-key.txt will be used.
2. The Pick Key will not do testing except for the Suspect Mode. 
3. The pick key will always return a key struct even if that key struct is all zeros. 
4. For testing purposes, this command should be callable by the user and show the the user a JSON string of the key returned. This command must also be callable by other processes. 
5. No files will be returned, only a key struct. 
6. The hash will not be used. Only the actual AN will be used as a key. The 16 byte ANs will not need to be converted to a 16 byte AES key as they are the same thing (Unless you know otherwise and there needs to be work in this area)
7. There is now no need for a Broken Key folder. 
8. We will not have to fix and broken keys in this command so ignor that for now. 

Any other questions before you start coding? 

1. The struct needs to be like: 
Each Struct has 25 rows with three columns in each row. 
typedef struct {
      uint8_t denomination[25][1];
      uint32_t serial_number[25][1];
      uint8_t ans[25][16];
 } EncryptionKeyStruct;
 
I would probably put it in the cc_types.h

2. Use secure random to pick the coin until we find a better way.

3. Interate and use the first valid AN found for each RAIDA. 

4. Make the entire Supect Mode a stub but the call to pick key needs to fail. So return an error that can be handled by the caller. 

5. Command 67 is fine. 
6. Show the entire key struct in the form of a JSON string. 
7. No need to display mode. 
8. Return an error that can be handled by the caller. 


 When Pick key is called, it will look in coin files and for each RAIDA, it will find an AN that has been marked passed or 0x00

=========================================
Frack Fix. 
Now I think it is time to create some composit commands. 

Sarting with the "Health Check" command. This command looks at all the coins in the Bank and Fracked folder and confirms their authenticity and fixing any issues. 

The workflow maybe something like this: 


1. Call the Decrypt Wallet Coins
2. Fix Broken keys (yet to be implemented)

Now we will work on encrypting network traffic. 

To do this, we will need to create a few commands first:
1. Pick Encryption Key

The Pick Encryption Key command.
Any CloudCoin file can be used as an encryption key because the ANs in the file are also on the RAIDA servers and act as shared secrets for 128 bit AES CTR encryption. 

When the client wants to make a request to the raida, it must choose one of these coins to use as a key. The Key picker will first look into the bank folder to see if there are coin files there. Otherwise it must look into the Fracked folder. If there are no coins, no encrypted calls can be made unless we are doing a Download locker but that is another issue. 

The key picker will check it's "prefered-key.txt" list to see if there are coins that were used successfully as keys last time. A key found in that file will be used first. 

When the key picker is done testing the key, it will enter this key into the prefered-key.txt file unless it is alreday there. 

Testing the key. The key picker will run the echo command to verify that the CloudCoin is not fracked and will encrypt properly on all RAIDA. 

If there are problems due to a 0x0B (Broken encryptoin) then the Coin file will be placed in the "Broken Key" folder. Then the Fix Encryption Keys command will be run againt it to see if the keys can be fixed. 

Once done, the Pick Encryption key will return a CloudCoin file name to the caller.  

Any questions about this new command?



It will chose a key denomination that is the least likly to be used. 


 will look at its encryption key table and see if there is an entry for a good key that was used last time for encryption. If an encryption key is used and it works, then this would be kept in the encyrption key memory file.

1. On second thought, instead of having a "prefered-key.txt" list, make it so that when a key becomes the prefered key, the memo in the file name will be changed from what ever its task ID was to the word "key". We only need one key but it would make things better if there was a key file in every wallet. However, any key can be used for any transaction. We will make it so that everytime money is withdrawn from the wallet, the Key Picker command will be called to prepare the next key in case the key was spent. This will speed up the next call because the key will already be keys that are ready and can be selected. Note that these keys will be coins in the Bank folders unless there are not coins in the Bank folder and coins from the Fracked folder are neccessary, 

2. 

3. If the prefered key fails testing, then every coin in the Bank should be tested until one is found that is good. If no good coins can be found, then the key fixgin process should go forward. 

7. The Broken Key folder is in the wallet folder along side Bank and Fracked. 

8. The Fix Encryption Keys command already exists. as Command 20. 

 
===========
I've changed my mind. This process will be much different. Nevermind about a Key Picker command, there will be a Key Provider command instead. 

Instead of the key picker returning a coin file, it will return a "key struct". This key struct needs to have 25 Denominations, 25 Serial Number and 25 ANs (16 bytes long).

Instead, there will be "Key Provider Modes" and each mode will fill the key struct in a different way. 

Decide what mode to work in:

If there are coins in the Bank folder use "Bank" mode.
Otherwise, if there are coins in the Fracked folder, use "Fracked" mode. 
Otherwise, if there are coin in the Suspect folder, use "Suspect" mode. 
Otherwiee return an empty struct and do not use encryption with a coin file. 



BANK MODE: 
Pick one key at random from Bank folder, load it into a Key Struct and return that Key Stuct to the caller. 

FRACKED MODE:
Since the coins are fracked, it means that many coins will need to be opened and the good parts of them need to be combined with the good parts of others to create a Key Struct. So if a coin with serial number #7726 is fracked on RAIDA 7 and a Coin with serial number #28933 is fracked on RAIDA 11 then all of coin #7726 would be used except that its Authenticity Number for RAIDA 7 would be replaced with the Authenticity number of coin #28933. Return this Key struct to the caller. If any member of the Key stuct cannot be filled because a good authenticity number cannot be found, return the stuct with that element set to all zeros.

SUSPECT MODE: 
In suspect mode, an empty Key struct is created. Then the first coin in the susect folder is sent to the Echo Encrypted command. We don't have this yet so make a stub. Everytime the Echo Encrypted returns with no encryption errors, that part goes into the Key Struct. A loop of all the keys continue until either all members of the key stuct are filled or all the coins in the Suspect folder are exhasted.  The Key Struct is then returned to the caller.   

Answers to question: 
1. No prefered-key.txt will be used.
2. The Pick Key will not do testing except for the Suspect Mode. 
3. The pick key will always return a key struct even if that key struct is all zeros. 
4. For testing purposes, this command should be callable by the user and show the the user a JSON string of the key returned. This command must also be callable by other processes. 
5. No files will be returned, only a key struct. 
6. The hash will not be used. Only the actual AN will be used as a key. The 16 byte ANs will not need to be converted to a 16 byte AES key as they are the same thing (Unless you know otherwise and there needs to be work in this area)
7. There is now no need for a Broken Key folder. 
8. We will not have to fix and broken keys in this command so ignor that for now. 

Any other questions before you start coding? 

1. The struct needs to be like: 
Each Struct has 25 rows with three columns in each row. 
typedef struct {
      uint8_t denomination[25][1];
      uint32_t serial_number[25][1];
      uint8_t ans[25][16];
 } EncryptionKeyStruct;
 
I would probably put it in the cc_types.h

2. Use secure random to pick the coin until we find a better way.

3. Interate and use the first valid AN found for each RAIDA. 

4. Make the entire Supect Mode a stub but the call to pick key needs to fail. So return an error that can be handled by the caller. 

5. Command 67 is fine. 
6. Show the entire key struct in the form of a JSON string. 
7. No need to display mode. 
8. Return an error that can be handled by the caller. 


 When Pick key is called, it will look in coin files and for each RAIDA, it will find an AN that has been marked passed or 0x00

=========================================
Frack Fix. 


You are incorrect about the fix and what the code should do. 

The purpose of this program is to allow large amounts of servers (up to 12) to fail but still allow the program to function. 

The process of encryption should only fail if there are less than 13 servers that are marked authentic in the Key Struck that the encryption function has obtained by calling the function that creates key structs. 

The encryption function must check that the key struct it has received has 13 good keys (Not all zeros) before using it. If the Key Struct does not have 13 keys, only then should it fail gracefully and throw and error.

This is why the function that creates the Key Struct must have at least two modes in the key selection process: Bank mode just uses a key from the Bank folder. In Fracked Mode, the function has to analyse more than one key to put together a fully functioning key into the struct. We arready have this function so we don't have to worry about this. 

The solution is to:

1. Have the encryption function check to see if the Key Stuct it received has enough keys (13) to continue. 
2. Use the same kind of CRC32b algorithm to create an non-encrypted version of the request that already contains the CRC calculations. Then encrypt everything without considering the CRC. 
3. If there are servers that do not have encryption keys, use encryption type zero (no encryption) but mark the response as 0x0B (broken Key) if the command is successful, if there is failure mark the coins as 0x0F instead of 0x0B. This is because we want to show that the operation was successful but needs to be fixed by either fixing fracks or by useing the encrypted fix.  These broken requests will be fixed later. 
4. Do not include any encryption keys in the generation of the CRC. 

Do you have any questions befor coding? 

My comments about the requirments. 
All is correct but to clarify, it is true that the CRC should be independent of the encryption. Right now, the CRC is working until the encryption is added.

Answers to questions:
1. I think the check should be made after getting the Key Struct call. The error you have suggested is good. 

2 & 3. Let's put off dealing with the 0x0B until after we get the CRC working. 

4. Correct



2. I think it should apply to all requests to the RAIDA that are successful. We can handle exception in the future if there are any. Here is some specifics:
Assuming that we are using encryption type 0 the followin commands: 

3. The 0x0B making logic should be in the

After the call, the command response handler will need to have access to the Key Struct. It seems that each command may have different rules.  

=====================





3. 

We need to create a plan to fix the issue of the error 37 (invalid encryption key \) also  called invalid CRC. 

This error can be thrown by any call to the RAIDA for any command. This error often comes as a suprise to us because we find out that the key we thought was authentic is actaully invalid. 

However, sometimes we get a key stuct that shows that no encryption is available for a call to one or more of the RAIDA. In this situation, we should try to fix the broken key first. 

Right now, this error is not being handled correctly. 

So, we should change a function like the raida_should_encrypt_command() so that if it detects one that cannot be encrypted, that the key be fixed before the command is issed by gettting Encrypted Ticket and sending them to the RAIDA that encrytion is broken with. 

However, if we think that the encryhption key is good and get an error after the call, then that encryption key shold be fixed right after the fall is made and then make the call again. 

There maybe other techniques we can employ too. Create a plan to repair encryption key failures.  Think about all the edge cases too. 

=====================================
Log may still not show errors. 

When we echo the raida, we can fix broken keys then if we use the encrypted version of the echo. 

=======================

When I call commands that must encrypt messages to the RAIDA, the program is suposed to pick a coin from the bank folder and use it for encryption keys. However, I see lines of cosole feedback that make it look like the key that was used was not from the Bank folder. Infact, it is not in the Fracked folder either.  like this: 


 [RAIDA 0] Connecting to 78.46.170.45:50000
================================================================================
  [RAIDA 0] Using pre-loaded encryption key from task
  [RAIDA 0] DN=3, SN=0021152
  [RAIDA 0] Random nonce (8 bytes): 1A D4 71 F5 BA E2 EE B7
  [RAIDA 0] Plaintext body (324 bytes): E3 DA 66 9C 2B 1C 6B 51 3D 71 04 7A B9 9A 8C 30 FF 00 00 01 25 FF 00 00 01 ... (324 total)
  [RAIDA 0] Encrypting 322 bytes (total body: 324, terminator: 2)

There is no coin file DN=3, SN=0021152 located in C:\Users\User\MyWallet3\Default\Bank How is this file being used as a preloaded key and where does it come from?



 sometimes RAIDA respond with an error 34 or 37 meaning the encryption key is bad. The program tries to handle this the best it can. However, key files that have bad encryption should be marked as 'f' for that raida id and then moved into the fracked folder. This is so they don't get used over and over. Instead, other keys will be tried first. 

Make a plan that will work within the currenct infrastructure but move key files into the Fracked folder while changing their POWN string so that they will not be used until they are fixed. 

=========================
Sometimes RAIDA respond with an error 34 or 37 meaning the encryption key is bad. The program tries to handle this the best it can. However, key files that have bad encryption should be marked as 'f' for that raida id and then moved into the fracked folder. This is so they don't get used over and over and other keys will be tried first. Make it so that if a call to the raida returns a 34 or 37 and the problem cannot be fixed using the current methods that the coin be moved to Fracked folder and marked 'f' in its POWN string. Keep in mind that this may only apply to coin in the bank folder. Also it would be better to pick coins randomly so that it is more likly that a good coin will be found. Anylaize this and make a plan to improve it. 
=======================
Make a plan to improve the logging for the Fix Encryption command. When I run the Fix Encryption Key command, the information put in the main log is not very helpful. 

There is not need to show the timestamps except at the beginning and ending of the commands. 

The Fix Encryption is suppose to look for situations in which the program has no coins that are athentic on a RAIDA. If there are no coins authentic on a RAIDA, then all the coins fracked on that raida should have encrypted tickets gathered from other raida and those tickets sent to the raida that has no shared secrets with the client. 

However, the log does not show if there are raida that do not have a shared secret with the client. If there are any coins in the Bank folder, then there are no raidas that could not have a shared secret with the client because all the raida are authentic.

The logs should show if any RAIDA were found to not share a secret with the client. 

Then, if there are problems, the log should show the process of getting encrypted tickets. 

Then, after that, it should show the process of calling the Fix Encrypted command and show how that goes. 

Right now the log shows:

  +-----------------------------------------------------------+
  | Response Header                                           |
  +-----------------------------------------------------------+
  | RAIDA ID:        0
  | Status Code:     0xFA (250) [Success]
  | Body Length:     4 bytes
  | Completion Time: 457 ms
  +-----------------------------------------------------------+

2025-10-29 23:00:14 -   [R00] FAILED after 1 attempt (1.0 seconds total)

Of the header shows success then why does it show FAILED after 1 attempt. And what was it attempting?

Create a plan that will make this command function properly and will log the command execution so that it is useful. 



======================================================================
  TASK START: Fix Encryption Keys
  Task ID: Oct-29-25_11-00-13-PM
  Time: October 29, 2025 11:00 PM Sec 13

2025-10-29 23:00:13 - 
=== Encryption Fix Analysis ===
2025-10-29 23:00:13 - Total coins analyzed: 51 (13 Bank + 38 Fracked)
2025-10-29 23:00:13 - Fracked RAIDAs found: 2
2025-10-29 23:00:13 - Helper RAIDAs available: 23
2025-10-29 23:00:13 - 
Fracked RAIDA IDs:
2025-10-29 23:00:13 -   R00: 13/51 passes (25.5%)
2025-10-29 23:00:13 -   R01: 23/51 passes (45.1%)
2025-10-29 23:00:13 - 
=== Fixing RAIDA 0 ===
2025-10-29 23:00:13 - [ENCRYPTION DEBUG] RAIDA 6, Cmd 0x042C, requested_type=1, enc_bytes[0]=0
2025-10-29 23:00:14 - [ENCRYPTION DEBUG] RAIDA 7, Cmd 0x042C, requested_type=1, enc_bytes[0]=0
2025-10-29 23:00:14 - [ENCRYPTION DEBUG] RAIDA 0, Cmd 0x042D, requested_type=0, enc_bytes[0]=0
2025-10-29 23:00:14 -   [R00] Attempt 1: Parse error from Fix Encryption response (status 0xFA: Success)

REQUEST PACKET (CloudCoin V3 Binary) (107 bytes):

  Request to Fracked RAIDA 0 (107 bytes, showing first 64):
  ┌──────────────────────────────────────────────────┬──────────────────┐
  │ Offset  Hex Values                              │ ASCII            │
  ├──────────────────────────────────────────────────┼──────────────────┤
  │ 0000    01 00 00 00 04 2d 00 06  00 00 00 00 00 00 00 00 │ .....-..........
  │ 0010    00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 │ ................
  │ 0020    32 75 87 30 38 8f 8a 81  3b 8f ce f5 68 6c e1 ee │ 2u.08...;...hl..
  │ 0030    03 00 00 15 98 00 06 00  06 00 03 00 00 15 98 c4 │ ................
  └──────────────────────────────────────────────────┴──────────────────┘


  Response from Fracked RAIDA 0 (36 bytes):
  ┌──────────────────────────────────────────────────┬──────────────────┐
  │ Offset  Hex Values                              │ ASCII            │
  ├──────────────────────────────────────────────────┼──────────────────┤
  │ 0000    00 00 fa 00 00 00 00 04  00 00 00 00 00 00 00 00 │ ................
  │ 0010    00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 │ ................
  │ 0020    00 00 3e 3e                                      │ ..>>
  └──────────────────────────────────────────────────┴──────────────────┘


  +-----------------------------------------------------------+
  | Response Header                                           |
  +-----------------------------------------------------------+
  | RAIDA ID:        0
  | Status Code:     0xFA (250) [Success]
  | Body Length:     4 bytes
  | Completion Time: 457 ms
  +-----------------------------------------------------------+

2025-10-29 23:00:14 -   [R00] FAILED after 1 attempt (1.0 seconds total)
2025-10-29 23:00:14 - 
=== Fixing RAIDA 1 ===
2025-10-29 23:00:14 - [ENCRYPTION DEBUG] RAIDA 15, Cmd 0x042C, requested_type=1, enc_bytes[0]=0
2025-10-29 23:00:15 - [ENCRYPTION DEBUG] RAIDA 17, Cmd 0x042C, requested_type=1, enc_bytes[0]=0
2025-10-29 23:00:15 - [ENCRYPTION DEBUG] RAIDA 1, Cmd 0x042D, requested_type=0, enc_bytes[0]=0
2025-10-29 23:00:15 -   [R01] Attempt 1: Parse error from Fix Encryption response (status 0xFA: Success)

REQUEST PACKET (CloudCoin V3 Binary) (107 bytes):

  Request to Fracked RAIDA 1 (107 bytes, showing first 64):
  ┌──────────────────────────────────────────────────┬──────────────────┐
  │ Offset  Hex Values                              │ ASCII            │
  ├──────────────────────────────────────────────────┼──────────────────┤
  │ 0000    01 00 01 00 04 2d 00 06  00 00 00 00 00 00 00 00 │ .....-..........
  │ 0010    00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 │ ................
  │ 0020    57 34 6f 93 cf f7 61 5d  53 a7 6c 64 ff 1d 80 7e │ W4o...a]S.ld...~
  │ 0030    03 00 00 15 98 00 06 00  0f 00 03 00 00 15 98 fe │ ................
  └──────────────────────────────────────────────────┴──────────────────┘


  Response from Fracked RAIDA 1 (36 bytes):
  ┌──────────────────────────────────────────────────┬──────────────────┐
  │ Offset  Hex Values                              │ ASCII            │
  ├──────────────────────────────────────────────────┼──────────────────┤
  │ 0000    01 00 fa 00 00 00 00 04  00 00 00 00 00 00 00 00 │ ................
  │ 0010    00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 │ ................
  │ 0020    00 00 3e 3e                                      │ ..>>
  └──────────────────────────────────────────────────┴──────────────────┘


  +-----------------------------------------------------------+
  | Response Header                                           |
  +-----------------------------------------------------------+
  | RAIDA ID:        1
  | Status Code:     0xFA (250) [Success]
  | Body Length:     4 bytes
  | Completion Time: 96 ms
  +-----------------------------------------------------------+

2025-10-29 23:00:15 -   [R01] FAILED after 1 attempt (1.0 seconds total)
2025-10-29 23:00:15 - 
=== Fix Encryption Keys Complete ===
2025-10-29 23:00:15 - Fracked RAIDAs attempted: 2
2025-10-29 23:00:15 - Successfully fixed: 0
2025-10-29 23:00:15 - Failed to fix: 2
  TASK COMPLETE
  Task ID: Oct-29-25_11-00-13-PM
  Time: October 29, 2025 11:00 PM Sec 15

  ======================================================================

 ==============
=======================
Now turn the program into a REST application that can also be used as a console. It seems you will need to include a web server for end points. This webserver can be very simple. A JSON parser is needed too. Make it ready to have end point because we will need endpoints for every command. I would like these endpoints to use the GET method because it is easier to troubleshoot. 

The program will need to store the port numbers to use in the existing config file in the Data directory. There maybe some other config information that needs to be included. 


If you want to do it now, you can create endpoints for all of the commands. But have them all use GET methods for easy testing. 

===================================

Can you create the API calls for a few of the commands 

For the Status Endpoint use the file-based approach. 

You are correct about the Synchronous execution. 
-=======================

We need command number 97 working. It works exactly like the Fix Fracks commands in that it gets a bunch of tickets. But, instead of sending the tickets to the Fix command, it sends one ticket to the Validate ticket command. So it gets a ticket from A RAIDA then sends the ticket to that same RAIDA to see what the ticket returns. Validate ticket is not encrypted. You can find the instructions to call this Validat Ticket here:  Any questions?



We will create a new command that will fall under the "Wallet Functions" heading. It is called "Zip Support Files"
The command will read a file called "Support files" that is located in the Data folder. This file will contain one file name per line. 
The command will then add all of these files (assuming that they are there) and zip them up and put them in the "Zipped Logs" folder and be called "ForSupport.Date Time.zip" where Date Time is a time stamp. 

Any questions? 

1.The file is called SupportFiles.txt"
2. The paths will be a Full Path. 
3. They will be in Data/Zipped Logs
4. menu number should be 60.
5. ISO is good.
6. Skip in silently. 
7. Use a C library like miniz.h

The command is called "Support 


Get Coin Nice Address. 

There are a bunch of commands that are basically functions or parts of larger commands.




For example, the Import command does the following: 
1. Puts Coins in the Import Locker
2. Unpacks the coins
3. POWN Sum Coins
4. Grades Coins
5. Find Coins if some are in Limbo
6. Fix Fracked Coins

Unpacks Coins
2


We will create a command called "List Serial Numbers". This command falls under the Wallet Management heading. This command will ask for the path to the folder the users wants to collect serial numbers for. The program will go to the folder and see if there are any .bin files. It will open them, read the denomination and four byte serial number. 

It will then create a file that has the name of the folder, the day and time and a .csv extention. The file with have a header with the "Denomination" and "Serial Number" headings on top. 

The program will write one coin per line. The Denomination and serial number will be seperated by a comma. The denomination will be displayed in human understandable form but with no foratting. The serial number will be shown as a number with not formatting. Examples of the contents of a serial number file:
File Name: 
Fracked.Sep 1, 25.SNs.csv 
Contents:
Denomination,Serial Number
1000,4322234
100,23232323
.001,9849

You are free to make improvements expecially how the date is formatted. 
Any questions before you start the command?

1. ISO format is good. 
2. This program should work like the "Backup Wallet" command in that the user has the locations that they per serial number files remebered and the user can choose the index of one that has been used befor or create a new location. 
3. If the files are encrypted, then the denomaintion and serial number should be taken from the file name. If there is no serial number in the file name and it is encrypted then an entry should be made in the serial number file: "encrypted,encrypted"
4. Subdirectores should not be scanned.
5. No sorting is necessary
6. Write duplicates and don't bother checking for them. 
There is one more thing, if the CloudCoin v3 file has more than one coin it it, get the serial numbers for all the coins. There probably is a function for this in the Unpack command. 


We will create another "Testing/Debug:" command called 
Proceed with threading. However, keep in mind that this program will be turned into a REST application and the expected flow is that the program will call the command to run and it will receive a task ID instantly. Then, the client can call "Status" command and give it the Task ID as a parameter and the program will return the progress. Can you add this as a stub now so that it can be ready in the future? Eitherway, proceed with threading. 


The first composite command is called Deposit. It takes coin files and changes their Authenticity numbers and makes sure they are authentic.

There was a problem in that all the RAIDA answered the
  requests very quickly except for two. The program was slowed because of these two. One of the servers is offlien and
  so I had to wait for it to timeout before the command was voer.  It is perfectly ok if not all the RAIDA change
  their authenticity numbers. So, it would be nice if the AI can recoment the two slowest or most likely RAIDA to not even bother with. Keep their ponw string as 0x00. 
  
  
  The 
  
  
  The command 71 Count coins asks for a password. Please change the command so that it does not ask for a password but instead uses this one: 
 8ec736a8421ce62588668b6f43abebc7
 
 
 But here is a request that maybe missing something. Please see if you can find an error
 REQUEST PACKET (CloudCoin V3 Binary) (70 bytes):
Offset | 00 01 02 03 04 05 06 07 08 09 0A 0B 0C 0D 0E 0F | ASCII
-------|------------------------------------------------|------------------
0x0000 | 01 00 10 00 00 02 00 06 00 00 00 00 00 00 00 00 | ................
0x0010 | 00 00 00 00 00 00 00 26 00 00 00 00 00 
0x0020 | 68 44 6F FE 02 84 A1 72 36 DB 68 3E 1A 35 C8 D1 | hDo....r6.h>.5..
0x0030 | 00 00 00 00 8E C7 36 A8 42 1C E6 25 88 66 8B 6F | ......6.B..%.f.o
0x0040 | 43 AB EB C7 3E 3E

This server source code file shows the password: 
This is where the password is checked. 

On second thought, before we do the networking, there are a few more commands we can do. 

The first is called "Backup without changing encryption". 

When this command is called, the program will look to see if there is a file called "BackupPlaces.txt". This is a file the keeps track of the places that the user likes to backup their wallets to
and will allow them to choose one by index without having to re-enter the path. The BackupPlaces file has one backup place per line with no header. 

If there is no BackupPlaces file the the program asks the user what is the path to the backup location. The program will then create a backupplaces.txt file and put this path in there. 

If there is a backupPlaces file, the program will create a JSON response that shows the index (based on the line number) and the path to the backup place. The program will add another
index for "New Backup Location"
The the program will prompt the user for the index and then that path will be set as the place that the files will be backed up or the program will prompt the user for the new place. 

New paths will be written to the backupPlaces.txt file and will be on the top row so that everything moves down. 

The actual backup takes place in the contents of the active wallet. The program will zip all of the contents of the wallet's Bank and Fracked folder. The name of the file will include the name of the wallet, the date. 

There will be some stubs added so that more functionality can be added in the future. The first stub is to have the program call on the operating systems file explorer and open it for the user at that path so the user can immeditaly work with it. 

The second stub is to allow the program to see if the coins are encrypted or decrypted and then do then encrpypte them if they are decrypted or decrypted them if they are encrypted and put them in the zip file. After that the files must be encrypted or decrypted back to their original state. 

Let me know if you have any questions. 

===================================================================================

The next task is to "Unpack Coins". Users will place files into the "Import" folder of the Wallet they want the coins to go in. 

The goal of the "Unpack Coins" command is to seperate all the coins into their own files and put them in the "Suspect" folder where they
will then be sent to the RAIDA for authentication and password changing (POwning). Coin files may have lots of coins in them. There
maybe zipped files with coins it them that need to be unzipped first. 
Some coins maybe of different version and must be parsed differently.

When ever the Unpack Coins process is called, an "Unpack Log" will be created. This log goes into a sub folder of the Imported folder called "Unpack_Logs". The name of the unpack log will be the words "UnpackLog" followed by the date and time with a .csv extension. 
The unpack log has a header with the columns "Relation, Name, Destination". The Types are either 'P' for parent or 'C' for child. The name is the name of the file. The destination is what folder the file was moved to. 


The process is like this: 
0. Make a list of all files in the "Import" folder and write them as parents in the UnpackLog or keep them in RAM until the end. This is because the destination will not be known yet. 
1. Unzip the files in the zip folder and put the unzipped coins in Import folder but not in a subfolder. 
2. Move any unzipped files from the "Import" folder into the "Imported" folder and enter that P, zipname.zip,Imported in the Unpack log.  
3. Look to see if there are any zip files that came out of the original zipped folder. If there is, then unzip them too. But only do this once. 
4. Look and see if there are any files that do not have a .png, .stack or .bin extention. These files must be moved to the "Trash" folder. Sub directores in the Import should be ignored. But these in the unpacklog as children. 
5. .stack files will be moved into a subfolder in the Import folder called "Version1". If this folder is not there then create it. Log in the unpack log. 
6. .png files will have the binaries extracted from them. The file header for the .bin coins embedded in the .png file starts at index 41 of the .png file. Index 41 in the .png file becomes index 0 of the cloudcoin file. Indexes 6 and 7 show how many coins are in the file. The header is the 32 bytes followed by 407 bytes per coin. Each coin is extracted into its own seperate file with its own header. The naming of the new file can be a random number with a .bin extension. The header can be the same as in the .png file except with the number of coin changed to 0x0001. All .pngs should now be removed from the Import folder to either the Import, Corrupted or Trash folders. Update the unpack log to show where the coins whent. 
7. We will prepare to parse the files. 
	a. The first thing to determine is if the .bin files are version 2 or version 3. Version 2 files have a 32 byte header and coins that are 416 bytes in length. Therefor, if you subtract 32 and devide the number by 416, it should have a remainder of zero. Version 3 files also have a 32 byte header and coins that are 407 bytes in length. Therefor, if you subtract 32 and devide the number by 407, it should have a remainder of zero.  The first byte of a version 3 file is always a 0x09. The first byte of a version 2 file is always 0x00. Use what ever method seems the easist. 
	b. Any bin file that does not start with a 0x00 or a 0x09 should be moved to the "Corrupted" folder. 
	c. Version 2 coins will be moved into a subfolder in the Import folder called "Version2". If there is no Version2 folders, then one should be created. Duplicate files should be moved into the Duplicate folder and overwrite any other files already there with the same name. 
	d. Create a stub function for now that will parse the version1 files. We can deal with that later. 
	e. Create a stub fundtion for now that will parse the version2 coins. We can deal with that later. 
8. Parsing the version 3 binaries. The files that are left in the Import folder shouls all be version 3. 	
	a. The goal is to read these and put them into the "Suspect" folder in the correct format with the correct file naming scheem. 
	b. Change the names so that they use the standard naming convention. 
	d. Change the POWN string in side so that they are all 0x00 for unknown/untried
	e. Check the Suspect, Bank, Limbo and Fracked folder to make sure these coins have not already been imported. If they have been imported, move them to the Duplicates folder. Log the uppack log. 
	d. Move the coin to the Suspect folder.
	f. All the files in the Import folder should now be gone.
	g. Write the unpack log to the unpack_logs in the Imported folder. 
	h. Return the unpack log to the caller in the form of a json file. 
	i. Check the size of the unpack log folder. If it is over 1 MB, zip it and put it in the Imported folder and empty the upack_logs folder. 

Note: If the files are not formatted correctly and cannot be parsed, they must be put into the "Corrupted" folder. 
2. If the file already exists in the Import folder and it is the same size, the new file must be put in the "Trash" folder. 
3. No files should be deleted. Just moved. 


Let me know if you have any questions. 
=========================================
Bugs with backup: 
1. If the user specifies a location that does not exist, the program will create that location. If there are any bugs that cause the backup to fail to be written to the location, a entery will not be made to the BackupPlaces file. 

=========================
The names of the files that were saved in the Suspect folder were incorrect and so were the contents of the file. One problem maybe the endian issue. All the
  bytes in the files are Big Endian. The second problem is that I gave you some incorrect information about the file format that I will try to fix here. TI said
  that the token could was on  
  
  
  
T712507044726
8BNU126



1 0 4 0 0 0 0 6 // 4 is the raida id,  
1 0 0 0 0 0 0 0 
ET 0 0 0 0 0 BL BL
0 0 0 0 0 0 0 0 

About the network protocol

The protocol is a custom binary protocol. 

Calls to the RAIDA server consist of three parts:
1. 32 Byte Fixed header that is never encrypted
2. A body that can be encrypted
3. 2 bytes that terminate the request that are never encrypted


Header Section:
For all unencrypted requests, the 32 bytes are exactly the same as below except for bytes show with letters. 
01 00 ID 00 CM CM 00 06 00 00 00 00 00 00 00 00 
00 00 00 00 00 00 BL BL 00 00 00 00 00 00 00 00 

ID is the RAIDA ID from 0 to 24. 
CM CM are the two bytes of the command ID. Big Endian
BL BL is the number of bytes in body, Big Endian

Body Section: 
If the packet is unencrypted, there is no checksum or challenge that is usually at the beginging of the Body Section.

Terminating bytes. The terminating bytes are allways 0x3E3E

Complete unencrypted Echo request to RAIDA ID 4 including the header, body and terminating bytes:

01 00 04 00 00 00 00 06 00 00 00 00 00 00 00 00 
00 00 00 00 00 00 00 02 00 00 00 00 00 00 00 00 
3E 3E

Note: The command for echo is 0x0000. The 0x02 shows that there are two bytes after the header. In this case, the 0x3E3E


RESPONSE: 


Responses from the RAIDA server consist of three parts:
1. 32 Byte Fixed header that is never encrypted
2. A body that can be encrypted
3. 2 bytes that terminate the request that are never encrypted


Header Section:
For all unencrypted responses using TCP, the 32 bytes are exactly the same as below except for bytes show with letters. 

ID 00 SC CG 00 00 00 00 00 BL BL BL EX EX EX EX 
00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 

ID is the RAIDA ID from 0 to 24. 
SC is the status code. We want 0xFA (250) that means success. 
CG is the command group and that is the first byte (HOB) of the 2 byte command. are the two bytes of the command ID. Big Endian
BL BL BL is the number of bytes in body, Big Endian
EX EX EX EX  is the number of nano seconds it took for the server to process the request internally. Big Endian

Body Section:
If the call is for echo using TCP/IP and it is not encrypted, there will be no body. 

Terminating bytes. The terminating bytes are allways 0x3E3E

Complete unencrypted Echo response from RAIDA 7 including header, body and terminating bytes: 

07 00 FA 00 00 00 00 00 00 00 00 02 00 05 34 D9 
00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
3E 3E

RESPONSE (CloudCoin V3 Binary) (32 bytes):
Offset | 00 01 02 03 04 05 06 07 08 09 0A 0B 0C 0D 0E 0F | ASCII
-------|------------------------------------------------|------------------
0x0000 | 00 00 10 00 00 01 00 00 00 00 00 00 00 00 00 38 | ...............8
0x0010 | EE EE EE EE EE EE EE EE EE EE EE EE 18 11 CA 6A | ...............j
         ID 00 SC CG 00 00 00 00 00 BL BL BL EX EX EX EX 
         00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 

Offset | 00 01 02 03 04 05 06 07 08 09 0A 0B 0C 0D 0E 0F | 
-------|------------------------------------------------|
0x0000 | 01 00 0D 00 00 00 00 06 00 00 00 00 00 00 00 00 | 
0x0010 | 00 00 00 00 00 00 00 12 00 00 00 00 00 00 00 00 | 
0x0020 | CF 15 1D 27 92 E6 A0 06 05 A6 5C 1C 22 70 D3 77 | 
0x0030 | 3E 3E                                           | 

Now we are getting another error: ERROR_INVALID_CRC = 37,
So it seems that the CRC is still calculated when it is unencrypted. This means you will need to follow the CRC protocol. See the attached document. Let me know if you have any questions. 

-----------------------
Ok, Let's do the Detect command. There are actually two Detect commands, Detect and Detect Sum. 
We will do the simple Detect first. The command number of Detect is 0x010A. We will create the command using TCP/IP no encryption and serial mode. 
This command will check all the coins in a wallet to see if they are authentic without changing the authenticity numbers.

this is the basic workflow:
These steps are all done in the context of the active wallet. 
1. The Suspect folder is checked to make sure it is empty. It there are some coin files already there, the "Finish authenticate" command will be called first. However, we don't have this command yet so create a stub fuction for "Finish Authentication". 
2. The Grade folder is checked to see if it is empty. If not, the Grade command is called first. 
3. All the files in the Bank and Fracked folders are moved into the Suspect folder. 

The coins files have their Authentication numbers devided into 25 different requests. The request headers are the same as the echo except with the different command number and different Body lenght. 

Each request body looks something like this: 

CH CH CH CH CH CH CH CH CH CH CH CH CH CH CH CH  // Challenge / CRC 
DN  SN SN SN SN  AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN    // One line per coin
DN  SN SN SN SN  AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN  
DN  SN SN SN SN  AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN  
DN  SN SN SN SN  AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN AN  
3E 3E //Not Encrypted

The respons header will have status 241 if all the coins were authentic. Status 242 if all the coins were counterfeit and 243 (Mixed) if some were authentic and others were counterfeit. 

If Mixed content bitfield. Maybe many bytes. One byte for 8 tokens. 0 is fail, 1 is pass. Will be padded with zero bits to the end of a byte. 

Then the terminating bytes:
3E 3E  //Not Encrypted

Do not send more than 65K bytes at a time. About 3095 coin files. 

Once the resluts are returned, the files are moved into the Grade folder. 

The POWn strings are entered into the files. 

If there is more than 3K notes, the process will loop until all the files are in the Grade folder. 

THen the Grade command is called and all the files will be sorted to their folders and a receipt is returned to the caller.

Do you have any questions? 
==================

When the results return, new files must 

The coins in the Suspect folder are moved into the 

There are some differences. The POWN command must delete all the files in the P



1. Encryption type two uses a locker key as a common secret but we don't have to worry about encryption just yet. For now we use encryption type 0.

2 and 3. DE is denomination. The program can just put the locker key now without encryption. 
4. I don't see any maxium amount. But if there is it might be in the cmd_locker.c server code. 
5. Existing users will use encryption type 1. 
6. I assume that the key sent to the PEEK service must have all 0xFFs on the last four bytes. 
7. Yes, 242 means no locker found. Lockers are always deleted after coins are removed from them. The RAIDA does not track lockers that have been deleted so it only knows if it is there or not. 
=========
1. AN (Authenticity Number) Field:
  You say "there is only one AN" - does this mean:
  - All coins in the locker share the same AN (the locker key)?
  - So the 16-byte AN field at bytes 16-31 is the locker key?
  - And this is the same for all coins being removed?

  2. PAN (Proposed AN) Field:
  For each coin (DN + SN + PN):
  - The PN (16 bytes) is the new AN we want to set for that coin after removal?
  - Each coin can have a different PAN, correct?
  - So we're essentially doing: "For all coins with this locker key (AN), change their ANs to the specified PANs"?

  3. Request Size Validation:
  Looking at the format:
  - 16 CH + 16 AN + (5 DN+SN + 16 PN) × N + 2 terminator
  - Minimum size: 16 + 16 + 21 + 2 = 55 bytes (for 1 coin)
  - Is this correct?

  4. Response Format:
  You show STATUS_ALL_PASS (241) and STATUS_ALL_FAIL (242).

  - Does REMOVE also support STATUS_MIXED (243) like regular POWN?
  - If yes, what's the response body format for MIXED?
    - Bitfield (1 bit per coin) indicating which succeeded?
    - Like: bitfield + 3E3E?

  5. Server Behavior:
  Looking at the server code (lines 155-304):
  - Line 199: ie = get_coins_from_index(an); - finds locker by AN (locker key)
  - Lines 233-247: Checks if each requested coin belongs to the locker
  - Line 263: memcpy(&page->data[sn_idx * 17], can, 16); - updates AN to PAN

  So the server:
  1. Finds the locker using the AN field (locker key)
  2. Verifies each coin DN+SN exists in that locker
  3. Updates each coin's AN to the provided PAN
  4. Returns bitfield showing which coins succeeded?

  6. Locker Deletion:
  You mentioned "Lockers are always deleted after coins are removed from them."

  - Does this happen automatically on the server side?
  - Or only when all coins are removed?
  - What if I do REMOVE with only some coins - does the locker persist with remaining coins?

  7. PAN Requirements:
  For regular POWN, PANs are usually new random 16-byte values. For REMOVE:
  - Can PANs be any 16-byte value?
  - Or must they follow specific rules (like NOT ending in 0xFF)?
  - Can I remove coins and immediately put them in a new locker (PAN ending in 0xFF)?

  8. Typical Use Case:
  The typical workflow would be:
  1. PEEK to get list of coins (DN+SN pairs)
  2. Generate new random ANs for each coin (PANs)
  3. REMOVE with locker key (AN) + DN+SN+PAN for each coin
  4. Coins now have new ANs and are out of the locker

  Is this correct?
  
  
  1. The client will tell the server what the PNs (Proposed Authenticty Numbers) will be  by specifiing the DN SN SN SN SN and then the PNs. The PNs can also be called the ANs in this case. 
  
  2. Correct.
  3. Correct. 
  4. There is no status mixed since there is only one key (AN) that is being used. 
  5. Correct.  I don't think there is any bitfield returned. I think the body is empty. But, if you see this i the server code, then be preparied to handle a mixed return with a bit fields. 
  6. If only some coins are removed, the locker will persist. 
  7. PANs can be any 16 bytes value including another locker key. (I think). I think they can end with 0xFFs. I have not tried this. Let's make a new command in the Command list that will move coins from one locker to another. Then we can test this by using the remove but setting the PNs to another locker. 
  8. Correct workflow but we need to add a Grade command at the end. 
  The new coins that come out of the locker should be put into the Grade folder and be given a task ID. The receipt will be .remove-from-locker.
  
  
  Where are we going to store the resource keys? In the SQL Database
  Free up the memory. 
  PING - 
  ================
  Attacher establishes many sessions
  Server can clearn up sessions after expiration. 
  server is suppose to trust the randomness of the client.
  
  Looks at the payload - creates a session key, then creates the session key sends back the nounce. Client has the client nounce and it has the server nounce and can recreate the
  session key. 
  
  Same pattern can be seen in TLS. One encryption key then you have the session key that encyrpted the database. server deletes all the data. 
  
  next time the client wants to talk to talk . Sends the request with a encryption key and can use it. 
  
  Creates the Ping - Don't send the sessionkey. 
========================================================

Eight Byte Session ID 
HKDF - 
  
  Put Coins in Import:


Wallet Management command 63 will be called "Put Files in Import".
The command will be supplied an array of filenames (Absolute). 
The program will take that list and move them (not copy and delete) to the Import folder of the active wallet. 
The program will only move files that have the extensions .stack, .bin and .png
The result will be that the files specified will disapear and reappear in the Import folder. 
It should return a json file showing the file name and then what happened to that file. This could include, read error, file not found, bad permissions, unsupported file extention or moved to Import. 
Any questions?

1. The files will be submitted by a JSON string. Please create the format required and show the user how to create it. This json string can be typed in or pasted. 
2. If a file all ready exists in the Import folder, do not move it but make a note in the return JSON file. 
3. JSON will be printed to console only.
4. No file validation. 
5. Path memeory is a good idea. That way the user only has to supply the names of the files. They can put a new path in too. 



Now is time to create two commands, 61 and 62. Once command is called "Encrypt Wallet Coins and the other is called "Decrypt Wallet Coins"

We allready have a command that allows the user to upload a password. 
There must be a password uploaded before the encrypt and decrypt commands can be called. Otherwise it returns and error. 
The Encrypt command is in the context of the active wallet. It encryptes all the coins in the Pending, Withdrawn, Suspect, Bank and Fracked folders. All other files are left unencrypted. 

The decrypte command does the exact opposite. No information is needed from the user so long as the program has the encryption key and the active wallet location. 

There are some changes that are mode to the file when encrypting and decrypting. 

When encrypting the 6th byte of the file (index 4) is changed to 0x01. When decrypting that byte is changed to 0x00. 

When encrypting, index numbers 8 to 14 (inclusive) of the coin file have the first 7 bytes of an SHA-256 hash of the password put in it. When decrypting, these 7 bytes are changed to all zeros. 

The encryption method that is used is AES 128 CTR. The program should try to use the assembly commands that are built into the computer's proccessor if they are available. 

These will be commands 63 and 64 under the Wallet Management header. 

Let me know if you have any more questions. 


1. Use 61 and 62. 
2. Use the key stored by that command
3. I made an error, the encryption should be 128.
	- If I rember correctly, the user will give you the key. 
	- We use the SHA-256 Hash just to see if the user provided the correct password. We write only the first zenven types to the file and compare them to see if the password provided is correct. 
	- Derive the nounce from the password
4. Everything after the 32 byte header is encrypted. 
5. If the file contains multi-coin files, we will not encrypt those. 
6. If there is an error partway through. Stop the command and return a JSON file that lists all the files that may have been effected. 
7. Show summary at the end. 



==========================

We are done with creating the primary commands and need to decide what to do next. These are the options I can think of but there maybe more that you can think of. 
1. Encrypt and decrypt the requests and responses to the RAIDA servers.
2. Make the requests to the server threaded so they can all run at once. 
3. Make composite commmands. There are a bunch of commands that are basically functions or parts of larger commands.
For example, the Import command does the following: 
	1. Puts Coins in the Import Locker
	2. Unpacks the coins
	3. POWN Sum Coins
	4. Grades Coins
	5. Find Coins if some are in Limbo
	6. Fix Fracked Coins



Withdraw coin. 

Now we can move on to either threading the Coin Operations to that all RAIDA are contacted in Parallel or adding encryption. What is a better option? We need to add ecryption to reading local files and reading and 

Coin Nice Address. 
Put Coins in Import:


Wallet Management command 63 will be called "Put Files in Import".
The command will be supplied an array of filenames (Absolute). 
The program will take that list and move them (not copy and delete) to the Import folder of the active wallet. 
The program will only move files that have the extensions .stack, .bin and .png
The result will be that the files specified will disapear and reappear in the Import folder. 
It should return a json file showing the file name and then what happened to that file. This could include, read error, file not found, bad permissions, unsupported file extention or moved to Import. 
Any questions?

1. The files will be submitted by a JSON string. Please create the format required and show the user how to create it. This json string can be typed in or pasted. 
2. If a file all ready exists in the Import folder, do not move it but make a note in the return JSON file. 
3. JSON will be printed to console only.
4. No file validation. 
5. Path memeory is a good idea. That way the user only has to supply the names of the files. They can put a new path in too. 



Now is time to create two commands, 61 and 62. Once command is called "Encrypt Wallet Coins and the other is called "Decrypt Wallet Coins"

We allready have a command that allows the user to upload a password. 
There must be a password uploaded before the encrypt and decrypt commands can be called. Otherwise it returns and error. 
The Encrypt command is in the context of the active wallet. It encryptes all the coins in the Pending, Withdrawn, Suspect, Bank and Fracked folders. All other files are left unencrypted. 

The decrypte command does the exact opposite. No information is needed from the user so long as the program has the encryption key and the active wallet location. 

There are some changes that are mode to the file when encrypting and decrypting. 

When encrypting the 6th byte of the file (index 4) is changed to 0x01. When decrypting that byte is changed to 0x00. 

When encrypting, index numbers 8 to 14 (inclusive) of the coin file have the first 7 bytes of an SHA-256 hash of the password put in it. When decrypting, these 7 bytes are changed to all zeros. 

The encryption method that is used is AES 128 CTR. The program should try to use the assembly commands that are built into the computer's proccessor if they are available. 

These will be commands 63 and 64 under the Wallet Management header. 

Let me know if you have any more questions. 


1. Use 61 and 62. 
2. Use the key stored by that command
3. I made an error, the encryption should be 128.
	- If I rember correctly, the user will give you the key. 
	- We use the SHA-256 Hash just to see if the user provided the correct password. We write only the first zenven types to the file and compare them to see if the password provided is correct. 
	- Derive the nounce from the password
4. Everything after the 32 byte header is encrypted. 
5. If the file contains multi-coin files, we will not encrypt those. 
6. If there is an error partway through. Stop the command and return a JSON file that lists all the files that may have been effected. 
7. Show summary at the end. 



==========================

We are done with creating the primary commands and need to decide what to do next. These are the options I can think of but there maybe more that you can think of. 
1. Encrypt and decrypt the requests and responses to the RAIDA servers.
2. Make the requests to the server threaded so they can all run at once. 
3. Make composite commmands. There are a bunch of commands that are basically functions or parts of larger commands.
For example, the Import command does the following: 
	1. Puts Coins in the Import Locker
	2. Unpacks the coins
	3. POWN Sum Coins
	4. Grades Coins
	5. Find Coins if some are in Limbo
	6. Fix Fracked Coins



Withdraw coin. 

Now we can move on to either threading the Coin Operations to that all RAIDA are contacted in Parallel or adding encryption. What is a better option? We need to add ecryption to reading local files and reading and 

Coin Nice Address. 
1. The encryption coin will be selected by using the "Get Encryption Key Struct" command/function. 

Technically, this stuct will be used for encryption and not a coin as the key struct maybe made of parts of many coins.

2. The requester will use what ever Key Struct the Get Encryption Key Struckt" returns. If rows of the struct are all zeros then no encyption will be used for that RAIDA request. The Get Encryption Key Stuckt may also return an error that needs to be handled. But in general, the caller will use what the struct tells it to use.  

The "Remove Coins from Locker" command is an exception to the rule that calls to the raida should use encryption type 1. The lockercode will be used as a key with encryption type 2 instead of encryption type 1 but only if there are no coins already in the wallet. 

3. The RAIDA's response body is encrypted using the same key and nouce as the client used for the request. If there is an empty response body then no decryption is necessary except for the challenge that the client sent the RAIDA. 
See attached standard. 
Encrypted responses are only received after encrypted requests. 

4. Nounce Echo is for future use and the response echo bytes can be ignored.

5. Generating a unique nounce for each raida is fine. 

6. Go with your recommendation to default to encrypted type 1 and fall back to 0.

7. The first 16 bytes of the request header are not encrypted and do not need to have any changes made. However, The next 16 bytes are specifically for encryption with the exception of bytes at index 22 and 23 that are to describe the length of the entire body including the last 2 terminating bytes. 

Let me know if you have more questions. 
=============
Answers to your latest questions. 
1. Please look at how the server handles this nounce issue. I think you can find it in this server source code or one of the source files around it. 

2. The 16 challenge bytes are always the first 16 bytes of the request body. They are always encrypted if encryption is used. However, I seem to remmber that part of the challenge was used for CRC. You can see how the CRC is used in the server's utils.c file. 
Sample Request that is not encrypted: 

Offset | 00 01 02 03 04 05 06 07 08 09 0A 0B 0C 0D 0E 0F | ASCII
-------|------------------------------------------------|------------------
0x0000 | 01 00 0C 00 00 00 00 06 00 00 00 00 00 00 00 00 | ................
0x0010 | 00 00 00 00 00 00 00 12 00 00 00 00 00 00 00 00 | ................
0x0020 | 1C 6D 18 5C E4 27 D3 AF 3C 73 A7 4C 50 A3 32 99 | .m.\.'..<s.LP.2.
0x0030 | 3E 3E                                           | >>

3. Do not include Type 2 encryption right now. 

Also, we need to be able to use the Echo command without encryption and with encryption. So perhaps create another command on the menu number 100 that uses encryption while command 99 does not use encryption. 


  
  
  
  

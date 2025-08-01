Fix commander reads all the coins into ram and organizes the fix process. 

Parameters:

path_to_wallet: String. A path that is to the parent folder that will contain the folders needed here inluding the Fracked folder. 

path_to_Key_Coin: String. The path to the coin file that will be used to encrypt the requests. 

echo_array: int. Time in milliseconds that the last echo required. 

last_times_array: Time it took the last calls to finnish in milliseconds.  


1. We look into a folder called "fracked" and make a list of all the file names
2. We create a table in RAM called "fracked_coins".
  The fracked_coins table has just two columns:
    coin_id which is a five byte primary key. The second column is an enumerator named coin_stats
   * enum coin_status = ["BANK", "FRACKED", "TRASH", "COUNTERFEIT", "LIMBO", "SUSPECT"]
Then we create 25 tables (one for each raida server 0-24. These are called "authenticity_number_status" tables the following columns:
  1. coin_id which is a foreigh key to the coin_status table.
  2. The column authenticity_number is a fixed sixteen bytes
  3. The column proposed_authenticity_number is a fixed sixteen bytes too.
  4. The last column is an enum called an_status defined as: ["AUTHENTIC", "BROKE_KEY", "CLOCK_TIMEOUT", "DNS", "ERROR", "FAILED", "0_UNTRIED"]
The length of the authenticity_number_status table should be the same as the number of .bin files in the "Fracked" folder.

Third table is actually just an array called "tickets" with a length of 25 and a data type of int. It should be initialized so that all are zeros. 

Function Read into array
The function shall look into a folder called "Fracked" that is within th path_to_wallet parameter passed to the function. 
A list of all the files that end in .bin in the fracked folder will be made and each coin will have it's own loop. The loops will:

1. Find the five byte coin_id in the .bin file and write it to the tables. These bytes are byte indexes 34,35,36,37 and 38 in the .bin file.
2. Get the POWN string by reading the bytes in the .bin file indexed 16 to 31 inclusive. Read this as an array of 32 hexidecimal characters. 
3. Put the coin_id in the fracked_coins table with the status set to "Fracked".
4. Put one row into all 25 authenticity_number_status tables with each row having the same coin_id.
5. The array of authenticity numbers will be extracted from bytes 39 to 439 in the .bin file. The first 16 bytes are writen to the table for raida server 0. Then the next 16 bytes being written to the table for raida server 1. And so on until the last 16 byes of the authenticity numbers are put in the tablre for raida server 24.
7. The columsn for the proposed_authenticity_numbers can be all zeros.
8. Set the an_status according to the pown string. Each hexidecimal character in the pown string correspond to a different status as shown:
   
   0x00 = "0_UNTRIED"

   0x01 =  "BANK"

   0x0A =  "AUTHENTIC"

   0x0B =  "BROKE_KEY"

   0x0C =  "CLOCK_TIMEOUT"

   0x0D  = "DNS"

   0x0E =  "ERROR"

   0x0F =  "FAILED"

Now the files are in the tables in RAM. 

Now we will create the request:

1. Create an array of 25 GUIDs (16 bytes) called "challenge_array"

2. Create 25 Threads (one for each raida server)
3. The threads are not allowed to read or write to the coin_status table. They can read and write to their own authenticity_number_status table. They are all able to read and write to the ticket array.
4. Pass by reference to each thread the authenticity_number_status and the ticket array.



5. Monitor the authenticity_number_status tables. If a coin has all status's equal to "AUTHENTIC", then that coin file in the Fracked Folder have its Pown array updated to all 0x0A and the file can then be moved from the Fracked Folder to the Bank folder. After the move, the coin_status table will have the coin status for the file changed to BANK. If when monitoring the statuses of the coins, there are 13 or more coins found to be "FAILED", that coin file can have its 


   

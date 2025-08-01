# Handle Deposit Responses.
Once response array is retuned, this fuction will break down the bytes and move the coins from the Detect folder to the Grade folder. 

Parameters: Path to parent folder. 
Array of responses (binary)
Bit of encryption. Integer either 128 or 256
Encryption Key Array (16 bytes each) or 32


What is does: 
1. Moves a file from the Suspect folder and into the Grade folder and changes the POWN string and the Authenticity Numbers
2. Records statistics into a CSV file so that it can be analysed by AI to create models.

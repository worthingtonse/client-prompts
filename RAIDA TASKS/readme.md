# Creating Prompts for RAIDA Calls

## General Policies
* Don't create new variables if you can use the existing ones. (Pass by reference)
* Keep consistant naming conventions.
* Create modules full of common functions that can be imported to the program

## Typical parts of any creating a prompt that will make requests to the RAIDA
0. Determine what variables should be global to the .exe so that all functions can access them. May include: 
   * Array of Challenges
   * Encryption Keys
   * New ANs (Proposed Authenticity Numbers)
   * Request array
   * response array
   * Location of error logs
   * Location of special logs like the Echo log.
   * Parent Director of wallet
2. Determine what general reusable functions should be improted into the program. These function should be created seperatly from the raida command and reusable by many commands.
    * Generate Proposed Authenticity Numbers 
    * Calcualte Timeout with AI (for each raida). Returns an array
    * Create, Read, Update and Move coins files (Coin files should never be deleted)
    * Decrypt coin files
    * Encrypt coin files
    * Encrypt the request bodies
    * Generate challenges (GUIDs send in the requests)
    * Send Request and return Response.
    * Decrypt Resulsts
    * Log results (sandard)

3. Determine what specialized/custom functions are required for the commands such as: 
   * Create an Array of Request to the Raida
   * Parse responses
   * Take specific Actions
   * Do specialized logging 

4. Determine what parameters the request will require such as: 
   * File encryption key (The hash of the users password) for file access
   * Path the shared secrets (Key files that maybe just be CloudCoin files)
   * Timeout calculations (How long should the program wait for a response after it sends a request to the Raida) **This could be calculated within the .exe**
   * Path to parent folder (wallet) that will be used (Bank, Fracked, Etc)
   * Array of files to used in the operation (if Any) **This could be calculated within the .exe**
   * Arrays of PANs ( if ANs are to change) **This could be calculated within the .exe**
   * Hash of Locker Key.  **This could be calculated within the .exe**
  
5. Create the sequence of events such as: 
   * Validate arguments/parameters passed in
   * Do the things that are needed before the array of requests can be created
   * Create the requests
   * Encrypt request bodies
   * Calculate timeouts
   * Send requests and return responses
   * Stop timer
   * Decrypt response and check challenge
6. When telling AI how to create the prompt, include the relevant Context files (or maybe just all of them)
   
   * Take actions that depend on the resluts
   * Log results
   * Return results



# Generate PANS

Function generate_pans()

Thie function returns an array of 25 random 128 bit AES keys. PAN means Proposed Authenticity Numbers. 

The function accepts a parameter that is an integer and is called the "generataion_method".

The generataion_method will be 0 for right now but we want to have a switch on it so that other generation methods can be added in the
future. 

The function uses the best random number generator possible. 

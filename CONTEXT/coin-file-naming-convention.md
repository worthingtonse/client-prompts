# Coin File Naming Convention
By using a standard naming convention, applications and users can see how many coins a file holds and tag the coins with memos. 

The binary files will have a common naming convention. There is one convention for a files with a single note and another for files with many notes. 

## Single Note File Names
We are accurate to one satoshi which represents a decimal, seven zeros, and a 1. However, for ease of human reading, we diplay fractions with a hyphen between every four digits. Trainling zeros are removed. 

Index | Part Name | Allowable Values | Description
---|---|---|---
0 | Denomination | See [Denomionations](denominations.md) | Number formatted. 
1 | space seperator | ' ' | A space to seperate index 0 and 1. 
2 | CoinName | "CloudCoin" | Name of the coin.
3 | space seperator | ' ' | A space to seperate index 0 and 1. 
4 | Prefix | '#'| Shows the next number will be a serial number. 
5 | Serial Number | Any Four Bytes |  The serial number of the coin formatted as an unsigned integer.
3 | space seperator | ' ' | A space to seperate index 0 and 1. 
6 | Tag | Any string allowable in all OS's filenames | Add a apostraphy at the fron and end of the string. 
7 | Extension | ".bin" | Short for binary. Allows binary readers to open it.


Sample file names:
```c
1,000 CloudCoin #7998 'From Ron'.bin
Key CloudCoin #499 'IP 46.65.33.34 port 7099 app 25'.bin
0.001 CloudCoin #89269 ''.bin
0.000-0001 CloudCoin #879398 'j'.bin
```


## File Nameing Convention For Files with Multiple Coins:
If there are more than 1 token in the file, the sum of all the tokens will be in the name and so will the number of coins.

Index | Part Name | Allowable Values | Description
---|---|---|---
0 | Total Value | Any value formatted with commas after each 3 digits in whole numbers and hypens after each four digits for fractions. No zeros at the end| How much the coin file is worth
1 | space seperator | ' ' | A space to seperate index 0 and 1. 
2 | CoinName | "CloudCoin" | Name of the coin.
3 | space seperator | ' ' | A space to seperate index 0 and 1. 
4 | Prefix | '#'| Shows the next number will be a number. 
5 | Numer of Notes | Any two Bytes |  The number of coins in the coin file. 
3 | space seperator | ' ' | A space to seperate index 0 and 1. 
6 | Tag | Any string allowable in all OS's filenames | Add a apostraphy at the fron and end of the string. 
7 | Extension | ".bin" | Short for binary. Allows binary readers to open it.

Samples:
```c
0.0830-01 CloudCoin #55 'From Ron'.bin
0.5016-7 CloudCoin #89 ''.bin
0.0040-0099 CloudCoin #2 ''.bin
12,441.0000-034 CloudCoin #12 ''.bin
```

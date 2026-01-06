# Address Format
For the format of the email addresses, I am thinking this:

Everything is case-insensitive
## Mail Parts
Part | Name | Command Character | Required?|  Explanation
---|---|---|---|---
0 | Title/Group/Affiliationor Domain| ~ | Optional | This is chosen by the user. No non printable characters like spaces, tabs, etc, Quote marks, Half Quotes and back ticks allowed. UTF-8
1 | First Name | .| Optional | Could also be something else later
2 | Last Name| . | Optional | Could also be something else later
3 | Domain | @ |Defaults to qmail|This is a byte of the four byte serial number. Default is @qmail
4 | SN(Serial Number) | in Base32 | Required 
5 | Class | First Word | Required | Shows how much the user Staked. See table below

## Status
Status | Stake in CC |
---|---
Bit | 1
Byte | 10
Kilo | 100
Mega | 1000
Giga | 10000

## Calculating base32
ABCDEFGHJKLMNPQRSTUVWXYZ23456789

## Sample Email Addresses
```
Sean.Worthington@Founder|73F.Giga

Tabeen.Khajawal.GUI@GUI|F28.Mega

Mohsin.Mehraj@Programmer|AF5.Kilo

Connie.Willis@BlueRockTalk|UHP.Byte

Wally.Johnson@Captain|MRC.Bit
```
Smalles address allowed:
```
HSW.Giga
```
This gives us a mix of user creativity, verified name, Status and fixed representation of the user's serial number. 

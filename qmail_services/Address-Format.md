# Address Format
For the format of the email addresses, I am thinking this:

Everything is case-insensitive
## Mail Parts
Part | Name | Command Character | Required?|  Explanation
---|---|---|---|---
1 | Status | First Word | Required | Shows how much the user Staked. See table below
2 | Title/Group/Affiliation| ~ | Optional | This is chosen by the user. No non printable characters like spaces, tabs, etc, Quote marks, Half Quotes and back ticks allowed. UTF-8
3 | First Name | .| Optional | Could also be something else later
2 | Last Name| . | Optional | Could also be something else later
2 | SN(Serial Number) | # | Required 
2 | TLD (Top Level Domain) | @ |Defaults to qmail|This is a byte of the four byte serial number. Default is @qmail

## Status
Status | Stake in CC |
---|---
Bit | 1
Byte | 10
Kilo | 100
Mega | 1000
Giga | 10000

## Sample Email Addresses
Status, User Defined Group, First Name, Last Name, SN in Base 31 @ TLD
For Phase I, we assume that everyone is on QMail domain and will not include the @Qmail but assume it it there.
```
Giga~Founder.Sean.Worthington#73F

Mega~GUI.Tabeen.Khajawal#F28

Kilo~Programmer.Mohsin.Mehraj#AF5

Byte~BlueRockTalk.Connie.Willis#UHP

Bit~Captain.Wally.Johnson#MRC
```
Smalles address allowed:
```
Giga#HSW
```
This gives us a mix of user creativity, verified name, Status and fixed representation of the user's serial number. 

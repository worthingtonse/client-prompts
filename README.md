
![AI Prompting](ai_prompt.webp "Prompting AI for a program")
# CloudCoin Desktop Prompts for AI
These are prompts that can be used for creating a client in any programming language.

They create data-pipelines so that each function is a workflow of different data transformers. 
 ## Here is a list of all the servicers we need to have done:

## Global Asyncronistic Functions (needs task check)
Name | Description | Parameters | sample call | sample response
---|---|---|---|---
echo-raida | Sees if raida can be contacted using no encryption | none | echo-raida | will return csv. See below
verify-encryption-keys | Echos with encryption to see if encryption keys need to be fixed | Path to keys| verify-keys "C:\User\Keys\mykey.key" | will return csv report. See below
show-verson | Returns the versions of the raida servers | none | show-verson | will return csv string. See below
count-raidas-coins | Returns the number of coins that each raida has | none | count-raidas-coins | will return csv string. See below
show-task-progress | Returns the state of a task (ansync call) | Task ID | show-task-progress 983920 | will return csv string. See below
translate-error | Translates an error code into the locale specified | error code, locale | translate-error 983920 en-US| 	A language code (e.g., "en-US", "es-ES") for translating error messages.
translate-text | Translates labels to other languages | words, local | translate-text "Delete Wallet" en-US | Returns translated words or error code. 

## Global Synchtoniztic Functions 

Name | Description | Parameters | sample call | sample response
---|---|---|---|---
show-config-info | Reads the configuration file | none | show-config-info | will return ini string (see format below)
update-config-info | Updates the configuration file | Many | update-config-info -something value -sos value -sob value | Returns "success" error string.
list-locations | Reads the locations file | none | list-locations | Returns a list of locations, one for each line
list-wallets | Returns the foldernames in the 'Wallets' folder  | location path | list-wallets "C:\Users\User\CC\"| Returns a list of wallets, one for each line
creat-wallet | Creates a folder in the 'Wallets' folder | Path, Wallet Name | creat-wallet "C:\Users\User\CloudCoin_Pro\Wallet" "Sean's Wallet" | Returns "success" error string.
usb-detected | Sees if the program is running from a USB drive | none | detect-usb | Will return "true" or "false" or error code. 
```
Alternative PDUs document. 
==================
Global Functions:
==================
	ASYNCRONIZED
	------------------
		echo-raida
		show-verson
		count-raidas-coins
		show-task-progress
	------------------
	SYNCRONIZED
	------------------
		show-config-info
		update-config-info
		list-locations
		list-wallets
		creat-wallet
		detect-usb
		load-and-verify-password
		
===================
Wallet Functions:
===================
	ASYNCRONIZED
	-------------------
		examine-coin-health
		withdraw-to-locker
		deposit-from-locker
		deposit-coins-from-files
		list-locker-coins
		fix-coins
		find-coins
		join-coins

	SYNCRONIZED
	--------------------
		pick-files
		transfer-coins
		show-coins
		delete-wallet
		list-transactions
		backup-wallet
		set-png-template
		show-transaction-receipt
		export-coins-to-bin
		export-coins-to-png-template
		read-dropdown-export-locations

========================
Exchange Functions
========================
	ASYNCRONIZED
	-------------------

read-exchange-rate
send-to-exchange
withdraw-from-exchange
exchange
exchange-address
exchange-peek
```
show-config-info | Reads the configuration file | none | show-config-info | will return ini string (see format below)
verify-password | creates a hash of the password and checks to see if it matches the ones in coin files | password | verify-password "I like turtles" | Returns "success" error string.

# Echo-Raida Response format
```
{  
	"online": 25,  
	"pownstring": 
	"ppppppppppppppppppppppppp",  
	"pownarray": [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],  
	"latencies": [1104,1104,1417,1407,1397,1416,1405,1412,1397,1407, 1406,1397,1413,1412,1405,1398,1413,1398,1414,1397,1410,1404,1403,1415,1113  ]
}
```



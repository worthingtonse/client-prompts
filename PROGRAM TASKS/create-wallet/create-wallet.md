# Create Wallet


## 1. Overview
The create wallet command writes the standard folders and files into the folder specified. 

## 2. Return Value

The variable the is return will be either "success" or an error as listed in the error table below. 

## 4. Main Function: Unpack
### 4.1. Parameters

Name | Type | Description
---|---|---
$path | string | The path to the Wallets folder such as: "C:\Users\User\CloudCoin_Pro\Wallets\"
$wallet-name | string | The name of the folder to become the wallet. Must not contain any illegal characters for file names. 

4.2. Return Value
Type: string 
Description: Results of this function

## 5. Execution Logic

1. Validate the $path parameters so that the path exists.
2. Validate the $wallet-name parameter so that it does not contain any characters that are not allowed for folder names and that a folder with that name does not already exist.

4. Create the folders in the path variable if it does not exist.
   
5. Write the following structure in the folder specified by the path. Files will be empty: 

```c
$path
├── Default
└── $wallet-name
      ├── Bank
      ├── Corrupted
      ├── config.toml
      ├── Counterfeit
      ├── Duplicates
      ├── Encryption_Failed
      ├── Errored
      ├── Export
      ├── Fracked
      ├── Grade
      ├── Import
      ├── Imported
      ├── Limbo
      ├── Lockered
      ├── Pending
      ├── Receipts
      ├── Sent
      ├── Suspect
      ├── transactions.csv
      ├── Trash
      └── Withdrawn
```


## **6\. Error Handling**

| Error Code | Description |
| :---- | :---- |
| ERROR:PATH-INVALID | The specified path is invalid. |
| ERROR:CANNOT-FIND-PARENT-FOLDER | The specified import directory does not exist. |
| ERROR:CANNOT-WRITE-TO-PARENT | The application lacks permissions to write files to the suspect directory. |
| ERROR:FOLDER-NAME-USES-PROHIBITED-CHARACTERS | The name for the wallet provided had characters that are not allowed to be in folder names. |
| ERROR:WALLET-ALREADY-EXISTS | That wallet already exists. |



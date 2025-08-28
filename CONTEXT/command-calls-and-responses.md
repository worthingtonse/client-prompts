# Command Calls and Responses

This document provides a quick reference for CloudCoin Pro commands, their parameters, and expected responses.

## Response Structure

All commands follow a consistent response structure. Only the `data` and `message` fields change between commands.

## Commands Overview

| Name | Type | Description | Parameters | Sample Call |
|------|------|-------------|------------|-------------|
| echo-raida | Async | Checks RAIDA server health and response times | None | `echo-raida` |
| task-status | Sync | Returns status of an asynchronous task | Task ID | `task-status "pown-Aug-18-2025-2:24pm-PST"` |
| show-version | Async | Gets software version of each RAIDA server | None | `show-version` |
| count-raidas-coins | Async | Queries each RAIDA server to determine the total number of coins held by each server | password (optional) | `count-raidas-coins` or `count-raidas-coins "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6"` |
| list-wallets | Sync | Scans and returns all valid wallet names in the wallets directory | wallets_path | `list-wallets "D:\CloudCoin\Pro\Wallets\"` |
| create-wallet | Sync | Creates a new wallet with complete directory structure | wallets_path, wallet_name | `create-wallet "D:\CloudCoin\Pro\Wallets\" "MyNewWallet"` |
| verify-password | Sync | Verifies password hash against encrypted coin files in a wallet | wallet_path, password_hash | `verify-password "D:\CloudCoin\Pro\Wallets\MyWallet" "a1b2c3d4e5f6a7"` |
| break-coins | Async | Breaks one higher-denomination coin into ten lower-denomination coins | wallet_name | `break-coins "MyWallet"` |
| join-coins | Async | Consolidates multiple lower-denomination coins into a single higher-denomination coin | wallet_name | `join-coins "MyWallet"` |
| find-coins | Async | Determines the status of coins that are in limbo after failed operations | wallet_name | `find-coins "MyWallet"` |
| fix-coins | Async | Repairs compromised coins by addressing inconsistencies and attempting recovery | wallet_name | `fix-coins "MyWallet"` |
| list-locations | Sync | Returns all configured data locations with real-time calculated information | None | `list-locations` |
| get-transaction-receipt | Sync | Retrieves the complete content of a specific transaction receipt file | wallet_path, receipt_filename | `get-transaction-receipt "D:\CloudCoin\Pro\Wallets\MyWallet" "2025-02-25_17-34-00.withdraw-to-locker.txt"` |
| list-transactions | Sync | Returns wallet transaction history with automatic balance reconciliation | wallet_path | `list-transactions "D:\CloudCoin\Pro\Wallets\MyWallet"` |
| show-wallet-coins | Sync | Returns detailed coin information including denomination counts and balance with automatic reconciliation | wallet_path | `show-wallet-coins "D:\CloudCoin\Pro\Wallets\MyWallet"` |

## 1. echo-raida

**Type**: Asynchronous  
**Description**: Checks the health, status, and response times of all RAIDA servers

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| None | - | - | No parameters required |

### Sample Response (Task Created)
```json
{
  "status": "success",
  "message": "Echo task created",
  "data": {
    "task_id": "echoraida-Aug-25-2025-10:30am-PST",
    "status": "pending"
  }
}
```

### Sample Response (Task Completed)
```json
{
  "status": "success",
  "message": "RAIDA echo check complete", 
  "data": {
    "online": 25,
    "pownstring": "ppppppppppppppppppppppppp",
    "pownarray": [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    "latencies": [210,215,230,205,288,212,218,221,244,217,219,209,211]
  }
}
```

## 2. task-status

**Type**: Synchronous  
**Description**: Returns information about a previously created task

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| id | string | Yes | Task ID in format: "command-date-time-timezone" |

### Sample Response (In Progress)
```json
{
  "status": "success",
  "payload": {
    "id": "pown-Aug-18-2025-2:24pm-PST",
    "status": "running",
    "progress": 50,
    "message": "Processing...",
    "data": null
  }
}
```

### Sample Response (Completed)
```json
{
  "status": "success",
  "payload": {
    "id": "pown-Aug-18-2025-2:24pm-PST", 
    "status": "completed",
    "progress": 100,
    "message": "Command Completed",
    "data": {
      "online": 25,
      "pownstring": "ppppppppppppppppppppppppp",
      "latencies": [1104,1417,1487,1327,1316,1485,1412]
    }
  }
}
```

## 3. show-version

**Type**: Asynchronous  
**Description**: Gets the software version of each server in the RAIDA network

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| None | - | - | No parameters required |

### Sample Response (Task Created)
```json
{
  "status": "success",
  "message": "Version check task created",
  "data": {
    "task_id": "showversion-Aug-25-2025-10:35am-PST",
    "status": "pending"
  }
}
```

### Sample Response (Task Completed)
```json
{
  "status": "success",
  "payload": {
    "id": "showversion-Aug-25-2025-10:35am-PST",
    "status": "completed",
    "progress": 100,
    "message": "Command Completed",
    "data": [
      {"raida_index": 0, "version": "2.8.1", "status": "pass"},
      {"raida_index": 1, "version": "2.8.1", "status": "pass"},
      {"raida_index": 2, "version": "2.8.1", "status": "pass"}
    ]
  }
}
```

## 4. count-raidas-coins

**Type**: Asynchronous  
**Description**: Queries each RAIDA server to determine the total number of coins held by each server in the network

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| password | string | No | Optional 16-byte password for authentication (hex string). If not provided, uses zeros |

### Sample Response (Task Created)
```json
{
  "status": "success",
  "message": "Count RAIDA coins task created",
  "data": {
    "task_id": "countraidascoins-Aug-25-2025-10:40am-PST",
    "status": "pending"
  }
}
```

### Sample Response (Task In Progress)
```json
{
  "status": "success",
  "payload": {
    "id": "countraidascoins-Aug-25-2025-10:40am-PST",
    "status": "running",
    "progress": 65,
    "message": "Querying RAIDA servers for coin counts...",
    "data": null
  }
}
```

### Sample Response (Task Completed)
```json
{
  "status": "success",
  "payload": {
    "id": "countraidascoins-Aug-25-2025-10:40am-PST",
    "status": "completed",
    "progress": 100,
    "message": "RAIDA coin count query completed",
    "data": {
      "total_servers_queried": 25,
      "successful_responses": 23,
      "failed_responses": 2,
      "coin_counts": [
        {"raida_id": 0, "coin_count": 15234, "status": "success"},
        {"raida_id": 1, "coin_count": 15287, "status": "success"},
        {"raida_id": 2, "coin_count": 15156, "status": "success"},
        {"raida_id": 3, "coin_count": 15198, "status": "success"},
        {"raida_id": 4, "coin_count": 15243, "status": "success"},
        {"raida_id": 5, "coin_count": 15267, "status": "success"},
        {"raida_id": 6, "coin_count": 15189, "status": "success"},
        {"raida_id": 7, "coin_count": 15212, "status": "success"},
        {"raida_id": 8, "coin_count": 15234, "status": "success"},
        {"raida_id": 9, "coin_count": 15198, "status": "success"},
        {"raida_id": 10, "coin_count": 15267, "status": "success"},
        {"raida_id": 11, "coin_count": 15243, "status": "success"},
        {"raida_id": 12, "coin_count": 15156, "status": "success"},
        {"raida_id": 13, "coin_count": 15287, "status": "success"},
        {"raida_id": 14, "coin_count": 15234, "status": "success"},
        {"raida_id": 15, "coin_count": 15198, "status": "success"},
        {"raida_id": 16, "coin_count": 15212, "status": "success"},
        {"raida_id": 17, "coin_count": 15189, "status": "success"},
        {"raida_id": 18, "coin_count": 15267, "status": "success"},
        {"raida_id": 19, "coin_count": 15243, "status": "success"},
        {"raida_id": 20, "coin_count": 15156, "status": "success"},
        {"raida_id": 21, "coin_count": 15287, "status": "success"},
        {"raida_id": 22, "coin_count": 15234, "status": "success"},
        {"raida_id": 23, "coin_count": 0, "status": "failed", "error": "timeout"},
        {"raida_id": 24, "coin_count": 0, "status": "failed", "error": "connection_refused"}
      ],
      "summary": {
        "total_coins_network": 381945,
        "average_coins_per_server": 16608,
        "network_health": "92% servers responding"
      }
    }
  }
}
```

## 5. list-wallets

**Type**: Synchronous  
**Description**: Scans the wallets directory and returns a simple list of all valid wallet names found

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| wallets_path | string | Yes | The path to the Wallets folder such as: "D:\CloudCoin\Pro\Wallets\" |

### Sample Response (Success)
```json
{
  "status": "success",
  "message": "Wallets found successfully",
  "data": [
    "Default",
    "MyPersonalWallet", 
    "BusinessWallet",
    "TestWallet"
  ]
}
```

### Sample Response (Error)
```json
{
  "status": "error",
  "message": "ERROR:PATH-INVALID",
  "data": null
}
```

## 6. create-wallet

**Type**: Synchronous  
**Description**: Creates a new wallet with complete directory structure and configuration files. Uses updated folder structure and transactions.csv format with new Task ID format.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| wallets_path | string | Yes | The path to the Wallets directory such as: "D:\CloudCoin\Pro\Wallets\" |
| wallet_name | string | Yes | The name of the wallet folder. Must not contain illegal characters for file names |

### Sample Response (Success)
```json
{
  "status": "success",
  "message": "Wallet created successfully",
  "data": "success"
}
```

### Sample Response (Error)
```json
{
  "status": "error",
  "message": "ERROR:WALLET-ALREADY-EXISTS",
  "data": null
}
```

## 7. verify-password

**Type**: Synchronous  
**Description**: Verifies that a pre-computed password hash matches the password hash stored in encrypted coin files within a wallet directory. Updated to test only one coin file from Bank/ or Fracked/ folders instead of multiple files.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| wallet_path | string | Yes | The path to a specific wallet directory such as: "D:\CloudCoin\Pro\Wallets\MyWallet" |
| password_hash | string | Yes | Pre-computed SHA-256 hash (first 7 bytes as hex string, 14 characters) |

### Sample Response (Success - Password Valid)
```json
{
  "status": "success",
  "message": "Password hash verification successful",
  "data": {
    "password_verification": {
      "timestamp": "2025-08-25T10:30:00Z",
      "wallet_path": "D:/CloudCoin/Pro/Wallets/MyWallet",
      "verification_result": "success",
      "summary": {
        "hash_valid": true,
        "files_tested": 1,
        "files_matched": 1,
        "files_failed": 0,
        "encrypted_files_found": 1,
        "unencrypted_files_found": 0
      },
      "verification_details": {
        "provided_hash": "a1b2c3d4e5f6a7",
        "hash_method": "SHA-256 (first 7 bytes)",
        "comparison_method": "secure_compare",
        "consistency_check": "passed"
      },
      "files_analyzed": [
        {
          "filename": "1,000 CloudCoin #7998 'From Ron'.bin",
          "path": "Bank/1,000 CloudCoin #7998 'From Ron'.bin",
          "file_size": 439,
          "encryption_type": 1,
          "encryption_name": "128-bit AES CTR",
          "stored_hash": "a1b2c3d4e5f6a7",
          "hash_match": true,
          "file_valid": true,
          "coin_count": 1
        }
      ],
      "validation": {
        "wallet_structure_valid": true,
        "coin_files_found": true,
        "encrypted_files_available": true,
        "hash_consistency": "match",
        "warnings": [],
        "errors": []
      }
    }
  }
}
```

### Sample Response (Error - Password Invalid)
```json
{
  "status": "error",
  "message": "Password hash does not match",
  "data": {
    "password_verification": {
      "timestamp": "2025-08-25T10:35:00Z",
      "wallet_path": "D:/CloudCoin/Pro/Wallets/MyWallet",
      "verification_result": "failed",
      "summary": {
        "hash_valid": false,
        "files_tested": 1,
        "files_matched": 0,
        "files_failed": 1,
        "encrypted_files_found": 1,
        "unencrypted_files_found": 0
      },
      "verification_details": {
        "provided_hash": "deadbeefcafebabe",
        "hash_method": "SHA-256 (first 7 bytes)",
        "comparison_method": "secure_compare",
        "consistency_check": "failed"
      },
      "validation": {
        "wallet_structure_valid": true,
        "coin_files_found": true,
        "encrypted_files_available": true,
        "hash_consistency": "no_match",
        "warnings": [],
        "errors": ["Password hash mismatch on encrypted file"]
      }
    }
  }
}
```

### Sample Response (Error - Wallet Not Found)
```json
{
  "status": "error",
  "message": "ERROR:WALLET-NOT-FOUND",
  "data": null
}
```

### Sample Response (Error - No Encrypted Files)
```json
{
  "status": "error",
  "message": "No encrypted files found for verification",
  "data": {
    "password_verification": {
      "timestamp": "2025-08-25T10:40:00Z",
      "wallet_path": "D:/CloudCoin/Pro/Wallets/EmptyWallet",
      "verification_result": "no_encrypted_files",
      "summary": {
        "hash_valid": null,
        "files_tested": 0,
        "files_matched": 0,
        "files_failed": 0,
        "encrypted_files_found": 0,
        "unencrypted_files_found": 2
      },
      "validation": {
        "wallet_structure_valid": true,
        "coin_files_found": true,
        "encrypted_files_available": false,
        "hash_consistency": "N/A",
        "warnings": ["No encrypted coin files available for password verification"],
        "errors": []
      }
    }
  }
}
```

### Sample Response (Error - Invalid Hash Format)
```json
{
  "status": "error",
  "message": "ERROR:INVALID-HASH-FORMAT",
  "data": {
    "expected_format": "14 hex characters (7 bytes)",
    "provided_hash": "abc123",
    "error_details": "Hash must be exactly 14 hexadecimal characters"
  }
}
```

## 8. break-coins

**Type**: Asynchronous  
**Description**: Breaks one higher-denomination coin into ten lower-denomination coins of the next lower denomination

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| wallet_name | string | Yes | The name of the wallet containing coins to break |

### Sample Response (Task Created)
```json
{
  "status": "success",
  "message": "Break coins task created",
  "data": {
    "task_id": "breakcoins-Aug-25-2025-11:15am-PST",
    "status": "pending"
  }
}
```

### Sample Response (Task In Progress)
```json
{
  "status": "success",
  "payload": {
    "id": "breakcoins-Aug-25-2025-11:15am-PST",
    "status": "running",
    "progress": 45,
    "message": "Breaking coins with RAIDA network...",
    "data": null
  }
}
```

### Sample Response (Task Completed - Success)
```json
{
  "status": "success",
  "payload": {
    "id": "breakcoins-Aug-25-2025-11:15am-PST",
    "status": "completed",
    "progress": 100,
    "message": "Coin break operation completed successfully",
    "data": {
      "coins_broken": 1,
      "coins_created": 10,
      "original_coin": {
        "denomination": "1000",
        "serial_number": 123456,
        "value": "1000.0"
      },
      "new_coins": [
        {
          "denomination": "100",
          "serial_number": 234567,
          "value": "100.0"
        },
        {
          "denomination": "100", 
          "serial_number": 234568,
          "value": "100.0"
        }
      ],
      "total_value_created": "1000.0",
      "raida_responses": {
        "passed": 23,
        "failed": 2,
        "success_rate": "92%"
      },
      "transaction_receipt": "breakcoins-Aug-25-2025-11:15am-PST"
    }
  }
}
```

### Sample Response (Task Completed - Partial Success)
```json
{
  "status": "success",
  "payload": {
    "id": "breakcoins-Aug-25-2025-11:15am-PST",
    "status": "completed",
    "progress": 100,
    "message": "Coin break completed with some failures",
    "data": {
      "coins_broken": 1,
      "coins_created": 10,
      "coins_in_limbo": 5,
      "original_coin": {
        "denomination": "1000",
        "serial_number": 123456,
        "value": "1000.0"
      },
      "successful_coins": 5,
      "limbo_coins": 5,
      "total_value_recovered": "500.0",
      "raida_responses": {
        "passed": 13,
        "failed": 12,
        "success_rate": "52%"
      },
      "transaction_receipt": "breakcoins-Aug-25-2025-11:15am-PST",
      "next_action": "Run fix-coins to recover coins in limbo"
    }
  }
}
```

### Sample Response (Task Failed)
```json
{
  "status": "error",
  "payload": {
    "id": "breakcoins-Aug-25-2025-11:15am-PST",
    "status": "error",
    "progress": 0,
    "message": "Break operation failed",
    "data": {
      "error_type": "INSUFFICIENT_COINS",
      "error_message": "No coins available for breaking in wallet",
      "wallet_name": "MyWallet",
      "coins_found": 0,
      "minimum_required": 1
    }
  }
}
```

### Sample Response (Error - Wallet Not Found)
```json
{
  "status": "error",
  "message": "ERROR:WALLET-NOT-FOUND",
  "data": {
    "wallet_name": "NonExistentWallet",
    "available_wallets": ["Default", "MyWallet", "BusinessWallet"]
  }
}
```

## 9. join-coins

**Type**: Asynchronous  
**Description**: Consolidates multiple lower-denomination coins into a single higher-denomination coin to optimize wallet storage

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| wallet_name | string | Yes | The name of the wallet containing coins to consolidate |

### Sample Response (Task Created)
```json
{
  "status": "success",
  "message": "Join coins task created",
  "data": {
    "task_id": "joincoins-Aug-25-2025-11:30am-PST",
    "status": "pending"
  }
}
```

### Sample Response (Task In Progress)
```json
{
  "status": "success",
  "payload": {
    "id": "joincoins-Aug-25-2025-11:30am-PST",
    "status": "running",
    "progress": 60,
    "message": "Consolidating coins with RAIDA network...",
    "data": null
  }
}
```

### Sample Response (Task Completed - Success)
```json
{
  "status": "success",
  "payload": {
    "id": "joincoins-Aug-25-2025-11:30am-PST",
    "status": "completed",
    "progress": 100,
    "message": "Coin consolidation completed successfully",
    "data": {
      "coins_joined": 10,
      "coins_created": 1,
      "original_coins": [
        {
          "denomination": "100",
          "serial_number": 123456,
          "value": "100.0"
        },
        {
          "denomination": "100",
          "serial_number": 123457,
          "value": "100.0"
        }
      ],
      "new_coin": {
        "denomination": "1000",
        "serial_number": 234567,
        "value": "1000.0"
      },
      "total_value_consolidated": "1000.0",
      "raida_responses": {
        "passed": 24,
        "failed": 1,
        "success_rate": "96%"
      },
      "transaction_receipt": "joincoins-Aug-25-2025-11:30am-PST",
      "optimization_result": {
        "coins_before": 10,
        "coins_after": 1,
        "space_saved": "90%"
      }
    }
  }
}
```

### Sample Response (Task Completed - Partial Success)
```json
{
  "status": "success",
  "payload": {
    "id": "joincoins-Aug-25-2025-11:30am-PST",
    "status": "completed",
    "progress": 100,
    "message": "Coin consolidation completed with some issues",
    "data": {
      "coins_joined": 10,
      "coins_created": 0,
      "coins_in_limbo": 10,
      "original_value": "1000.0",
      "recovered_value": "0.0",
      "raida_responses": {
        "passed": 10,
        "failed": 15,
        "success_rate": "40%"
      },
      "transaction_receipt": "joincoins-Aug-25-2025-11:30am-PST",
      "status_details": {
        "new_coin_status": "failed_creation",
        "original_coins_status": "destroyed_but_unrecovered"
      },
      "next_action": "Run fix-coins to attempt recovery of coins in limbo"
    }
  }
}
```

### Sample Response (Task Failed)
```json
{
  "status": "error",
  "payload": {
    "id": "joincoins-Aug-25-2025-11:30am-PST",
    "status": "error",
    "progress": 0,
    "message": "Join operation failed",
    "data": {
      "error_type": "INSUFFICIENT_COINS",
      "error_message": "Not enough coins of same denomination for consolidation",
      "wallet_name": "MyWallet",
      "required_coins": 10,
      "available_coins": 3,
      "suggested_action": "Add more coins of the same denomination or try break-coins instead"
    }
  }
}
```

### Sample Response (Error - Wallet Not Found)
```json
{
  "status": "error",
  "message": "ERROR:WALLET-NOT-FOUND",
  "data": {
    "wallet_name": "NonExistentWallet",
    "available_wallets": ["Default", "MyWallet", "BusinessWallet"]
  }
}
```

## 10. find-coins

**Type**: Asynchronous  
**Description**: Determines the status of coins that are in limbo after potentially failed POWN operations by checking with RAIDA servers

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| wallet_name | string | Yes | The name of the wallet containing coins in limbo to check |

### Sample Response (Task Created)
```json
{
  "status": "success",
  "message": "Find coins task created",
  "data": {
    "task_id": "findcoins-Aug-25-2025-12:00pm-PST",
    "status": "pending"
  }
}
```

### Sample Response (Task In Progress)
```json
{
  "status": "success",
  "payload": {
    "id": "findcoins-Aug-25-2025-12:00pm-PST",
    "status": "running",
    "progress": 40,
    "message": "Checking coin status with RAIDA network...",
    "data": {
      "coins_being_checked": 5,
      "servers_queried": 10,
      "responses_received": 8
    }
  }
}
```

### Sample Response (Task Completed - Coins Found)
```json
{
  "status": "success",
  "payload": {
    "id": "findcoins-Aug-25-2025-12:00pm-PST",
    "status": "completed",
    "progress": 100,
    "message": "Coin status check completed",
    "data": {
      "total_coins_checked": 5,
      "coins_found": 3,
      "coins_lost": 1,
      "coins_still_limbo": 1,
      "detailed_results": [
        {
          "coin_id": "1 CloudCoin #123456",
          "denomination": "1",
          "serial_number": 123456,
          "status": "found_with_pan",
          "authenticity_status": "authentic",
          "current_password": "pan",
          "raida_consensus": "23/25 servers confirm PAN",
          "moved_to_folder": "Bank"
        },
        {
          "coin_id": "1 CloudCoin #123457",
          "denomination": "1", 
          "serial_number": 123457,
          "status": "found_with_an",
          "authenticity_status": "authentic",
          "current_password": "an",
          "raida_consensus": "24/25 servers confirm AN",
          "moved_to_folder": "Bank"
        },
        {
          "coin_id": "1 CloudCoin #123458",
          "denomination": "1",
          "serial_number": 123458,
          "status": "found_with_pan",
          "authenticity_status": "authentic", 
          "current_password": "pan",
          "raida_consensus": "25/25 servers confirm PAN",
          "moved_to_folder": "Bank"
        },
        {
          "coin_id": "1 CloudCoin #123459",
          "denomination": "1",
          "serial_number": 123459,
          "status": "not_found",
          "authenticity_status": "counterfeit",
          "current_password": "none",
          "raida_consensus": "0/25 servers recognize coin",
          "moved_to_folder": "Counterfeit"
        },
        {
          "coin_id": "1 CloudCoin #123460",
          "denomination": "1",
          "serial_number": 123460,
          "status": "conflicted",
          "authenticity_status": "uncertain",
          "current_password": "mixed",
          "raida_consensus": "12 AN, 11 PAN, 2 neither",
          "moved_to_folder": "Limbo"
        }
      ],
      "recovery_summary": {
        "coins_moved_to_bank": 3,
        "coins_moved_to_counterfeit": 1,
        "coins_remaining_limbo": 1,
        "total_value_recovered": "3.0"
      },
      "transaction_receipt": "findcoins-Aug-25-2025-12:00pm-PST"
    }
  }
}
```

### Sample Response (Task Completed - No Limbo Coins)
```json
{
  "status": "success",
  "payload": {
    "id": "findcoins-Aug-25-2025-12:00pm-PST",
    "status": "completed",
    "progress": 100,
    "message": "No coins in limbo found",
    "data": {
      "total_coins_checked": 0,
      "limbo_coins_found": 0,
      "wallet_status": "clean",
      "folders_checked": ["Limbo", "Suspect", "Fracked"],
      "message": "All coins in wallet are properly authenticated"
    }
  }
}
```

### Sample Response (Task Failed)
```json
{
  "status": "error",
  "payload": {
    "id": "findcoins-Aug-25-2025-12:00pm-PST",
    "status": "error",
    "progress": 0,
    "message": "Find operation failed",
    "data": {
      "error_type": "NETWORK_FAILURE",
      "error_message": "Unable to reach sufficient RAIDA servers",
      "servers_reachable": 8,
      "servers_required": 13,
      "suggested_action": "Check network connection and try again"
    }
  }
}
```

### Sample Response (Error - Wallet Not Found)
```json
{
  "status": "error",
  "message": "ERROR:WALLET-NOT-FOUND",
  "data": {
    "wallet_name": "NonExistentWallet",
    "available_wallets": ["Default", "MyWallet", "BusinessWallet"]
  }
}
```

## 11. fix-coins

**Type**: Asynchronous  
**Description**: A comprehensive wallet maintenance tool that repairs compromised coins by addressing inconsistencies ("fracked") and attempting to recover coins that have failed authenticity checks ("limbo")

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| wallet_name | string | Yes | The name of the wallet containing coins to fix. Ex: "Default" |

### Sample Response (Task Created)
```json
{
  "status": "success",
  "message": "Fix coins task created",
  "data": {
    "task_id": "fixcoins-Aug-25-2025-1:45pm-PST",
    "status": "pending"
  }
}
```

### Sample Response (Task In Progress)
```json
{
  "status": "success",
  "payload": {
    "id": "fixcoins-Aug-25-2025-1:45pm-PST",
    "status": "running",
    "progress": 75,
    "message": "Healing fractured coins with RAIDA network...",
    "data": {
      "phase": "fix_operation",
      "coins_being_processed": 15,
      "tickets_obtained": 20,
      "raida_servers_responding": 23,
      "current_operation": "Sending fix requests to fractured servers"
    }
  }
}
```

### Sample Response (Task Completed - Success)
```json
{
  "status": "success",
  "payload": {
    "id": "fixcoins-Aug-25-2025-1:45pm-PST",
    "status": "completed",
    "progress": 100,
    "message": "Fix operation finished.",
    "data": {
      "total_fracked": 7500,
      "total_limbo": 1000,
      "total_fixed": 6000,
      "total_skipped": 1500,
      "total_errors": 0,
      "total_limbo_recovered": 1000,
      "summary": {
        "coins_moved_to_bank": 7000,
        "coins_moved_to_counterfeit": 500,
        "coins_remaining_fracked": 0,
        "coins_remaining_limbo": 0,
        "total_value_recovered": "7000.0"
      },
      "detailed_results": {
        "get_ticket_phase": {
          "tickets_requested": 7500,
          "tickets_obtained": 7200,
          "ticket_success_rate": "96%",
          "raida_responses": {
            "successful_servers": 24,
            "failed_servers": 1,
            "average_response_time": "245ms"
          }
        },
        "fix_phase": {
          "fix_requests_sent": 6000,
          "coins_successfully_healed": 5500,
          "coins_failed_healing": 500,
          "healing_success_rate": "92%"
        },
        "limbo_recovery": {
          "limbo_coins_found": 1000,
          "limbo_coins_recovered": 1000,
          "recovery_success_rate": "100%"
        }
      },
      "network_health": {
        "raida_consensus": "96% servers healthy",
        "total_requests_sent": 187500,
        "total_successful_responses": 179250,
        "overall_success_rate": "95.6%"
      },
      "transaction_receipt": "fixcoins-Aug-25-2025-1:45pm-PST"
    }
  }
}
```

### Sample Response (Task Completed - Partial Success)
```json
{
  "status": "success",
  "payload": {
    "id": "fixcoins-Aug-25-2025-1:45pm-PST",
    "status": "completed",
    "progress": 100,
    "message": "Fix operation completed with some issues",
    "data": {
      "total_fracked": 5000,
      "total_limbo": 500,
      "total_fixed": 3000,
      "total_skipped": 2000,
      "total_errors": 0,
      "total_limbo_recovered": 200,
      "summary": {
        "coins_moved_to_bank": 3200,
        "coins_moved_to_counterfeit": 0,
        "coins_remaining_fracked": 2000,
        "coins_remaining_limbo": 300,
        "total_value_recovered": "3200.0"
      },
      "issues_encountered": [
        "Network connectivity issues with 8 RAIDA servers",
        "2000 coins require additional healing cycles",
        "300 limbo coins need manual intervention"
      ],
      "recommendations": [
        "Check network connection and retry fix-coins",
        "Run fix-coins again for remaining fracked coins",
        "Consider running find-coins for remaining limbo coins"
      ],
      "transaction_receipt": "fixcoins-Aug-25-2025-1:45pm-PST"
    }
  }
}
```

### Sample Response (Task Completed - No Coins to Fix)
```json
{
  "status": "success",
  "payload": {
    "id": "fixcoins-Aug-25-2025-1:45pm-PST",
    "status": "completed",
    "progress": 100,
    "message": "No coins requiring fixes found",
    "data": {
      "total_fracked": 0,
      "total_limbo": 0,
      "total_fixed": 0,
      "total_skipped": 0,
      "total_errors": 0,
      "total_limbo_recovered": 0,
      "wallet_status": "healthy",
      "folders_checked": ["Fracked", "Limbo", "Suspect"],
      "message": "All coins in wallet are properly authenticated",
      "bank_coins_count": 1500,
      "total_wallet_value": "1500.0"
    }
  }
}
```

### Sample Response (Task Failed)
```json
{
  "status": "error",
  "payload": {
    "id": "fixcoins-Aug-25-2025-1:45pm-PST",
    "status": "error",
    "progress": 0,
    "message": "Fix operation failed",
    "data": {
      "error_type": "NETWORK_INSUFFICIENT",
      "error_message": "Unable to reach minimum required RAIDA servers for healing",
      "servers_reachable": 8,
      "servers_required_minimum": 13,
      "network_health": "32% servers responding",
      "suggested_actions": [
        "Check internet connection",
        "Verify RAIDA network status",
        "Try again when network conditions improve"
      ]
    }
  }
}
```

### Sample Response (Error - Wallet Not Found)
```json
{
  "status": "error",
  "message": "ERROR:WALLET-NOT-FOUND",
  "data": {
    "wallet_name": "NonExistentWallet",
    "available_wallets": ["Default", "MyWallet", "BusinessWallet"]
  }
}
```

## 12. list-locations

**Type**: Synchronous  
**Description**: Returns all configured data locations for CloudCoin Pro with real-time calculated information including accessibility, storage usage, and wallet counts

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| None | - | - | No parameters required - reads from standard CloudCoin Pro configuration |

### Sample Response (Success)
```json
{
  "status": "success",
  "message": "Locations retrieved successfully",
  "data": {
    "locations_info": {
      "timestamp": "2025-08-25T13:15:00Z",
      "total_locations": 4,
      "primary_location": "D:\\CloudCoin\\Pro\\Wallets",
      "config_source": "locations.csv",
      
      "locations": [
        {
          "path": "D:\\CloudCoin\\Pro\\Wallets",
          "is_primary": true,
          "order_index": 0,
          "csv_type": "local",
          "calculated_data": {
            "label": "Wallets",
            "detected_type": "local",
            "accessible": true,
            "exists": true,
            "writable": true,
            "last_used": "2025-08-25T13:15:00Z",
            "storage": {
              "total_size_mb": 1250.5,
              "available_space_gb": 45.2,
              "wallet_count": 3
            }
          },
          "validation": {
            "status": "valid",
            "warnings": [],
            "errors": []
          }
        },
        {
          "path": "C:\\Users\\User\\Documents\\CloudCoin\\Backup",
          "is_primary": false,
          "order_index": 1,
          "csv_type": "local",
          "calculated_data": {
            "label": "Backup",
            "detected_type": "local",
            "accessible": true,
            "exists": true,
            "writable": true,
            "last_used": "2025-08-24T15:20:00Z",
            "storage": {
              "total_size_mb": 850.2,
              "available_space_gb": 120.5,
              "wallet_count": 2
            }
          },
          "validation": {
            "status": "valid",
            "warnings": [],
            "errors": []
          }
        },
        {
          "path": "E:\\USB_Backup\\CloudCoin\\Data",
          "is_primary": false,
          "order_index": 2,
          "csv_type": "usb",
          "calculated_data": {
            "label": "Data",
            "detected_type": "usb",
            "accessible": false,
            "exists": false,
            "writable": false,
            "last_used": "2025-08-23T09:15:00Z",
            "storage": {
              "total_size_mb": 0,
              "available_space_gb": 0,
              "wallet_count": 0
            }
          },
          "validation": {
            "status": "error",
            "warnings": [],
            "errors": ["Drive not accessible", "Path does not exist"]
          }
        },
        {
          "path": "\\\\NetworkDrive\\CloudCoin\\Shared",
          "is_primary": false,
          "order_index": 3,
          "csv_type": "network",
          "calculated_data": {
            "label": "Shared",
            "detected_type": "network",
            "accessible": true,
            "exists": true,
            "writable": true,
            "last_used": "2025-08-20T14:30:00Z",
            "storage": {
              "total_size_mb": 2100.8,
              "available_space_gb": 500.0,
              "wallet_count": 5
            }
          },
          "validation": {
            "status": "valid",
            "warnings": ["Network latency detected"],
            "errors": []
          }
        }
      ],
      
      "recent_export_folders": [
        {
          "path": "C:\\Users\\User\\Documents\\CloudCoin\\Exports",
          "calculated_data": {
            "accessible": true,
            "last_used": "2025-08-25T09:45:00Z"
          }
        },
        {
          "path": "E:\\USB_Exports\\CloudCoin",
          "calculated_data": {
            "accessible": false,
            "last_used": "2025-08-22T14:15:00Z"
          }
        }
      ],
      
      "summary": {
        "total_accessible_locations": 3,
        "total_inaccessible_locations": 1,
        "total_wallets_across_locations": 10,
        "total_storage_used_mb": 4201.5,
        "locations_with_errors": 1,
        "locations_with_warnings": 1
      }
    }
  }
}
```

### Sample Response (Success - Default Configuration)
```json
{
  "status": "success",
  "message": "Using default location configuration",
  "data": {
    "locations_info": {
      "timestamp": "2025-08-25T13:15:00Z",
      "total_locations": 1,
      "primary_location": "D:\\CloudCoin\\Pro\\Wallets",
      "config_source": "default (locations.csv not found)",
      
      "locations": [
        {
          "path": "D:\\CloudCoin\\Pro\\Wallets",
          "is_primary": true,
          "order_index": 0,
          "csv_type": "local",
          "calculated_data": {
            "label": "Wallets",
            "detected_type": "local",
            "accessible": true,
            "exists": true,
            "writable": true,
            "last_used": "2025-08-25T13:15:00Z",
            "storage": {
              "total_size_mb": 450.2,
              "available_space_gb": 120.8,
              "wallet_count": 1
            }
          },
          "validation": {
            "status": "valid",
            "warnings": [],
            "errors": []
          }
        }
      ],
      
      "recent_export_folders": [],
      
      "summary": {
        "total_accessible_locations": 1,
        "total_inaccessible_locations": 0,
        "total_wallets_across_locations": 1,
        "total_storage_used_mb": 450.2,
        "locations_with_errors": 0,
        "locations_with_warnings": 0
      }
    }
  }
}
```

### Sample Response (Error - All Locations Inaccessible)
```json
{
  "status": "error",
  "message": "All configured locations are inaccessible",
  "data": {
    "locations_info": {
      "timestamp": "2025-08-25T13:15:00Z",
      "total_locations": 2,
      "primary_location": "D:\\CloudCoin\\Pro\\Wallets",
      "config_source": "locations.csv",
      
      "locations": [
        {
          "path": "D:\\CloudCoin\\Pro\\Wallets",
          "is_primary": true,
          "order_index": 0,
          "csv_type": "local",
          "calculated_data": {
            "label": "Wallets",
            "detected_type": "local",
            "accessible": false,
            "exists": false,
            "writable": false,
            "last_used": null,
            "storage": {
              "total_size_mb": 0,
              "available_space_gb": 0,
              "wallet_count": 0
            }
          },
          "validation": {
            "status": "error",
            "warnings": [],
            "errors": ["Drive not accessible", "Path does not exist"]
          }
        }
      ],
      
      "summary": {
        "total_accessible_locations": 0,
        "total_inaccessible_locations": 2,
        "total_wallets_across_locations": 0,
        "total_storage_used_mb": 0,
        "locations_with_errors": 2,
        "locations_with_warnings": 0
      },
      
      "troubleshooting": [
        "Check if primary drive D:\\ is accessible",
        "Connect USB drive if using portable storage",
        "Verify network connectivity for network locations",
        "Check file system permissions"
      ]
    }
  }
}
```


## 13. get-transaction-receipt

**Type**: Synchronous  
**Description**: Retrieves the complete content of a specific transaction receipt file from the Receipts folder without any processing or formatting

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| wallet_path | string | Yes | The path to the wallet directory containing the Receipts folder |
| receipt_filename | string | Yes | The complete filename of the receipt including extension |

### Sample Response (Success - Withdrawal Receipt)
```json
{
  "status": "success",
  "message": "Receipt retrieved successfully",
  "data": {
    "receipt_info": {
      "wallet_path": "D:\\CloudCoin\\Pro\\Wallets\\MyWallet",
      "receipt_filename": "2025-08-25_17-34-00.withdraw-to-locker.txt",
      "file_size": 2847,
      "retrieved_at": "2025-08-25T13:30:00Z"
    },
    "receipt_content": "====================================================\nCLOUDCOIN WITHDRAWAL RECEIPT\n====================================================\nTransaction ID: withdraw-Aug-25-2025-5:34pm-PST\nDate: August 25, 2025 at 5:34 PM PST\nWallet: MyWallet\n\nTRANSACTION DETAILS\n====================================================\nOperation: Withdraw to Locker\nLocker Code: ABC123DEF456\nAmount Withdrawn: 1,000.0 CloudCoins\nWallet Balance Before: 5,250.75 CloudCoins\nWallet Balance After: 4,250.75 CloudCoins\n\nCOINS WITHDRAWN\n====================================================\n• 1,000 CloudCoin #12345 'Savings Fund'\n  Status: ✅ Successfully uploaded to locker\n  Locker Slot: A-001\n  Upload Time: 5:34:15 PM\n  Verification: Passed\n\nRAIDA NETWORK STATUS\n====================================================\nServers Online: 25/25 (100%)\nUpload Success Rate: 100%\nAverage Response Time: 187ms\nNetwork Health: Excellent\n\nTRANSACTION SUMMARY\n====================================================\n✅ Withdrawal completed successfully\n✅ All coins uploaded to locker ABC123DEF456\n✅ Wallet balance updated\n✅ Transaction recorded in wallet history\n\nRECEIPT INFORMATION\n====================================================\nGenerated: August 25, 2025 at 5:34:00 PM PST\nReceipt ID: 2025-08-25_17-34-00.withdraw-to-locker\nWallet Location: D:\\CloudCoin\\Pro\\Wallets\\MyWallet\nTransaction Log Updated: Yes\n\nFor support or questions about this transaction,\nreference Transaction ID: withdraw-Aug-25-2025-5:34pm-PST\n\nThis receipt serves as proof of your CloudCoin withdrawal.\nKeep this receipt for your records.\n===================================================="
  }
}
```

### Sample Response (Success - Deposit Receipt)
```json
{
  "status": "success",
  "message": "Receipt retrieved successfully",
  "data": {
    "receipt_info": {
      "wallet_path": "D:\\CloudCoin\\Pro\\Wallets\\BusinessWallet",
      "receipt_filename": "2025-08-24_16-08-00.deposit-from-file.txt",
      "file_size": 3421,
      "retrieved_at": "2025-08-25T13:30:00Z"
    },
    "receipt_content": "====================================================\nCLOUDCOIN DEPOSIT RECEIPT\n====================================================\nTransaction ID: deposit-Aug-24-2025-4:08pm-PST\nDate: August 24, 2025 at 4:08 PM PST\nWallet: BusinessWallet\n\nTRANSACTION DETAILS\n====================================================\nOperation: Deposit from File\nSource File: C:\\Users\\User\\Downloads\\payment-coins.bin\nAmount Deposited: 2,500.25 CloudCoins\nWallet Balance Before: 10,750.00 CloudCoins\nWallet Balance After: 13,250.25 CloudCoins\n\nCOINS DEPOSITED\n====================================================\n• 1,000 CloudCoin #98765 'Client Payment A'\n  Status: ✅ Authenticated and moved to Bank\n  Authentication: 25/25 RAIDA servers confirmed\n  \n• 1,000 CloudCoin #98766 'Client Payment B'\n  Status: ✅ Authenticated and moved to Bank\n  Authentication: 25/25 RAIDA servers confirmed\n  \n• 500 CloudCoin #98767 'Client Payment C'\n  Status: ✅ Authenticated and moved to Bank\n  Authentication: 24/25 RAIDA servers confirmed\n  \n• 0.25 CloudCoin #98768 'Client Payment Fee'\n  Status: ✅ Authenticated and moved to Bank\n  Authentication: 25/25 RAIDA servers confirmed\n\nFILE PROCESSING RESULTS\n====================================================\nTotal Coins Found: 4\nSuccessfully Processed: 4\nMoved to Bank: 4\nMoved to Fracked: 0\nMoved to Counterfeit: 0\nProcessing Success Rate: 100%\n\nRAIDA NETWORK STATUS\n====================================================\nServers Online: 25/25 (100%)\nAuthentication Success Rate: 99.2%\nAverage Response Time: 156ms\nNetwork Health: Excellent\n\nTRANSACTION SUMMARY\n====================================================\n✅ Deposit completed successfully\n✅ All coins authenticated and secured\n✅ Wallet balance updated\n✅ Transaction recorded in wallet history\n✅ Source file processed and archived\n\nRECEIPT INFORMATION\n====================================================\nGenerated: August 24, 2025 at 4:08:00 PM PST\nReceipt ID: 2025-08-24_16-08-00.deposit-from-file\nWallet Location: D:\\CloudCoin\\Pro\\Wallets\\BusinessWallet\nTransaction Log Updated: Yes\n\nFor support or questions about this transaction,\nreference Transaction ID: deposit-Aug-24-2025-4:08pm-PST\n\nThis receipt serves as proof of your CloudCoin deposit.\nKeep this receipt for your records.\n===================================================="
  }
}
```

### Sample Response (Success - POWN Operation Receipt)
```json
{
  "status": "success",
  "message": "Receipt retrieved successfully",
  "data": {
    "receipt_info": {
      "wallet_path": "D:\\CloudCoin\\Pro\\Wallets\\MyWallet",
      "receipt_filename": "2025-08-23_12-41-00.pown-authentication.txt",
      "file_size": 1856,
      "retrieved_at": "2025-08-25T13:30:00Z"
    },
    "receipt_content": "====================================================\nCLOUDCOIN POWN AUTHENTICATION RECEIPT\n====================================================\nTransaction ID: pown-Aug-23-2025-12:41pm-PST\nDate: August 23, 2025 at 12:41 PM PST\nWallet: MyWallet\n\nOPERATION DETAILS\n====================================================\nOperation: POWN Authentication\nCoins Processed: 15 CloudCoins\nTotal Value: 1,500.0 CloudCoins\nAuthentication Method: RAIDA Network Consensus\n\nAUTHENTICATION RESULTS\n====================================================\nSuccessfully Authenticated: 13 coins\nMoved to Bank: 13 coins (1,300.0 value)\nMoved to Fracked: 2 coins (200.0 value)\nMoved to Counterfeit: 0 coins\nAuthentication Success Rate: 86.7%\n\nRAIDA NETWORK RESPONSE\n====================================================\nServers Contacted: 25/25\nConsensus Achieved: Yes\nAverage Response Time: 198ms\nNetwork Health: Good\nTimeout Issues: 2 servers\n\nFRACKED COINS DETAILS\n====================================================\n• 100 CloudCoin #78901 'Payment #5'\n  Status: ⚠️ Partially authenticated (18/25 servers)\n  Moved to: Fracked folder\n  Recommendation: Run fix-coins operation\n  \n• 100 CloudCoin #78902 'Payment #6'\n  Status: ⚠️ Partially authenticated (19/25 servers)\n  Moved to: Fracked folder\n  Recommendation: Run fix-coins operation\n\nTRANSACTION SUMMARY\n====================================================\n✅ POWN authentication completed\n⚠️ 2 coins require additional healing\n✅ Wallet balance updated\n✅ Transaction recorded in wallet history\n\nRECEIPT INFORMATION\n====================================================\nGenerated: August 23, 2025 at 12:41:00 PM PST\nReceipt ID: 2025-08-23_12-41-00.pown-authentication\nWallet Location: D:\\CloudCoin\\Pro\\Wallets\\MyWallet\nTransaction Log Updated: Yes\n\nFor support or questions about this transaction,\nreference Transaction ID: pown-Aug-23-2025-12:41pm-PST\n\nThis receipt serves as proof of your coin authentication.\nKeep this receipt for your records.\n===================================================="
  }
}
```

### Sample Response (Error - Receipt Not Found)
```json
{
  "status": "error",
  "message": "Receipt file not found",
  "data": {
    "wallet_path": "D:\\CloudCoin\\Pro\\Wallets\\MyWallet",
    "receipt_filename": "2025-08-25_99-99-99.nonexistent.txt",
    "error_details": "Receipt file '2025-08-25_99-99-99.nonexistent.txt' not found",
    "available_receipts": [
      "2025-08-25_17-34-00.withdraw-to-locker.txt",
      "2025-08-24_16-08-00.deposit-from-file.txt",
      "2025-08-23_12-41-00.pown-authentication.txt",
      "2025-08-22_09-22-30.break-coins.txt",
      "2025-08-21_15-18-45.join-coins.txt",
      "2025-08-20_11-05-12.fix-coins.txt"
    ]
  }
}
```

### Sample Response (Error - Wallet Not Found)
```json
{
  "status": "error",
  "message": "Wallet directory not found",
  "data": {
    "wallet_path": "D:\\CloudCoin\\Pro\\Wallets\\NonExistentWallet",
    "error_details": "Wallet directory not found",
    "suggested_wallets": ["Default", "MyWallet", "BusinessWallet"]
  }
}
```

### Sample Response (Error - Receipts Folder Missing)
```json
{
  "status": "error",
  "message": "Receipts directory not found in wallet",
  "data": {
    "wallet_path": "D:\\CloudCoin\\Pro\\Wallets\\MyWallet",
    "error_details": "Receipts directory not found in wallet",
    "wallet_structure_valid": false,
    "missing_folders": ["Receipts"],
    "suggestion": "This wallet may be corrupted or incomplete"
  }
}
```

### Sample Response (Error - Permission Denied)
```json
{
  "status": "error",
  "message": "Unable to read receipt file",
  "data": {
    "wallet_path": "D:\\CloudCoin\\Pro\\Wallets\\MyWallet",
    "receipt_filename": "2025-08-25_17-34-00.withdraw-to-locker.txt",
    "error_details": "Permission denied when accessing receipt file",
    "file_exists": true,
    "suggested_action": "Check file permissions or run with administrator privileges"
  }
}
```

### Sample Response (Error - Empty Receipts Folder)
```json
{
  "status": "error",
  "message": "No receipts found in wallet",
  "data": {
    "wallet_path": "D:\\CloudCoin\\Pro\\Wallets\\EmptyWallet",
    "error_details": "Receipts folder exists but contains no receipt files",
    "receipts_folder_exists": true,
    "available_receipts": [],
    "suggestion": "No transaction receipts have been generated for this wallet yet"
  }
}
```

## 14. list-transactions

**Type**: Synchronous  
**Description**: Returns the complete transaction history from transactions.csv with automatic balance reconciliation. Verifies wallet balance against actual coins and adds adjustment records if discrepancies are found

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| wallet_path | string | Yes | The path to the wallet directory containing transactions.csv |

### Sample Response (Success - No Adjustment Needed)
```json
{
  "status": "success",
  "message": "Transaction list retrieved successfully",
  "data": {
    "balance_verification": {
      "true_balance": 1250.75,
      "recorded_balance": 1250.75,
      "balance_matches": true,
      "adjustment_needed": false,
      "coins_in_bank": 1200.75,
      "coins_in_fracked": 50.0,
      "total_coin_files": 8
    },
    "transactions_csv_content": "Symbol,Task ID,Date & Time,Remarks,Deposit,Withdraw,Description,Balance\n🡆,\"deposit-Aug-24-2025-2:30pm-PST\",\"8/24/2025, 2:30 PM\",\"Success\",500.0,,\"Deposited coin files\",\"1,250.75\"\n🡄,\"withdraw-Aug-23-2025-4:15pm-PST\",\"8/23/2025, 4:15 PM\",\"Transferred to BusinessWallet\",,200.0,\"Transferred Out\",\"750.75\"\n🡆,\"deposit-Aug-22-2025-1:45pm-PST\",\"8/22/2025, 1:45 PM\",\"Success\",950.75,,\"Deposited coin files\",\"950.75\"\n⚠️,,\"8/20/2025, 9:30 AM\",\"25 coins found\",25.0,,\"Balance Adjusted\",\"25.0\"\n🡆,\"deposit-Aug-19-2025-3:20pm-PST\",\"8/19/2025, 3:20 PM\",\"Success\",0.0,,\"Initial wallet creation\",\"0.0\"",
    "transaction_summary": {
      "total_transactions": 5,
      "total_deposits": 1475.75,
      "total_withdrawals": 225.0,
      "balance_adjustments": 1,
      "last_transaction_date": "2025-08-24T14:30:00Z"
    }
  }
}
```

### Sample Response (Success - Balance Adjustment Added)
```json
{
  "status": "success",
  "message": "Balance discrepancy found and corrected",
  "data": {
    "balance_verification": {
      "true_balance": 1150.5,
      "recorded_balance": 1250.75,
      "balance_matches": false,
      "adjustment_needed": true,
      "adjustment_amount": -100.25,
      "coins_in_bank": 1100.5,
      "coins_in_fracked": 50.0,
      "total_coin_files": 7
    },
    "adjustment_record": {
      "symbol": "⚠️",
      "task_id": "",
      "date_time": "8/25/2025, 1:45 PM",
      "remarks": "100.25 coins missing",
      "deposit": "",
      "withdraw": "100.25",
      "description": "Balance Adjusted",
      "amount": -100.25,
      "balance": "1,150.5"
    },
    "transactions_csv_content": "Symbol,Task ID,Date & Time,Remarks,Deposit,Withdraw,Description,Balance\n⚠️,,\"8/25/2025, 1:45 PM\",\"100.25 coins missing\",,100.25,\"Balance Adjusted\",\"1,150.5\"\n🡆,\"deposit-Aug-24-2025-2:30pm-PST\",\"8/24/2025, 2:30 PM\",\"Success\",500.0,,\"Deposited coin files\",\"1,250.75\"\n🡄,\"withdraw-Aug-23-2025-4:15pm-PST\",\"8/23/2025, 4:15 PM\",\"Transferred to BusinessWallet\",,200.0,\"Transferred Out\",\"750.75\"\n🡆,\"deposit-Aug-22-2025-1:45pm-PST\",\"8/22/2025, 1:45 PM\",\"Success\",950.75,,\"Deposited coin files\",\"950.75\"\n🡆,\"deposit-Aug-19-2025-3:20pm-PST\",\"8/19/2025, 3:20 PM\",\"Success\",0.0,,\"Initial wallet creation\",\"0.0\"",
    "transaction_summary": {
      "total_transactions": 5,
      "total_deposits": 1450.75,
      "total_withdrawals": 300.25,
      "balance_adjustments": 1,
      "last_transaction_date": "2025-08-25T13:45:00Z"
    }
  }
}
```

### Sample Response (Success - Coins Found Adjustment)
```json
{
  "status": "success",
  "message": "Extra coins found and balance corrected",
  "data": {
    "balance_verification": {
      "true_balance": 1325.25,
      "recorded_balance": 1250.75,
      "balance_matches": false,
      "adjustment_needed": true,
      "adjustment_amount": 74.5,
      "coins_in_bank": 1275.25,
      "coins_in_fracked": 50.0,
      "total_coin_files": 9
    },
    "adjustment_record": {
      "symbol": "⚠️",
      "task_id": "",
      "date_time": "8/25/2025, 1:45 PM",
      "remarks": "74.5 coins found",
      "deposit": "74.5",
      "withdraw": "",
      "description": "Balance Adjusted",
      "amount": 74.5,
      "balance": "1,325.25"
    },
    "transactions_csv_content": "Symbol,Task ID,Date & Time,Remarks,Deposit,Withdraw,Description,Balance\n⚠️,,\"8/25/2025, 1:45 PM\",\"74.5 coins found\",74.5,,\"Balance Adjusted\",\"1,325.25\"\n🡆,\"deposit-Aug-24-2025-2:30pm-PST\",\"8/24/2025, 2:30 PM\",\"Success\",500.0,,\"Deposited coin files\",\"1,250.75\"\n🡄,\"withdraw-Aug-23-2025-4:15pm-PST\",\"8/23/2025, 4:15 PM\",\"Transferred to BusinessWallet\",,200.0,\"Transferred Out\",\"750.75\"\n🡆,\"deposit-Aug-22-2025-1:45pm-PST\",\"8/22/2025, 1:45 PM\",\"Success\",950.75,,\"Deposited coin files\",\"950.75\"\n🡆,\"deposit-Aug-19-2025-3:20pm-PST\",\"8/19/2025, 3:20 PM\",\"Success\",0.0,,\"Initial wallet creation\",\"0.0\"",
    "transaction_summary": {
      "total_transactions": 5,
      "total_deposits": 1525.25,
      "total_withdrawals": 200.0,
      "balance_adjustments": 1,
      "last_transaction_date": "2025-08-25T13:45:00Z"
    }
  }
}
```

### Sample Response (Success - Complex Transaction History)
```json
{
  "status": "success",
  "message": "Transaction list retrieved successfully",
  "data": {
    "balance_verification": {
      "true_balance": 5847.25,
      "recorded_balance": 5847.25,
      "balance_matches": true,
      "adjustment_needed": false,
      "coins_in_bank": 5500.0,
      "coins_in_fracked": 347.25,
      "total_coin_files": 23
    },
    "transactions_csv_content": "Symbol,Task ID,Date & Time,Remarks,Deposit,Withdraw,Description,Balance\n🔧,\"fixcoins-Aug-25-2025-9:15am-PST\",\"8/25/2025, 9:15 AM\",\"347.25 coins recovered\",347.25,,\"Fix Coins Operation\",\"5,847.25\"\n🡆,\"deposit-Aug-24-2025-3:30pm-PST\",\"8/24/2025, 3:30 PM\",\"Success\",2500.0,,\"Deposited coin files\",\"5,500.0\"\n🔄,\"breakcoins-Aug-23-2025-11:45am-PST\",\"8/23/2025, 11:45 AM\",\"1000 → 10x100\",,,\"Break Coins Operation\",\"3,000.0\"\n🔄,\"joincoins-Aug-22-2025-2:20pm-PST\",\"8/22/2025, 2:20 PM\",\"10x100 → 1000\",,,\"Join Coins Operation\",\"3,000.0\"\n🡄,\"withdraw-Aug-21-2025-4:10pm-PST\",\"8/21/2025, 4:10 PM\",\"Transfer to savings\",,500.0,\"Transferred Out\",\"3,000.0\"\n🡆,\"deposit-Aug-20-2025-10:00am-PST\",\"8/20/2025, 10:00 AM\",\"Success\",3500.0,,\"Deposited coin files\",\"3,500.0\"\n🡆,\"deposit-Aug-19-2025-9:00am-PST\",\"8/19/2025, 9:00 AM\",\"Success\",0.0,,\"Initial wallet creation\",\"0.0\"",
    "transaction_summary": {
      "total_transactions": 7,
      "total_deposits": 6347.25,
      "total_withdrawals": 500.0,
      "balance_adjustments": 0,
      "last_transaction_date": "2025-08-25T09:15:00Z",
      "operation_breakdown": {
        "deposits": 3,
        "withdrawals": 1,
        "fix_operations": 1,
        "break_operations": 1,
        "join_operations": 1
      }
    }
  }
}
```

### Sample Response (Success - Empty Transaction History)
```json
{
  "status": "success",
  "message": "Empty transaction history",
  "data": {
    "balance_verification": {
      "true_balance": 0.0,
      "recorded_balance": 0.0,
      "balance_matches": true,
      "adjustment_needed": false,
      "coins_in_bank": 0.0,
      "coins_in_fracked": 0.0,
      "total_coin_files": 0
    },
    "transactions_csv_content": "Symbol,Task ID,Date & Time,Remarks,Deposit,Withdraw,Description,Balance",
    "transaction_summary": {
      "total_transactions": 0,
      "total_deposits": 0.0,
      "total_withdrawals": 0.0,
      "balance_adjustments": 0,
      "last_transaction_date": null
    }
  }
}
```

### Sample Response (Error - Wallet Not Found)
```json
{
  "status": "error",
  "message": "Wallet directory not found",
  "data": {
    "wallet_path": "D:\\CloudCoin\\Pro\\Wallets\\NonExistentWallet",
    "error_details": "Wallet directory not found",
    "suggested_wallets": ["Default", "MyWallet", "BusinessWallet"]
  }
}
```

### Sample Response (Error - Invalid Wallet Structure)
```json
{
  "status": "error",
  "message": "Invalid wallet structure",
  "data": {
    "wallet_path": "D:\\CloudCoin\\Pro\\Wallets\\CorruptedWallet",
    "error_details": "Required wallet components missing",
    "missing_components": ["transactions.csv", "Bank", "Fracked"],
    "found_components": ["Receipts"],
    "suggestion": "This wallet appears to be corrupted or incomplete"
  }
}
```

### Sample Response (Error - Transactions File Corrupted)
```json
{
  "status": "error",
  "message": "Unable to read transactions file",
  "data": {
    "wallet_path": "D:\\CloudCoin\\Pro\\Wallets\\MyWallet",
    "transactions_file": "transactions.csv",
    "error_details": "Transactions file is corrupted or unreadable",
    "file_exists": true,
    "suggested_actions": [
      "Check file permissions",
      "Verify file is not locked by another process",
      "Consider wallet recovery options"
    ]
  }
}
```

### Sample Response (Error - Permission Denied)
```json
{
  "status": "error",
  "message": "Unable to access wallet directory",
  "data": {
    "wallet_path": "D:\\CloudCoin\\Pro\\Wallets\\RestrictedWallet",
    "error_details": "Permission denied when accessing wallet directory",
    "suggested_actions": [
      "Check folder permissions",
      "Run application with administrator privileges",
      "Verify wallet is not locked by another process"
    ]
  }
}
```

## 15. show-wallet-coins

**Type**: Synchronous  
**Description**: Returns detailed information about coins in a specified wallet including denomination histogram, total balance, folder distribution, and automatic balance reconciliation with transaction log

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| wallet_path | string | Yes | The full path to the specific wallet folder containing Bank, Fracked, and Limbo folders |

### Sample Response (Success - Balanced Wallet)
```json
{
  "status": "success",
  "message": "Wallet coins retrieved successfully",
  "data": {
    "denomination_count": {
      "0": 45,
      "1": 12,
      "2": 8,
      "3": 0,
      "4": 2,
      "5": 0,
      "6": 1,
      "7": 0,
      "8": 3,
      "9": 0,
      "10": 0,
      "11": 0
    },
    "total": 34343.776,
    "bank": 30000.5,
    "fracked": 4000.276,
    "limbo": 343.0,
    "balance_reconciled": true,
    "folder_summary": {
      "bank_files": 58,
      "fracked_files": 10,
      "limbo_files": 3,
      "total_files": 71
    },
    "denomination_details": {
      "highest_denomination": 8,
      "lowest_denomination": 0,
      "most_common_denomination": 0,
      "currency_coins": 68,
      "key_coins": 3
    },
    "value_distribution": {
      "percentage_in_bank": 87.3,
      "percentage_in_fracked": 11.6,
      "percentage_in_limbo": 1.0,
      "largest_single_coin": 25000.0,
      "smallest_single_coin": 0.001
    }
  }
}
```

### Sample Response (Success - Empty Wallet)
```json
{
  "status": "success",
  "message": "Empty wallet - no coins found",
  "data": {
    "denomination_count": {
      "0": 0, "1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0,
      "7": 0, "8": 0, "9": 0, "10": 0, "11": 0
    },
    "total": 0.0,
    "bank": 0.0,
    "fracked": 0.0,
    "limbo": 0.0,
    "balance_reconciled": true,
    "folder_summary": {
      "bank_files": 0,
      "fracked_files": 0,
      "limbo_files": 0,
      "total_files": 0
    },
    "denomination_details": {
      "highest_denomination": null,
      "lowest_denomination": null,
      "most_common_denomination": null,
      "currency_coins": 0,
      "key_coins": 0
    },
    "value_distribution": {
      "percentage_in_bank": 0.0,
      "percentage_in_fracked": 0.0,
      "percentage_in_limbo": 0.0,
      "largest_single_coin": null,
      "smallest_single_coin": null
    }
  }
}
```

### Sample Response (Success - Balance Adjustment Created)
```json
{
  "status": "success",
  "message": "Balance discrepancy found and corrected",
  "data": {
    "denomination_count": {
      "0": 10, "1": 5, "2": 2, "3": 0, "4": 0, "5": 0, "6": 0,
      "7": 0, "8": 1, "9": 0, "10": 0, "11": 0
    },
    "total": 1205.5,
    "bank": 1000.0,
    "fracked": 200.5,
    "limbo": 5.0,
    "balance_reconciled": false,
    "balance_adjustment": {
      "adjustment_needed": true,
      "recorded_balance": 1300.0,
      "actual_balance": 1205.5,
      "difference": -94.5,
      "adjustment_type": "withdraw",
      "adjustment_description": "94.5 coins missing",
      "adjustment_record_created": true,
      "adjustment_timestamp": "2025-08-25T13:45:00Z"
    },
    "folder_summary": {
      "bank_files": 15,
      "fracked_files": 2,
      "limbo_files": 1,
      "total_files": 18
    },
    "denomination_details": {
      "highest_denomination": 8,
      "lowest_denomination": 0,
      "most_common_denomination": 0,
      "currency_coins": 17,
      "key_coins": 1
    },
    "value_distribution": {
      "percentage_in_bank": 82.9,
      "percentage_in_fracked": 16.6,
      "percentage_in_limbo": 0.4,
      "largest_single_coin": 25000.0,
      "smallest_single_coin": 0.5
    }
  }
}
```

### Sample Response (Success - Large Mixed Wallet)
```json
{
  "status": "success",
  "message": "Wallet coins retrieved successfully",
  "data": {
    "denomination_count": {
      "0": 100, "1": 50, "2": 25, "3": 10, "4": 5, "5": 2, "6": 1,
      "7": 0, "8": 5, "9": 2, "10": 1, "11": 0
    },
    "total": 2500750.12345,
    "bank": 2500000.0,
    "fracked": 750.12345,
    "limbo": 0.0,
    "balance_reconciled": true,
    "folder_summary": {
      "bank_files": 195,
      "fracked_files": 6,
      "limbo_files": 0,
      "total_files": 201
    },
    "denomination_details": {
      "highest_denomination": 10,
      "lowest_denomination": 0,
      "most_common_denomination": 0,
      "currency_coins": 193,
      "key_coins": 8
    },
    "value_distribution": {
      "percentage_in_bank": 99.97,
      "percentage_in_fracked": 0.03,
      "percentage_in_limbo": 0.0,
      "largest_single_coin": 100000000.0,
      "smallest_single_coin": 0.0001
    },
    "detailed_breakdown": {
      "by_denomination": {
        "fractional_coins": {
          "count": 100,
          "total_value": 0.12345,
          "denominations": ["0"]
        },
        "unit_coins": {
          "count": 50,
          "total_value": 50.0,
          "denominations": ["1"]
        },
        "higher_denomination_coins": {
          "count": 51,
          "total_value": 2500700.0,
          "denominations": ["2", "3", "4", "5", "6", "8", "9", "10"]
        }
      },
      "file_size_analysis": {
        "average_file_size": 439,
        "largest_file_size": 3207,
        "smallest_file_size": 439,
        "multi_coin_files": 5
      }
    }
  }
}
```

### Sample Response (Success - Wallet with Key Coins)
```json
{
  "status": "success",
  "message": "Wallet coins retrieved successfully",
  "data": {
    "denomination_count": {
      "0": 5, "1": 3, "2": 2, "3": 0, "4": 1, "5": 0, "6": 0,
      "7": 0, "8": 0, "9": 0, "10": 0, "11": 15
    },
    "total": 112.05,
    "bank": 112.05,
    "fracked": 0.0,
    "limbo": 0.0,
    "balance_reconciled": true,
    "folder_summary": {
      "bank_files": 26,
      "fracked_files": 0,
      "limbo_files": 0,
      "total_files": 26
    },
    "denomination_details": {
      "highest_denomination": 11,
      "lowest_denomination": 0,
      "most_common_denomination": 11,
      "currency_coins": 11,
      "key_coins": 15
    },
    "value_distribution": {
      "percentage_in_bank": 100.0,
      "percentage_in_fracked": 0.0,
      "percentage_in_limbo": 0.0,
      "largest_single_coin": 100.0,
      "smallest_single_coin": 0.001
    },
    "special_coins": {
      "key_coins_found": true,
      "key_coin_details": [
        {
          "filename": "Key CloudCoin #1001 'Server Access Token'.bin",
          "purpose": "Server Access",
          "ip_address": "192.168.1.100",
          "port": 8080,
          "application_id": 25
        },
        {
          "filename": "Key CloudCoin #1002 'API Gateway Key'.bin",
          "purpose": "API Access",
          "ip_address": "10.0.0.50",
          "port": 443,
          "application_id": 42
        }
      ]
    }
  }
}
```

### Sample Response (Error - Wallet Not Found)
```json
{
  "status": "error",
  "message": "ERROR:CANNOT-FIND-WALLET-FOLDER",
  "data": {
    "error_code": "ERROR:CANNOT-FIND-WALLET-FOLDER",
    "error_details": "The specified wallet directory 'D:\\CloudCoin\\Pro\\Wallets\\NonExistentWallet' does not exist.",
    "wallet_path": "D:\\CloudCoin\\Pro\\Wallets\\NonExistentWallet",
    "suggested_wallets": ["Default", "MyWallet", "BusinessWallet"]
  }
}
```

### Sample Response (Error - Missing Required Folders)
```json
{
  "status": "error",
  "message": "ERROR:MISSING-REQUIRED-FOLDERS",
  "data": {
    "error_code": "ERROR:MISSING-REQUIRED-FOLDERS",
    "error_details": "Required folders (Bank, Fracked, Limbo) are missing from the wallet directory.",
    "wallet_path": "D:\\CloudCoin\\Pro\\Wallets\\CorruptedWallet",
    "missing_folders": ["Bank", "Fracked"],
    "found_folders": ["Limbo", "Receipts", "Counterfeit"],
    "required_folders": ["Bank", "Fracked", "Limbo"]
  }
}
```

### Sample Response (Error - Permission Issues)
```json
{
  "status": "error",
  "message": "ERROR:CANNOT-READ-WALLET-FOLDER",
  "data": {
    "error_code": "ERROR:CANNOT-READ-WALLET-FOLDER",
    "error_details": "The application lacks permissions to read the wallet directory.",
    "wallet_path": "D:\\CloudCoin\\Pro\\Wallets\\RestrictedWallet",
    "suggested_actions": [
      "Check file permissions for the wallet directory",
      "Run application with administrator privileges",
      "Verify the wallet is not locked by another process"
    ]
  }
}
```

### Sample Response (Error - Transaction File Issues)
```json
{
  "status": "error",
  "message": "ERROR:CANNOT-READ-TRANSACTIONS",
  "data": {
    "error_code": "ERROR:CANNOT-READ-TRANSACTIONS",
    "error_details": "Unable to read or parse transactions.csv file",
    "wallet_path": "D:\\CloudCoin\\Pro\\Wallets\\MyWallet",
    "transactions_file": "transactions.csv",
    "file_exists": true,
    "suggested_actions": [
      "Check if transactions.csv is corrupted",
      "Verify file is not locked by another application",
      "Consider wallet recovery options"
    ]
  }
}
```

### Sample Response (Error - Corrupted Coin Files)
```json
{
  "status": "error",
  "message": "ERROR:CORRUPTED-COIN-FILES",
  "data": {
    "error_code": "ERROR:CORRUPTED-COIN-FILES",
    "error_details": "Multiple coin files in the wallet appear to be corrupted",
    "wallet_path": "D:\\CloudCoin\\Pro\\Wallets\\DamagedWallet",
    "corrupted_files": [
      "Bank/1000 CloudCoin #12345 'corrupted'.bin",
      "Fracked/500 CloudCoin #67890 'damaged'.bin"
    ],
    "valid_files_found": 8,
    "suggested_actions": [
      "Move corrupted files to Corrupted folder",
      "Run wallet recovery tools",
      "Restore from backup if available"
    ]
  }
}
```

### Sample Response (Error - Disk Space Issues)
```json
{
  "status": "error",
  "message": "ERROR:INSUFFICIENT-DISK-SPACE",
  "data": {
    "error_code": "ERROR:INSUFFICIENT-DISK-SPACE",
    "error_details": "Insufficient disk space to complete balance reconciliation",
    "wallet_path": "D:\\CloudCoin\\Pro\\Wallets\\MyWallet",
    "disk_space_available": "50MB",
    "disk_space_required": "125MB",
    "suggested_actions": [
      "Free up disk space",
      "Move wallet to drive with more space",
      "Clean up temporary files"
    ]
  }
}
```


## Task ID Format Recommendation

For better usability and readability, we use this task ID format:

**Format**: `{command}-{date}-{time}-{timezone}`

**Examples**:
- `"pown-Aug-18-2025-2:24pm-PST"`
- `"echoraida-Aug-19-2025-3:15pm-PST"`
- `"countraidascoins-Aug-19-2025-4:30pm-EST"`

**Benefits**:
- Human readable and easier to reference
- Much shorter and more memorable than GUIDs
- CLI-friendly when quoted in JSON
- Natural chronological sorting
- Can be used as receipt numbers for powning operations

**Format Components**:
- `command`: The actual command name (pown, echoraida, etc.)
- `date`: Month-DD-YYYY format
- `time`: 12-hour format with am/pm
- `timezone`: Standard timezone abbreviation

**Note**: For powning operations, task IDs and receipt numbers are the same.

## Task Status Values

| Status | Description |
|--------|-------------|
| `running` | Task in progress |
| `completed` | Task finished successfully |
| `error` | Task failed |
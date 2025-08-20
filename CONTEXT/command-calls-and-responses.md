# Command Calls and Responses

This document provides a quick reference for CloudCoin Pro commands, their parameters, and expected responses.

## Response Structure

All commands follow a consistent response structure. Only the `data` and `message` fields change between commands.

## Commands Overview

| Name | Type | Description | Parameters | Sample Call |
|------|------|-------------|------------|-------------|
| echo-raida | Async | Checks RAIDA server health and response times | None | `echo-raida` |
| task-status | Sync | Returns status of an asynchronous task | Task ID | `task-status "pown Aug-18-2025 2:24pm 2321 PST"` |
| show-version | Async | Gets software version of each RAIDA server | None | `show-version` |
| count-raidas-coins | Async | Returns the number of coins that each RAIDA has | None | `count-raidas-coins` |
| list-wallets | Sync | Scans and returns all valid wallet names in the wallets directory | wallets_path | `list-wallets "C:\Users\User\CloudCoin_Pro\Wallets\"` |
| create-wallet | Sync | Creates a new wallet with complete directory structure | wallets_path, wallet_name | `create-wallet "C:\Users\User\CloudCoin_Pro\Wallets\" "MyNewWallet"` |

## echo-raida

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
    "task_id": "bce8e95d-dd86-40e9-8848-f9f8eef16c71",
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

## task-status

**Type**: Synchronous  
**Description**: Returns information about a previously created task

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| id | string | Yes | Task ID in format: "command date time microseconds timezone" |

### Sample Response (In Progress)
```json
{
  "status": "success",
  "payload": {
    "id": "pown Aug-18-2025 2:24pm 2321 PST",
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
    "id": "pown Aug-18-2025 2:24pm 2321 PST", 
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

## show-version

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
    "task_id": "b2c3d4e5-f6a7-4b89-9c01-234567890abcd",
    "status": "pending"
  }
}
```

### Sample Response (Task Completed)
```json
{
  "status": "success",
  "payload": {
    "id": "b2c3d4e5-f6a7-4b89-9c01-234567890abcd",
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

## count-raidas-coins

**Type**: Asynchronous  
**Description**: Returns the number of coins that each RAIDA has

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| None | - | - | No parameters required |

### Sample Response (Task Created)
```json
{
  "status": "success",
  "message": "Count RAIDA coins task created",
  "data": {
    "task_id": "c3d4e5f6-g7h8-4i90-j123-456789012345",
    "status": "pending"
  }
}
```

### Sample Response (Task In Progress)
```json
{
  "status": "success",
  "payload": {
    "id": "c3d4e5f6-g7h8-4i90-j123-456789012345",
    "status": "running",
    "progress": 65,
    "message": "Counting coins on RAIDA servers...",
    "data": null
  }
}
```

### Sample Response (Task Completed)
```json
{
  "status": "success",
  "payload": {
    "id": "c3d4e5f6-g7h8-4i90-j123-456789012345",
    "status": "completed",
    "progress": 100,
    "message": "Command Completed",
    "data": "raida_id,coin_count\n0,15234\n1,15287\n2,15156\n3,15198\n4,15243\n5,15267\n6,15189\n7,15212\n8,15234\n9,15198\n10,15267\n11,15243\n12,15156\n13,15287\n14,15234\n15,15198\n16,15212\n17,15189\n18,15267\n19,15243\n20,15156\n21,15287\n22,15234\n23,15198\n24,15267"
  }
}
```

## list-wallets

**Type**: Synchronous  
**Description**: Scans the wallets directory and returns a simple list of all valid wallet names found

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| wallets_path | string | Yes | The path to the Wallets folder such as: "C:\Users\User\CloudCoin_Pro\Wallets\" |

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

## create-wallet

**Type**: Synchronous  
**Description**: Creates a new wallet with complete directory structure and configuration files

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| wallets_path | string | Yes | The path to the Wallets directory such as: "C:\Users\User\CloudCoin_Pro\Wallets\" |
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

## Task ID Format Recommendation

For better usability and readability, consider using this task ID format instead of GUIDs:

**Format**: `{command} {date} {time} {microseconds} {timezone}`

**Examples**:
- `"pown Aug-18-2025 2:24pm 2321 PST"`
- `"echo Aug-19-2025 3:15pm 1847 PST"`
- `"count-raidas-coins Aug-19-2025 4:30pm 5692 EST"`

**Benefits**:
- Human readable and easier to reference
- Includes microseconds for precise timing
- Timezone aware for global usage
- CLI-friendly when quoted in JSON
- Natural chronological sorting
- Much shorter and more memorable than GUIDs

**Format Components**:
- `command`: The actual command name (pown, echo, etc.)
- `date`: Month-DD-YYYY format
- `time`: 12-hour format with am/pm
- `microseconds`: 4-digit microsecond precision
- `timezone`: Standard timezone abbreviation

## Task Status Values

| Status | Description |
|--------|-------------|
| `running` | Task in progress |
| `completed` | Task finished successfully |
| `error` | Task failed |
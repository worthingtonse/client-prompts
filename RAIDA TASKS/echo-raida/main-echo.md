
# echo

CLI ASYNC

Checks the health, status, and response times of all RAIDA servers by
sending echo requests.

C:\echo.exe or just echo

## Description

The \`/echo\` endpoint provides a simple way to verify the operational
status of the entire RAIDA network. It\'s a fundamental utility for
developers to test network connectivity and RAIDA health before
attempting more complex operations. Since this is an asynchronous call,
it initiates a task and returns a task ID immediately, which you can
then use to poll for the result.


💡 Why use /echo?

Before executing critical transactions like sending or receiving
CloudCoins, you can use this endpoint to get a real-time snapshot of the
network\'s health. This allows your application to gracefully handle
potential network issues and provide better feedback to the end-user.

## Asynchronous Workflow

#### Understanding Asynchronous API Calls

This endpoint is asynchronous, which means:

1.  When you call this endpoint, it **immediately returns a task ID**.
2.  You then need to **periodically check the task status** using the
    `/api/v1/task/{task_id}` endpoint.
3.  Once the task is complete, the task status endpoint will return the
    full results in the \`data\` field.
## Parameters

This endpoint does not require any parameters.

## Response

When the asynchronous task completes, the \`data\` field of the task
status response will contain the \`EchoResponse\` object with the
following properties.


#### Response Properties


online integer


The total number of RAIDA servers that are online and responded
successfully.

pownstring  string

A 25-character string representing the pass/fail status for each RAIDA
server. \'p\' indicates a pass, and \'f\' indicates a fail.

pownarray array\<integer\>

An array of 25 integers where \`1\` indicates a pass (online) and \`0\`
indicates a fail (offline or error).

latencies array\<integer\>

An array of 25 integers, where each value is the response time in
milliseconds for the corresponding RAIDA server.

#### Example Response (from task endpoint after completion)

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIGhlaWdodD0iMjQiIHZpZXdib3g9IjAgMCAyNCAyNCIgd2lkdGg9IjI0IiBmaWxsPSJjdXJyZW50Q29sb3IiPjxwYXRoIGQ9Ik0wIDBoMjR2MjRIMHoiIGZpbGw9Im5vbmUiPjwvcGF0aD48cGF0aCBkPSJNMTYgMUg0Yy0xLjEgMC0yIC45LTIgMnYxNGgyVjNoMTJWMXptMyA0SDhjLTEuMSAwLTIgLjktMiAydjE0YzAgMS4xLjkgMiAyIDJoMTFjMS4xIDAgMi0uOSAyLTJWN2MwLTEuMS0uOS0yLTItMnptMCAxNkg4VjdoMTF2MTR6Ij48L3BhdGg+PC9zdmc+)

``` json
{
  "id": "task123",
  "status": "completed",
  "progress": 100,
  "message": "RAIDA check complete.",
  "data": {
    "online": 25,
    "pownstring": "ppppppppppppppppppppppppp",
    "pownarray": [
      1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1
    ],
    "latencies": [
      210, 215, 220, 205, 208, 212, 218, 221, 214, 217, 219, 209, 211,
      213, 216, 222, 223, 225, 206, 207, 224, 226, 227, 228, 229
    ]
  }
}
```
This JSON response object will also be written to the file named last-echo-log.json        

That is found in CloudCoin/Pro/last-echo-log.json        

::: page-container
::: {.content role="main"}
::: command-header
::: command-title
# /echo {#echo .command-name}

[GET]{.method-badge .method-get} [ASYNC]{.async-badge}
:::

Checks the health, status, and response times of all RAIDA servers by
sending echo requests.

::: endpoint-container
::: endpoint
GET /api/v1/echo

::: alias
Alias: /check-all-raida-status
:::
:::
:::
:::

::: section
## Description

The \`/echo\` endpoint provides a simple way to verify the operational
status of the entire RAIDA network. It\'s a fundamental utility for
developers to test network connectivity and RAIDA health before
attempting more complex operations. Since this is an asynchronous call,
it initiates a task and returns a task ID immediately, which you can
then use to poll for the result.

::: {.alert-box .note}
::: alert-title
💡 Why use /echo?
:::

Before executing critical transactions like sending or receiving
CloudCoins, you can use this endpoint to get a real-time snapshot of the
network\'s health. This allows your application to gracefully handle
potential network issues and provide better feedback to the end-user.
:::
:::

::: section
## Asynchronous Workflow

::: task-status
#### Understanding Asynchronous API Calls

This endpoint is asynchronous, which means:

1.  When you call this endpoint, it **immediately returns a task ID**.
2.  You then need to **periodically check the task status** using the
    `/api/v1/task/{task_id}` endpoint.
3.  Once the task is complete, the task status endpoint will return the
    full results in the \`data\` field.
:::
:::

::: section
## Parameters

This endpoint does not require any parameters.
:::

::: section
## Response

When the asynchronous task completes, the \`data\` field of the task
status response will contain the \`EchoResponse\` object with the
following properties.

::: response-object
#### Response Properties

::: response-property
[online]{.property-name} [integer]{.property-type}

::: property-description
The total number of RAIDA servers that are online and responded
successfully.
:::
:::

::: response-property
[pownstring]{.property-name} [string]{.property-type}

::: property-description
A 25-character string representing the pass/fail status for each RAIDA
server. \'p\' indicates a pass, and \'f\' indicates a fail.
:::
:::

::: response-property
[pownarray]{.property-name} [array\<integer\>]{.property-type}

::: property-description
An array of 25 integers where \`1\` indicates a pass (online) and \`0\`
indicates a fail (offline or error).
:::
:::

::: response-property
[latencies]{.property-name} [array\<integer\>]{.property-type}

::: property-description
An array of 25 integers, where each value is the response time in
milliseconds for the corresponding RAIDA server.
:::
:::
:::

::: response-example
#### Example Response (from task endpoint after completion)

::: code-block-container
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
:::
:::
:::

::: section
## Examples

::: code-tabs
::: tabs-header
JavaScript

cURL

Go
:::

::: {#js .tab-content .active}
### JavaScript (async/await)

::: code-block-container
![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIGhlaWdodD0iMjQiIHZpZXdib3g9IjAgMCAyNCAyNCIgd2lkdGg9IjI0IiBmaWxsPSJjdXJyZW50Q29sb3IiPjxwYXRoIGQ9Ik0wIDBoMjR2MjRIMHoiIGZpbGw9Im5vbmUiPjwvcGF0aD48cGF0aCBkPSJNMTYgMUg0Yy0xLjEgMC0yIC45LTIgMnYxNGgyVjNoMTJWMXptMyA0SDhjLTEuMSAwLTIgLjktMiAydjE0YzAgMS4xLjkgMiAyIDJoMTFjMS4xIDAgMi0uOSAyLTJWN2MwLTEuMS0uOS0yLTItMnptMCAxNkg4VjdoMTF2MTR6Ij48L3BhdGg+PC9zdmc+)

``` js
const API_HOST = 'http://localhost:8006';

// Function to delay execution
const sleep = ms => new Promise(resolve => setTimeout(resolve, ms));

async function checkRaidaHealth() {
    try {
        // 1. Start the echo task
        const initialResponse = await fetch(`${API_HOST}/api/v1/echo`);
        const task = await initialResponse.json();
        console.log(`Task created with ID: ${task.id}`);

        let taskStatus;

        // 2. Poll for the result
        while (true) {
            const statusResponse = await fetch(`${API_HOST}/api/v1/task/${task.id}`);
            taskStatus = await statusResponse.json();
            
            console.log(`Task status: ${taskStatus.status}, Progress: ${taskStatus.progress}%`);

            if (taskStatus.status === 'completed' || taskStatus.status === 'error') {
                break;
            }

            await sleep(1000); // Wait 1 second before polling again
        }

        // 3. Process the final result
        if (taskStatus.status === 'completed') {
            const result = taskStatus.data;
            console.log('RAIDA Health Check Complete:');
            console.log(`  Online Servers: ${result.online} / 25`);
            console.log(`  Status (pownstring): ${result.pownstring}`);
        } else {
            console.error('Task failed:', taskStatus.message);
        }

    } catch (error) {
        console.error('An error occurred:', error);
    }
}

checkRaidaHealth();
```
:::
:::

::: {#curl .tab-content}
### cURL

::: code-block-container
![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIGhlaWdodD0iMjQiIHZpZXdib3g9IjAgMCAyNCAyNCIgd2lkdGg9IjI0IiBmaWxsPSJjdXJyZW50Q29sb3IiPjxwYXRoIGQ9Ik0wIDBoMjR2MjRIMHoiIGZpbGw9Im5vbmUiPjwvcGF0aD48cGF0aCBkPSJNMTYgMUg0Yy0xLjEgMC0yIC45LTIgMnYxNGgyVjNoMTJWMXptMyA0SDhjLTEuMSAwLTIgLjktMiAydjE0YzAgMS4xLjkgMiAyIDJoMTFjMS4xIDAgMi0uOSAyLTJWN2MwLTEuMS0uOS0yLTItMnptMCAxNkg4VjdoMTF2MTR6Ij48L3BhdGg+PC9zdmc+)

``` bash
# Step 1: Initiate the echo task and capture the task ID
TASK_ID=$(curl -s -X GET "http://localhost:8006/api/v1/echo" | jq -r .id)

echo "Task started with ID: $TASK_ID"

# Step 2: Poll the task endpoint until the status is 'completed' or 'error'
while true; do
  RESPONSE=$(curl -s -X GET "http://localhost:8006/api/v1/task/$TASK_ID")
  STATUS=$(echo $RESPONSE | jq -r .status)
  PROGRESS=$(echo $RESPONSE | jq .progress)
  
  echo "Polling task... Status: $STATUS, Progress: $PROGRESS%"
  
  if [ "$STATUS" = "completed" ] || [ "$STATUS" = "error" ]; then
    echo "Task finished. Final Response:"
    echo $RESPONSE | jq
    break
  fi
  
  sleep 2
done
```
:::
:::

::: {#go .tab-content}
### Go

::: code-block-container
![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIGhlaWdodD0iMjQiIHZpZXdib3g9IjAgMCAyNCAyNCIgd2lkdGg9IjI0IiBmaWxsPSJjdXJyZW50Q29sb3IiPjxwYXRoIGQ9Ik0wIDBoMjR2MjRIMHoiIGZpbGw9Im5vbmUiPjwvcGF0aD48cGF0aCBkPSJNMTYgMUg0Yy0xLjEgMC0yIC45LTIgMnYxNGgyVjNoMTJWMXptMyA0SDhjLTEuMSAwLTIgLjktMiAydjE0YzAgMS4xLjkgMiAyIDJoMTFjMS4xIDAgMi0uOSAyLTJWN2MwLTEuMS0uOS0yLTItMnptMCAxNkg4VjdoMTF2MTR6Ij48L3BhdGg+PC9zdmc+)

``` go
package main

import (
    "encoding/json"
    "fmt"
    "io/ioutil"
    "net/http"
    "time"
)

const ApiHost = "http://localhost:8006"

type TaskResponse struct {
    ID       string          `json:"id"`
    Status   string          `json:"status"`
    Progress int             `json:"progress"`
    Message  string          `json:"message"`
    Data     json.RawMessage `json:"data"`
}

type EchoResponse struct {
    Online     int    `json:"online"`
    PownString string `json:"pownstring"`
    Latencies  []int  `json:"latencies"`
}

func main() {
    // 1. Start the echo task
    resp, err := http.Get(fmt.Sprintf("%s/api/v1/echo", ApiHost))
    if err != nil {
        panic(err)
    }
    defer resp.Body.Close()

    var task TaskResponse
    if err := json.NewDecoder(resp.Body).Decode(&task); err != nil {
        panic(err)
    }
    fmt.Printf("Task created with ID: %s\n", task.ID)

    // 2. Poll for the result
    for {
        resp, err := http.Get(fmt.Sprintf("%s/api/v1/task/%s", ApiHost, task.ID))
        if err != nil {
            panic(err)
        }

        body, _ := ioutil.ReadAll(resp.Body)
        resp.Body.Close()

        var taskStatus TaskResponse
        if err := json.Unmarshal(body, &taskStatus); err != nil {
            panic(err)
        }
        
        fmt.Printf("Task status: %s, Progress: %d%%\n", taskStatus.Status, taskStatus.Progress)

        if taskStatus.Status == "completed" {
            var echoResult EchoResponse
            if err := json.Unmarshal(taskStatus.Data, &echoResult); err != nil {
                panic(err)
            }
            fmt.Printf("Echo complete. Online servers: %d/25\n", echoResult.Online)
            break
        } else if taskStatus.Status == "error" {
            fmt.Printf("Task failed: %s\n", taskStatus.Message)
            break
        }

        time.Sleep(1 * time.Second)
    }
}
```
:::
:::
:::
:::

::: {.section .api-comparison}
## Related Endpoints

::: guide-cards
::: guide-card
### /task/{task_id}

Poll this endpoint to check the status, progress, and results of any
asynchronous operation.

::: guide-card-links
[View Details](https://raidagroup.com/commands/task.php)
:::
:::
:::
:::
:::
:::

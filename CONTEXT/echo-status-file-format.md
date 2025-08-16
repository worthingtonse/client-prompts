# Echo Status File. 

This file is called "echos.csv"

It can be found by looking at the 

https://github.com/worthingtonse/client-prompts/blob/sean/CONTEXT/program-file-structure.md

The file structure is shown here in an example: 

```json
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
 ## Meanings of JSON values

 Name | Data Type | Description 
 ---|---|---
 id | string | This is the id that was assigned the task that the econ happened in. All Asynchronistic calls have a task id
 status | string | Should be "completed" if the task is done. "error" if there is an error. Any other value means incomplete and should be tried again later.
 progress | int | The percentage (0-100) that the job has yet to do. Only needed if job is uncomplet or errored. 
 message | string | Details about the status that can be showed to the user such as the error information.
 data | Object | informatin about the echo.
 online | int | The number of raida that responded.
 pownstring | string | A 25-character string representing the pass/fail status for each RAIDA server. 'p' indicates a pass, and 'f' indicates a fail.
pownarray | array of ints | An array of 25 integers where `1` indicates a pass (online) and `0` indicates a fail (offline or error).
latencies | int | An array of 25 integers, where each value is the response time in milliseconds for the client to send and receive a call to the corresponding RAIDA server.



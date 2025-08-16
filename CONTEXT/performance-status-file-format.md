# Performance Status File Format

Performance status files are used to collect data about the time it takes to complete calls to the RAIDA. 

The reason we want to collect this data is so we can feed it into an AI model to calculate the timeouts of calls to the raida. 

We will track the performance of all commands that are called to the RAIDA. The file name will specifiy the command. 

Sample file names for the echo, fix, pown and upload commands: 

```bash
echo_performance.csv
fix_performance.csv
pown_performance.csv
upload_performance.csv
```
## File Formt
The format is csv and the first row is always the header that describes the contents of the column. 

Header | Data Type |Description
---|---|---
raida_id | int | 0-25
command | int | 0-256
timestamp | string | Human readable four byte timestamp
last-echo-time | int | the number of ms that the last echo to that server required. 
time-out-used | int | The amount of time in ms the command was allowed to run for
bytes-sent | int | Number of bytes, including the header, sent to the raida 
bytes-returned | int |  Number of bytes, including the header, received from the raida 
total-ms-request-took | int | Time from client sending request to client receinving reponse. 
raida-ns-spent-processing | int | Each raida will self report the time ip processed internally
did-timeout | int | 0 no, 1 yes.

## Example File Contents
```json
raida_id, command, timestamp, last-echo-check, time-out-used, bytes-sent, bytes-returned, total-ns-spent-processing, did-timeout
13, 0, , 230, 1000, 62000, 350, 235, 0
```

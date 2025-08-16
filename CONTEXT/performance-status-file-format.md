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

Sample file format:

Header | Data Type |Description
---|---|---
raida_id | int | 
command | int | 
timestamp | string | 
time-out-used | int | 
bytes-sent | int | 
bytes-returned | int | 
total-ms-request-took | int | 
raida-ns-spent-processing | int | 
did-timeout | boolean | 







```json



```

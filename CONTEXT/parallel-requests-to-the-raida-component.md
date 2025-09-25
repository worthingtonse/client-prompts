# Parallel Request to the RAIDA Component 
There are dozens of different commands that the client will have to issue to the RAIDA. The RAIDA consistes of 25 servers. 

All 25 RAIDA servers must be contacted simultaneously for optimal performance. Sequential requests would take 25x longer and are not acceptable.

There many problems the each request could have such as:
1. No response from RAIDA given an appropriate timeout 
2. Errors with encryption due to incorrect shared secrets between the client and the RAIDA.
3. Client decided not to send a request to a specific RAIDA because it knows that the RAIDA is down or cannot be contacted. 

## Overview
This component should only send requests that have been sent by other components that are designed to create the requests. 
This componenet should only handle the returing data that does not pertain to the Server response. The server response should be
handed over to other components who are specifically designed for handling responses for the specific command. However, this component
must be able to communicate important information about network errors, threading problems and anything that causes the process of 
requesting and receiving to fail. 

Therefor, This component should receive an array of requests and return an array of responses. This component must encode requests to binary and decode request to strings.  The array of request may contain special codes that specify a certain raida should not be contacted. The response may return error strings that a raida returned. 

This component can write information to a status file so that the information can be analysed later by AI to develope models to predict the best timeouts for calls. 

See status file standars in other documents within this repo. 

## Deliverables
1. Calculate the timeouts for the requests
2. Create or manage the threads to be used
3. Figure out the IP addresses and port numbers of the RAIDA servers to be contacted
4. A binary array of responses that may include standard error codes.
5. Entries into a statistics file using a common format. 

## What it does not need to do
1. Encrypt requests or decrypte responses
2. Make changes to binary request stings.
3. Analyse response strings that come from the RAIDA servers. 

### Asynchronous Network Operations
- **Concurrent requests**: Send all 25 requests at the same time
- **Non-blocking I/O**: Don't wait for one response before sending the next
- **Timeout per request**: Each request has independent timeout
- **Result aggregation**: Collect all responses when complete or timed out

### When to use UDP and when to use TCP
- **Size of one packet**: It is believed that if the request is less than 1400 bytes, it can fit in one packet. 
- **Number of packets**: UDP should only be used when the entire request can fit into one UDP packet, otherwise use TCP.
- **Exceptions**: There may be some services that require TCP like a command that must keep a response window open for more than 2 minutes. 
- **Serial Mode**: Sometimes, when the client is in an extreem situation where bandwidth is low, the network is unreliable or ports are blocked, the client will go into "Serial Mode" and Serial Mode will always use TCP. 

### UDP Protocol Specifics
- **Fire-and-forget**: UDP doesn't guarantee delivery
- **No connection state**: Each request is independent
- **Packet size limit**: Keep requests under 1400 bytes for single packet
- **Port handling**: Use ephemeral ports for client sockets

### Timeout Implementation
- **Recording Request Statistics**: Client software should record request statistics so that we can create an AI model that can predict the best timeout to use. The statistics file should be a .csv file that can be uploaded into python AI modules.
- **Statistics Needing Recording**: Predictions of the time a request should take should be made based on echo times, past requests, the amount of data being sent, the command that is being issed and other relavent items. 
- **Individual timeouts**: Each RAIDA request has its own timeout
- **Convert milliseconds to seconds**: Most async libraries use seconds
- **Default timeout**: 3000ms (3 seconds)
- **Timeout error handling**: Treat timeouts as server failures

### Error Categories
1. **Network errors**: Connection refused, host unreachable, etc.
2. **Timeout errors**: No response within timeout period
3. **Protocol errors**: Invalid response format or failed challenge
4. **Server errors**: Valid response but error status code

### Language-Specific Examples

#### Python (asyncio)
```python
async def send_parallel_requests(requests, challenges, timeout_sec):
    tasks = []
    for i in range(25):
        host, port = RAIDA_IPS[i]
        task = asyncio.create_task(send_single_request(
            requests[i], host, port, timeout_sec, challenges[i]
        ))
        tasks.append(task)
    
    results = await asyncio.gather(*tasks)
    return results
```

#### JavaScript (Promise.all)
```javascript
async function sendParallelRequests(requests, challenges, timeoutMs) {
    const promises = requests.map((request, i) => 
        sendSingleRequest(request, RAIDA_IPS[i], timeoutMs, challenges[i])
    );
    return await Promise.all(promises);
}
```

#### C# (Task.WhenAll)
```csharp
public async Task<Result[]> SendParallelRequestsAsync(
    byte[][] requests, byte[][] challenges, int timeoutMs)
{
    var tasks = new Task<Result>[25];
    for (int i = 0; i < 25; i++)
    {
        tasks[i] = SendSingleRequestAsync(
            requests[i], RAIDA_IPS[i], timeoutMs, challenges[i]);
    }
    return await Task.WhenAll(tasks);
}
```

### Result Processing
- **Status array**: Create array of 25 status strings
- **Latency array**: Create array of 25 latency values (float/double)
- **Error handling**: Failed requests get error status and timeout latency
- **Success validation**: Check both challenge validation AND status code

### Performance Considerations
- **Connection pooling**: Reuse UDP sockets where possible
- **Memory efficiency**: Clean up resources after each request
- **CPU usage**: Parallel processing uses multiple cores
- **Network efficiency**: All requests sent simultaneously reduces total time

## Implementation Checklist
- [ ] Asynchronous/parallel request sending
- [ ] Individual timeout handling per request
- [ ] Proper UDP socket management
- [ ] Challenge validation for each response
- [ ] Status code parsing from byte 2
- [ ] Error categorization and reporting
- [ ] Latency measurement (start to finish)
- [ ] Resource cleanup (sockets, memory)

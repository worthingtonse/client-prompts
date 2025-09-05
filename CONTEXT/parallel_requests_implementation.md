# Parallel Request Implementation Guide

## Overview
All 25 RAIDA servers must be contacted simultaneously for optimal performance. Sequential requests would take 25x longer and are not acceptable.

## Implementation Requirements

### Asynchronous Network Operations
- **Concurrent requests**: Send all 25 requests at the same time
- **Non-blocking I/O**: Don't wait for one response before sending the next
- **Timeout per request**: Each request has independent timeout
- **Result aggregation**: Collect all responses when complete or timed out

### UDP Protocol Specifics
- **Fire-and-forget**: UDP doesn't guarantee delivery
- **No connection state**: Each request is independent
- **Packet size limit**: Keep requests under 1400 bytes for single packet
- **Port handling**: Use ephemeral ports for client sockets

### Timeout Implementation
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
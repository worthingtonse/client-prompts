# Challenge Response Validation for Echo Command

## Overview
The echo command includes challenge-response validation to prevent spoofing and ensure authentic server responses.

## Challenge Field Construction
1. **Generate 16 random bytes** for the original challenge
2. **Take first 12 bytes** of the random data
3. **Calculate CRC32** of those 12 bytes
4. **Append CRC32** (4 bytes, big-endian) to create the 16-byte challenge field
5. **Store the complete 16-byte challenge** for response validation

## Challenge Field Format
```
[12 bytes random data][4 bytes CRC32 checksum]
```

## CRC32 Calculation
- **Algorithm**: Standard CRC32 (polynomial 0x04C11DB7)
- **Input**: First 12 bytes of random challenge data
- **Output**: 4-byte checksum in big-endian byte order
- **Example (Python)**: `crc_bytes = struct.pack('>I', zlib.crc32(challenge_data))`

## Response Validation
1. **Extract challenge echo** from response bytes 16-32 (header signature field)
2. **Compare with sent challenge**: Must match exactly
3. **Validation logic**:
   ```python
   # In response validation
   if len(response) < 32 or response[16:32] != expected_challenge:
       return 'error:failed_challenge'
   ```

## Security Purpose
- **Prevents replay attacks**: Each request has unique challenge
- **Authenticates responses**: Only server with correct challenge can respond
- **Detects network errors**: Corrupted responses fail challenge validation

## Implementation Requirements
- **Unique challenges**: Never reuse challenge bytes across requests
- **Secure random generation**: Use cryptographically secure random number generator
- **Exact matching**: Challenge response must match sent challenge byte-for-byte
- **Proper error handling**: Failed challenge validation should be treated as server error

## Error Messages
- `error:failed_challenge`: Response challenge doesn't match sent challenge
- Include this check before parsing status codes from response
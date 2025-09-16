# Start Session API - Simplified Guide

## What This Does
This API lets a client start a secure session with a content server (like QMail) by proving their identity using CloudCoin and special "tickets" from RAIDA servers.

## Overview
Think of this like getting into a secure building:
1. You get multiple ID badges (tickets) from security checkpoints (RAIDA servers)
2. You present all your badges to the building (content server)  
3. The building verifies your badges with the security checkpoints
4. If enough checkpoints confirm your identity, you're allowed in

## Step-by-Step Process

### What the Client Does:
1. **Get tickets**: Request authentication tickets from at least 13 RAIDA servers using your CloudCoin ID
2. **Send everything**: Send all 25 tickets (some may be empty placeholders) plus your proposed session key to the content server

### What the Content Server Does:
1. **Receive request**: Gets your tickets, CloudCoin serial number, and proposed session key
2. **Verify tickets**: Sends all tickets to RAIDA servers to check if they're valid
3. **Check responses**: Compares the serial numbers returned by RAIDA with your CloudCoin ID
4. **Make decision**: If 13+ RAIDA servers confirm your identity, accepts your session key

## Request Format
The request contains:
- **16 bytes**: Challenge data
- **7 bytes**: Your CloudCoin info (type + denomination + serial number)
- **16 bytes**: Your proposed session key  
- **100 bytes**: 25 tickets (4 bytes each, some may be all zeros if empty)
- **2 bytes**: End of request bytes that are not encrypted (0xE3E3)

## Possible Responses
- **250** - Success
- **241** - All tickets validated successfully
- **242** - All tickets failed validation  
- **243** - Some tickets passed, some failed

## Key Points
- You need at least 13 valid RAIDA servers to confirm your identity
- The system always expects exactly 25 tickets, even if some are just placeholder zeros
- Empty tickets are represented as `0x00 0x00 0x00 0x00`
- The content server does the verification work by talking to RAIDA servers directly


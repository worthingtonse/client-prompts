# QMail API Specification

QMail is a distributed, quantum-safe email system that enables secure file transfer and messaging with advanced features like striping, redundancy, and mutual authentication.

## Overview

QMail allows users to send and receive messages with attachments using a distributed architecture. The system provides quantum-safe communication through shared secrets and RAIDA (Redundant Array of Independent Detection Agents) authentication.

### Key Features

- **Distributed Architecture**: Messages can be distributed across multiple QMail servers for redundancy
- **Quantum-Safe Security**: Uses quantum key exchange (QKE) for secure communication
- **File Striping**: Large files can be split across multiple servers using various RAID configurations
- **Automatic Expiration**: Files are automatically deleted after a specified time period
- **Version Control**: Support for file versioning and overwriting
- **Mutual Authentication**: Both clients and servers authenticate through RAIDA

## Architecture

### File Storage

Files on QMail servers use a structured naming convention:
- **QMail files**: `{qmail-id}.stripe{XX}-{Y}.type{ZZZ}.exp{AAA}.qmail`
- **Attachments**: `{qmail-id}.stripe{XXX}.type{ZZZ}.v{BBB}.bin`

Where:
- `{qmail-id}`: Half-GUID identifier (8 bytes)
- `{XX}-{Y}`: Stripe number and total stripes
- `{ZZZ}`: File type identifier (3 digits)
- `{AAA}`: Days until expiration (3 digits)
- `{BBB}`: Version number (3 digits)

**Note**: Files stored locally use "whole" instead of stripe numbers.

### RAID Configuration

QMail supports multiple RAID types for data redundancy:

See the [RAID Standard](raid-codes.md) for figuring out these bytes.

## Authentication

### Account Creation

Before receiving email, users must:

1. Create accounts on multiple QMail servers for distribution
2. Establish shared secrets using Quantum Key Exchange (QKE)
3. Pay account creation fees (typically with CloudCoin or similar)
4. Query the DRD (Distributed Resource Directory) for server information

### Mutual Authentication Process

1. Both client and server obtain tickets from RAIDA using the [Get Ticket Service](get-ticket.md)
2. Minimum 13 of 25 RAIDA tickets required for authentication
3. Authenticated tickets can be reused as session tokens
4. Session timeout configurable by user (server permitting)

## API Endpoints

### Send QMail Service

Transfers files from user's computer to receiver's mail folder on QMail servers.

#### Request Format

```
CH CH CH CH CH CH CH CH CH CH CH CH CH CH CH CH // 16-byte Challenge
[Send Mail CBDF]
E3 E3 // End of body marker
```

#### Send Mail CBDF Structure

The request uses Compact Binary Document Format (CBDF) with fixed and variable sections.

##### Fixed Part (23 bytes)

| Field | Size (bytes) | Description |
|-------|--------------|-------------|
| Email Half GUID | 8 | Unique identifier for this email across all servers |
| File Type/Index | 1 | File type identifier (see File Types table) |
| Sender ID | 6 | 2-byte coin ID + 1-byte denomination + 4-byte serial |
| Primary Receiver ID | 6 | 2-byte coin ID + 1-byte denomination + 4-byte serial |
| RAID Type | 2 | How the data is spread out of the QMail servers including fault tolerance data. See [RAID Standard](raid-codes.md) |
| Stripe Number | 1 | Stripe index (0 to N, max 32 servers) |
| Of Number | 1 | Total number of stripes |

**Note**: Phase I uses coin ID `0x0006`.

##### Variable Part (Optional Fields)

| ID | Field Name | Format | Description |
|----|------------|---------|-------------|
| 1 | To Array | 6 bytes per recipient | Primary recipients |
| 2 | CCs Array | 6 bytes per recipient | Carbon copy recipients |
| 3 | BCCs Array | 6 bytes per recipient | Blind carbon copy recipients |
| 4 | Ticket Array | Variable | RAIDA authentication tickets |
| 5 | Session ID | GUID | Previously authenticated session token |
| 6 | Peer-to-Peer Secret CBDF | Variable | Private user identification data |
| 7 | Group ID | GUID | Reserved for future group functionality |
| 8 | Version Number | Variable | File version (default: 0) |
| 9 | Subject Stripe | 256 bytes | RAID type + stripe info + subject text (253 bytes) |
| 10-12 | Shuffle Table Shards | Variable | RAID shuffle table (Phase II) |

**Recipient Format**: Each recipient entry contains:
- 2 bytes: Coin type (0x0006 for Phase I)
- 1 byte: Denomination  
- 4 bytes: Serial number

**Ticket Format**: Each ticket contains:
- 2 bytes: Chip type
- 1 byte: RAIDA index
- 1 byte: Sender denomination
- 4 bytes: Sender serial number

#### Response Status Codes

```c
STATUS_SUCCESS = 250
ERROR_OVERWRITE_FAILED_FILE_WAS_REMOVED_OR_NEVER_EXISTED = 8
ERROR_FEW_COINS_IN_LOCKER = 153
ERROR_LOCKER_EMPTY_OR_NOT_EXISTS = 179
ERROR_INVALID_PARAMETER = 198
```

## File Types

| Type ID | Name | Description |
|---------|------|-------------|
| 0 | QMAIL | Primary email message file |
| 1 | QTEXT | Reserved for future text processing |
| 2 | QCHAT | Reserved for future chat functionality |
| 3 | PEER_TO_PEER_SECRET_CBDF | Private user identification data |
| 4 | GROUPS_SECRET_CBDF | Private group identification data |
| 5 | QPACKET | Reserved for future packet management |
| 6 | QDATA | File management for QData servers |
| 10-255 | Attachment N | File attachments (10 = first attachment, etc.) |

## Storage Duration

Files can be stored for varying durations based on the storage code:

| Code | Duration | Calculation | Description |
|------|----------|-------------|-------------|
| 0 | Server-dependent | N/A | Free storage, server decides deletion time |
| 1-6 | 1-6 days | Code × 1 day | Daily storage |
| 7-10 | 1-4 weeks | (Code - 6) × 7 days | Weekly storage |
| 11-22 | 1-12 months | (Code - 10) × 30 days | Monthly storage |
| 23-32 | 1-10 years | (Code - 22) × 365 days | Yearly storage |

**Note**: Longer storage periods incur higher fees as specified in the server's DRD.

## File Management

### File Size Limits

- Maximum file size determined by individual QMail servers
- Limits published in server's DRD (Distributed Resource Directory)
- Pricing varies based on file size and storage duration

### Editing and Versioning

To modify sent emails:

1. Upload file with same QMail ID but new version number
2. Set "Overwrite" command flag
3. Success only if original file hasn't been downloaded or expired
4. Returns `STATUS_SUCCESS` (0xFA) on successful overwrite

### Automatic Deletion

Files are automatically removed when:
- Downloaded by recipient
- Storage period expires
- Explicitly deleted by user (if supported)

## Communication Types Comparison

| Feature | QMail | Traditional Email | Chat/IM | SMS |
|---------|--------|------------------|---------|-----|
| **Formality** | Flexible | Formal | Informal | Very informal |
| **Response Time** | Asynchronous | Asynchronous | Real-time | Near-instant |
| **Message Length** | Unlimited | Unlimited | Platform-limited | 160 characters |
| **Network** | Internet (quantum-safe) | Internet (SMTP) | Internet | Cellular |
| **Security** | Quantum-safe + RAIDA | Encryption optional | Varies | Not encrypted |
| **File Support** | Advanced (striping/redundancy) | Standard attachments | Limited multimedia | MMS only |
| **Distribution** | Multi-server redundancy | Single server | Platform-dependent | Network-dependent |

## Implementation Notes

### Best Practices

1. **Server Distribution**: Create accounts on multiple QMail servers for optimal redundancy
2. **RAID Selection**: Choose appropriate RAID type based on security vs. performance needs
3. **Session Management**: Reuse authentication tickets within timeout periods
4. **Version Control**: Use versioning for important documents requiring change tracking

### Security Considerations

- Always verify RAIDA tickets before processing requests
- Implement proper session timeout handling
- Use appropriate storage durations to balance cost and availability
- Regularly update shared secrets and authentication tokens

### Error Handling

Implement robust error handling for:
- Network connectivity issues during multi-server operations
- Authentication failures and ticket expiration
- Storage quota exceeded scenarios
- File corruption during striping operations

## Future Enhancements

- **Phase II Features**: Advanced shuffle table implementations
- **Group Management**: Enhanced group communication features  
- **QData Integration**: Expanded file management capabilities
- **Enhanced Chat**: Real-time messaging integration
- **Advanced Encryption**: Additional quantum-safe algorithms

---

*This specification is subject to updates. Check the latest version in the official QMail documentation repository.*

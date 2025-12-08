# OPTION 1: Legacy RKE/DRD Flow (Current Code)

## System Architecture
- **Authentication:** Relies on Session IDs (8 bytes) and session keys established via RKE Handshake (Type 6).
- **Directory Service:** Uses DRD (Distributed Relations Database) to locate users.
- **Storage Path:**  
  `/opt/Q/Qmail/bin/public_upload/`
- **Inbox Path:**  
  `/opt/Q/Qmail/bin/data/<CoinID>/<Denom>/<SN>/inbox/`

---

# Prerequisites: DRD Registration (One-Time Setup)
Before any file transfer can occur, the Directory (DRD) must know where everyone is.

## Server Registration (Admin/System Level):
- **Action:** Every QMail Storage Server (RAIDA 0-24) must register itself with the DRD.
- **Command:** CMD_DRD_REGISTER_QMAIL.
- **Purpose:** Maps a Server ID (e.g., 5) to an IP Address (e.g., 192.168.1.50) in the global database. Without this, the DRD cannot tell users where to upload files.

## Receiver Registration (User Level):
- **Action:** The Receiver (User B) must implicitly or explicitly register their "Home Server" on the DRD.
- **Command:** CMD_DRD_INSERT_UPDATE.
- **Logic:**
  - User B sends a signed packet to the DRD.
  - The DRD updates its database: User SN 500200 → QMail Server ID 5.
- **Necessity:** If this step is skipped, when Sender A tries to "Tell" the Beacon, the Beacon will query the DRD for User B, find no record, and fail with ERROR_USER_NOT_FOUND.

---

# Step 1: The Upload (Sender -> Storage Server)

## Scenario:
User A uploads a file stripe to a specific Storage Server.

## Authentication
- Client sends a packet encrypted with the Session Key (Type 6).
- **Header:** CMD_UPLOAD (Code 60)
- **Payload Prefix:** Client attaches valid 16-byte Session ID.

## Server Parsing
- Server validates Session ID. If invalid -> STATUS_SESSION_TIMEOUT.
- Server extracts File Group GUID (16 bytes) from offset 16.
- Server extracts Locker Code (8 bytes) from offset 32.
- Server extracts File Type (offset 42) and Storage Duration (offset 43).
- Server extracts RAID Header (2 bytes) from offset 52 (Index & Total Stripes).

## Payment Validation
- Server sends HTTP request to  
  `http://127.0.0.1:8080/api/transactions/locker/download?locker_key=....`
- If coins < cost -> Returns ERROR_PAYMENT_REQUIRED.

## Path Construction
- Server converts GUID a1b2c3... to Hex Strings: a1, b2, a1b2c3....
- Storage Path: `/opt/Q/Qmail/bin/public_upload/a1/b2/a1b2c3.../`
- Filename: `stripeXX-YY_typeZZ_expAA_v00.qmail`

## Execution
- Server ensures directory exists (`mkdir -p`).
- Server writes binary data to disk.
- Server returns STATUS_SUCCESS.

---

# Step 2: The Notification (Sender -> Beacon)

## Scenario:
User A tells the Beacon to notify User B.

## Authentication
- Client sends packet encrypted with Session Key (Type 6).
- **Header:** CMD_TELL (Code 61).

## Server Parsing
- Server extracts Recipient List (CoinID, Denom, SN) from payload.
- Server extracts Payment Locker Code (8 bytes) from offset 32.

## Payment Logic (Split)
- Server calls Core API to consume the Sender's Locker Code.
- Server calculates 90% share.
- Server calls  
  `http://127.0.0.1:8080/api/export?amount=90`  
  to create a Receiver Locker Code.

## Inbox Logic
- Server identifies User B (SN 500200).
- Inbox Path: `/opt/Q/Qmail/bin/data/<CoinID>/<Denom>/500200/inbox/`.
- Meta File: Creates file named <GUID>.meta.
- Content: Writes Metadata + Receiver Locker Code into the file.

## Trigger
- Calls `network_notify_new_meta()` to wake up any active PING connections.

---

# Step 3: The Check (Receiver -> Beacon)

## Scenario:
User B waits for mail.

## Authentication
- User B connects with Session ID (Type 6).
- **Header:** CMD_PING (Code 62).

## Execution
- Server checks `/opt/Q/Qmail/bin/data/.../inbox/`.
- If Empty: Adds socket to **inotify list** (Long Polling) and waits.
- On Event: When `.meta` file appears (from Step 2), Server reads the file.

## Response
- Sends the .meta file content to User B.

---

# Step 4: The Download (Receiver -> Storage Server)

## Scenario:
User B downloads the file.

## Authentication
- User B connects with Session ID (Type 6).
- **Header:** CMD_DOWNLOAD (Code 64).

## Server Parsing
- Extracts GUID (16 bytes) from payload.
- Extracts File Type, Version, Page Number.

## Lookup
- Reconstructs path `/opt/Q/Qmail/bin/public_upload/a1/b2/<GUID>/`.
- Scans directory for file matching typeZZ and v00.

## Execution
- Opens file `stripeXX-YY....`
- Reads chunk (based on Page Number).
- Sends binary data to User B.

---

# OPTION 2: New RAIDAX Flow (Type 1 / Stateless)

## System Architecture
- **Authentication:** Stateless Type 1. Identity is derived from the Coin AN in the packet header. No Session IDs.
- **Directory Service:** Static Text Files (user.txt, mail.txt).
- **Storage Path:** `/opt/raidax/public_uploads/`
- **Inbox Path:** `/opt/raidax/mailboxes/<SN>/inbox/`

---

# Phase 0: Configuration Load

## Startup
- main.c calls `files_init()`.

## Load Map
- Reads `/opt/raidax/config/user.txt` into memory.
- Entry: `500200 5` (User 500200 is on RAIDA 5).

## Load IP
- Reads `/opt/raidax/config/mail.txt`.
- Entry: `5 192.168.1.50` (RAIDA 5 IP).

---

# Step 1: The Upload (Sender -> Storage Server)

## Scenario:
User A uploads a stripe to RAIDA 5.

## Authentication
- Client encrypts packet using Sender's Coin AN (Type 1 Header).
- Header: CMD_UPLOAD (Code 60). Contains Sender SN.

## Server Parsing (No Session)
- Server validates AN. Identity is confirmed.
- Server parses Payload (starting at Byte 0, since no Session ID):
  - GUID: Bytes 0-15.
  - Locker Code: Bytes 16-23 (Optional/Ignored if payment is at Beacon).
  - RAID Header: Bytes 36-37.
  - Data: Bytes 38+.

## Path Construction
- Base: `/opt/raidax/public_uploads/`
- Hashed: `/opt/raidax/public_uploads/a1/b2/<GUID>/`
- Filename: `stripeXX-YY_type00_v00.qmail`

## Execution
- Writes file to disk.
- Returns STATUS_SUCCESS. (No DB update, no Beacon communication).

---

# Step 2: The Notification (Sender -> Beacon)

## Scenario:
User A notifies RAIDA 13 (Beacon).

## Authentication
- Client encrypts packet using Sender's Coin AN (Type 1).
- Header: CMD_TELL (Code 61).

## Server Parsing
- Payload (Byte 0+): GUID, Locker Code, Recipient SNs.

## Payment Logic
- RAIDA 13 calls Core API (Port 8080) to process the Locker Code (Import/Split/Export).
- Generates Receiver Locker Code.

## Inbox Logic
- Server extracts Recipient SN (500200).
- Inbox Path: `/opt/raidax/mailboxes/500200/inbox/`.
- Meta File: Writes `<RandomID>.meta`.
- Content: Metadata + Receiver Locker Code.

## Trigger
- inotify (OS mechanism) detects the new file and alerts the net.c loop.

---

# Step 3: The Check (Receiver -> Beacon)

## Scenario:
User B connects to RAIDA 13.

## Authentication
- Client encrypts packet using Receiver's Coin AN (Type 1).
- Header: Contains SN 500200.
- Payload: Empty.

## Execution
- Server reads SN 500200 from Header.
- Server watches `/opt/raidax/mailboxes/500200/inbox/`.
- Wait: Holds socket open (STATE_PING_ACTIVE).
- Event: When Step 2 writes the file, Server wakes up.

## Response
- Reads .meta file and sends it to User B.

---

# Step 4: The Download (Receiver -> Storage Server)

## Scenario:
User B downloads from RAIDA 5.

## Authentication
- Client encrypts using Receiver's Coin AN (Type 1).
- Header: CMD_DOWNLOAD (Code 64).

## Server Parsing
- Payload (Byte 0+): GUID, Version.

## Lookup
- Server checks user.txt.  
  Is User B allowed here? (Optional/Supervisor logic).
- Path: `/opt/raidax/public_uploads/a1/b2/<GUID>/`.

## Execution
- Finds stripeXX-YY....
- Streams binary data to User B.

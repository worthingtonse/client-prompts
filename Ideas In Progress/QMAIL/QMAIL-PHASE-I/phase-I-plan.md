# Phase I Plan

## Phase I: Foundational Workflow
In this initial phase, the core messaging functionality is esQMAIL-PHASE-IIItablished with a simple DRD (Distributed Resource Directory).

Goal of this Phase: 
1. Install Distributed Key Exchange RAIDA Server and Content Server on all RAIDA.
2. Build the Phase I Distributed Resource Directory Services (start session, Update DRD and Search DRD)
3. Install Distributed Resource Directory on all RAIDA.
4. Build the Phase I QMail services (Send, PING, PEEK, Download Meta, Download File), 
5. Get servers that are out the up and running again,
6. Implement a QMail Server on these servers.
8. Get it working on the Client and test everything.

## Server Discovery: 
  1. DRD Documentation: Ideas In [Phase I DRD Documentation](https://github.com/worthingtonse/client-prompts/blob/main/Ideas%20In%20Progress/QMAIL/phase-I-drd.md)
  2. The Register QMail Server Service (If I have a QMail server, I can advertise it in the DRD.
  3. Client Registration in the DRD. Most importantly the QMail Servers the client uses.
  4. Client will specify what the push server is and the backup push server is. 
  5. The client downloads a basic, static directory to locate the initial beta QMail servers.

TODO: Create a service called "Start Session", Add a session table to the ERD. Add Change date to ERD user. Hard code location of DRD into Client.

## Key Exchange: Users establish secure keys with their chosen QMail servers via the QKE protocol.


## Contact Exchange: Users must exchange their user IDs manually (e.g., over another secure channel).

## Sending Messages: Users can send plain-text qmails with small attachment limits. No tips or fees are implemented yet.

Receiving Messages: The client periodically polls the QMail servers for new messages.


Message Download: The receiver downloads their qmails and attachments for local storage and viewing.

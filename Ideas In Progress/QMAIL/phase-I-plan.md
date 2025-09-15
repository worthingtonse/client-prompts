# Phase I Plan

## Phase I: Foundational Workflow
In this initial phase, the core messaging functionality is established with a simple DRD (Distributed Resource Directory).

Goal of this Phase: 
1. Implement a Simple DRD Server/service
2. Implement a QMail Server
3. Integrate with the existing QKey, DKE, RKE (Code written by Mohsin and implemented in his RAIDAX repo on GitLab 
4. Create some services on the client to test the functionality of QMail.

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

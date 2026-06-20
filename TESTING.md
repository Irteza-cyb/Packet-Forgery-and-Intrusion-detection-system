# Testing Notes — ScapyShield Project

## Overview
This project (ScapyShield) was cloned from my friend's GitHub repository. 
The goal of this branch is to document the steps I took to set up, run, 
and test the project on my own system, along with any issues I faced 
and how I resolved them.

## Environment
- OS: Windows
- Editor: Visual Studio Code
- Terminal used: PowerShell (inside VS Code)
- Python version: (you can check this by typing `python --version` in the terminal)

## Setup Steps
1. Cloned the repository from my friend's GitHub to my local machine.
2. Opened the project folder in VS Code.
3. Installed all required Python packages using:
   pip install -r requirements.txt
   This installed dependencies including scapy (version 2.7.0).
4. Attempted to run the application using:
   python app.py

## Issue Encountered
On the first run, the application launched the GUI dashboard successfully, 
but the terminal displayed the following warning and error:

   WARNING: No libpcap provider available! pcap won't be used
   Critical Sniffer Thread Error: Sniffing and sending packets is not 
   available at layer 2: winpcap is not installed.

This meant the sniffer module (sniffer.py) could not capture real network 
packets because Windows requires a packet capture driver, which was missing.

## Fix Applied
1. Downloaded and installed Npcap from the official site (npcap.com).
2. During installation, enabled the option "Install Npcap in WinPcap 
   API-compatible Mode," since scapy relies on this compatibility mode.
3. Restarted VS Code.
4. Re-ran VS Code as Administrator, since raw packet sniffing requires 
   elevated permissions on Windows.
5. Ran the project again using:
   python app.py

## Result After Fix
The application launched successfully with no errors. The dashboard 
("ScapyShield // Cyber Security Dashboard") opened and displayed live data:

- Packets Sniffed: updating in real time
- SYN Scans Detected: counter increasing
- Spoofed Responses: counter increasing

The Live Sniffer Console showed real-time detection and response logs, 
for example:

   [!] SCAN DETECTED: Host 192.168.1.2 is probing Port 443
   [Detector Engine] Source IP: 192.168.1.2 -> Target Port: 443
   [*] FORGER MODULE ACTIVATED
   [*] Assembling Layer 2, Layer 3 & Layer 4 packets with SYN-ACK flags
   [+] INJECTION SUCCESSFUL. Scanner Deceived.

This confirmed that all core modules of the project are working as intended:

- sniffer.py — successfully captured raw network traffic
- detector.py — correctly identified incoming SYN scan attempts
- forger.py — successfully crafted and injected spoofed SYN-ACK 
  packets to deceive the scanning host
- The GUI dashboard (analytics_panel.py / rules_panel.py) correctly 
  displayed live statistics and console output
- Data logging to scapyshield.db appeared to be functioning, based on 
  the updating counters

## Conclusion
After resolving the missing Npcap driver issue, the project ran 
completely as expected. The packet sniffing, intrusion detection, 
and packet forgery/deception modules all worked together correctly, 
and the dashboard accurately reflected live activity.

## Notes for Future Setup (for anyone else running this project on Windows)
- Make sure Npcap is installed with WinPcap-compatible mode enabled 
  before running the project.
- Run the IDE/terminal as Administrator, since packet sniffing requires 
  elevated system permissions on Windows.
- If the sniffer error appears again, double check that Npcap installed 
  correctly and that no other process is using the network interface.
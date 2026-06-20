# ScapyShield

## Active Network Defense and Intrusion Detection Framework

ScapyShield is a Python-based network security platform that combines intrusion detection, packet monitoring, packet forgery, database logging, and real-time analytics into a unified defensive framework.

The system leverages Scapy for packet inspection and manipulation while providing a graphical interface for monitoring suspicious activity and managing detection rules.

---

## Features

* Real-time packet capture and inspection
* Intrusion detection engine
* Packet forgery and deception responses
* SQLite database logging
* Analytics dashboard
* Detection rules management
* Multi-threaded architecture
* Modular GUI design

---

## Architecture

```text
Network Traffic
       |
       v
+------------------+
| Packet Sniffer   |
|   sniffer.py     |
+------------------+
       |
       v
+------------------+
| Detection Engine |
|   detector.py    |
+------------------+
       |
       +------------------+
       |                  |
       v                  v
+-------------+   +----------------+
| Packet      |   | SQLite Database|
| Forgery     |   |  database.py   |
| forger.py   |   +----------------+
+-------------+
       |
       v
+------------------+
| GUI Components   |
| app.py           |
| rules_panel.py   |
| analytics_panel.py
+------------------+
```

---

## Project Structure

```text
ScapyShield/
│
├── app.py
├── detector.py
├── sniffer.py
├── forger.py
├── database.py
├── config.py
├── rules_panel.py
├── analytics_panel.py
└── requirements.txt
```

---

## Requirements

### Python

* Python 3.9+

### Packet Capture Support

Windows:

* Npcap

Linux:

* Libpcap

macOS:

* Libpcap

---

## Installation

Clone the repository:

```bash
git clone <repository-url>
cd ScapyShield
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Running the Application

```bash
python app.py
```

Administrator privileges may be required for packet capture operations.

---

## Configuration

Application settings can be modified through:

```text
config.py
```

---

## Database

The system uses SQLite for storing detection events and network activity logs.

---

## Disclaimer

This project is intended for educational and research purposes. Only use on networks where you have authorization to monitor traffic.

---

## License

Open Source Educational Project.


# 🛡️ ScapyShield — Packet Forgery and Intrusion Detection System

ScapyShield is a Python-based defensive networking tool that **detects TCP SYN port scans in real time** and responds by **forging spoofed SYN-ACK replies**, tricking the scanning tool into believing the probed port is open. The project also includes a desktop dashboard (built with Tkinter) for visualizing sniffer activity, detected scans, and forged responses.

> ⚠️ **Educational Use Only**: This tool crafts and injects raw network packets. It is intended strictly for learning about network security concepts (port scanning, packet crafting, deception techniques) in a **controlled lab environment** that you own or have explicit permission to test on. Do not run this against networks or systems you do not control.

---

## ✨ Features

- **Live Packet Sniffing** — Captures TCP traffic on a chosen network interface using Scapy.
- **SYN Scan Detection** — Identifies incoming SYN packets (the signature of a port scan) and extracts source IP, source port, destination port, and sequence number.
- **Packet Forging Engine** — Crafts a spoofed IP/TCP SYN-ACK packet and injects it back to the scanner, simulating an "open port" to mislead the attacker.
- **Attack Logging** — Persists scan events (attacker IP, target port, attack type, timestamp) to a local SQLite database.
- **Security Dashboard (GUI)** — A dark-themed Tkinter control panel showing live console logs, packet/scan metrics, and module status (Sniffer, Detector, Forger).

---

## 🧩 Project Structure

```
Packet-Forgery-and-Intrusion-detection-system/
│
├── sniffer.py      # Captures raw TCP packets on the network interface
├── detector.py      # Parses captured packets, builds the spoofed response data
├── forger.py        # Assembles and injects the spoofed SYN-ACK packet
├── database.py       # Logs detected attacks into a SQLite database
├── app.py             # Tkinter-based GUI dashboard (visual demo / mock console)
└── README.md
```

### How the modules connect

```
sniffer.py  →  detector.py  →  forger.py
   (capture)     (analyze)      (deceive)
                     ↓
                database.py
                  (log)
```

1. **`sniffer.py`** listens on a network interface and filters for TCP packets. When a bare `SYN` flag is detected, it packages the packet's details into a `PacketInfo` object.
2. **`detector.py`** receives the `PacketInfo`, calculates the appropriate ACK number, prints a summary, and hands the data off to the forger.
3. **`forger.py`** builds a fake `IP`/`TCP` SYN-ACK packet using Scapy and sends it back to the source, making the scanner believe the port is open.
4. **`database.py`** provides functions to initialize a SQLite database and log each detected attack with a timestamp.
5. **`app.py`** is a standalone GUI dashboard that visually mocks up the system's live console, metrics, and module status — useful for demos/presentations.

---

## 🛠️ Requirements

- Python 3.8+
- [Scapy](https://scapy.net/)
- Tkinter (usually bundled with Python; on Linux you may need `python3-tk`)
- Administrator/root privileges (required for raw packet sniffing and injection)

Install dependencies:

```bash
pip install scapy
```

On Linux, if Tkinter is missing:

```bash
sudo apt-get install python3-tk
```

---

## 🚀 Usage

### 1. Run the Sniffer + Detector + Forger pipeline

This requires elevated privileges since it sniffs and injects raw packets.

```bash
sudo python3 sniffer.py -i eth0
```

- `-i` / `--interface` — network interface to listen on (e.g. `eth0`, `wlan0`). Defaults to Scapy's default interface if omitted.

When a SYN packet is detected, the console will log the scan, show the detector's calculated response, and trigger the forger to send a spoofed SYN-ACK back to the source.

### 2. Initialize and test the logging database

```bash
python3 database.py
```

This creates `scapyshield.db` with an `attack_logs` table and inserts a sample log entry.

### 3. Launch the GUI dashboard (demo mode)

```bash
python3 app.py
```

Opens the ScapyShield desktop dashboard with mocked console output, metrics, and module status — no live sniffing required.

---

## 🗄️ Database Schema

**Table: `attack_logs`**

| Column         | Type     | Description                          |
|----------------|----------|---------------------------------------|
| `log_id`       | INTEGER  | Auto-incrementing primary key         |
| `attacker_ip`  | TEXT     | Source IP of the detected scan        |
| `target_port`  | INTEGER  | Port that was probed                  |
| `attack_type`  | TEXT     | Type of attack (e.g. "SYN Scan")      |
| `timestamp`    | DATETIME | Auto-recorded time of the log entry   |

---

## ⚠️ Known Issues / TODO

- `detector.py` calls `send_spoofed_syn_ack()` with an extra `ack_number` argument, but the current `forger.py` function signature (`hacker_ip, target_port, hacker_port`) does not accept it — this needs to be reconciled before the live pipeline will run end-to-end.
- `database.py`'s `if __name__ == "_main_":` guard has a typo (should be `"__main__"`), so running the file directly currently does nothing.
- `sniffer.py` and `detector.py` are not yet wired to call `database.py` to persist logs automatically.
- `app.py` is currently a static visual mockup — it does not yet pull live data from the sniffer/detector pipeline.

---

## 👥 Team / Module Ownership

| Module          | Responsibility                          |
|-----------------|-------------------------------------------|
| `sniffer.py`    | Packet capture                            |
| `detector.py`   | Scan detection & response calculation     |
| `forger.py`     | Spoofed packet construction & injection   |
| `database.py`   | Attack logging (Database Lead)            |
| `app.py`        | Dashboard / GUI                           |

---

## 📜 Disclaimer

This project is built for academic/educational purposes to demonstrate concepts in network packet analysis, intrusion detection, and active deception defense. Unauthorized use against networks you do not own or lack explicit permission to test may be illegal under computer misuse laws in your jurisdiction. Use responsibly.

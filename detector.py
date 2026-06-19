# detector.py
# Contributor: Huraira (Irtiza ke project mein)
# Improvement: Added scan type detection, severity levels, and safe error handling

from dataclasses import dataclass, field
from datetime import datetime
from forger import send_spoofed_syn_ack
from database import log_attack

# Ports considered high-value targets
CRITICAL_PORTS = {22, 23, 80, 443, 3306, 8080}

@dataclass
class PacketInfo:
    source_ip: str
    source_port: int
    destination_ip: str
    destination_port: int
    sequence_number: int
    flags: str = "S"


def _get_severity(destination_port: int) -> str:
    """Return HIGH if critical port is targeted, else MEDIUM."""
    return "HIGH" if destination_port in CRITICAL_PORTS else "MEDIUM"


def _get_scan_type(flags: str) -> str:
    """Identify scan type from TCP flags."""
    scan_map = {
        "S":  "SYN Scan",
        "F":  "FIN Scan",
        "":   "NULL Scan",
        "FPU": "XMAS Scan",
    }
    return scan_map.get(flags, "Unknown Scan")


class Detector:

    def build_response(self, packet: PacketInfo) -> dict:
        return {
            "timestamp":     datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "source_ip":     packet.source_ip,
            "source_port":   packet.source_port,
            "target_port":   packet.destination_port,
            "response_type": "SYN-ACK",
            "ack_number":    packet.sequence_number + 1,
            "severity":      _get_severity(packet.destination_port),
            "scan_type":     _get_scan_type(packet.flags),
        }

    def process_packet(self, packet: PacketInfo, ui_callback=None):
        result   = self.build_response(packet)
        severity = result["severity"]
        scan     = result["scan_type"]

        # 1. Log to database with severity and scan type
        try:
            log_attack(packet.source_ip, packet.destination_port, scan)
        except Exception as e:
            if ui_callback:
                ui_callback(f"[!] DB Error: {e}", tag="warning")

        # 2. Send messages to UI
        if ui_callback:
            ui_callback(
                f"[{severity}] {scan} from {packet.source_ip} "
                f"-> Port {packet.destination_port} | ACK: {result['ack_number']}",
                tag="success"
            )
            ui_callback("[*] FORGER MODULE ACTIVATED", tag="forger")
            ui_callback("[*] Assembling Layer 3 & Layer 4 packets with SYN-ACK flags...", tag="forger")

        # 3. Inject spoofed SYN-ACK via Forger
        try:
            send_spoofed_syn_ack(
                hacker_ip=packet.source_ip,
                target_port=packet.destination_port,
                hacker_port=packet.source_port,
            )
        except Exception as e:
            if ui_callback:
                ui_callback(f"[!] Injection failed: {e}", tag="warning")
            return result

        if ui_callback:
            ui_callback("[+] INJECTION SUCCESSFUL. Scanner Deceived.\n", tag="success")

        return result
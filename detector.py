# detector.py (Updated Section)
from dataclasses import dataclass
from datetime import datetime
from forger import send_spoofed_syn_ack
from database import log_attack  # <-- Import the database lead's function

@dataclass
class PacketInfo:
    source_ip: str
    source_port: int
    destination_ip: str
    destination_port: int
    sequence_number: int

class Detector:
    def build_response(self, packet: PacketInfo):
        response = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "source_ip": packet.source_ip,
            "source_port": packet.source_port,
            "target_port": packet.destination_port,
            "response_type": "SYN-ACK",
            "ack_number": packet.sequence_number + 1
        }
        return response

    def process_packet(self, packet: PacketInfo, ui_callback=None):
        result = self.build_response(packet)

        # 1. Save attack signatures immediately to SQLite Database
        log_attack(packet.source_ip, packet.destination_port, "SYN Scan")

        # 2. Format and output messages to the UI Console securely
        if ui_callback:
            ui_callback(f"[Detector Engine] Source IP: {packet.source_ip} -> Target Port: {packet.destination_port} | Generated ACK: {result['ack_number']}", tag="success")
            ui_callback("[*] FORGER MODULE ACTIVATED", tag="forger")
            ui_callback(f"[*] Assembling Layer 3 & Layer 4 packets with SYN-ACK flags...", tag="forger")

        # 3. Trigger raw Scapy wire injections via Forger module
        send_spoofed_syn_ack(
            hacker_ip=packet.source_ip,
            target_port=packet.destination_port,
            hacker_port=packet.source_port,
        )
        
        if ui_callback:
            ui_callback("[+] INJECTION SUCCESSFUL. Scanner Deceived.\n", tag="success")

        return result

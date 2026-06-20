from dataclasses import dataclass
from datetime import datetime
from forger import send_spoofed_syn_ack
from database import log_attack  

@dataclass
class PacketInfo:
    source_ip: str
    source_port: int
    destination_ip: str
    destination_port: int
    sequence_number: int
    src_mac: str  
    dst_mac: str  
    iface: str

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
        try:
            result = self.build_response(packet)

            # 1. Temporarily bypass DB logging to test the pipeline
            try:
                log_attack(packet.source_ip, packet.destination_port, "SYN Scan")
            except Exception as db_error:
                if ui_callback:
                    ui_callback(f"[-] DB Warning (Ignored): {db_error}", tag="warning")

            # 2. Format and output messages to the UI Console
            if ui_callback:
                ui_callback(f"[Detector Engine] Source IP: {packet.source_ip} -> Target Port: {packet.destination_port} | Generated ACK: {result['ack_number']}", tag="success")
                ui_callback("[*] FORGER MODULE ACTIVATED", tag="forger")
                ui_callback("[*] Assembling Layer 2, Layer 3 & Layer 4 packets with SYN-ACK flags...", tag="forger")

            # 3. Trigger raw Scapy wire injections via Forger module
            send_spoofed_syn_ack(
                hacker_ip=packet.source_ip,
                target_port=packet.destination_port,
                hacker_port=packet.source_port,
                ack_number=result['ack_number'],
                src_mac=packet.src_mac,  
                dst_mac=packet.dst_mac,
                iface=packet.iface
            )
            
            if ui_callback:
                ui_callback("[+] INJECTION SUCCESSFUL. Scanner Deceived.\n", tag="success")

            return result

        except Exception as e:
            # THIS WILL CATCH ANY SILENT CRASHES AND PRINT THEM TO YOUR GUI!
            if ui_callback:
                ui_callback(f"[-] CRITICAL THREAD CRASH: {e}", tag="warning")
            print(f"CRITICAL ERROR: {e}")
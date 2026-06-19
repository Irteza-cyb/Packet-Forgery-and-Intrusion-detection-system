# sniffer.py (Updated Section)
import logging
import argparse
from scapy.all import sniff, IP, TCP
from detector import Detector, PacketInfo

logging.basicConfig(level=logging.INFO, format='%(message)s')
detector_engine = Detector()

# Global reference for UI routing
ui_logger = None

def packet_callback(packet):
    if packet.haslayer(IP) and packet.haslayer(TCP):
        tcp_flags = packet[TCP].flags

        if tcp_flags == "S":
            msg = f"[!] SCAN DETECTED: Host {packet[IP].src} is probing Port {packet[TCP].dport}"
            logging.warning(msg)
            
            # Send alert to Tkinter console if available
            if ui_logger:
                ui_logger(msg, tag="warning")
            
            scanned_packet_data = PacketInfo(
                source_ip=packet[IP].src,
                source_port=packet[TCP].sport,
                destination_ip=packet[IP].dst,
                destination_port=packet[TCP].dport,
                sequence_number=packet[TCP].seq
            )
            
            # Pass down the UI logger so the detector and forger can output to the screen
            detector_engine.process_packet(scanned_packet_data, ui_callback=ui_logger)

def start_sniffer(interface_name, ui_callback=None):
    global ui_logger
    ui_logger = ui_callback  # Attach the GUI console logger
    
    logging.info(f"[*] Starting ScapyShield sniffer on interface: {interface_name if interface_name else 'Default'}")
    sniff(
        iface=interface_name,   
        filter="tcp",           
        prn=packet_callback,    
        store=0                 
    )
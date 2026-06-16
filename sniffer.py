import logging
import argparse
from scapy.all import sniff, IP, TCP
# Imports the dataclass and engine from your detector.py file
from detector import Detector, PacketInfo

# Configure logging so INFO messages actually print to the terminal
logging.basicConfig(level=logging.INFO, format='%(message)s')

# Initialize the detector engine globally
detector_engine = Detector()

def packet_callback(packet):
    if packet.haslayer(IP) and packet.haslayer(TCP):
        tcp_flags = packet[TCP].flags

        if tcp_flags == "S":
            logging.warning(f"SCAN DETECTED: Host {packet[IP].src} is probing Port {packet[TCP].dport}")
            
            # Pack the raw Scapy data into the Dataclass format the detector expects
            scanned_packet_data = PacketInfo(
                source_ip=packet[IP].src,
                source_port=packet[TCP].sport,
                destination_ip=packet[IP].dst,
                destination_port=packet[TCP].dport,
                sequence_number=packet[TCP].seq
            )
            
            # Pass the structured object to the detector engine
            detector_engine.process_packet(scanned_packet_data)

def start_sniffer(interface_name):
    logging.info(f"[*] Starting ScapyShield sniffer on interface: {interface_name if interface_name else 'Default'}")
    sniff(
        iface=interface_name,   
        filter="tcp",           
        prn=packet_callback,    
        store=0                 
    )

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Packet Forgery and Intrusion Detection System")
    parser.add_argument("-i", "--interface", help="Network interface to sniff on", default=None)
    args = parser.parse_args()

    try:
        start_sniffer(args.interface)
    except KeyboardInterrupt:
        print("\n")  
        logging.info("[!] Ctrl+C detected. Exiting ScapyShield. Goodbye!")
import logging
import argparse
from datetime import datetime
from scapy.all import sniff, IP, TCP
from detector import Detector, PacketInfo

# Configure logging with timestamp format
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(message)s',
    datefmt='%H:%M:%S'
)

# Initialize the detector engine globally
detector_engine = Detector()
packet_count = 0
scan_count = 0

def packet_callback(packet):
    global packet_count, scan_count

    if packet.haslayer(IP) and packet.haslayer(TCP):
        packet_count += 1
        tcp_flags = packet[TCP].flags

        if tcp_flags == "S":
            scan_count += 1
            logging.warning(f"[!] SYN SCAN DETECTED #{scan_count} | Source: {packet[IP].src}:{packet[TCP].sport} -> Port: {packet[TCP].dport}")

            scanned_packet_data = PacketInfo(
                source_ip=packet[IP].src,
                source_port=packet[TCP].sport,
                destination_ip=packet[IP].dst,
                destination_port=packet[TCP].dport,
                sequence_number=packet[TCP].seq
            )

            detector_engine.process_packet(scanned_packet_data)
        else:
            logging.info(f"[*] Packet #{packet_count} | {packet[IP].src} -> {packet[IP].dst} | Flags: {tcp_flags}")

def start_sniffer(interface_name):
    iface_display = interface_name if interface_name else 'Default'
    logging.info(f"[*] ScapyShield sniffer started on interface: {iface_display}")
    logging.info(f"[*] Listening for TCP traffic... Press Ctrl+C to stop.\n")
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
        logging.info(f"[!] Exiting ScapyShield. Total Packets: {packet_count} | Scans Detected: {scan_count}")
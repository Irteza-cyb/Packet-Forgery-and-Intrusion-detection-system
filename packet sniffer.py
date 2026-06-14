import logging
import argparse
from scapy.all import sniff , IP, TCP

def packet_callback(packet):
    if packet.haslayer(IP) and packet.haslayer(TCP):
        src_ip=packet[IP].src
        target_port=packet[IP].dport
        tcp_flags=packet[TCP].flags

        if tcp_flags == "S":
            logging.warning(f"SCAN DETECTED: Host {src_ip} is probing Port {target_port}")


def start_sniffer(interface_name):
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
    logging.info("Ctrl+C detected. Exiting ScapyShield . Goodbye!")
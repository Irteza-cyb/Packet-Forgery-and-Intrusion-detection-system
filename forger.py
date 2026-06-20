from scapy.all import Ether, IP, TCP, sendp
import time

# Add "iface" to the end of your parameters list
def send_spoofed_syn_ack(hacker_ip, target_port, hacker_port, ack_number, src_mac, dst_mac, iface):
    """
    Constructs and injects a spoofed Layer 2 Ethernet frame bound to a specific interface.
    """
    print("\n" + "="*50)
    print("[*] FORGER MODULE ACTIVATED (LAYER 2 Windows Mode)")
    print("="*50)
    
    eth_layer = Ether(src=dst_mac, dst=src_mac)
    ip_layer = IP(dst=hacker_ip)
    tcp_layer = TCP(sport=target_port, dport=hacker_port, flags="SA", seq=1000, ack=ack_number)

    spoofed_packet = eth_layer / ip_layer / tcp_layer

    print(f"[*] Injecting raw Ethernet frame via Npcap on interface: {iface}...")
    
    # Explicitly tell sendp which interface to blast the packet out of!
    sendp(spoofed_packet, iface=iface, verbose=False)  
    
    print("[+] INJECTION SUCCESSFUL. Frame sent past Windows Kernel.")
    print("="*50 + "\n")

# ==========================================
# Example Execution (For your local testing)
# ==========================================
if __name__ == "__main__":
    # Simulated variables
    simulated_hacker_ip = "192.168.1.150"
    simulated_target_port = 443
    simulated_hacker_src_port = 55432
    simulated_ack_number = 12345 
    simulated_src_mac = "aa:bb:cc:dd:ee:ff"
    simulated_dst_mac = "11:22:33:44:55:66"
    simulated_iface = "Wi-Fi"  # <-- ADDED THIS VARIABLE FOR SAFE STANDALONE TESTING
    
    # Fire the function safely with all 7 arguments
    send_spoofed_syn_ack(
        simulated_hacker_ip, 
        simulated_target_port, 
        simulated_hacker_src_port, 
        simulated_ack_number,
        simulated_src_mac,
        simulated_dst_mac,
        simulated_iface  # <-- PASSED HERE TO MATCH THE FUNCTION
    )
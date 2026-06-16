from scapy.all import IP, TCP, send
import time

def send_spoofed_syn_ack(hacker_ip, target_port, hacker_port):
    """
    Constructs and injects a spoofed TCP SYN-ACK packet to deceive an incoming port scanner.
    
    Parameters:
    hacker_ip (str): The IP address of the attacker.
    target_port (int): The port the attacker is attempting to scan.
    hacker_port (int): The source port the attacker's scan originated from.
    """
    
    print("\n" + "="*50)
    print("[*] FORGER MODULE ACTIVATED")
    print("="*50)
    print(f"[*] Intrusion detected from IP: {hacker_ip}")
    print(f"[*] Probed Port: {target_port} | Attacker Source Port: {hacker_port}")
    time.sleep(1) # Added for aesthetic terminal flow

    # ---------------------------------------------------------
    # STEP 1: Build Layer 3 (The IP Envelope)
    # Source IP is automatically resolved by Scapy
    # ---------------------------------------------------------
    print("[*] Assembling Layer 3 (IP Envelope)...")
    ip_layer = IP(dst=hacker_ip)

    # ---------------------------------------------------------
    # STEP 2: Build Layer 4 (The TCP Envelope)
    # sport: The port we are pretending is open
    # dport: The port the hacker is listening on for a reply
    # flags: "SA" (SYN-ACK) is the master trick to fake an open port
    # ---------------------------------------------------------
    print("[*] Assembling Layer 4 (TCP Envelope) with SYN-ACK flags...")
    tcp_layer = TCP(sport=target_port, dport=hacker_port, flags="SA")

    # ---------------------------------------------------------
    # STEP 3: Stitch the Packet Together
    # ---------------------------------------------------------
    spoofed_packet = ip_layer / tcp_layer

    # ---------------------------------------------------------
    # STEP 4: Inject the Packet
    # ---------------------------------------------------------
    print(f"[*] Injecting crafted packet into the wire...")
    send(spoofed_packet, verbose=False)
    
    print("[+] INJECTION SUCCESSFUL. Scanner deceived.")
    print("="*50 + "\n")

# ==========================================
# Example Execution (For your local testing)
# ==========================================
if __name__ == "__main__":
    # Simulated variables (Member 3 would normally pass these into your function)
    simulated_hacker_ip = "192.168.1.150"
    simulated_target_port = 443
    simulated_hacker_src_port = 55432
    
    # Fire the function
    send_spoofed_syn_ack(simulated_hacker_ip, simulated_target_port, simulated_hacker_src_port)
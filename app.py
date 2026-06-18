import tkinter as tk
from tkinter import ttk, scrolledtext

# --- Theme Configuration Constants ---
BG_MAIN = "#0a0b10"
BG_SURFACE = "#121420"
BG_CONSOLE = "#05060a"
TEXT_PRIMARY = "#e2e8f0"
TEXT_MUTED = "#6272a4"

# Neon Accents
NEON_CYAN = "#00f0ff"
NEON_MAGENTA = "#ff007f"
NEON_YELLOW = "#ffb86c"
NEON_GREEN = "#50fa7b"

class ScapyShieldApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ScapyShield // Cyber Security Dashboard")
        self.root.geometry("1100x650")
        self.root.configure(bg=BG_MAIN)
        
        # Configure Styles for standard ttk widgets
        self.style = ttk.Style()
        self.style.theme_use('default')
        self.style.configure('.', background=BG_SURFACE, foreground=TEXT_PRIMARY)

        self.setup_layout()

    def setup_layout(self):
        # 1. SIDEBAR NAVIGATION PANELS
        sidebar = tk.Frame(self.root, bg=BG_SURFACE, width=240, padx=15, pady=20)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        # Logo Area
        logo_label = tk.Label(sidebar, text="🛡️ SCAPYSHIELD", font=("Courier New", 14, "bold"), fg=NEON_CYAN, bg=BG_SURFACE)
        logo_label.pack(anchor="w", pady=(0, 25))

        # Nav Links
        nav_items = [("📺 Console", True), ("🔌 Sniffer Settings", False), 
                     ("🧠 Detector Rules", False), ("⚡ Forger Engine", False), ("📊 Analytics", False)]
        for item, is_active in nav_items:
            fg_color = TEXT_PRIMARY if is_active else TEXT_MUTED
            lbl = tk.Label(sidebar, text=item, font=("Arial", 10, "bold"), fg=fg_color, bg=BG_SURFACE, anchor="w", cursor="hand2")
            lbl.pack(fill="x", pady=6, ipady=4)

        # System Status
        status_frame = tk.Frame(sidebar, bg=BG_SURFACE)
        status_frame.pack(side="bottom", anchor="w", pady=10)
        dot = tk.Label(status_frame, text="●", fg=NEON_GREEN, bg=BG_SURFACE, font=("Arial", 12))
        dot.pack(side="left")
        status_txt = tk.Label(status_frame, text=" SYSTEM ACTIVE", fg=NEON_GREEN, bg=BG_SURFACE, font=("Courier New", 9, "bold"))
        status_txt.pack(side="left")

        # 2. MAIN CONTAINER ARCHITECTURE
        main_content = tk.Frame(self.root, bg=BG_MAIN, padx=20, pady=20)
        main_content.pack(side="right", fill="both", expand=True)

        # Header Ribbon
        header_frame = tk.Frame(main_content, bg=BG_MAIN)
        header_frame.pack(fill="x", pady=(0, 15))
        
        title_lbl = tk.Label(header_frame, text="SECURITY CONTROL CENTER", font=("Arial", 12, "bold"), fg=TEXT_PRIMARY, bg=BG_MAIN)
        title_lbl.pack(side="left")
        
        iface_lbl = tk.Label(header_frame, text="IFACE: eth0", font=("Courier New", 9, "bold"), fg=NEON_CYAN, bg=BG_MAIN, bd=1, relief="solid", padx=6, pady=2)
        iface_lbl.pack(side="right")

        # 3. METRICS UPPER DISPLAY ROW
        metrics_frame = tk.Frame(main_content, bg=BG_MAIN)
        metrics_frame.pack(fill="x", pady=(0, 20))
        metrics_frame.grid_columnconfigure((0, 1, 2), weight=1, uniform="equal")

        self.create_metric_card(metrics_frame, 0, "Packets Sniffed", "142,839", NEON_CYAN)
        self.create_metric_card(metrics_frame, 1, "SYN Scans Detected", "42", NEON_YELLOW)
        self.create_metric_card(metrics_frame, 2, "Spoofed Responses", "42", NEON_MAGENTA)

        # 4. LOWER INTERACTION PANELS (Grid setup)
        modules_frame = tk.Frame(main_content, bg=BG_MAIN)
        modules_frame.pack(fill="both", expand=True)
        modules_frame.grid_columnconfigure(0, weight=2)
        modules_frame.grid_columnconfigure(1, weight=1)
        modules_frame.grid_rowconfigure(0, weight=1)

        # Live Terminal Panel Console
        console_panel = tk.Frame(modules_frame, bg=BG_SURFACE, bd=1, relief="solid", highlightbackground=TEXT_MUTED)
        console_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        console_hdr = tk.Frame(console_panel, bg=BG_SURFACE, padx=10, pady=8)
        console_hdr.pack(fill="x")
        tk.Label(console_hdr, text="💻 Live Sniffer Console", font=("Arial", 10, "bold"), fg=NEON_CYAN, bg=BG_SURFACE).pack(side="left")
        tk.Label(console_hdr, text="● Sniffing...", font=("Arial", 9, "bold"), fg=NEON_GREEN, bg=BG_SURFACE).pack(side="right")

        console_text = scrolledtext.ScrolledText(console_panel, bg=BG_CONSOLE, fg=TEXT_MUTED, insertbackground=NEON_CYAN, font=("Courier New", 9.5), bd=0, padx=10, pady=10)
        console_text.pack(fill="both", expand=True)
        
        # Populate Console Logs with color tags
        console_text.tag_config('warning', foreground=NEON_YELLOW)
        console_text.tag_config('success', foreground=NEON_GREEN)
        console_text.tag_config('forger', foreground=NEON_CYAN)

        console_text.insert(tk.END, "[*] Starting ScapyShield sniffer on interface: eth0\n")
        console_text.insert(tk.END, "[!] SCAN DETECTED: Host 192.168.1.150 is probing Port 443\n", 'warning')
        console_text.insert(tk.END, "[Detector Engine] Source: 192.168.1.150 -> Target Port: 443 | Generated ACK: 1001\n", 'success')
        console_text.insert(tk.END, "[*] FORGER MODULE ACTIVATED\n", 'forger')
        console_text.insert(tk.END, "[*] Assembling Layer 3 (IP Envelope)... Destination: 192.168.1.150\n", 'forger')
        console_text.insert(tk.END, "[*] Assembling Layer 4 (TCP Envelope) with SYN-ACK flags... Fake Port: 443\n", 'forger')
        console_text.insert(tk.END, "[+] INJECTION SUCCESSFUL. Scanner Deceived.\n\n", 'success')
        console_text.insert(tk.END, "[!] SCAN DETECTED: Host 10.0.0.52 is probing Port 80\n", 'warning')
        console_text.configure(state="disabled")

        # Module Architecture Sidebar Right Box
        arch_panel = tk.Frame(modules_frame, bg=BG_SURFACE, bd=1, relief="solid")
        arch_panel.grid(row=0, column=1, sticky="nsew", padx=(10, 0))

        arch_hdr = tk.Frame(arch_panel, bg=BG_SURFACE, padx=10, pady=8)
        arch_hdr.pack(fill="x")
        tk.Label(arch_hdr, text="⚙️ Module Architecture", font=("Arial", 10, "bold"), fg=NEON_MAGENTA, bg=BG_SURFACE).pack(side="left")

        # Sub-components List
        self.create_component_item(arch_panel, "sniffer.py", "Captures raw TCP packets", "RUNNING", NEON_CYAN)
        self.create_component_item(arch_panel, "detector.py", "Parses raw packet data", "STANDBY", NEON_YELLOW)
        self.create_component_item(arch_panel, "forger.py", "Assembles & injects packets", "INJECTING", NEON_MAGENTA)

    def create_metric_card(self, parent, col, title, value, color):
        card = tk.Frame(parent, bg=BG_SURFACE, bd=1, relief="solid", highlightthickness=1, highlightbackground=color)
        card.grid(row=0, column=col, sticky="nsew", padx=8, pady=5)
        
        lbl_title = tk.Label(card, text=title.upper(), font=("Arial", 8, "bold"), fg=TEXT_MUTED, bg=BG_SURFACE)
        lbl_title.pack(anchor="w", padx=12, pady=(10, 2))
        
        lbl_val = tk.Label(card, text=value, font=("Courier New", 18, "bold"), fg=color, bg=BG_SURFACE)
        lbl_val.pack(anchor="w", padx=12, pady=(0, 10))

    def create_component_item(self, parent, filename, desc, status, accent_color):
        item_frame = tk.Frame(parent, bg=BG_MAIN, bd=1, relief="flat", highlightthickness=1, highlightbackground="rgba(255,255,255,0.05)")
        item_frame.pack(fill="x", padx=12, pady=8, ipady=4)

        text_container = tk.Frame(item_frame, bg=BG_MAIN)
        text_container.pack(side="left", padx=8)
        
        tk.Label(text_container, text=filename, font=("Courier New", 9, "bold"), fg=TEXT_PRIMARY, bg=BG_MAIN).pack(anchor="w")
        tk.Label(text_container, text=desc, font=("Arial", 7), fg=TEXT_MUTED, bg=BG_MAIN).pack(anchor="w")

        badge = tk.Label(item_frame, text=status, font=("Arial", 7, "bold"), fg=accent_color, bg=BG_SURFACE, bd=1, relief="solid", padx=4)
        badge.pack(side="right", padx=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = ScapyShieldApp(root)
    root.mainloop()
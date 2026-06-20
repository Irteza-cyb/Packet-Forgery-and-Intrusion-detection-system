import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
import time

# Import teammate panels
from rules_panel import DetectionRulesPanel
from analytics_panel import AnalyticsPanel

# Import teammate backend engines & execution entry point
from sniffer import start_sniffer   

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

        # Track navigation elements and state
        self.nav_buttons = {}
        self.current_view = "console"
        
        # Build layout architecture
        self.setup_layout()

        # --- START BACKGROUND LIVE SNIFFER WORKER ---
        self.start_monitoring()

    def setup_layout(self):
        # 1. SIDEBAR NAVIGATION PANELS
        sidebar = tk.Frame(self.root, bg=BG_SURFACE, width=240, padx=15, pady=20)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        # Logo Area
        logo_label = tk.Label(sidebar, text="🛡️ SCAPYSHIELD", font=("Courier New", 14, "bold"), fg=NEON_CYAN, bg=BG_SURFACE)
        logo_label.pack(anchor="w", pady=(0, 25))

        # Nav Links Mapping to Panel Methods
        nav_items = [
            ("📺 Console", "console"), 
            ("🧠 Detector Rules", "rules"), 
            ("📊 Analytics", "analytics")
        ]
        
        for item_text, target_view in nav_items:
            is_initial_active = (target_view == "console")
            fg_color = TEXT_PRIMARY if is_initial_active else TEXT_MUTED
            bg_color = BG_CONSOLE if is_initial_active else BG_SURFACE
            border_color = NEON_CYAN if is_initial_active else "#262626"
            
            # High-tactility solid outline button style instead of flat label
            btn = tk.Button(
                sidebar, 
                text=item_text, 
                font=("Courier New", 10, "bold"), 
                fg=fg_color, 
                bg=bg_color,
                activebackground=BG_CONSOLE,
                activeforeground=NEON_CYAN,
                bd=1, 
                relief="solid",
                highlightthickness=0,
                highlightbackground=border_color,
                anchor="w",
                padx=15,
                pady=4,
                cursor="hand2"
            )
            btn.pack(fill="x", pady=8, ipady=4)
            
            # Bind dynamic hover animation behavior
            btn.bind("<Enter>", lambda event, b=btn, v=target_view: self.on_nav_hover(b, v))
            btn.bind("<Leave>", lambda event, b=btn, v=target_view: self.on_nav_leave(b, v))
            btn.bind("<Button-1>", lambda event, view=target_view: self.switch_view(view))
            
            self.nav_buttons[target_view] = btn

        # System Status Footer
        status_frame = tk.Frame(sidebar, bg=BG_SURFACE)
        status_frame.pack(side="bottom", anchor="w", pady=10)
        self.status_dot = tk.Label(status_frame, text="●", fg=NEON_GREEN, bg=BG_SURFACE, font=("Arial", 12))
        self.status_dot.pack(side="left")
        self.status_txt = tk.Label(status_frame, text=" SYSTEM ACTIVE", fg=NEON_GREEN, bg=BG_SURFACE, font=("Courier New", 9, "bold"))
        self.status_txt.pack(side="left")

        # 2. MAIN CONTAINER ARCHITECTURE
        self.main_content = tk.Frame(self.root, bg=BG_MAIN, padx=20, pady=20)
        self.main_content.pack(side="right", fill="both", expand=True)

        # Header Ribbon
        header_frame = tk.Frame(self.main_content, bg=BG_MAIN)
        header_frame.pack(fill="x", pady=(0, 15))
        
        title_lbl = tk.Label(header_frame, text="SECURITY CONTROL CENTER", font=("Courier New", 12, "bold"), fg=TEXT_PRIMARY, bg=BG_MAIN)
        title_lbl.pack(side="left")
        
        iface_lbl = tk.Label(header_frame, text="IFACE: Default", font=("Courier New", 9, "bold"), fg=NEON_CYAN, bg=BG_MAIN, bd=1, relief="solid", padx=8, pady=2)
        iface_lbl.pack(side="right")

        # 3. METRICS UPPER DISPLAY ROW (Glowing Borders)
        metrics_frame = tk.Frame(self.main_content, bg=BG_MAIN)
        metrics_frame.pack(fill="x", pady=(0, 20))
        metrics_frame.grid_columnconfigure((0, 1, 2), weight=1, uniform="equal")

        self.create_metric_card(metrics_frame, 0, "Packets Sniffed", "142,839", NEON_CYAN)
        self.create_metric_card(metrics_frame, 1, "SYN Scans Detected", "42", NEON_YELLOW)
        self.create_metric_card(metrics_frame, 2, "Spoofed Responses", "42", NEON_MAGENTA)

        # 4. VIEWPORT CONTEXT FRAME (Dynamic Display Area)
        self.viewport_frame = tk.Frame(self.main_content, bg=BG_MAIN)
        self.viewport_frame.pack(fill="both", expand=True)

        # Default View initialization
        self.load_console_panel()

    def on_nav_hover(self, btn, view_name):
        """Highlights the navbar item under the mouse cursor"""
        if self.current_view != view_name:
            btn.config(fg=NEON_CYAN, bg=BG_CONSOLE)

    def on_nav_leave(self, btn, view_name):
        """Reverts styling when the mouse leaves the navigation element"""
        if self.current_view != view_name:
            btn.config(fg=TEXT_MUTED, bg=BG_SURFACE)

    def clear_viewport(self):
        """Wipes the dynamic content window before switching views"""
        for widget in self.viewport_frame.winfo_children():
            widget.destroy()

    def switch_view(self, view_name):
        """Handles changing button layouts and swapping panel views"""
        self.current_view = view_name
        
        # Update styling profiles for active vs inactive tabs
        for name, btn in self.nav_buttons.items():
            if name == view_name:
                btn.config(fg=TEXT_PRIMARY, bg=BG_CONSOLE, highlightbackground=NEON_CYAN)
            else:
                btn.config(fg=TEXT_MUTED, bg=BG_SURFACE, highlightbackground="#262626")

        self.clear_viewport()
        
        if view_name == "console":
            self.load_console_panel()
        elif view_name == "rules":
            self.current_panel = DetectionRulesPanel(self.viewport_frame)
            self.current_panel.pack(fill="both", expand=True)
        elif view_name == "analytics":
            self.current_panel = AnalyticsPanel(self.viewport_frame)

    def load_console_panel(self):
        """Builds your default main live console view layout"""
        self.viewport_frame.grid_columnconfigure(0, weight=2)
        self.viewport_frame.grid_columnconfigure(1, weight=1)
        self.viewport_frame.grid_rowconfigure(0, weight=1)

        # Live Terminal Panel Console Frame
        console_panel = tk.Frame(self.viewport_frame, bg=BG_SURFACE, bd=1, relief="solid", highlightbackground=TEXT_MUTED)
        console_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        console_hdr = tk.Frame(console_panel, bg=BG_SURFACE, padx=10, pady=8)
        console_hdr.pack(fill="x")
        tk.Label(console_hdr, text="💻 Live Sniffer Console", font=("Courier New", 10, "bold"), fg=NEON_CYAN, bg=BG_SURFACE).pack(side="left")
        self.sniff_status_lbl = tk.Label(console_hdr, text="● Sniffing...", font=("Courier New", 9, "bold"), fg=NEON_GREEN, bg=BG_SURFACE)
        self.sniff_status_lbl.pack(side="right")

        self.console_text = scrolledtext.ScrolledText(
            console_panel, 
            bg=BG_CONSOLE, 
            fg=TEXT_MUTED, 
            insertbackground=NEON_CYAN, 
            selectbackground=BG_SURFACE,
            selectforeground=TEXT_PRIMARY,
            font=("Courier New", 10), 
            bd=0, 
            padx=10, 
            pady=10
        )
        self.console_text.pack(fill="both", expand=True)
        
        # Color logging definitions
        self.console_text.tag_config('warning', foreground=NEON_YELLOW)
        self.console_text.tag_config('success', foreground=NEON_GREEN)
        self.console_text.tag_config('forger', foreground=NEON_CYAN)
        self.console_text.tag_config('error', foreground=NEON_MAGENTA)

        self.console_text.configure(state="normal")
        self.console_text.insert(tk.END, "[*] GUI Console Thread Attached Successfully.\n")
        self.console_text.configure(state="disabled")

        # Module Architecture Sidebar Box
        arch_panel = tk.Frame(self.viewport_frame, bg=BG_SURFACE, bd=1, relief="solid")
        arch_panel.grid(row=0, column=1, sticky="nsew", padx=(10, 0))

        arch_hdr = tk.Frame(arch_panel, bg=BG_SURFACE, padx=10, pady=8)
        arch_hdr.pack(fill="x")
        tk.Label(arch_hdr, text="⚙️ Module Architecture", font=("Courier New", 10, "bold"), fg=NEON_MAGENTA, bg=BG_SURFACE).pack(side="left")

        # Status displays
        self.create_component_item(arch_panel, "sniffer.py", "Captures raw TCP packets", "RUNNING", NEON_CYAN)
        self.create_component_item(arch_panel, "detector.py", "Parses raw packet data", "ACTIVE", NEON_YELLOW)
        self.create_component_item(arch_panel, "forger.py", "Assembles & injects packets", "STANDBY", NEON_MAGENTA)

    # --- MULTI-THREADING BACKGROUND ENGINE ---
    def start_monitoring(self):
        """Spins up the network engine capture loop on an unblocked background thread"""
        sniffer_worker = threading.Thread(target=self.run_sniffer_loop, daemon=True)
        sniffer_worker.start()

    def run_sniffer_loop(self):
        """Launches your teammate's actual scapy sniffer loop using our safe UI logging channel"""
        try:
            start_sniffer(interface_name=None, ui_callback=self.log_packet_safe)
        except Exception as e:
            self.log_packet_safe(f"[-] Critical Sniffer Thread Error: {str(e)}", tag="warning")

    def log_packet_safe(self, message, tag=None):
        """Thread-safe interface function to drop strings directly into console window"""
        if hasattr(self, 'console_text') and self.console_text.winfo_exists():
            self.console_text.config(state="normal")
            if tag:
                self.console_text.insert(tk.END, f"{message}\n", tag)
            else:
                self.console_text.insert(tk.END, f"{message}\n")
            self.console_text.see(tk.END)
            self.console_text.config(state="disabled")

    # --- HELPER UI COMPONENT GENERATORS ---
    def create_metric_card(self, parent, col, title, value, color):
        # Increased highlightthickness to create a premium glowing neon border effect
        card = tk.Frame(parent, bg=BG_SURFACE, bd=0, highlightthickness=2, highlightbackground=color)
        card.grid(row=0, column=col, sticky="nsew", padx=12, pady=8)
        
        lbl_title = tk.Label(card, text=title.upper(), font=("Courier New", 8, "bold"), fg=TEXT_MUTED, bg=BG_SURFACE)
        lbl_title.pack(anchor="w", padx=15, pady=(12, 2))
        
        lbl_val = tk.Label(card, text=value, font=("Courier New", 20, "bold"), fg=color, bg=BG_SURFACE)
        lbl_val.pack(anchor="w", padx=15, pady=(0, 12))

    def create_component_item(self, parent, filename, desc, status, accent_color):
        item_frame = tk.Frame(parent, bg=BG_MAIN, bd=1, relief="flat", highlightthickness=1, highlightbackground="#262626")
        item_frame.pack(fill="x", padx=12, pady=8, ipady=4)

        text_container = tk.Frame(item_frame, bg=BG_MAIN)
        text_container.pack(side="left", padx=8)
        
        tk.Label(text_container, text=filename, font=("Courier New", 9, "bold"), fg=TEXT_PRIMARY, bg=BG_MAIN).pack(anchor="w")
        tk.Label(text_container, text=desc, font=("Courier New", 7), fg=TEXT_MUTED, bg=BG_MAIN).pack(anchor="w")

        badge = tk.Label(item_frame, text=status, font=("Courier New", 7, "bold"), fg=accent_color, bg=BG_SURFACE, bd=1, relief="solid", padx=4)
        badge.pack(side="right", padx=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = ScapyShieldApp(root)
    root.mainloop()
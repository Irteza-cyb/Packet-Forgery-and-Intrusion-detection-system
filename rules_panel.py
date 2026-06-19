# rules_panel.py
import tkinter as tk
import config

class DetectionRulesPanel(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#0d0d13", bd=0, relief="flat")
        
        # Header Text
        header = tk.Label(
            self, text="🛡️ INTRUSION DETECTION HEURISTICS", 
            fg="#00FFFF", bg="#0d0d13", 
            font=("Courier New", 14, "bold")
        )
        header.pack(anchor="w", padx=20, pady=20)
        
        # Rule Mock Container
        self.create_rule_card("RULE_01: TCP SYN FLOOD", "Triggers mitigation when exceeding 50 SYN packets/sec from a single source.", "ACTIVE")
        self.create_rule_card("RULE_02: STEALTH PORT SCAN", "Monitors horizontal probing sequences across sequential destination ports.", "ACTIVE")
        self.create_rule_card("RULE_03: BANNING THRESHOLD", "Automated IP dropping via OS firewall wrappers after 3 malicious events.", "STANDBY")

    def create_rule_card(self, title, desc, status):
        card = tk.Frame(self, bg="#121217", highlightthickness=1, highlightbackground="#262626")
        card.pack(fill="x", padx=20, pady=10)
        
        lbl_title = tk.Label(card, text=title, fg="#FFFFFF", bg="#121217", font=("Courier New", 11, "bold"))
        lbl_title.pack(anchor="w", padx=15, pady=(10, 2))
        
        lbl_desc = tk.Label(card, text=desc, fg="#888888", bg="#121217", font=("Courier New", 9), wraplength=500, justify="left")
        lbl_desc.pack(anchor="w", padx=15, pady=(0, 10))
        
        status_color = "#00FF00" if status == "ACTIVE" else "#FF00FF"
        lbl_status = tk.Label(card, text=status, fg=status_color, bg="#121217", font=("Courier New", 9, "bold"))
        lbl_status.place(relx=0.95, rely=0.5, anchor="e")
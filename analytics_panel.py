import tkinter as tk

class AnalyticsPanel:
    def __init__(self, parent_frame):
        # Create a placeholder layout so the app doesn't crash
        self.frame = tk.Frame(parent_frame, bg="#0a0b10")
        self.frame.pack(fill="both", expand=True)
        
        lbl = tk.Label(
            self.frame, 
            text="📊 Analytics Panel Placeholder\n(Waiting for teammate's final code UI)", 
            font=("Arial", 12, "bold"), 
            fg="#6272a4", 
            bg="#0a0b10"
        )
        lbl.pack(expand=True)
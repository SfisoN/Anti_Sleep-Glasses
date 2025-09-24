from pathlib import Path
import tkinter as tk
from tkinter import Canvas, Scrollbar, Frame
from datetime import datetime

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = Path(__file__).parent.parent / "Assets/Alerts"

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

class Alerts(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#D0DFFF")
        self.controller = controller
        
        # Live alerts data - starts empty
        self.live_alerts_data = []
        
        # Sample alert data for initial display
        self.sample_alerts_data = [
            {
                "title": "Drowsiness Alert #001",
                "username": "John Doe", 
                "condition": "Eyes closed for 3+ seconds",
                "action": "Audio alarm triggered",
                "response": "User acknowledged",
                "date": "2025-01-15 14:52",
                "status": "resolved"
            },
            {
                "title": "Drowsiness Alert #002",
                "username": "John Doe",
                "condition": "Head nodding detected", 
                "action": "Vibration alert sent",
                "response": "No response",
                "date": "2025-01-15 14:30",
                "status": "active"
            },
            {
                "title": "Blink Rate Alert #003",
                "username": "John Doe",
                "condition": "Low blink rate: 5/min",
                "action": "Warning notification",
                "response": "User took break",
                "date": "2025-01-15 14:12",
                "status": "resolved"
            }
        ]
        
        # Combine live and sample data
        self.all_alerts_data = self.live_alerts_data + self.sample_alerts_data
        
        # Setup UI canvas
        self.setup_canvas()
        
        # Start live updates
        self.start_live_updates()
        
    def setup_canvas(self):
        """Create scrollable canvas for alerts display"""
        self.canvas = Canvas(self, bg="#D0DFFF", highlightthickness=0)
        self.scrollbar = Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scroll_frame = Frame(self.canvas, bg="#D0DFFF")
        
        self.scroll_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )
        
        self.canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
    
    def start_live_updates(self):
        """Check for new alerts every 1 second"""
        self.refresh_alerts_display()
        self.after(1000, self.start_live_updates)
        
    def add_live_alert(self, alert_data):
        """Add a new live alert from the sensor monitor"""
        # Add timestamp and status
        alert_data["status"] = "new"
        alert_data["date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Add to beginning of live alerts
        self.live_alerts_data.insert(0, alert_data)
        
        # Keep only last 50 alerts
        if len(self.live_alerts_data) > 50:
            self.live_alerts_data = self.live_alerts_data[:50]
        
        # Update combined data
        self.all_alerts_data = self.live_alerts_data + self.sample_alerts_data
        
        print(f"New alert added: {alert_data['title']} at {alert_data['date']}")
    
    def refresh_alerts_display(self):
        """Clear and re-render alerts list"""
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
        
        for i, alert in enumerate(self.all_alerts_data):
            bg_color = "#ffffff" if i % 2 == 0 else "#f2f2f2"
            
            card = tk.Frame(self.scroll_frame, bg=bg_color, bd=1, relief="solid")
            card.pack(fill="x", padx=5, pady=2)
            
            title = tk.Label(card, text=alert["title"], font=("Arial", 12, "bold"), bg=bg_color)
            title.pack(anchor="w", padx=5, pady=2)
            
            details = (
                f"User: {alert['username']} | Condition: {alert['condition']} | "
                f"Action: {alert['action']} | Response: {alert['response']} | "
                f"Date: {alert['date']} | Status: {alert['status']}"
            )
            body = tk.Label(card, text=details, font=("Arial", 10), bg=bg_color, wraplength=600, justify="left")
            body.pack(anchor="w", padx=5, pady=2)

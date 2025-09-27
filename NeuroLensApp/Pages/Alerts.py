# Pages/Alerts.py - Fixed Version
from pathlib import Path
import tkinter as tk
from tkinter import Canvas, Entry, Button, PhotoImage, messagebox, filedialog
import csv
from datetime import datetime

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH.parent / "assets/alerts"

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

class Alerts(tk.Frame):  
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#3A404D")
        self.controller = controller

        
        # Alerts data
        self.alerts_data = []
        self.live_alerts = []
        
        self.setup_ui()
        self.load_sample_alerts()
    
    def setup_ui(self):
        self.canvas = Canvas(
            self,
            bg="#3A404D",
            height=618,
            width=1072,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)
        
        self.load_static_elements()
        self.add_static_text()  # FIXED: Added missing text elements
        self.setup_interactive_elements()
        self.setup_transparent_navigation()  # FIXED: Added navigation buttons
        self.display_alerts()
    
    def load_static_elements(self):
        """Load static UI elements with wider images"""
        image_files = [
            ("image_1.png", 102.0, 351.0),   # Sidebar
            ("image_2.png", 27.0, 173.0),    # Nav icon
            ("image_3.png", 29.0, 101.0),    # Nav icon
            ("image_4.png", 27.0, 136.0),    # Nav icon
            ("image_5.png", 28.0, 216.0),    # Nav icon

            ("image_6.png", 475.0, 188.0),   # Alert background
            ("image_7.png", 475.0, 419.0),   # Alert background
            ("image_8.png", 564.0, 28.0),    # Top bar
            ("image_9.png", 898.0, 28.0),    # Top bar
            ("image_10.png", 928.0, 28.0),   # Top bar
            ("image_11.png", 959.0, 28.0),   # Top bar
            ("image_12.png", 27.0, 22.0)     # Logo
        ]
        
        for filename, x, y in image_files:
            try:
                img = PhotoImage(file=relative_to_assets(filename))
                setattr(self, filename.replace('.png', ''), img)
                self.canvas.create_image(x, y, image=img)
            except:
                # Create fallback rectangles for alert backgrounds (wider)
                if filename == "image_6.png":
                    self.canvas.create_rectangle(400, 120, 700, 260, fill="#2D2D2D", outline="#444444", width=2)
                elif filename == "image_7.png":
                    self.canvas.create_rectangle(400, 350, 700, 490, fill="#2D2D2D", outline="#444444", width=2)
    
    def add_static_text(self):
        """FIXED: Add all missing static text elements"""
        # App title - Like other pages
        self.canvas.create_text(54.0, 8.0, anchor="nw", text="NeuroLens",
                               fill="#FFFFFF", font=("Arial", 18, "bold"))
        
        # Navigation with proper highlighting
        nav_items = [
            ("DashBoard", 91, False),
            ("Alerts", 127, True),   # ACTIVE page
            ("Help/Info", 167, False),
            ("Log Out", 207, False)
        ]
        
        for text, y, is_active in nav_items:
            color = "#4277FF" if is_active else "#FFFFFF"
            weight = "bold" if is_active else "normal"
            self.canvas.create_text(57.0, y, anchor="nw", text=text,
                                   fill=color, font=("Arial", 12, weight))
        
        # FIXED: Added breadcrumb like other pages
        self.canvas.create_text(294.0, 24.0, anchor="nw", text="Alerts  /    Alert History",
                               fill="#FFFFFF", font=("Arial", 11))
    
    def setup_transparent_navigation(self):
        """FIXED: Create transparent navigation buttons"""
        nav_areas = [
            (30, 83, 170, 103),   # Dashboard
            (30, 119, 170, 139),  # Alerts (current, no button)
            (30, 159, 170, 179),  # Help/Info
            (30, 199, 170, 219)   # Log Out
        ]
        
        nav_commands = [
            lambda: self.controller.show_page('Dashboard'),
            None,  # Current page
            lambda: self.controller.show_page('Help'),
            self.controller.logout
        ]
        
        for i, (x1, y1, x2, y2) in enumerate(nav_areas):
            if nav_commands[i] is not None:
                btn = tk.Button(
                    self,
                    text="",
                   bg=self["bg"],  # Use frame background color
            activebackground=self["bg"],  # Use frame background color
                    bd=0,
                    highlightthickness=0,
                    cursor="hand2",
                    command=nav_commands[i]
                )
                btn.place(x=x1, y=y1, width=x2-x1, height=y2-y1)
    
    def setup_interactive_elements(self):
        """Setup interactive elements with smaller fonts"""
        # Search entry - smaller font
        self.search_entry = Entry(
            self, 
            bd=1,
            bg="#2D2D2D", 
            fg="#999999", 
            insertbackground="#FFFFFF",
            highlightthickness=1,
            relief="flat",
            font=("Arial", 11)  # FIXED: Smaller font
        )
        self.search_entry.place(x=590.0, y=13.0, width=266.0, height=28.0)
        self.search_entry.insert(0, "Search alerts...")
        
        self.search_entry.bind("<FocusIn>", self.on_entry_focus_in)
        self.search_entry.bind("<FocusOut>", self.on_entry_focus_out)
        self.search_entry.bind("<KeyRelease>", self.on_search)
        
        # Export button - blue theme, smaller font
        self.export_btn = Button(
            self,
            text="Export CSV",
            fg="#FFFFFF",
            bg="#4277FF",
            font=("Arial", 11, "bold"),  # FIXED: Smaller font
            command=self.export_data,
            relief="flat",
            bd=0,
            cursor="hand2",
            padx=10,
            pady=4
        )
        self.export_btn.place(x=250.0, y=550.0, width=100, height=30)
        
        
    
    def load_sample_alerts(self):
        """Load sample alerts data"""
        self.alerts_data = [
            {
                "title": "Drowsiness Alert #001",
                "username": "John Doe", 
                "condition": "Eyes closed for 3+ seconds",
                "action": "Audio alarm triggered",
                "response": "User acknowledged",
                "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "live": False
            },
            {
                "title": "Drowsiness Alert #002", 
                "username": "John Doe",
                "condition": "Head nodding detected", 
                "action": "Vibration alert sent",
                "response": "No response", 
                "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "live": False
            }
        ]
    
    def add_live_alert(self, alert_data):
        """Add a live alert from dashboard"""
        alert_data["live"] = True
        self.live_alerts.insert(0, alert_data)
        self.alerts_data = self.live_alerts + self.alerts_data[:2]  # Keep 2 sample + live alerts
        
        if len(self.alerts_data) > 4:
            self.alerts_data = self.alerts_data[:4]
        
        self.refresh_display()
    

    
    def display_alerts(self):
        """Display alerts with smaller fonts"""
        alert_positions = [
            (248.0, 122.0),  # FIXED: Adjusted positions for wider layout
            (248.0, 352.0)   
        ]
        
        for i, alert in enumerate(self.alerts_data[:2]):
            if i >= len(alert_positions):
                break
                
            x_base, y_base = alert_positions[i]
            
            # Alert title - smaller font, mark live alerts
            title = alert["title"]
            if alert.get("live", False):
                title = "🔴 " + title
            
            self.canvas.create_text(
                x_base, y_base, anchor="nw", text=title,
                fill="#FF6B6B" if alert.get("live", False) else "#FFFFFF", 
                font=("Arial", 13, "bold"), tags="alerts"  # FIXED: Smaller font
            )
            
            # Alert details - smaller fonts
            details = [
                f"User: {alert['username']}",
                f"Condition: {alert['condition']}", 
                f"Action: {alert['action']}",
                f"Response: {alert['response']}"
            ]
            
            y_offset = y_base + 25
            for detail in details:
                self.canvas.create_text(
                    x_base, y_offset, anchor="nw", text=detail,
                    fill="#FFFFFF", font=("Arial", 10), tags="alerts"  # FIXED: Smaller font
                )
                y_offset += 18  # FIXED: Reduced spacing
            
            # Date - smaller font
            self.canvas.create_text(
                x_base + 380,  # FIXED: Adjusted for wider layout
                y_base + 3, anchor="nw", text=alert['date'],
                fill="#C4C4C4", font=("Arial", 9), tags="alerts"  # FIXED: Smaller font
            )
    
    def refresh_display(self):
        """Refresh the alerts display"""
        self.canvas.delete("alerts")
        self.display_alerts()
    
    def on_entry_focus_in(self, event):
        if self.search_entry.get() == "Search alerts...":
            self.search_entry.delete(0, tk.END)
            self.search_entry.config(fg="#FFFFFF", bg="#3A404D")
    
    def on_entry_focus_out(self, event):
        if not self.search_entry.get():
            self.search_entry.insert(0, "Search alerts...")
            self.search_entry.config(fg="#999999", bg="#2D2D2D")
    
    def on_search(self, event):
        search_term = self.search_entry.get().lower()
        if search_term and search_term != "search alerts...":
            filtered_alerts = [
                alert for alert in self.alerts_data 
                if search_term in alert["title"].lower() or 
                   search_term in alert["condition"].lower() or
                   search_term in alert["username"].lower()
            ]
            print(f"Found {len(filtered_alerts)} alerts matching '{search_term}'")
    
    def export_data(self):
        """Export alerts data to CSV"""
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                title="Save Alerts Data"
            )
            
            if filename:
                with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                    fieldnames = ['Title', 'Username', 'Condition', 'Action', 'User Response', 'Date', 'Type']
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    
                    writer.writeheader()
                    for alert in self.alerts_data:
                        writer.writerow({
                            'Title': alert['title'],
                            'Username': alert['username'],
                            'Condition': alert['condition'], 
                            'Action': alert['action'],
                            'User Response': alert['response'],
                            'Date': alert['date'],
                            'Type': 'LIVE' if alert.get('live', False) else 'HISTORICAL'
                        })
                
                messagebox.showinfo("Export Successful", 
                                   f"Alerts data exported to:\n{filename}\n"
                                   f"Total alerts: {len(self.alerts_data)}")
                
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export data:\n{str(e)}")
    
    def on_page_show(self):
        """Called when page is shown"""
        self.refresh_display()
        print("Alerts page shown")
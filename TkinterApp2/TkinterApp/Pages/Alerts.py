from pathlib import Path
import tkinter as tk
from tkinter import Canvas, Entry, PhotoImage, Button, messagebox, filedialog, Scrollbar, Frame
import csv
from datetime import datetime

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = Path(__file__).parent.parent / "Assets/Alerts"

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

class Alerts(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#D0DFFF")
        self.controller = controller
        
        # Live alerts data - starts empty, gets populated by sensor monitor
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
        
        self.setup_canvas()
        
        # Start live updates
        self.start_live_updates()
        
    def start_live_updates(self):
        """Check for new alerts every 1 second"""
        self.refresh_alerts_display()
        self.after(1000, self.start_live_updates)
        
    def add_live_alert(self, alert_data):
        """Add a new live alert from the sensor monitor"""
        # Add timestamp and status
        alert_data["status"] = "new"
        alert_data["timestamp"] = datetime.now()
        
        # Add to beginning of live alerts
        self.live_alerts_data.insert(0, alert_data)
        
        # Keep only last 50 alerts to prevent memory issues
        if len(self.live_alerts_data) > 50:
            self.live_alerts_data = self.live_alerts_data[:50]
        
        # Update combined data
        self.all_alerts_data = self.live_alerts_data + self.sample_alerts_data
        
        print(f"New live alert added: {alert_data['title']}")
        
        # Refresh the display immediately
        self.refresh_alerts_display()
    
    def refresh_alerts_display(self):
        """Refresh the alerts display with current data"""
        # Clear existing alert displays
        if hasattr(self, 'alerts_canvas'):
            self.alerts_canvas.delete("alert_content")
        
        # Redraw alerts
        self.display_alerts()
    
    def setup_canvas(self):
        canvas = Canvas(
            self,
            bg="#D0DFFF",
            height=747,
            width=1200,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        canvas.place(x=0, y=0)
        
        self.alerts_canvas = canvas
        
        self.load_images(canvas)
        self.add_text_elements(canvas)
        self.add_entry_field(canvas)
        self.add_export_button(canvas)
        self.create_scrollable_alerts_area()
        
    def create_scrollable_alerts_area(self):
        """Create a scrollable area for alerts"""
        # Main alerts frame
        self.alerts_frame = Frame(self, bg="#FFFFFF", relief="ridge", bd=1)
        self.alerts_frame.place(x=250, y=100, width=750, height=450)
        
        # Scrollable canvas inside the frame
        self.scroll_canvas = Canvas(self.alerts_frame, bg="#FFFFFF", highlightthickness=0)
        self.scrollbar = Scrollbar(self.alerts_frame, orient="vertical", command=self.scroll_canvas.yview)
        self.scrollable_frame = Frame(self.scroll_canvas, bg="#FFFFFF")
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.scroll_canvas.configure(scrollregion=self.scroll_canvas.bbox("all"))
        )
        
        self.scroll_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.scroll_canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.scroll_canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
    def display_alerts(self):
        """Display alerts in scrollable format"""
        # Clear existing content
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        # Header
        header_frame = Frame(self.scrollable_frame, bg="#1657FF", height=40)
        header_frame.pack(fill="x", padx=5, pady=5)
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text="LIVE ALERTS MONITOR", 
                font=("Arial", 14, "bold"), bg="#1657FF", fg="white").pack(pady=10)
        
        # Display all alerts (live first, then samples)
        for i, alert in enumerate(self.all_alerts_data):
            alert_frame = Frame(self.scrollable_frame, bg="#F8F9FA", relief="ridge", bd=1)
            alert_frame.pack(fill="x", padx=5, pady=3)
            
            # Alert status indicator
            status_color = "#FF0000" if alert.get("status") == "new" else "#FFA500" if alert.get("status") == "active" else "#00AA00"
            status_text = "🔴 NEW" if alert.get("status") == "new" else "🟡 ACTIVE" if alert.get("status") == "active" else "🟢 RESOLVED"
            
            # Status and timestamp
            header_info = Frame(alert_frame, bg="#F8F9FA")
            header_info.pack(fill="x", padx=10, pady=5)
            
            tk.Label(header_info, text=status_text, font=("Arial", 10, "bold"), 
                    fg=status_color, bg="#F8F9FA").pack(side="left")
            
            tk.Label(header_info, text=f"Date: {alert['date']}", 
                    font=("Arial", 9), fg="#666666", bg="#F8F9FA").pack(side="right")
            
            # Alert title
            tk.Label(alert_frame, text=alert["title"], 
                    font=("Arial", 16, "bold"), fg="#000000", bg="#F8F9FA", 
                    anchor="w").pack(fill="x", padx=10, pady=2)
            
            # Alert details in a structured format
            details_frame = Frame(alert_frame, bg="#F8F9FA")
            details_frame.pack(fill="x", padx=10, pady=5)
            
            details = [
                f"👤 User: {alert['username']}",
                f"⚠️ Condition: {alert['condition']}", 
                f"🔔 Action Taken: {alert['action']}",
                f"💬 User Response: {alert['response']}"
            ]
            
            for j, detail in enumerate(details):
                detail_label = tk.Label(details_frame, text=detail, font=("Arial", 11), 
                                       fg="#333333", bg="#F8F9FA", anchor="w")
                detail_label.pack(fill="x", pady=2)
            
            # Add live indicator for new alerts
            if alert.get("status") == "new":
                live_frame = Frame(alert_frame, bg="#FFE6E6")
                live_frame.pack(fill="x", padx=10, pady=5)
                tk.Label(live_frame, text="🚨 LIVE ALERT - Just occurred", 
                        font=("Arial", 10, "bold"), fg="#FF0000", bg="#FFE6E6").pack(pady=3)
            
            # Separator
            separator = Frame(alert_frame, height=2, bg="#E0E0E0")
            separator.pack(fill="x", padx=10, pady=5)
        
        # Update scroll region
        self.scroll_canvas.update_idletasks()
        self.scroll_canvas.configure(scrollregion=self.scroll_canvas.bbox("all"))
        
        # Show count
        total_alerts = len(self.all_alerts_data)
        live_alerts = len([a for a in self.all_alerts_data if a.get("status") == "new"])
        
        count_frame = Frame(self.scrollable_frame, bg="#E8F4FD", height=30)
        count_frame.pack(fill="x", padx=5, pady=5)
        count_frame.pack_propagate(False)
        
        tk.Label(count_frame, text=f"Total Alerts: {total_alerts} | Live Alerts: {live_alerts}", 
                font=("Arial", 10), bg="#E8F4FD", fg="#1657FF").pack(pady=5)
        
    def load_images(self, canvas):
        """Load all images with error handling"""
        try:
            image_positions = {
                1: (617.0, 361.0), 2: (617.0, 185.0), 3: (617.0, 362.0),
                4: (617.0, 539.0), 5: (98.0, 373.0), 6: (29.0, 213.0),
                7: (29.0, 101.0), 8: (28.0, 23.0), 9: (28.0, 157.0),
                10: (26.0, 456.0), 11: (722.0, 26.0), 12: (963.0, 27.0),
                13: (902.0, 27.0), 14: (930.0, 27.0), 15: (243.0, 33.0),
                16: (275.0, 33.0)
            }
            
            for i, (x, y) in image_positions.items():
                try:
                    img = PhotoImage(file=relative_to_assets(f"image_{i}.png"))
                    setattr(self, f"image_{i}", img)
                    canvas.create_image(x, y, image=img)
                except Exception as e:
                    print(f"Could not load image_{i}.png: {e}")
                    
        except Exception as e:
            print(f"Error loading images: {e}")
    
    def add_text_elements(self, canvas):
        """Add all text elements with consistent fonts"""
        # App title - CONSISTENT ACROSS ALL PAGES
        canvas.create_text(54.0, 8.0, anchor="nw", text="NeuroLens", 
                          fill="#2C2745", font=("Arial", 18, "bold"))
        
        # Sidebar navigation - CONSISTENT
        nav_items = [
            ("DashBoard", 91), ("Alerts", 147), ("Help/Info", 205), ("Log Out", 450)
        ]
        for text, y in nav_items:
            canvas.create_text(53.0, y, anchor="nw", text=text, 
                              fill="#B9C0DE", font=("Arial", 12))
        
        # Page header - CONSISTENT
        canvas.create_text(294.0, 24.0, anchor="nw", text="Alerts  /  Live Monitor", 
                          fill="#1657FF", font=("Arial", 11))
        
        # Live status indicator
        canvas.create_text(250.0, 70.0, anchor="nw", text="🔴 LIVE MONITORING ACTIVE", 
                          fill="#FF0000", font=("Arial", 12, "bold"))
        
        canvas.create_text(450.0, 70.0, anchor="nw", text="Real-time alerts from NeuroLens glasses", 
                          fill="#666666", font=("Arial", 10))
    
    def add_entry_field(self, canvas):
        """Add search entry field"""
        try:
            self.entry_image_1 = PhotoImage(file=relative_to_assets("entry_1.png"))
            canvas.create_image(808.5, 26.0, image=self.entry_image_1)
            
            self.entry_1 = Entry(
                self, 
                bd=0, 
                bg="#FFFFFF", 
                fg="#000716", 
                highlightthickness=0,
                font=("Arial", 9)
            )
            self.entry_1.place(x=751.0, y=15.0, width=115.0, height=20.0)
            self.entry_1.insert(0, "Search alerts...")
            
            self.entry_1.bind("<FocusIn>", self.on_entry_focus_in)
            self.entry_1.bind("<FocusOut>", self.on_entry_focus_out)
            self.entry_1.bind("<KeyRelease>", self.on_search)
            
        except Exception as e:
            print(f"Error creating entry field: {e}")
    
    def on_entry_focus_in(self, event):
        if self.entry_1.get() == "Search alerts...":
            self.entry_1.delete(0, tk.END)
            self.entry_1.config(fg="#000716")
    
    def on_entry_focus_out(self, event):
        if not self.entry_1.get():
            self.entry_1.insert(0, "Search alerts...")
            self.entry_1.config(fg="#999999")
    
    def on_search(self, event):
        """Handle search functionality"""
        search_term = self.entry_1.get().lower()
        if search_term and search_term != "search alerts...":
            filtered_alerts = [
                alert for alert in self.all_alerts_data 
                if search_term in alert["title"].lower() or 
                   search_term in alert["condition"].lower() or
                   search_term in alert["username"].lower()
            ]
            print(f"Found {len(filtered_alerts)} alerts matching '{search_term}'")
    
    def add_export_button(self, canvas):
        """Add export data button with functionality"""
        try:
            self.button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
            
            button_1 = Button(
                self,
                image=self.button_image_1,
                borderwidth=0,
                highlightthickness=0,
                command=self.export_data,
                relief="flat",
                cursor="hand2"
            )
            button_1.place(x=1050.0, y=600.0, width=128.0, height=51.0)
            
            canvas.create_text(1114.0, 625.0, text="Export All", 
                              fill="#FFFFFF", font=("Arial", 12, "bold"))
                              
        except Exception as e:
            print(f"Error creating export button: {e}")
            button_1 = Button(
                self,
                text="Export All Data",
                command=self.export_data,
                bg="#1657FF",
                fg="white",
                font=("Arial", 12),
                cursor="hand2"
            )
            button_1.place(x=1050.0, y=600.0, width=128.0, height=51.0)
    
    def export_data(self):
        """Export all alerts data (live + sample) to CSV file"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = filedialog.asksaveasfilename(
                defaultextension=".csv",
                initialname=f"neurolens_alerts_{timestamp}.csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                title="Save Complete Alerts Data"
            )
            
            if filename:
                with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                    fieldnames = ['Title', 'Username', 'Condition', 'Action', 'User Response', 'Date', 'Status', 'Source']
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    
                    writer.writeheader()
                    
                    # Write live alerts
                    for alert in self.live_alerts_data:
                        writer.writerow({
                            'Title': alert['title'],
                            'Username': alert['username'],
                            'Condition': alert['condition'], 
                            'Action': alert['action'],
                            'User Response': alert['response'],
                            'Date': alert['date'],
                            'Status': alert.get('status', 'unknown'),
                            'Source': 'Live Sensor'
                        })
                    
                    # Write sample alerts
                    for alert in self.sample_alerts_data:
                        writer.writerow({
                            'Title': alert['title'],
                            'Username': alert['username'],
                            'Condition': alert['condition'], 
                            'Action': alert['action'],
                            'User Response': alert['response'],
                            'Date': alert['date'],
                            'Status': alert.get('status', 'sample'),
                            'Source': 'Sample Data'
                        })
                
                total_exported = len(self.all_alerts_data)
                live_exported = len(self.live_alerts_data)
                messagebox.showinfo("Export Successful", 
                                   f"Complete alerts database exported!\n"
                                   f"File: {filename}\n"
                                   f"Total alerts: {total_exported}\n"
                                   f"Live alerts: {live_exported}")
                
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export data:\n{str(e)}")
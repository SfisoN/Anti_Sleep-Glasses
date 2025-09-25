from pathlib import Path
import tkinter as tk
from tkinter import Canvas, Entry, PhotoImage, Button, messagebox, filedialog
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
        
        # Live alerts from sensors - start empty
        self.live_alerts_data = []
        
        # Keep the original sample alerts format you liked
        self.sample_alerts_data = [
            {
                "title": "Drowsiness Alert #001",
                "username": "John Doe", 
                "condition": "Eyes closed for 3+ seconds",
                "action": "Audio alarm triggered",
                "response": "User acknowledged",
                "date": "2025-01-15 14:52"
            },
            {
                "title": "Drowsiness Alert #002",
                "username": "John Doe",
                "condition": "Head nodding detected", 
                "action": "Vibration alert sent",
                "response": "No response",
                "date": "2025-01-15 14:30"
            },
            {
                "title": "Blink Rate Alert #003",
                "username": "John Doe",
                "condition": "Low blink rate: 5/min",
                "action": "Warning notification",
                "response": "User took break",
                "date": "2025-01-15 14:12"
            }
        ]
        
        # Combined alerts data
        self.all_alerts_data = self.live_alerts_data + self.sample_alerts_data
        
        self.setup_canvas()
        
        # Check for new alerts every 5 seconds
        self.start_live_updates()
        
    def start_live_updates(self):
        """Check for new alerts every 5 seconds"""
        self.after(5000, self.start_live_updates)
        
    def add_live_alert(self, alert_data):
        """Add a new live alert from the sensor monitor"""
        # Add to beginning of live alerts
        self.live_alerts_data.insert(0, alert_data)
        
        # Keep only last 20 alerts
        if len(self.live_alerts_data) > 20:
            self.live_alerts_data = self.live_alerts_data[:20]
        
        # Update combined data
        self.all_alerts_data = self.live_alerts_data + self.sample_alerts_data
        
        print(f"New live alert added: {alert_data['title']}")
        
        # Refresh the display
        self.refresh_display()
    
    def refresh_display(self):
        """Refresh the alerts display"""
        # Clear and redraw alert entries
        self.canvas.delete("alert_entries")
        self.display_alerts(self.canvas)
        
    def setup_canvas(self):
        self.canvas = Canvas(
            self,
            bg="#D0DFFF",
            height=747,
            width=1200,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)
        
        self.load_images(self.canvas)
        self.add_text_elements(self.canvas)
        self.add_entry_field(self.canvas)
        self.add_export_button(self.canvas)
        
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
        canvas.create_text(294.0, 24.0, anchor="nw", text="Alerts", 
                          fill="#1657FF", font=("Arial", 11))
        
        # Alert entries - same format you liked
        self.display_alerts(canvas)
    
    def display_alerts(self, canvas):
        """Display alert information in the same format you liked"""
        y_positions = [111, 286, 467]
        
        # Show live alerts first, then sample alerts
        alerts_to_show = self.all_alerts_data[:3]  # Show first 3 alerts
        
        for i, alert in enumerate(alerts_to_show):
            if i >= 3:  # Only show 3 alerts max
                break
                
            y_base = y_positions[i]
            
            # Alert title - add "LIVE" indicator for live alerts
            title_text = alert["title"]
            if alert in self.live_alerts_data:
                title_text = f"🔴 LIVE - {alert['title']}"
            
            canvas.create_text(314.0, y_base, anchor="nw", text=title_text, 
                              fill="#FF0000" if alert in self.live_alerts_data else "#000000", 
                              font=("Arial", 16, "bold"), tags="alert_entries")
            
            # Alert details - same format as before
            details = [
                f"UserName: {alert['username']}",
                f"Condition: {alert['condition']}", 
                f"Action: {alert['action']}",
                f"User Response: {alert['response']}"
            ]
            
            for j, detail in enumerate(details):
                canvas.create_text(314.0, y_base + 32 + (j * 28), anchor="nw", text=detail,
                                  fill="#000000", font=("Arial", 12), tags="alert_entries")
            
            # Date - same position as before
            canvas.create_text(741.0, y_base + 3, anchor="nw", text=f"Date: {alert['date']}", 
                              fill="#C4C4C4", font=("Arial", 12), tags="alert_entries")
    
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
            button_1.place(x=265.0, y=659.0, width=128.0, height=51.0)
            
            canvas.create_text(329.0, 684.0, text="Export Data", 
                              fill="#000000", font=("Arial", 12))
                              
        except Exception as e:
            print(f"Error creating export button: {e}")
            button_1 = Button(
                self,
                text="Export Data",
                command=self.export_data,
                bg="#4A90E2",
                fg="white",
                font=("Arial", 12),
                cursor="hand2"
            )
            button_1.place(x=265.0, y=659.0, width=128.0, height=51.0)
    
    def export_data(self):
        """Export alerts data to CSV file"""
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                title="Save Alerts Data"
            )
            
            if filename:
                with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                    fieldnames = ['Title', 'Username', 'Condition', 'Action', 'User Response', 'Date', 'Source']
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    
                    writer.writeheader()
                    
                    # Export all alerts (live + sample)
                    for alert in self.all_alerts_data:
                        source = "Live Sensor" if alert in self.live_alerts_data else "Sample Data"
                        writer.writerow({
                            'Title': alert['title'],
                            'Username': alert['username'],
                            'Condition': alert['condition'], 
                            'Action': alert['action'],
                            'User Response': alert['response'],
                            'Date': alert['date'],
                            'Source': source
                        })
                
                live_count = len(self.live_alerts_data)
                total_count = len(self.all_alerts_data)
                messagebox.showinfo("Export Successful", 
                                   f"Alerts data exported to:\n{filename}\n"
                                   f"Total alerts: {total_count}\n"
                                   f"Live alerts: {live_count}")
                
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export data:\n{str(e)}")
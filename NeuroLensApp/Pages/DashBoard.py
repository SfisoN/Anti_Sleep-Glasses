# Pages/DashBoard.py
from pathlib import Path
import tkinter as tk
from tkinter import Canvas, Entry, Button, PhotoImage
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random
from datetime import datetime, timedelta

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("../assets/dashboard")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

class Dashboard(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#3A404D")
        self.controller = controller
        
        # Initialize sensor data
        self.drowsiness_level = 3  # 1-5 scale
        self.battery_percentage = 78
        self.blink_count = 0
        self.device_connected = True
        self.session_start_time = datetime.now()
        self.status = "Active"
        self.alerts = []  # List to store dynamic alerts
        
        # Initialize sample alerts
        self.initialize_sample_alerts()
        
        self.setup_ui()
        self.start_live_updates()
    
    def initialize_sample_alerts(self):
        """Initialize with sample alerts"""
        current_time = datetime.now()
        self.alerts = [
            {"type": "Drowsiness", "time": current_time - timedelta(minutes=5), "message": "Drowsiness Detected"},
            {"type": "Connection", "time": current_time - timedelta(minutes=15), "message": "Device Reconnected"},
            {"type": "Battery", "time": current_time - timedelta(minutes=30), "message": "Battery Low"},
            {"type": "Drowsiness", "time": current_time - timedelta(minutes=45), "message": "Drowsiness Detected"}
        ]
    
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
        
        # Load static images FIRST
        self.load_static_elements()
        
        # Then add ALL static text elements
        self.add_all_static_text()
        
        # Setup navigation buttons
        self.setup_navigation()
        
        # Setup dynamic text elements
        self.setup_dynamic_elements()
        
        # Setup performance graph
        self.setup_performance_graph()
        
        # Setup alerts section
        self.setup_alerts_section()
    
    def load_static_elements(self):
        """Load all static UI elements"""
        try:
            # Sidebar background
            self.image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
            self.canvas.create_image(102.0, 351.0, image=self.image_1)
            
            # Navigation icons
            self.image_2 = PhotoImage(file=relative_to_assets("image_2.png"))
            self.canvas.create_image(27.0, 173.0, image=self.image_2)
            
            self.image_3 = PhotoImage(file=relative_to_assets("image_3.png"))
            self.canvas.create_image(29.0, 101.0, image=self.image_3)
            
            self.image_4 = PhotoImage(file=relative_to_assets("image_4.png"))
            self.canvas.create_image(27.0, 136.0, image=self.image_4)
            
            self.image_5 = PhotoImage(file=relative_to_assets("image_5.png"))
            self.canvas.create_image(28.0, 216.0, image=self.image_5)
            
            # Content background images
            self.image_6 = PhotoImage(file=relative_to_assets("image_6.png"))
            self.canvas.create_image(475.0, 188.0, image=self.image_6)
            
            self.image_7 = PhotoImage(file=relative_to_assets("image_7.png"))
            self.canvas.create_image(887.0, 349.0, image=self.image_7)
            
            self.image_8 = PhotoImage(file=relative_to_assets("image_8.png"))
            self.canvas.create_image(887.0, 183.0, image=self.image_8)
            
            self.image_9 = PhotoImage(file=relative_to_assets("image_9.png"))
            self.canvas.create_image(886.0, 505.0, image=self.image_9)
            
            self.image_10 = PhotoImage(file=relative_to_assets("image_10.png"))
            self.canvas.create_image(474.0, 505.0, image=self.image_10)
            
            self.image_11 = PhotoImage(file=relative_to_assets("image_11.png"))
            self.canvas.create_image(601.0, 355.0, image=self.image_11)
            
            self.image_12 = PhotoImage(file=relative_to_assets("image_12.png"))
            self.canvas.create_image(342.0, 355.0, image=self.image_12)
            
            self.image_13 = PhotoImage(file=relative_to_assets("image_13.png"))
            self.canvas.create_image(632.0, 128.0, image=self.image_13)
            
            # Top bar icons
            self.image_14 = PhotoImage(file=relative_to_assets("image_14.png"))
            self.canvas.create_image(237.0, 32.0, image=self.image_14)
            
            self.image_15 = PhotoImage(file=relative_to_assets("image_15.png"))
            self.canvas.create_image(562.0, 28.0, image=self.image_15)
            
            self.image_16 = PhotoImage(file=relative_to_assets("image_16.png"))
            self.canvas.create_image(898.0, 28.0, image=self.image_16)
            
            self.image_17 = PhotoImage(file=relative_to_assets("image_17.png"))
            self.canvas.create_image(928.0, 28.0, image=self.image_17)
            
            self.image_18 = PhotoImage(file=relative_to_assets("image_18.png"))
            self.canvas.create_image(959.0, 28.0, image=self.image_18)
            
            self.image_19 = PhotoImage(file=relative_to_assets("image_19.png"))
            self.canvas.create_image(27.0, 22.0, image=self.image_19)
            
        except Exception as e:
            print(f"Error loading images: {e}")
    
    def setup_navigation(self):
        """Setup navigation buttons with click functionality"""
        # Dashboard button
        self.dashboard_btn = Button(
            self,
            text="DashBoard",
            fg="#FFFFFF",
            bg="#3A404D",
            bd=0,
            font=("Arial", 12),
            cursor="hand2",
            command=lambda: self.controller.show_page('Dashboard')
        )
        self.dashboard_btn.place(x=40, y=85, width=80, height=25)
        
        # Alerts button
        self.alerts_btn = Button(
            self,
            text="Alerts",
            fg="#FFFFFF",
            bg="#3A404D",
            bd=0,
            font=("Arial", 12),
            cursor="hand2",
            command=lambda: self.controller.show_page('Alerts')
        )
        self.alerts_btn.place(x=40, y=120, width=50, height=25)
        
        # Help/Info button
        self.help_btn = Button(
            self,
            text="Help/Info",
            fg="#FFFFFF",
            bg="#3A404D",
            bd=0,
            font=("Arial", 12),
            cursor="hand2",
            command=lambda: self.controller.show_page('HelpInfo')
        )
        self.help_btn.place(x=40, y=160, width=70, height=25)
        
        # Logout button
        self.logout_btn = Button(
            self,
            text="Log Out",
            fg="#FFFFFF",
            bg="#3A404D",
            bd=0,
            font=("Arial", 12),
            cursor="hand2",
            command=self.logout
        )
        self.logout_btn.place(x=40, y=200, width=60, height=25)
    
    def add_all_static_text(self):
        """Add ALL static text elements with proper positioning and smaller fonts"""
        # App title - Smaller fonts
        self.canvas.create_text(
            54.0, 8.0, anchor="nw", text="NeuroLens",
            fill="#FFFFFF", font=("Arial", 18, "bold")  # Reduced from 24
        )
        
        # Breadcrumb
        self.canvas.create_text(
            294.0, 24.0, anchor="nw", text="DashBoard  /    Default",
            fill="#FFFFFF", font=("Arial", 11)  # Reduced from 14
        )
        
        # Section titles - Smaller fonts
        self.canvas.create_text(
            252.0, 115.0, anchor="nw", text="Drowsiness Level",
            fill="#FFFFFF", font=("Arial", 16, "bold")  # Reduced from 22
        )
        
        self.canvas.create_text(
            786.0, 304.0, anchor="nw", text="Blink Count",
            fill="#FFFFFF", font=("Arial", 16, "bold")  # Reduced from 22
        )
        
        self.canvas.create_text(
            247.0, 467.0, anchor="nw", text="Alerts",
            fill="#FFFFFF", font=("Arial", 16, "bold")  # Reduced from 22
        )
        
        self.canvas.create_text(
            252.0, 217.0, anchor="nw", text="Active",
            fill="#FFFFFF", font=("Arial", 14, "bold")  # Reduced from 20
        )
        
        self.canvas.create_text(
            252.0, 313.0, anchor="nw", text="Status",
            fill="#FFFFFF", font=("Arial", 16, "bold")  # Reduced from 22
        )
        
        self.canvas.create_text(
            504.0, 316.0, anchor="nw", text="Session Timer",
            fill="#FFFFFF", font=("Arial", 16, "bold")  # Reduced from 22
        )
        
        self.canvas.create_text(
            780.0, 436.0, anchor="nw", text="Device Connectivity",
            fill="#FFFFFF", font=("Arial", 16, "bold")  # Reduced from 22
        )
        
        self.canvas.create_text(
            796.0, 119.0, anchor="nw", text="Performance",
            fill="#FFFFFF", font=("Arial", 16, "bold")  # Reduced from 22
        )
    
    def setup_dynamic_elements(self):
        """Setup elements that will update dynamically"""
        # Drowsiness Level - Smaller font
        self.drowsiness_text = self.canvas.create_text(
            256.0, 145.0, anchor="nw", text="3", 
            fill="#FFFFFF", font=("Arial", 36, "bold"), tags="dynamic"  # Reduced from 50
        )
        
        # Battery Percentage - Smaller font
        self.battery_text = self.canvas.create_text(
            601.0, 163.0, anchor="nw", text="78%", 
            fill="#FFFFFF", font=("Arial", 24, "bold"), tags="dynamic"  # Reduced from 30
        )
        
        # Blink Count - Smaller font
        self.blink_text = self.canvas.create_text(
            786.0, 348.0, anchor="nw", text="0", 
            fill="#FFFFFF", font=("Arial", 24, "bold"), tags="dynamic"  # Reduced from 30
        )
        
        # Status - Smaller font
        self.status_text = self.canvas.create_text(
            284.0, 348.0, anchor="nw", text="Active", 
            fill="#AEF5B0", font=("Arial", 18), tags="dynamic"  # Reduced from 23
        )
        
        # Session Timer - Smaller font
        self.timer_text = self.canvas.create_text(
            515.0, 348.0, anchor="nw", text="0H00m", 
            fill="#FFFFFF", font=("Arial", 18), tags="dynamic"  # Reduced from 23
        )
        
        # Device Connectivity - Smaller font
        self.connectivity_text = self.canvas.create_text(
            816.0, 486.0, anchor="nw", text="connected", 
            fill="#AEF5B0", font=("Arial", 16), tags="dynamic"  # Reduced from 20
        )
        
        # Add Sync Data button functionality
        self.sync_button = Button(
            self,
            text="Sync Data",
            fg="#FFFFFF",
            bg="#4277FF",  # Blue theme
            bd=0,
            font=("Arial", 12),
            cursor="hand2",
            command=self.sync_data,
            relief="flat",
            padx=10,
            pady=5
        )
        self.sync_button.place(x=820.0, y=530.0, width=80, height=30)
    


    
    def setup_alerts_section(self):
        """Setup dynamic alerts section"""
        # View All button with blue theme and rounded background
        self.view_all_btn = Button(
            self,
            text="View All",
            fg="#FFFFFF",
            bg="#4277FF",  # Blue theme
            bd=0,
            font=("Arial", 10, "bold"),
            cursor="hand2",
            command=self.view_all_alerts,
            relief="flat",
            padx=10,
            pady=2
        )
        self.view_all_btn.place(x=650.0, y=470.0, width=60, height=25)
        
        # Alerts display area
        self.alert_texts = []  # Store references to alert text items
    
    def update_alerts_display(self):
        """Update the alerts display with dynamic content"""
        # Clear existing alerts
        for text_id in self.alert_texts:
            self.canvas.delete(text_id)
        self.alert_texts = []
        
        # Display latest 2-3 alerts
        recent_alerts = self.alerts[:3]  # Show 3 most recent alerts
        y_position = 510
        
        for i, alert in enumerate(recent_alerts):
            # Format time
            time_str = alert["time"].strftime("%H:%M")
            
            # Create alert text
            alert_text = f"{time_str}  {alert['message']}"
            text_id = self.canvas.create_text(
                242.0, y_position, anchor="nw",
                text=alert_text,
                fill="#FFFFFF", font=("Arial", 11)
            )
            self.alert_texts.append(text_id)
            
            # Add "new" tag for recent alerts (within last 10 minutes)
            if (datetime.now() - alert["time"]).total_seconds() < 600:  # 10 minutes
                new_tag = self.canvas.create_text(
                    540.0, y_position, anchor="nw", text="new",
                    fill="#AEF5B0", font=("Arial", 9, "bold")
                )
                self.alert_texts.append(new_tag)
            
            y_position += 25
    
    def setup_performance_graph(self):
        """Setup the performance graph"""
        try:
            # Simple bar chart for performance
            fig, ax = plt.subplots(figsize=(2.5, 1.8))  # Smaller figure
            
            # Sample performance data
            days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']
            performance = [75, 82, 78, 85, 80]
            
            bars = ax.bar(days, performance, color=['#4277FF', '#4277FF', '#4277FF', '#4277FF', '#4277FF'])
            ax.set_facecolor('#3A404D')
            fig.patch.set_facecolor('#3A404D')
            ax.tick_params(colors='white', labelsize=6)  # Smaller labels
            
            # Set y-axis limit to 100
            ax.set_ylim(0, 100)
            
            # Remove spines
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['left'].set_color('white')
            ax.spines['bottom'].set_color('white')
            
            self.performance_canvas = FigureCanvasTkAgg(fig, self)
            self.performance_canvas.draw()
            self.performance_widget = self.performance_canvas.get_tk_widget()
            self.performance_widget.place(x=780, y=140, width=180, height=130)  # Adjusted size
            
        except Exception as e:
            print(f"Error creating performance graph: {e}")
            # Fallback text
            self.canvas.create_text(
                830.0, 200.0, anchor="nw", text="Performance: 80%", 
                fill="#FFFFFF", font=("Arial", 12), tags="graph_fallback"
            )
    
    def start_live_updates(self):
        """Start updating dashboard data"""
        self.update_dashboard()
    
    def update_dashboard(self):
        """Update all dynamic elements"""
        try:
            # Simulate sensor data changes
            self.drowsiness_level = max(1, min(5, self.drowsiness_level + random.randint(-1, 1)))
            self.battery_percentage = max(10, self.battery_percentage - 0.02)
            self.blink_count += random.randint(0, 2)
            
            # Update session timer
            current_time = datetime.now()
            session_duration = current_time - self.session_start_time
            hours = int(session_duration.total_seconds() // 3600)
            minutes = int((session_duration.total_seconds() % 3600) // 60)
            
            # Update canvas text elements
            self.canvas.itemconfig(self.drowsiness_text, text=str(self.drowsiness_level))
            self.canvas.itemconfig(self.battery_text, text=f"{int(self.battery_percentage)}%")
            self.canvas.itemconfig(self.blink_text, text=str(self.blink_count))
            self.canvas.itemconfig(self.timer_text, text=f"{hours}H{minutes:02d}m")
            
            # Update status color based on drowsiness
            if self.drowsiness_level <= 2:
                status = "Alert"
                color = "#AEF5B0"  # Green
            elif self.drowsiness_level <= 3:
                status = "Normal" 
                color = "#FFFF00"  # Yellow
            else:
                status = "Drowsy"
                color = "#FF6B6B"  # Red
                
            self.canvas.itemconfig(self.status_text, text=status, fill=color)
            
            # Update connectivity status occasionally
            if random.random() < 0.05:
                self.device_connected = not self.device_connected
                status_text = "connected" if self.device_connected else "disconnected"
                status_color = "#AEF5B0" if self.device_connected else "#FF6B6B"
                self.canvas.itemconfig(self.connectivity_text, text=status_text, fill=status_color)
            
            # Simulate new alerts occasionally (10% chance each update)
            if random.random() < 0.1:
                self.generate_new_alert()
            
            # Update alerts display
            self.update_alerts_display()
            
        except Exception as e:
            print(f"Error updating dashboard: {e}")
        
        # Schedule next update
        self.after(3000, self.update_dashboard)
    
    def generate_new_alert(self):
        """Generate a new simulated alert"""
        alert_types = [
            {"type": "Drowsiness", "message": "Drowsiness Detected"},
            {"type": "Connection", "message": "Device Connection Lost"},
            {"type": "Battery", "message": "Battery Low"},
            {"type": "Connection", "message": "Device Reconnected"},
            {"type": "System", "message": "System Calibration Needed"}
        ]
        
        new_alert = random.choice(alert_types)
        new_alert["time"] = datetime.now()
        
        # Add to beginning of list (most recent first)
        self.alerts.insert(0, new_alert)
        
        # Keep only last 20 alerts
        self.alerts = self.alerts[:20]
        
        print(f"New alert generated: {new_alert['message']} at {new_alert['time']}")
    
    def sync_data(self):
        """Sync data button handler"""
        print("Syncing data with glasses...")
        # Refresh all data
        self.battery_percentage = 78
        self.blink_count = 0
        self.session_start_time = datetime.now()
        
        # Add sync alert
        sync_alert = {
            "type": "Sync", 
            "time": datetime.now(), 
            "message": "Data Sync Completed"
        }
        self.alerts.insert(0, sync_alert)
        
        # Show sync confirmation
        self.show_sync_confirmation()
    
    def show_sync_confirmation(self):
        """Show sync confirmation message"""
        confirmation = self.canvas.create_text(
            820.0, 565.0, anchor="nw", text="Data synced successfully!", 
            fill="#AEF5B0", font=("Arial", 10), tags="sync_confirmation"
        )
        
        # Remove confirmation after 2 seconds
        self.after(2000, lambda: self.canvas.delete(confirmation))
    
    def view_all_alerts(self):
        """Navigate to Alerts page"""
        print("Navigating to Alerts page")
        self.controller.show_page('Alerts')
    
    def logout(self):
        """Handle logout functionality"""
        print("Logging out...")
        # Add logout confirmation or cleanup here
        self.controller.show_page('Login')  # Assuming you have a Login page
    
    def on_page_show(self):
        """Called when page is shown"""
        print("Dashboard page shown")
        # Refresh data when page is shown
        self.update_alerts_display()
        self.update_dashboard()
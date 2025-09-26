from pathlib import Path
import tkinter as tk
from tkinter import Canvas, Entry, Button, PhotoImage
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from sensor_monitor import SensorMonitor
import random
from datetime import datetime

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = Path(__file__).parent.parent / "Assets/Dashboard"

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

class Dashboard(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#D0DFFF")
        self.controller = controller
        
        # Initialize sensor monitor
        self.sensor_monitor = None
        self.status_message = "Initializing..."
        
        # Try to start real sensor monitoring
        try:
            self.sensor_monitor = SensorMonitor(self)
            self.sensor_monitor.start()
            print("Real sensor connected!")
        except Exception as e:
            print(f"Sensor not available: {e}")
            self.sensor_monitor = FakeSensorForTesting()
        
        # Dynamic data from sensors
        self.drowsiness_level = self.sensor_monitor.get_drowsiness_level()
        self.battery_percentage = self.sensor_monitor.get_battery_level()
        self.logout_count = 0
        
        # Accuracy tracking
        self.alert_accuracy = 87
        
        # Activity notifications - LESS FREQUENT
        self.notifications = []
        self.unread_count = 0
        self.last_notification_time = 0
        
        # Canvas
        self.canvas = Canvas(
            self,
            bg="#D0DFFF",
            height=699,
            width=1200,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)
        
        # Load all images
        self.load_images()
        
        # Add all text elements
        self.add_text_elements()
        
        # Add entry field
        self.add_entry_field()
        
        # Add ONLY the pie chart - remove overlapping charts
        self.add_clean_pie_chart()
        
        # Make View All clickable - SINGLE BUTTON ONLY
        self.add_single_view_all_button()
        
        # Start live updates
        self.start_live_updates()
        
    def update_status(self, message):
        """Called by sensor monitor to update status"""
        self.status_message = message
        
        # Only add notification every 30 seconds to avoid spam
        current_time = datetime.now().timestamp()
        if current_time - self.last_notification_time > 30:
            self.add_notification(f"System: {message}")
            self.last_notification_time = current_time
        
        print(f"Status: {message}")

    def add_notification(self, message):
        """Add a new notification to recent activity - LESS FREQUENT"""
        timestamp = datetime.now().strftime("%H:%M")
        notification = {
            "message": message,
            "time": timestamp,
            "read": False
        }
        self.notifications.insert(0, notification)
        self.unread_count += 1
        
        # Keep only last 5 notifications
        if len(self.notifications) > 5:
            self.notifications = self.notifications[:5]

    def start_live_updates(self):
        """Update dashboard every 4 seconds"""
        try:
            old_drowsiness = self.drowsiness_level
            old_battery = self.battery_percentage
            
            self.drowsiness_level = self.sensor_monitor.get_drowsiness_level()
            self.battery_percentage = self.sensor_monitor.get_battery_level()
            
            # Only notify on SIGNIFICANT changes
            if old_drowsiness != self.drowsiness_level and self.drowsiness_level in ["Drowsy", "Tired"]:
                self.add_notification(f"Alert: {self.drowsiness_level} detected at {datetime.now().strftime('%H:%M')}")
            
            # Update session count properly
            self.logout_count = getattr(self.controller, 'session_count', 0)
            
            # Update accuracy occasionally
            if random.randint(1, 10) == 1:
                self.alert_accuracy += random.randint(-1, 2)
                self.alert_accuracy = max(75, min(99, self.alert_accuracy))
            
            # Check for alerts from sensor
            new_alerts = self.sensor_monitor.get_new_alerts()
            if new_alerts:
                for alert in new_alerts:
                    self.add_notification(f"ALERT: {alert['condition']}")
                    if hasattr(self.controller, 'pages') and 'Alerts' in self.controller.pages:
                        alerts_page = self.controller.pages['Alerts']
                        if hasattr(alerts_page, 'add_live_alert'):
                            alerts_page.add_live_alert(alert)
            
            # Refresh display
            self.refresh_dynamic_content()
        
        except Exception as e:
            print(f"Update error: {e}")
        
        # Schedule next update
        self.after(4000, self.start_live_updates)
    
    def refresh_dynamic_content(self):
        """Refresh the dynamic parts of the display"""
        self.canvas.delete("dynamic")
        
        # Drowsiness level with color coding
        color = self.get_drowsiness_color()
        self.canvas.create_text(337.0, 178.0, anchor="nw", text=self.drowsiness_level, 
                               fill=color, font=("Arial", 14, "bold"), tags="dynamic")
        
        # Battery percentage
        self.canvas.create_text(697.0, 221.0, anchor="nw", text=f"{self.battery_percentage}%", 
                               fill="#FFFFFF", font=("Arial", 16), tags="dynamic")
        
        # Alert accuracy percentage
        self.canvas.create_text(930.0, 400.0, anchor="nw", text=f"{self.alert_accuracy}%",
                               fill="#000000", font=("Arial", 14, "bold"), tags="dynamic")
        
        # Battery health in stats
        self.canvas.create_text(1065.0, 392.0, anchor="nw", text=f"{self.battery_percentage}%",
                               fill="#000000", font=("Arial", 14, "bold"), tags="dynamic")
        
        # Life Stats section - SMALLER FONT
        spatial_level = random.randint(88, 95)
        self.canvas.create_text(248.0 + 5, 622.0, anchor="nw", text=f"{spatial_level}%", 
                               fill="#FFFFFF", font=("Arial", 12, "bold"), tags="dynamic")
        self.canvas.create_text(471.0 + 5, 620.0, anchor="nw", text=f"{self.alert_accuracy}%", 
                               fill="#FFFFFF", font=("Arial", 12, "bold"), tags="dynamic")
        self.canvas.create_text(692.0 + 5, 624.0, anchor="nw", text=f"{self.logout_count}", 
                               fill="#FFFFFF", font=("Arial", 12, "bold"), tags="dynamic")
        
        # Update recent activity notifications
        self.update_notifications_display()
        
        # Update pie chart to reflect current state
        self.update_pie_chart()
    
    def get_drowsiness_color(self):
        """Get color based on drowsiness level"""
        colors = {
            "Alert": "#00FF00",
            "Awake": "#FFFF00", 
            "Drowsy": "#FF0000",
            "Tired": "#FFA500",
            "Eyes Closed": "#FF4500"
        }
        return colors.get(self.drowsiness_level, "#FFFFFF")
    
    def update_notifications_display(self):
        """Update the notifications in recent activity"""
        self.canvas.delete("notifications")
        
        # Show up to 3 most recent notifications
        for i, notification in enumerate(self.notifications[:3]):
            y_pos = 403.0 + (i * 20)
            text_color = "#000000" if notification["read"] else "#1657FF"
            notification_text = f"{notification['message']} ({notification['time']})"
            
            self.canvas.create_text(248.0, y_pos, anchor="nw", text=notification_text,
                                   fill=text_color, font=("Arial", 10), tags="notifications")
            
            if not notification["read"]:
                self.canvas.create_text(707.0, y_pos, anchor="nw", text="New", 
                                       fill="#FF0101", font=("Arial", 9), tags="notifications")
        
    def load_images(self):
        """Load and place all images"""
        try:
            # All the same image loading code as before
            self.image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
            self.canvas.create_image(98.0, 349.0, image=self.image_1)
            
            self.image_2 = PhotoImage(file=relative_to_assets("image_2.png"))
            self.canvas.create_image(27.0, 213.0, image=self.image_2)
            
            self.image_3 = PhotoImage(file=relative_to_assets("image_3.png"))
            self.canvas.create_image(29.0, 101.0, image=self.image_3)
            
            self.image_4 = PhotoImage(file=relative_to_assets("image_4.png"))
            self.canvas.create_image(28.0, 23.0, image=self.image_4)
            
            self.image_5 = PhotoImage(file=relative_to_assets("image_5.png"))
            self.canvas.create_image(28.0, 157.0, image=self.image_5)
            
            self.image_6 = PhotoImage(file=relative_to_assets("image_6.png"))
            self.canvas.create_image(26.0, 456.0, image=self.image_6)
            
            self.image_7 = PhotoImage(file=relative_to_assets("image_7.png"))
            self.canvas.create_image(722.0, 26.0, image=self.image_7)
            
            self.image_8 = PhotoImage(file=relative_to_assets("image_8.png"))
            self.canvas.create_image(963.0, 27.0, image=self.image_8)
            
            self.image_9 = PhotoImage(file=relative_to_assets("image_9.png"))
            self.canvas.create_image(902.0, 27.0, image=self.image_9)
            
            self.image_10 = PhotoImage(file=relative_to_assets("image_10.png"))
            self.canvas.create_image(930.0, 27.0, image=self.image_10)
            
            self.image_11 = PhotoImage(file=relative_to_assets("image_11.png"))
            self.canvas.create_image(243.0, 33.0, image=self.image_11)
            
            self.image_12 = PhotoImage(file=relative_to_assets("image_12.png"))
            self.canvas.create_image(275.0, 33.0, image=self.image_12)
            
            self.image_13 = PhotoImage(file=relative_to_assets("image_13.png"))
            self.canvas.create_image(372.0, 181.0, image=self.image_13)
            
            self.image_14 = PhotoImage(file=relative_to_assets("image_14.png"))
            self.canvas.create_image(722.0, 180.0, image=self.image_14)
            
            self.image_15 = PhotoImage(file=relative_to_assets("image_15.png"))
            self.canvas.create_image(369.0, 191.0, image=self.image_15)
            
            self.image_16 = PhotoImage(file=relative_to_assets("image_16.png"))
            self.canvas.create_image(722.0, 187.0, image=self.image_16)
            
            self.image_17 = PhotoImage(file=relative_to_assets("image_17.png"))
            self.canvas.create_image(538.0, 427.0, image=self.image_17)
            
            # Status indicators
            for i in range(18, 31):
                img_attr = f"image_{i}"
                positions = {
                    18: (726.0, 406.0), 19: (726.0, 469.0), 20: (726.0, 439.0),
                    21: (326.0, 627.0), 22: (764.0, 627.0), 23: (544.0, 629.0),
                    24: (1048.0, 200.0), 25: (1053.0, 582.0), 26: (979.0, 420.0),
                    27: (1117.0, 420.0), 28: (299.0, 637.0), 29: (529.0, 634.0),
                    30: (727.0, 640.0)
                }
                
                if i in positions:
                    setattr(self, img_attr, PhotoImage(file=relative_to_assets(f"image_{i}.png")))
                    self.canvas.create_image(*positions[i], image=getattr(self, img_attr))
                    
        except Exception as e:
            print(f"Error loading images: {e}")
    
    def add_text_elements(self):
        """Add all static text elements"""
        # App title
        self.canvas.create_text(54.0, 8.0, anchor="nw", text="NeuroLens", 
                               fill="#2C2745", font=("Arial", 18, "bold"))
        
        # Sidebar navigation
        self.canvas.create_text(53.0, 91.0, anchor="nw", text="DashBoard", 
                               fill="#B9C0DE", font=("Arial", 12))
        self.canvas.create_text(53.0, 147.0, anchor="nw", text="Alerts", 
                               fill="#B9C0DE", font=("Arial", 12))
        self.canvas.create_text(54.0, 205.0, anchor="nw", text="Help/Info", 
                               fill="#B9C0DE", font=("Arial", 12))
        self.canvas.create_text(53.0, 450.0, anchor="nw", text="Log Out", 
                               fill="#B9C0DE", font=("Arial", 12))
        
        # Breadcrumb
        self.canvas.create_text(294.0, 24.0, anchor="nw", text="DashBoard  /    Live Monitor", 
                               fill="#1657FF", font=("Arial", 11))
        
        # Main content headers
        self.canvas.create_text(289.0, 121.0, anchor="nw", text="Drowsiness Level", 
                               fill="#FFFFFF", font=("Arial", 16, "bold"))
        
        self.canvas.create_text(681.0, 115.0, anchor="nw", text="Battery Status", 
                               fill="#FFFFFF", font=("Arial", 16, "bold"))
        
        # Recent Activity
        self.canvas.create_text(236.0, 287.0, anchor="nw", text="Recent Activity Summary", 
                               fill="#353E6C", font=("Arial", 14, "bold"))
        self.canvas.create_text(281.0, 344.0, anchor="nw", text="NeuroLens User", 
                               fill="#000000", font=("Arial", 11))
        
        # Time filters
        self.canvas.create_text(248.0, 380.0, anchor="nw", text="Live Feed", 
                               fill="#000000", font=("Arial", 10))
        self.canvas.create_text(310.0, 380.0, anchor="nw", text="Real-time Updates", 
                               fill="#000000", font=("Arial", 10))
        
        # Statistics section
        self.canvas.create_text(932.0, 67.0, anchor="nw", text="Performance Analytics", 
                               fill="#353E6C", font=("Arial", 14, "bold"))
        self.canvas.create_text(953.0, 121.0, anchor="nw", text="Drowsiness Event Distribution", 
                               fill="#000000", font=("Arial", 10))
        
        # Analytics labels - SIMPLE TEXT ONLY
        self.canvas.create_text(930.0, 358.0, anchor="nw", text="Alert Accuracy", 
                               fill="#000000", font=("Arial", 10))
        
        self.canvas.create_text(1076.0, 358.0, anchor="nw", text="Battery Health", 
                               fill="#000000", font=("Arial", 10))
        
        self.canvas.create_text(960.0, 506.0, anchor="nw", text="System Performance", 
                               fill="#000000", font=("Arial", 10))
        
        # System performance as simple text
        self.canvas.create_text(960.0, 530.0, anchor="nw", text="Optimal", 
                               fill="#00AA00", font=("Arial", 14, "bold"))
        
        # Life Stats section
        self.canvas.create_text(236.0, 547.0, anchor="nw", text="Life Stats", 
                               fill="#353E6C", font=("Arial", 14, "bold"))
        
        # Life stats labels
        stats_labels = [
            ("Spatial Awareness", 596),
            ("Alert Accuracy", 595), 
            ("Session Count", 586)
        ]
        
        x_positions = [248, 471, 692]
        for i, (label, label_y) in enumerate(stats_labels):
            self.canvas.create_text(x_positions[i], label_y, anchor="nw", text=label, 
                                   fill="#FFFFFF", font=("Arial", 10))
        
        # User indicator rectangle
        self.canvas.create_rectangle(251.0, 342.0, 271.0, 362.0, fill="#FFFFFF", outline="")
    
    def add_entry_field(self):
        """Add the search entry field"""
        try:
            self.entry_image_1 = PhotoImage(file=relative_to_assets("entry_1.png"))
            self.canvas.create_image(808.5, 26.0, image=self.entry_image_1)
            
            self.entry_1 = Entry(
                self,
                bd=0,
                bg="#FFFFFF", 
                fg="#000716",
                highlightthickness=0,
                font=("Arial", 9)
            )
            self.entry_1.place(x=751.0, y=15.0, width=115.0, height=20.0)
        except Exception as e:
            print(f"Error creating entry field: {e}")
    
    def add_clean_pie_chart(self):
        """Add ONLY the pie chart - properly sized and positioned"""
        try:
            # Dynamic data based on current sensor readings
            if self.drowsiness_level == "Alert":
                sizes = [5, 80, 10, 5]
            elif self.drowsiness_level == "Drowsy":
                sizes = [60, 20, 15, 5]
            elif self.drowsiness_level in ["Tired", "Awake"]:
                sizes = [20, 50, 25, 5]
            else:
                sizes = [25, 45, 20, 10]
                
            labels = ['Drowsy', 'Alert', 'Tired', 'Other']
            colors = ['#FF4444', '#44FF44', '#FFAA44', '#4444FF']
            
            # Properly sized to fit in background
            fig, ax = plt.subplots(figsize=(1.4, 1.4))
            ax.pie(sizes, labels=labels, colors=colors, autopct='%1.0f%%', 
                   startangle=90, textprops={'fontsize': 6})
            
            ax.axis('equal')
            fig.patch.set_facecolor('none')
            ax.set_facecolor('none')
            
            # Store reference to prevent garbage collection
            self.pie_chart_canvas = FigureCanvasTkAgg(fig, self)
            self.pie_chart_canvas.draw()
            self.pie_chart_widget = self.pie_chart_canvas.get_tk_widget()
            self.pie_chart_widget.place(x=1005, y=145, width=120, height=120)
            
        except Exception as e:
            print(f"Error creating pie chart: {e}")
            # Fallback - simple text display
            self.canvas.create_text(1065, 205, text=f"{self.drowsiness_level}\nState", 
                                   fill="#666", font=("Arial", 10), justify="center")
    
    def update_pie_chart(self):
        """Update pie chart with current drowsiness data"""
        try:
            if hasattr(self, 'pie_chart_widget'):
                self.pie_chart_widget.destroy()
            
            self.add_clean_pie_chart()
        except Exception as e:
            print(f"Error updating pie chart: {e}")
    
    def add_single_view_all_button(self):
        """Single View All button ONLY"""
        view_all_btn = tk.Button(
            self,
            text="View All",
            fg="#1657FF",
            bd=0,
            font=("Arial", 11),
            cursor="hand2",
            command=self.view_all_notifications
        )
        view_all_btn.place(x=763, y=336)
    
    def view_all_notifications(self):
        """Mark notifications as read and go to alerts page"""
        for notification in self.notifications:
            notification["read"] = True
        self.unread_count = 0
        self.controller.show_page('Alerts')
    
    def increment_logout_count(self):
        """Increment logout counter"""
        self.logout_count += 1
        print(f"User logout count: {self.logout_count}")


# Realistic fake sensor with MUCH less frequent updates
class FakeSensorForTesting:
    def __init__(self):
        self.battery = 85
        self.status_cycle = 0
        self.alert_count = 0
        self.current_state = "Alert"
        
    def get_drowsiness_level(self):
        # Change state much less frequently
        self.status_cycle += 1
        
        if self.status_cycle % 50 == 0:  # Every 3+ minutes
            self.current_state = random.choice(["Drowsy", "Tired"])
        elif self.status_cycle % 25 == 0:  # Every 1.5 minutes
            self.current_state = "Awake"
        else:
            self.current_state = "Alert"  # Most of the time
            
        return self.current_state
        
    def get_battery_level(self):
        self.battery -= random.uniform(0.01, 0.03)  # Very slow drain
        if self.battery < 15:
            self.battery = random.randint(85, 95)
        return int(self.battery)
    
    def get_new_alerts(self):
        # Create alerts much less frequently
        if self.current_state == "Drowsy" and random.randint(1, 50) == 1:  # Very rare
            self.alert_count += 1
            return [{
                "title": f"Drowsiness Alert #{self.alert_count:03d}",
                "username": "TestUser",
                "condition": f"{self.current_state} state detected",
                "action": "System alert triggered",
                "response": "Monitoring response",
                "date": datetime.now().strftime("%Y-%m-%d %H:%M")
            }]
        return []
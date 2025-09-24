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
        self.alert_accuracy = 87  # Start with 87%
        self.accuracy_history = [85, 86, 87]  # Historical accuracy data
        
        # Activity notifications
        self.notifications = []
        self.unread_count = 0
        
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
        
        # Add enhanced charts
        self.add_enhanced_pie_chart()
        self.add_accuracy_line_chart()
        self.add_battery_health_chart()
        
        # Make View All clickable
        self.add_view_all_button()
        
        # Start live updates
        self.start_live_updates()
        
    def update_status(self, message):
        """Called by sensor monitor to update status"""
        self.status_message = message
        self.add_notification(f"Sensor status: {message}")
        print(f"Status: {message}")

    def add_notification(self, message):
        """Add a new notification to recent activity"""
        timestamp = datetime.now().strftime("%H:%M")
        notification = {
            "message": message,
            "time": timestamp,
            "read": False
        }
        self.notifications.insert(0, notification)  # Add to beginning
        self.unread_count += 1
        
        # Keep only last 10 notifications
        if len(self.notifications) > 10:
            self.notifications = self.notifications[:10]

    def start_live_updates(self):
        """Update dashboard every 2 seconds"""
        try:
            # Get fresh data from sensors
            old_drowsiness = self.drowsiness_level
            old_battery = self.battery_percentage
            
            self.drowsiness_level = self.sensor_monitor.get_drowsiness_level()
            self.battery_percentage = self.sensor_monitor.get_battery_level()
            
            # Update notifications when drowsiness changes
            if old_drowsiness != self.drowsiness_level:
                self.add_notification(f"Drowsiness level: {self.drowsiness_level} at {datetime.now().strftime('%H:%M')}")
                
            # Update accuracy (simulate changes)
            self.alert_accuracy += random.randint(-2, 3)
            self.alert_accuracy = max(70, min(100, self.alert_accuracy))  # Keep between 70-100%
            self.accuracy_history.append(self.alert_accuracy)
            if len(self.accuracy_history) > 10:
                self.accuracy_history = self.accuracy_history[-10:]
            
            # Check for new alerts from sensor
            new_alerts = self.sensor_monitor.get_new_alerts()
            if new_alerts:
                for alert in new_alerts:
                    self.add_notification(f"ALERT: {alert['condition']}")
                    # Add to controller's alerts page if it exists
                    if hasattr(self.controller, 'pages') and 'Alerts' in self.controller.pages:
                        alerts_page = self.controller.pages['Alerts']
                        if hasattr(alerts_page, 'add_live_alert'):
                            alerts_page.add_live_alert(alert)
            
            # Refresh display
            self.refresh_dynamic_content()
        
        except Exception as e:
            print(f"Update error: {e}")
        
        # Schedule next update
        self.after(2000, self.start_live_updates)
    
    def refresh_dynamic_content(self):
        """Refresh the dynamic parts of the display"""
        # Clear and redraw dynamic text elements
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
                               fill="#000000", font=("Arial", 16, "bold"), tags="dynamic")
        
        # Battery health in stats
        self.canvas.create_text(1065.0, 392.0, anchor="nw", text=f"{self.battery_percentage}%",
                               fill="#000000", font=("Arial", 16, "bold"), tags="dynamic")
        
        # Life Stats section
        spatial_level = random.randint(85, 98)  # Simulate spatial awareness
        self.canvas.create_text(248.0 + 5, 622.0, anchor="nw", text=f"{spatial_level}%", 
                               fill="#FFFFFF", font=("Arial", 16, "bold"), tags="dynamic")
        self.canvas.create_text(471.0 + 5, 620.0, anchor="nw", text=f"{self.alert_accuracy}%", 
                               fill="#FFFFFF", font=("Arial", 16, "bold"), tags="dynamic")
        self.canvas.create_text(692.0 + 5, 624.0, anchor="nw", text=f"{self.logout_count}", 
                               fill="#FFFFFF", font=("Arial", 16, "bold"), tags="dynamic")
        
        # Update recent activity notifications
        self.update_notifications_display()
    
    def get_drowsiness_color(self):
        """Get color based on drowsiness level"""
        colors = {
            "Alert": "#00FF00",      # Green - good
            "Awake": "#FFFF00",      # Yellow - caution  
            "Drowsy": "#FF0000",     # Red - danger
            "Tired": "#FFA500",      # Orange - warning
            "Eyes Closed": "#FF4500" # Orange-red - immediate attention
        }
        return colors.get(self.drowsiness_level, "#FFFFFF")
    
    def update_notifications_display(self):
        """Update the notifications in recent activity"""
        self.canvas.delete("notifications")
        
        # Show up to 4 most recent notifications
        for i, notification in enumerate(self.notifications[:4]):
            y_pos = 403.0 + (i * 20)
            text_color = "#000000" if notification["read"] else "#1657FF"  # Blue if unread
            notification_text = f"{notification['message']} ({notification['time']})"
            
            self.canvas.create_text(248.0, y_pos, anchor="nw", text=notification_text,
                                   fill=text_color, font=("Arial", 10), tags="notifications")
            
            # Unread indicator
            if not notification["read"]:
                self.canvas.create_text(707.0, y_pos, anchor="nw", text="New", 
                                       fill="#FF0101", font=("Arial", 9), tags="notifications")
        
        # Update unread count in View All button area
        if self.unread_count > 0:
            self.canvas.create_text(800.0, 336.0, anchor="nw", text=f"({self.unread_count} new)", 
                                   fill="#FF0101", font=("Arial", 9), tags="notifications")
        
    def load_images(self):
        """Load and place all images"""
        try:
            # Sidebar icon
            self.image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
            self.canvas.create_image(98.0, 349.0, image=self.image_1)
            
            # Navigation icons
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
            
            # Top bar icons
            self.image_7 = PhotoImage(file=relative_to_assets("image_7.png"))
            self.canvas.create_image(722.0, 26.0, image=self.image_7)
            
            self.image_8 = PhotoImage(file=relative_to_assets("image_8.png"))
            self.canvas.create_image(963.0, 27.0, image=self.image_8)
            
            self.image_9 = PhotoImage(file=relative_to_assets("image_9.png"))
            self.canvas.create_image(902.0, 27.0, image=self.image_9)
            
            self.image_10 = PhotoImage(file=relative_to_assets("image_10.png"))
            self.canvas.create_image(930.0, 27.0, image=self.image_10)
            
            # Breadcrumb icons
            self.image_11 = PhotoImage(file=relative_to_assets("image_11.png"))
            self.canvas.create_image(243.0, 33.0, image=self.image_11)
            
            self.image_12 = PhotoImage(file=relative_to_assets("image_12.png"))
            self.canvas.create_image(275.0, 33.0, image=self.image_12)
            
            # Dashboard content images
            self.image_13 = PhotoImage(file=relative_to_assets("image_13.png"))
            self.canvas.create_image(372.0, 181.0, image=self.image_13)
            
            self.image_14 = PhotoImage(file=relative_to_assets("image_14.png"))
            self.canvas.create_image(722.0, 180.0, image=self.image_14)
            
            self.image_15 = PhotoImage(file=relative_to_assets("image_15.png"))
            self.canvas.create_image(369.0, 191.0, image=self.image_15)
            
            self.image_16 = PhotoImage(file=relative_to_assets("image_16.png"))
            self.canvas.create_image(722.0, 187.0, image=self.image_16)
            
            # Activity summary
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
        """Add all static text elements to the canvas"""
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
        self.canvas.create_text(236.0, 287.0, anchor="nw", text="Recent Activity Notifications", 
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
        
        # Analytics labels
        self.canvas.create_text(930.0, 358.0, anchor="nw", text="Alert Accuracy", 
                               fill="#000000", font=("Arial", 10))
        
        self.canvas.create_text(1076.0, 358.0, anchor="nw", text="Battery Health", 
                               fill="#000000", font=("Arial", 10))
        
        self.canvas.create_text(960.0, 506.0, anchor="nw", text="System Performance", 
                               fill="#000000", font=("Arial", 10))
        
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
    
    def add_enhanced_pie_chart(self):
        """Add larger, more appealing pie chart"""
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
            explode = (0.05, 0.05, 0.05, 0.05)  # Slightly separate slices
            
            # Create larger matplotlib figure
            fig, ax = plt.subplots(figsize=(2.2, 2.2))
            wedges, texts, autotexts = ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', 
                                            startangle=90, textprops={'fontsize': 7}, explode=explode,
                                            shadow=True)
            
            # Make percentage text bold and white
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontweight('bold')
            
            ax.axis('equal')
            fig.patch.set_facecolor('none')
            ax.set_facecolor('none')
            
            # Embed in tkinter
            chart_canvas = FigureCanvasTkAgg(fig, self)
            chart_canvas.draw()
            chart_canvas.get_tk_widget().place(x=980, y=130, width=180, height=180)
            
        except Exception as e:
            print(f"Error creating enhanced pie chart: {e}")
            self.canvas.create_text(1070, 200, text="Enhanced Chart\nLoading...", 
                                   fill="#666", font=("Arial", 8), justify="center")
    
    def add_accuracy_line_chart(self):
        """Add dynamic line graph for alert accuracy"""
        try:
            # Time points for x-axis
            time_points = list(range(len(self.accuracy_history)))
            
            # Create line chart
            fig, ax = plt.subplots(figsize=(2.0, 1.4))
            ax.plot(time_points, self.accuracy_history, marker='o', linewidth=2, 
                   color='#1657FF', markersize=4, markerfacecolor='#FF6B6B')
            ax.set_ylabel('Accuracy %', fontsize=8)
            ax.set_ylim(70, 100)
            ax.grid(True, alpha=0.3)
            ax.tick_params(axis='both', which='major', labelsize=7)
            fig.patch.set_facecolor('none')
            ax.set_facecolor('none')
            
            # Embed in tkinter
            chart_canvas = FigureCanvasTkAgg(fig, self)
            chart_canvas.draw()
            chart_canvas.get_tk_widget().place(x=980, y=320, width=160, height=112)
            
        except Exception as e:
            print(f"Error creating accuracy chart: {e}")
    
    def add_battery_health_chart(self):
        """Add battery health line graph"""
        try:
            # Battery history (simulate recent values)
            battery_history = [min(100, self.battery_percentage + i) for i in range(-9, 1)]
            time_points = list(range(len(battery_history)))
            
            # Create battery health chart
            fig, ax = plt.subplots(figsize=(2.0, 1.2))
            ax.plot(time_points, battery_history, marker='s', linewidth=2, 
                   color='#4ECDC4', markersize=3)
            ax.set_ylabel('Battery %', fontsize=8)
            ax.set_ylim(0, 100)
            ax.grid(True, alpha=0.3)
            ax.tick_params(axis='both', which='major', labelsize=7)
            fig.patch.set_facecolor('none')
            ax.set_facecolor('none')
            
            # Color code based on battery level
            if self.battery_percentage < 20:
                ax.plot(time_points, battery_history, color='#FF4444')
            elif self.battery_percentage < 50:
                ax.plot(time_points, battery_history, color='#FFAA44')
            
            # Embed in tkinter
            chart_canvas = FigureCanvasTkAgg(fig, self)
            chart_canvas.draw()
            chart_canvas.get_tk_widget().place(x=980, y=520, width=160, height=96)
            
        except Exception as e:
            print(f"Error creating battery health chart: {e}")
    
    def add_view_all_button(self):
        """Enhanced View All button with notification count"""
        view_all_btn = tk.Button(
            self,
            text="View All Alerts",
            fg="#1657FF",
            bd=0,
            font=("Arial", 11, "bold"),
            cursor="hand2",
            command=self.view_all_notifications
        )
        view_all_btn.place(x=743, y=336)
    
    def view_all_notifications(self):
        """Mark notifications as read and go to alerts page"""
        # Mark all notifications as read
        for notification in self.notifications:
            notification["read"] = True
        self.unread_count = 0
        
        # Go to alerts page
        self.controller.show_page('Alerts')
    
    def increment_logout_count(self):
        """Increment logout counter"""
        self.logout_count += 1
        self.add_notification(f"User session ended (#{self.logout_count})")
        print(f"User logout count: {self.logout_count}")


# Enhanced fake sensor with more realistic patterns
class FakeSensorForTesting:
    def __init__(self):
        self.battery = 85
        self.status_cycle = 0
        self.alert_count = 0
        self.states = ["Alert", "Alert", "Alert", "Awake", "Tired", "Drowsy"]  # Weighted toward alert
        
    def get_drowsiness_level(self):
        # Cycle through states more realistically
        self.status_cycle += 1
        if self.status_cycle % 20 == 0:  # Change state every 40 seconds (20 * 2-second updates)
            return random.choice(["Drowsy", "Tired"])
        elif self.status_cycle % 10 == 0:  # Change to awake occasionally
            return "Awake"
        else:
            return "Alert"  # Mostly alert
        
    def get_battery_level(self):
        self.battery -= random.uniform(0.05, 0.15)  # More realistic battery drain
        if self.battery < 15:
            self.battery = random.randint(80, 100)  # Simulate recharging
        return int(self.battery)
    
    def get_new_alerts(self):
        # Create alerts when drowsy state is detected
        current_state = self.get_drowsiness_level()
        if current_state in ["Drowsy", "Tired"] and random.randint(1, 10) == 1:
            self.alert_count += 1
            return [{
                "title": f"Drowsiness Alert #{self.alert_count:03d}",
                "username": "TestUser",
                "condition": f"{current_state} state detected during simulation",
                "action": "Alert notification sent to dashboard",
                "response": "Monitoring user response",
                "date": datetime.now().strftime("%Y-%m-%d %H:%M")
            }]
        return []
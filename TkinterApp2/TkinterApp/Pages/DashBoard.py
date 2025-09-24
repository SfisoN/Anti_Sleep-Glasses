from pathlib import Path
import tkinter as tk
from tkinter import Canvas, Entry, Button, PhotoImage
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = Path(__file__).parent.parent / "Assets/Dashboard"

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

class Dashboard(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#D0DFFF")
        self.controller = controller
        
        # Dynamic data variables (TODO: Connect to IoT glasses)
        self.drowsiness_level = "Drowsy"  # TODO: Get from glasses sensor
        self.battery_percentage = 78      # TODO: Get from glasses battery
        self.logout_count = 0            # Track application logouts
        
        # Canvas
        canvas = Canvas(
            self,
            bg="#D0DFFF",
            height=699,
            width=1200,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        canvas.place(x=0, y=0)
        
        # Load all images
        self.load_images(canvas)
        
        # Add all text elements
        self.add_text_elements(canvas)
        
        # Add entry field
        self.add_entry_field(canvas)
        
        # Add dynamic charts
        self.add_pie_chart(canvas)
        self.add_line_chart(canvas)
        
        # Make View All clickable
        self.add_view_all_button(canvas)
        
    def load_images(self, canvas):
        """Load and place all images"""
        try:
            # Sidebar icon
            self.image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
            canvas.create_image(98.0, 349.0, image=self.image_1)
            
            # Navigation icons
            self.image_2 = PhotoImage(file=relative_to_assets("image_2.png"))
            canvas.create_image(27.0, 213.0, image=self.image_2)
            
            self.image_3 = PhotoImage(file=relative_to_assets("image_3.png"))
            canvas.create_image(29.0, 101.0, image=self.image_3)
            
            self.image_4 = PhotoImage(file=relative_to_assets("image_4.png"))
            canvas.create_image(28.0, 23.0, image=self.image_4)
            
            self.image_5 = PhotoImage(file=relative_to_assets("image_5.png"))
            canvas.create_image(28.0, 157.0, image=self.image_5)
            
            self.image_6 = PhotoImage(file=relative_to_assets("image_6.png"))
            canvas.create_image(26.0, 456.0, image=self.image_6)
            
            # Top bar icons
            self.image_7 = PhotoImage(file=relative_to_assets("image_7.png"))
            canvas.create_image(722.0, 26.0, image=self.image_7)
            
            self.image_8 = PhotoImage(file=relative_to_assets("image_8.png"))
            canvas.create_image(963.0, 27.0, image=self.image_8)
            
            self.image_9 = PhotoImage(file=relative_to_assets("image_9.png"))
            canvas.create_image(902.0, 27.0, image=self.image_9)
            
            self.image_10 = PhotoImage(file=relative_to_assets("image_10.png"))
            canvas.create_image(930.0, 27.0, image=self.image_10)
            
            # Breadcrumb icons
            self.image_11 = PhotoImage(file=relative_to_assets("image_11.png"))
            canvas.create_image(243.0, 33.0, image=self.image_11)
            
            self.image_12 = PhotoImage(file=relative_to_assets("image_12.png"))
            canvas.create_image(275.0, 33.0, image=self.image_12)
            
            # Dashboard content images
            self.image_13 = PhotoImage(file=relative_to_assets("image_13.png"))
            canvas.create_image(372.0, 181.0, image=self.image_13)
            
            self.image_14 = PhotoImage(file=relative_to_assets("image_14.png"))
            canvas.create_image(722.0, 180.0, image=self.image_14)
            
            self.image_15 = PhotoImage(file=relative_to_assets("image_15.png"))
            canvas.create_image(369.0, 191.0, image=self.image_15)
            
            self.image_16 = PhotoImage(file=relative_to_assets("image_16.png"))
            canvas.create_image(722.0, 187.0, image=self.image_16)
            
            # Activity summary
            self.image_17 = PhotoImage(file=relative_to_assets("image_17.png"))
            canvas.create_image(538.0, 427.0, image=self.image_17)
            
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
                    canvas.create_image(*positions[i], image=getattr(self, img_attr))
                    
        except Exception as e:
            print(f"Error loading images: {e}")
    
    def add_text_elements(self, canvas):
        """Add all text elements to the canvas with consistent fonts"""
        # App title - consistent across all pages
        canvas.create_text(54.0, 8.0, anchor="nw", text="NeuroLens", 
                          fill="#2C2745", font=("Arial", 18, "bold"))
        
        # Sidebar navigation - consistent
        canvas.create_text(53.0, 91.0, anchor="nw", text="DashBoard", 
                          fill="#B9C0DE", font=("Arial", 12))
        canvas.create_text(53.0, 147.0, anchor="nw", text="Alerts", 
                          fill="#B9C0DE", font=("Arial", 12))
        canvas.create_text(54.0, 205.0, anchor="nw", text="Help/Info", 
                          fill="#B9C0DE", font=("Arial", 12))
        canvas.create_text(53.0, 450.0, anchor="nw", text="Log Out", 
                          fill="#B9C0DE", font=("Arial", 12))
        
        # Breadcrumb - consistent
        canvas.create_text(294.0, 24.0, anchor="nw", text="DashBoard  /    Default", 
                          fill="#1657FF", font=("Arial", 11))
        
        # Main content - Dynamic drowsiness level
        canvas.create_text(289.0, 121.0, anchor="nw", text="Drowsiness Level", 
                          fill="#FFFFFF", font=("Arial", 16, "bold"))
        canvas.create_text(337.0, 178.0, anchor="nw", text=self.drowsiness_level, 
                          fill="#FFFFFF", font=("Arial", 14))
        
        # Dynamic battery percentage
        canvas.create_text(681.0, 115.0, anchor="nw", text="Battery", 
                          fill="#FFFFFF", font=("Arial", 16, "bold"))
        canvas.create_text(697.0, 221.0, anchor="nw", text=f"{self.battery_percentage}%", 
                          fill="#FFFFFF", font=("Arial", 16))
        
        # Recent Activity
        canvas.create_text(236.0, 287.0, anchor="nw", text="Recent Activity Summary", 
                          fill="#353E6C", font=("Arial", 14, "bold"))
        canvas.create_text(281.0, 344.0, anchor="nw", text="LunaWolf47", 
                          fill="#000000", font=("Arial", 11))
        
        # Time filters
        canvas.create_text(248.0, 380.0, anchor="nw", text="Today", 
                          fill="#000000", font=("Arial", 10))
        canvas.create_text(295.0, 380.0, anchor="nw", text="This Week", 
                          fill="#000000", font=("Arial", 10))
        
        # Activity entries - TODO: Make dynamic from glasses data
        activities = [
            "Drowsiness Detected 14:52 pm",  # TODO: Get from glasses
            "Drowsiness Detected 14:30 pm",  # TODO: Get from glasses
            "Blinked 23/min at 14:12pm",     # TODO: Get from glasses
            "Exported dataset at 9:00am"     # TODO: Track app actions
        ]
        
        for i, activity in enumerate(activities):
            canvas.create_text(248.0, 403.0 + (i * 20), anchor="nw", text=activity,
                              fill="#000000", font=("Arial", 10))
        
        # Unread indicators - TODO: Track read status
        unread_positions = [403, 420, 441]
        for y_pos in unread_positions:
            canvas.create_text(707.0, y_pos, anchor="nw", text="Unread", 
                              fill="#FF0101", font=("Arial", 9))
        
        # Statistics section
        canvas.create_text(932.0, 67.0, anchor="nw", text="Statistics", 
                          fill="#353E6C", font=("Arial", 14, "bold"))
        canvas.create_text(953.0, 121.0, anchor="nw", text="Drowsiness Event Breakdown", 
                          fill="#000000", font=("Arial", 10))
        
        # Dynamic statistics - TODO: Calculate from glasses data
        canvas.create_text(930.0, 358.0, anchor="nw", text="Alert Accuracy", 
                          fill="#000000", font=("Arial", 10))
        canvas.create_text(930.0, 400.0, anchor="nw", text="86%",  # TODO: Calculate accuracy
                          fill="#000000", font=("Arial", 16, "bold"))
        
        canvas.create_text(1076.0, 358.0, anchor="nw", text="Weekly Trend", 
                          fill="#000000", font=("Arial", 10))
        canvas.create_text(1065.0, 392.0, anchor="nw", text="+34%",  # TODO: Calculate trend
                          fill="#000000", font=("Arial", 16, "bold"))
        
        canvas.create_text(960.0, 506.0, anchor="nw", text="Monthly Drowsiness Events", 
                          fill="#000000", font=("Arial", 10))
        
        # Rankings section
        canvas.create_text(236.0, 547.0, anchor="nw", text="Rankings", 
                          fill="#353E6C", font=("Arial", 14, "bold"))
        
        # Dynamic statistics cards
        stats = [
            ("Fully Asleep Count", "4", 596, 622),    # TODO: Get from glasses
            ("Blink Count", "52", 595, 620),          # TODO: Get from glasses  
            ("Times User Left", f"{self.logout_count}", 586, 624)  # Dynamic logout count
        ]
        
        x_positions = [248, 471, 692]
        for i, (label, value, label_y, value_y) in enumerate(stats):
            canvas.create_text(x_positions[i], label_y, anchor="nw", text=label, 
                              fill="#FFFFFF", font=("Arial", 10))
            canvas.create_text(x_positions[i] + 5, value_y, anchor="nw", text=value, 
                              fill="#FFFFFF", font=("Arial", 16, "bold"))
        
        # User indicator rectangle
        canvas.create_rectangle(251.0, 342.0, 271.0, 362.0, fill="#FFFFFF", outline="")
    
    def add_entry_field(self, canvas):
        """Add the search entry field"""
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
        except Exception as e:
            print(f"Error creating entry field: {e}")
    
    def add_pie_chart(self, canvas):
        """Add pie chart for drowsiness event breakdown"""
        # TODO: Replace with real data from glasses
        try:
            # Sample data - replace with actual data
            labels = ['Drowsy', 'Alert', 'Micro-sleep', 'Normal']
            sizes = [25, 45, 15, 15]  # TODO: Calculate from glasses data
            colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4']
            
            # Create matplotlib figure with transparent background
            fig, ax = plt.subplots(figsize=(1.8, 1.8))
            ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', 
                   startangle=90, textprops={'fontsize': 6})
            ax.axis('equal')
            fig.patch.set_facecolor('none')  # Transparent background
            ax.set_facecolor('none')  # Transparent plot area
            
            # Embed in tkinter
            chart_canvas = FigureCanvasTkAgg(fig, self)
            chart_canvas.draw()
            chart_canvas.get_tk_widget().place(x=1000, y=140, width=140, height=140)
            
        except Exception as e:
            print(f"Error creating pie chart: {e}")
            # Fallback text
            canvas.create_text(1070, 200, text="Pie Chart\n(TODO: Add chart)", 
                              fill="#666", font=("Arial", 8), justify="center")
    
    def add_line_chart(self, canvas):
        """Add line chart for monthly drowsiness events with transparent background"""
        # TODO: Replace with real monthly data from glasses
        try:
            # Sample data - replace with actual monthly data
            months = ['Nov', 'Dec']
            events = [15, 8]  # TODO: Get from glasses database
            
            # Create matplotlib figure with transparent background
            fig, ax = plt.subplots(figsize=(1.8, 1.2))
            ax.plot(months, events, marker='o', linewidth=2, color='#1657FF')
            ax.set_ylabel('Events', fontsize=8)
            ax.tick_params(axis='both', which='major', labelsize=7)
            fig.patch.set_facecolor('none')  # Transparent background like pie chart
            ax.set_facecolor('none')  # Transparent plot area
            
            # Embed in tkinter
            chart_canvas = FigureCanvasTkAgg(fig, self)
            chart_canvas.draw()
            chart_canvas.get_tk_widget().place(x=1000, y=530, width=140, height=90)
            
        except Exception as e:
            print(f"Error creating line chart: {e}")
            # Fallback text
            canvas.create_text(1070, 580, text="Line Chart\n(TODO: Add chart)", 
                              fill="#666", font=("Arial", 8), justify="center")
    
    def add_view_all_button(self, canvas):
        """Make View All clickable to go to Alerts page"""
        view_all_btn = tk.Button(
            self,
            text="View All",
            fg="#1657FF",
            bd=0,
            font=("Arial", 11),
            cursor="hand2",
            command=lambda: self.controller.show_page('Alerts')
        )
        view_all_btn.place(x=763, y=336)
    
    def increment_logout_count(self):
        """Increment logout counter - call this when user logs out"""
        self.logout_count += 1
        # TODO: Save to database/file for persistence
        print(f"User logout count: {self.logout_count}")
    
    def update_drowsiness_level(self, level):
        """Update drowsiness level from glasses data"""
        self.drowsiness_level = level
        # TODO: Refresh the display
    
    def update_battery_level(self, percentage):
        """Update battery percentage from glasses"""
        self.battery_percentage = percentage
        # TODO: Refresh the display


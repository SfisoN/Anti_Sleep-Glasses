from pathlib import Path
import tkinter as tk
from tkinter import Canvas, PhotoImage, Text, Scrollbar, Entry

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = Path(__file__).parent.parent / "Assets/Dashboard"  # Use Dashboard assets

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

class Help(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#D0DFFF")
        self.controller = controller
        
        self.setup_canvas()
        self.add_help_content()
        
    def setup_canvas(self):
        """Setup the main canvas with all dashboard elements"""
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
        
        # Load all the same images as dashboard
        self.load_images()
        self.add_navigation_elements()
        self.add_entry_field()
        
    def load_images(self):
        """Load all dashboard images for consistency"""
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
                    
        except Exception as e:
            print(f"Error loading images: {e}")
    
    def add_navigation_elements(self):
        """Add all navigation elements same as dashboard"""
        # App title - CONSISTENT ACROSS ALL PAGES
        self.canvas.create_text(54.0, 8.0, anchor="nw", text="NeuroLens", 
                               fill="#2C2745", font=("Arial", 18, "bold"))
        
        # Sidebar navigation - CONSISTENT
        self.canvas.create_text(53.0, 91.0, anchor="nw", text="DashBoard", 
                               fill="#B9C0DE", font=("Arial", 12))
        self.canvas.create_text(53.0, 147.0, anchor="nw", text="Alerts", 
                               fill="#B9C0DE", font=("Arial", 12))
        self.canvas.create_text(54.0, 205.0, anchor="nw", text="Help/Info", 
                               fill="#B9C0DE", font=("Arial", 12))
        self.canvas.create_text(53.0, 450.0, anchor="nw", text="Log Out", 
                               fill="#B9C0DE", font=("Arial", 12))
        
        # Page header - CONSISTENT (changed to Help/Info)
        self.canvas.create_text(294.0, 24.0, anchor="nw", text="Help/Info  /    User Guide", 
                               fill="#1657FF", font=("Arial", 11))
    
    def add_entry_field(self):
        """Add the search entry field same as dashboard"""
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
    
    def add_help_content(self):
        """Add help content with smaller width"""
        # Help content frame - SMALLER WIDTH (reduced from 700 to 500)
        content_frame = tk.Frame(self, bg="#FFFFFF", relief="ridge", bd=1)
        content_frame.place(x=300, y=80, width=500, height=400)  # Reduced width and adjusted x position
        
        # Title - SMALLER FONT
        title_label = tk.Label(content_frame, text="NeuroLens Quick Help", 
                              font=("Arial", 16, "bold"), bg="#FFFFFF", fg="#2C2745")
        title_label.pack(pady=10)  # Reduced padding
        
        # Create text widget - SMALLER
        text_frame = tk.Frame(content_frame, bg="#FFFFFF")
        text_frame.pack(fill="both", expand=True, padx=15, pady=5)  # Reduced padding
        
        # Text widget - SMALLER FONT
        self.help_text = Text(text_frame, wrap="word", 
                             font=("Arial", 10), bg="#FFFFFF",  # Smaller font
                             fg="#2C2745", relief="flat", padx=10, pady=5,
                             height=15)  # Fixed height
        self.help_text.pack(fill="both", expand=True)
        
        # CONCISE help content
        help_content = """ABOUT NEUROLENS
NeuroLens monitors drowsiness in real-time to prevent fatigue-related incidents.

DASHBOARD
• Drowsiness Level: Current alertness status
• Battery: Device battery percentage  
• Recent Activity: Timeline of drowsiness events
• Statistics: Weekly trends and accuracy

ALERTS
• Real-time drowsiness alerts
• User response tracking
• Export functionality

ALERT TYPES
• Eyes Closed: 3+ seconds
• Head Nodding: Movement patterns
• Blink Rate: Low frequency detection
• Micro-sleep: Brief sleep episodes

TIPS
• Ensure good lighting
• Take breaks when alerted
• Review data for patterns

SUPPORT
Email: support@neurolens.com
Phone: +27 21 555 1234

Version: 1.0.0 (2025)"""
        
        self.help_text.insert("1.0", help_content)
        self.help_text.config(state="disabled")  # Make read-only
        
        # Add scrollbar
        scrollbar = Scrollbar(text_frame, command=self.help_text.yview)
        scrollbar.pack(side="right", fill="y")
        self.help_text.config(yscrollcommand=scrollbar.set)
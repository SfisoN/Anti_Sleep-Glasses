# NeuroLens - Anti-Sleep Glasses Dashboard

A comprehensive desktop application for monitoring drowsiness and managing anti-sleep smart glasses data in real-time.

![NeuroLens Dashboard](https://img.shields.io/badge/Status-In%20Development-yellow)
![Python](https://img.shields.io/badge/Python-3.7%2B-blue)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/yourusername/NeuroLens.git
cd NeuroLens

# Install dependencies
pip install matplotlib numpy

# Run the application
python App.py
📁 Project Structure
text
NeuroLens/
│
├── App.py                 # Main application entry point
├── sensor_monitor.py      # Hardware/simulation sensor interface
├── Pages/                 # Application pages/screens
│   ├── DashBoard.py       # Main dashboard with real-time data
│   ├── Alerts.py          # Alerts management and history
│   └── Help.py            # Help and user guide
├── Assets/                # UI Assets and images
│   ├── dashboard/         # Dashboard page assets
│   ├── alerts/            # Alerts page assets  
│   └── help/              # Help page assets
└── README.md              # This file
🎯 Features
✅ Implemented Features
Real-time Dashboard: Drowsiness level, battery status, session timer

Alert Management: History tracking, search, CSV export

Responsive UI: Dark theme with consistent navigation

Hardware Simulation: Fake sensor data for testing

Multi-page Navigation: Smooth transitions between sections

🔄 In Development
IoT glasses hardware integration

Real Bluetooth/WiFi connectivity

Advanced analytics and reporting

🖥️ UI Components
Dashboard (Pages/DashBoard.py)
Drowsiness Level: 1-5 scale with color-coded status

Battery Monitoring: Real-time percentage display

Session Timer: Active usage tracking

Performance Analytics: Matplotlib charts

Device Connectivity: Status indicators

Recent Alerts: Live notification feed

Alerts Management (Pages/Alerts.py)
Alert History: Timestamped event logging

Search Functionality: Filter by type, date, user

CSV Export: Data backup and analysis

Live Updates: Real-time alert streaming

Help System (Pages/Help.py)
User Guide: Comprehensive documentation

Troubleshooting: Common issues and solutions

Interactive Search: Content filtering

🛠️ Installation & Setup
Prerequisites
Python 3.7 or higher

pip package manager

Dependencies
bash
pip install -r requirements.txt
Required Packages:

matplotlib - Data visualization charts

numpy - Numerical computations (for advanced analytics)

🚦 Current Status & Known Issues
✅ Working Features
Main application framework

Page navigation system

Dashboard with simulated data

Alert management system

CSV export functionality

Responsive sidebar navigation

⚠️ Known Design Issues
Navigation & Layout:

Sidebar button alignment needs refinement

Some image assets not properly sized

Font consistency across pages

Functional Gaps:

Help page scrollbar sizing

Search functionality needs UI feedback

Export button visibility in alerts page

Hardware Integration:

Currently using simulated sensor data

Bluetooth/WiFi connectivity pending

Real-time glasses integration needed

🔧 Immediate Fixes Needed
Image Asset Sizing: Ensure consistent image dimensions

Font Consistency: Standardize font families and sizes

Button Visibility: Improve contrast and positioning

Scrollbar Fix: Proper sizing in help page

🔌 Hardware Integration
Current Simulation
python
# Fake sensor data for development
self.drowsiness_level = random.randint(1, 5)
self.battery_percentage = 78  # Simulated
self.blink_count = random.randint(0, 10)
Planned IoT Integration
python
# Target hardware interface
class GlassesInterface:
    def get_drowsiness_level():  # From EEG/eye tracking
    def get_battery_level():     # From glasses battery
    def get_blink_rate():        # From camera sensor
    def send_alert():            # To vibration motor
🎨 UI/UX Design
Color Scheme
Primary: #3A404D (Dark background)

Accent: #4277FF (Blue highlights)

Text: #FFFFFF (White)

Status Indicators: #AEF5B0 (Green), #FF6B6B (Red)

Typography
Headers: Arial Bold

Body Text: Arial Regular

Navigation: SF Pro Rounded (where available)

🔄 Development Roadmap
Phase 1: UI Polish (Current)
Fix image asset sizing and positioning

Standardize font usage across pages

Improve button visibility and contrast

Resolve scrollbar issues in help page

Phase 2: Hardware Integration
Bluetooth/WiFi connectivity implementation

Real sensor data streaming

Alert system with physical feedback

Battery monitoring from actual hardware

Phase 3: Advanced Features
Multi-user support

Cloud synchronization

Advanced analytics dashboard

Mobile companion app

🐛 Troubleshooting
Common Issues
Application won't start:

bash
# Check Python version
python --version

# Install missing dependencies
pip install matplotlib numpy
Missing images/assets:

Ensure Assets folder structure matches expected paths

Check image file permissions

Navigation errors:

Verify all page files exist in Pages/ directory

Check console for specific error messages

Getting Help
Check the in-app Help section (Help.py)

Review console output for error messages

Ensure all dependencies are installed

🤝 Contributing
We welcome contributions! Please:

Fork the repository

Create a feature branch

Test your changes thoroughly

Submit a pull request

Development Setup
bash
git clone https://github.com/yourusername/NeuroLens.git
cd NeuroLens
pip install -r requirements.txt
python App.py
📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

🙏 Acknowledgments
Icons and UI elements designed for optimal drowsiness monitoring

Real-time data visualization using Matplotlib

Tkinter for cross-platform desktop compatibility

Version: 2.0.0
Last Updated: September 2025
Maintainer: NeuroLens Development Team

For support or questions, please open an issue on GitHub.

text


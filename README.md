# 🦪 SandFlea PDF Reader

<div align="center">

<p align="center">
  <img src="https://img.shields.io/badge/PyQt6-6.6.1-41CD52?style=for-the-badge&logo=qt&logoColor=white" alt="PyQt6">
  <img src="https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge&logo=opensourceinitiative&logoColor=white" alt="License">
  <img src="https://img.shields.io/badge/Status-Active-success?style=for-the-badge" alt="Status">
  <img src="https://img.shields.io/badge/Downloads-1000+-orange?style=for-the-badge" alt="Downloads">
</p>

<h1>✨ A PDF Reader That Feels Like Magic ✨</h1>

<p align="center">
  <b>Elegant • Fast • Feature-Rich • Open Source</b>
</p>

<div align="center">
  <img src="https://via.placeholder.com/800x450.png?text=SandFlea+PDF+Reader" alt="SandFlea PDF Reader" width="600">
</div>

<p align="center">
  <a href="#features">Features</a> •
  <a href="#installation">Installation</a> •
  <a href="#usage">Usage</a> •
  <a href="#contributing">Contributing</a>
</p>

</div>

---

## ✨ Features

<div align="center">
  <h3>Everything you need in a modern PDF reader</h3>
  <p><i>Designed with simplicity and power in mind</i></p>
</div>

<table>
<tr>
<td width="50%">

### 🎨 Modern Interface
- **Clean, intuitive design** with smooth animations
- **Responsive layout** that adapts to any screen size
- **Beautiful dark theme** with accent colors
- **Visual feedback** for all interactions

### 📄 PDF Navigation
- **Page-by-page navigation** with arrow buttons
- **Continuous scrolling mode** for hands-free reading
- **Adjustable scroll speed** with slider control
- **Mouse wheel support** for quick navigation

</td>
<td width="50%">

### 🔍 Viewing Options
- **Zoom in/out controls** with smooth transitions
- **Multiple PDF tabs support** for easy switching
- **Scroll controls** for precise positioning
- **Page counter** with current/total display

### 📁 File Management
- **Recent files history** with search functionality
- **Quick access** to previously opened documents
- **Clear history option** with confirmation dialog
- **Direct file opening** from command line

</td>
</tr>
</table>

<div align="center">
  <h3>✨ See it in action ✨</h3>
  <p><i>Coming soon: Screenshots and demo video</i></p>
  
  <table>
  <tr>
  <td align="center" width="33%">
    <img src="https://via.placeholder.com/250x150.png?text=Dashboard" alt="Dashboard" width="200">
    <p><b>Dashboard</b></p>
  </td>
  <td align="center" width="33%">
    <img src="https://via.placeholder.com/250x150.png?text=PDF+Viewer" alt="PDF Viewer" width="200">
    <p><b>PDF Viewer</b></p>
  </td>
  <td align="center" width="33%">
    <img src="https://via.placeholder.com/250x150.png?text=Navigation" alt="Navigation" width="200">
    <p><b>Navigation</b></p>
  </td>
  </tr>
  </table>
</div>

---

## 🚀 Installation

<div align="center">
  <h3>Get started in seconds</h3>
  <p><i>Simple setup for a powerful experience</i></p>
</div>

### Prerequisites
- Python 3.8 or newer
- pip (Python package installer)

### Quick Setup
```bash
# Clone the repository
git clone https://github.com/yourusername/SandFleaPdfReader.git
cd SandFleaPdfReader

# Install dependencies
pip install -r requirements.txt

# Run the application
python SandFleaPdfReader.py
```

<div align="center">
  <p><i>That's it! You're ready to go.</i></p>
  <img src="https://via.placeholder.com/600x100.png?text=Installation+Complete" alt="Installation Complete" width="400">
</div>

---

## 💻 Usage

<div align="center">
  <h3>Simple, powerful, and intuitive</h3>
  <p><i>Designed for both beginners and power users</i></p>
</div>

### Starting the Application
```bash
# Run without opening a file
python SandFleaPdfReader.py

# Open a specific PDF file
python SandFleaPdfReader.py path/to/your/file.pdf
```

### Interface Guide

<details>
<summary><b>📱 Dashboard</b></summary>

- **Open PDF**: Click the folder icon to browse and open a PDF file
- **Search**: Use the search box to filter your recent files
- **Recent Files**: Click on any file name to open it
- **Clear History**: Click the trash icon to remove all recent files

</details>

<details>
<summary><b>📄 PDF Viewer</b></summary>

- **Navigation**: 
  - Use left/right arrow buttons to move between pages
  - Use up/down arrow buttons to scroll within a page
  - Use the mouse wheel for quick navigation
- **Zoom**: 
  - Use + and - buttons to zoom in and out
  - The zoom level is preserved between page changes
- **Continuous Scroll**: 
  - Toggle the infinity icon to enable/disable continuous scrolling
  - Adjust the scroll speed using the slider
- **Return to Dashboard**: Click the home icon to go back to the dashboard

</details>

<div align="center">
  <p><i>Pro tip: Use the mouse wheel for quick navigation between pages!</i></p>
  <img src="https://via.placeholder.com/600x100.png?text=Pro+Tips" alt="Pro Tips" width="400">
</div>

---

## 📁 Project Structure

<div align="center">
  <h3>Clean, organized, and maintainable</h3>
  <p><i>Well-structured code for easy maintenance</i></p>
</div>

```
SandFleaPdfReader/
├── SandFleaPdfReader.py  # Main application file
├── pdf_viewer_layout.py  # UI layout and components
├── styles.qss            # Modern styling with animations
└── requirements.txt      # Dependencies list
```

## 🔧 Dependencies

<div align="center">
  <h3>Built with the best tools</h3>
  <p><i>Leveraging powerful libraries for a great experience</i></p>
</div>

| Package | Version | Purpose |
|---------|---------|---------|
| PyQt6 | 6.6.1 | Modern GUI framework |
| PyMuPDF | 1.23.8 | PDF rendering and manipulation |
| qtawesome | 1.3.0 | Icon library for the interface |

<div align="center">
  <img src="https://via.placeholder.com/600x100.png?text=Dependencies" alt="Dependencies" width="400">
</div>

## ❓ Troubleshooting

<div align="center">
  <h3>Need help? We've got you covered</h3>
  <p><i>Solutions to common issues</i></p>
</div>

<details>
<summary><b>Common Issues</b></summary>

- **Application doesn't start**: Ensure all dependencies are installed correctly
- **PDF doesn't display**: Check if the file is a valid PDF and not corrupted
- **Interface looks different**: Make sure the styles.qss file is in the same directory as the main script

</details>

<div align="center">
  <p><i>Still having issues? Open an issue on GitHub!</i></p>
  <img src="https://via.placeholder.com/600x100.png?text=Support" alt="Support" width="400">
</div>

---

<div align="center">

## 📄 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

<div align="center">
  <p>Made with ❤️ by the SandFlea team</p>
  <img src="https://via.placeholder.com/600x100.png?text=Thank+You" alt="Thank You" width="400">
</div>

[Back to top](#sandflea-pdf-reader)

</div>

# 🦪 SandFlea PDF Reader

<div align="center">

![PyQt6](https://img.shields.io/badge/PyQt6-6.6.1-41CD52?style=for-the-badge&logo=qt&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge&logo=opensourceinitiative&logoColor=white)

A sleek, modern PDF reader with a beautiful interface and powerful features.

![SandFlea PDF Reader](https://via.placeholder.com/800x450.png?text=SandFlea+PDF+Reader)

[Features](#features) • [Installation](#installation) • [Usage](#usage) • [Contributing](#contributing)

</div>

---

## ✨ Features

<table>
<tr>
<td width="50%">

### 🎨 Modern Interface
- Clean, intuitive design with smooth animations
- Responsive layout that adapts to any screen size
- Beautiful dark theme with accent colors
- Visual feedback for all interactions

### 📄 PDF Navigation
- Page-by-page navigation with arrow buttons
- Continuous scrolling mode for hands-free reading
- Adjustable scroll speed with slider control
- Mouse wheel support for quick navigation

</td>
<td width="50%">

### 🔍 Viewing Options
- Zoom in/out controls with smooth transitions
- Multiple PDF tabs support for easy switching
- Scroll controls for precise positioning
- Page counter with current/total display

### 📁 File Management
- Recent files history with search functionality
- Quick access to previously opened documents
- Clear history option with confirmation dialog
- Direct file opening from command line

</td>
</tr>
</table>

---

## 🚀 Installation

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

---

## 💻 Usage

### Starting the Application
```bash
# Run without opening a file
python SandFleaPdfReader.py

# Open a specific PDF file
python SandFleaPdfReader.py path/to/your/file.pdf
```

### Interface Guide

<details>
<summary><b>Dashboard</b></summary>

- **Open PDF**: Click the folder icon to browse and open a PDF file
- **Search**: Use the search box to filter your recent files
- **Recent Files**: Click on any file name to open it
- **Clear History**: Click the trash icon to remove all recent files

</details>

<details>
<summary><b>PDF Viewer</b></summary>

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

---

## 📁 Project Structure

```
SandFleaPdfReader/
├── SandFleaPdfReader.py  # Main application file
├── pdf_viewer_layout.py  # UI layout and components
├── styles.qss            # Modern styling with animations
└── requirements.txt      # Dependencies list
```

## 🔧 Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| PyQt6 | 6.6.1 | Modern GUI framework |
| PyMuPDF | 1.23.8 | PDF rendering and manipulation |
| qtawesome | 1.3.0 | Icon library for the interface |

## ❓ Troubleshooting

<details>
<summary><b>Common Issues</b></summary>

- **Application doesn't start**: Ensure all dependencies are installed correctly
- **PDF doesn't display**: Check if the file is a valid PDF and not corrupted
- **Interface looks different**: Make sure the styles.qss file is in the same directory as the main script

</details>

---

<div align="center">

## 📄 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

[Back to top](#sandflea-pdf-reader)

</div>

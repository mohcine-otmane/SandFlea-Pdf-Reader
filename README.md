# SandFlea PDF Reader

A modern, feature-rich PDF reader built with PyQt6, offering a sleek interface and powerful functionality.

![SandFlea PDF Reader](https://via.placeholder.com/800x450.png?text=SandFlea+PDF+Reader)

## Features

- **Modern Interface**: Clean, intuitive design with smooth animations and visual feedback
- **PDF Navigation**: 
  - Page-by-page navigation with arrow buttons
  - Continuous scrolling mode for hands-free reading
  - Adjustable scroll speed
  - Mouse wheel support for quick navigation
- **Viewing Options**:
  - Zoom in/out controls
  - Multiple PDF tabs support
  - Scroll controls for precise positioning
- **File Management**:
  - Recent files history with search functionality
  - Quick access to previously opened documents
  - Clear history option
- **User Experience**:
  - Responsive layout that adapts to window size
  - Tooltips for all controls
  - Visual feedback for all actions

## Installation

### Prerequisites
- Python 3.8 or newer
- pip (Python package installer)

### Setup
1. Clone this repository or download the files
2. Navigate to the project directory
3. Install the required packages:
```bash
pip install -r requirements.txt
```

## Usage

### Starting the Application
Run the application from the command line:
```bash
python SandFleaPdfReader.py
```

You can also open a PDF file directly:
```bash
python SandFleaPdfReader.py path/to/your/file.pdf
```

### Interface Guide

#### Dashboard
- **Open PDF**: Click the folder icon to browse and open a PDF file
- **Search**: Use the search box to filter your recent files
- **Recent Files**: Click on any file name to open it
- **Clear History**: Click the trash icon to remove all recent files

#### PDF Viewer
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

## Project Structure

- `SandFleaPdfReader.py`: Main application file containing the PDF viewer logic
- `pdf_viewer_layout.py`: UI layout and component definitions
- `styles.qss`: Application styling with modern visual effects
- `requirements.txt`: Required Python packages and versions

## Dependencies

- **PyQt6**: Modern GUI framework
- **PyMuPDF**: PDF rendering and manipulation
- **qtawesome**: Icon library for the interface

## Troubleshooting

- **Application doesn't start**: Ensure all dependencies are installed correctly
- **PDF doesn't display**: Check if the file is a valid PDF and not corrupted
- **Interface looks different**: Make sure the styles.qss file is in the same directory as the main script

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

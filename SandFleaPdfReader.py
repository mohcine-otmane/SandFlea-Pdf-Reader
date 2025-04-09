import sys
import fitz
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QMessageBox, QFileDialog)
from PyQt6.QtCore import Qt, QTimer, QSettings, QSize
from PyQt6.QtGui import QPixmap, QWheelEvent, QResizeEvent
from pdf_viewer_layout import PDFViewerLayout

class PDFViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.current_pdf = None
        self.current_page = 0
        self.zoom_factor = 1.0
        self.continuous_scroll = False
        self.scroll_speed = 50
        self.scroll_threshold = 0
        
        # Setup settings
        self.settings = QSettings('SandFlea', 'PDF Reader')
        self.recent_files = self.settings.value('recent_files', [])
        
        # Setup scroll timer
        self.scroll_timer = QTimer()
        self.scroll_timer.timeout.connect(self.reset_scroll_threshold)
        
        # Update recent files list
        self.layout.update_recent_files_list(self.recent_files)
        
        # Install event filter for scroll handling
        self.layout.current_tab.scroll_area.installEventFilter(self)

    def init_ui(self):
        self.setWindowTitle('SandFlea PDF Reader')
        # Use a more standard window size that works on most screens
        self.setGeometry(100, 100, 800, 600)
        # Set minimum size to prevent layout issues
        self.setMinimumSize(800, 600)

        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Initialize layout
        self.layout = PDFViewerLayout(central_widget)
        
        # Connect signals
        self.connect_signals()
        
        # Load stylesheet
        self.load_stylesheet()

    def connect_signals(self):
        slots = {
            'prev_page': self.prev_page,
            'next_page': self.next_page,
            'zoom_in': self.zoom_in,
            'zoom_out': self.zoom_out,
            'scroll_up': self.scroll_up,
            'scroll_down': self.scroll_down,
            'toggle_continuous_scroll': self.toggle_continuous_scroll,
            'update_scroll_speed': self.update_scroll_speed,
            'show_dashboard': self.show_dashboard,
            'clear_recent_files': self.clear_recent_files,
            'filter_recent_files': self.filter_recent_files,
            'open_pdf': self.show_open_dialog
        }
        self.layout.connect_signals(slots)

    def load_stylesheet(self):
        try:
            # Get the absolute path to the stylesheet
            stylesheet_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'styles.qss')
            with open(stylesheet_path, 'r') as f:
                self.setStyleSheet(f.read())
        except Exception as e:
            print(f"Error loading stylesheet: {e}")

    def show_dashboard(self):
        self.layout.show_dashboard()
        self.layout.dashboard_button.setEnabled(False)
        self.layout.prev_button.setEnabled(False)
        self.layout.next_button.setEnabled(False)
        self.layout.zoom_in_button.setEnabled(False)
        self.layout.zoom_out_button.setEnabled(False)
        self.layout.scroll_up_button.setEnabled(False)
        self.layout.scroll_down_button.setEnabled(False)
        self.layout.continuous_scroll_button.setEnabled(False)
        self.layout.scroll_speed_slider.setEnabled(False)

    def show_pdf_viewer(self):
        self.layout.show_pdf_viewer()
        self.layout.dashboard_button.setEnabled(True)
        self.layout.prev_button.setEnabled(True)
        self.layout.next_button.setEnabled(True)
        self.layout.zoom_in_button.setEnabled(True)
        self.layout.zoom_out_button.setEnabled(True)
        self.layout.scroll_up_button.setEnabled(True)
        self.layout.scroll_down_button.setEnabled(True)
        self.layout.continuous_scroll_button.setEnabled(True)
        self.layout.scroll_speed_slider.setEnabled(True)

    def open_pdf(self, filename):
        try:
            self.current_pdf = fitz.open(filename)
            self.current_page = 0
            self.layout.add_pdf_tab(filename)
            self.show_pdf_viewer()
            self.update_pdf_display()
            self.add_to_recent_files(filename)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not open PDF file: {str(e)}")

    def add_to_recent_files(self, filename):
        if filename in self.recent_files:
            self.recent_files.remove(filename)
        self.recent_files.insert(0, filename)
        self.recent_files = self.recent_files[:10]  # Keep only 10 most recent
        self.settings.setValue('recent_files', self.recent_files)
        self.layout.update_recent_files_list(self.recent_files)

    def update_pdf_display(self):
        if not self.current_pdf:
            return

        # Update page counter
        total_pages = len(self.current_pdf)
        self.layout.update_page_display(self.current_page + 1, total_pages)

        # Get the current page
        page = self.current_pdf[self.current_page]
        
        # Apply zoom
        zoom = self.zoom_factor
        mat = fitz.Matrix(zoom, zoom)
        
        # Render page
        pix = page.get_pixmap(matrix=mat)
        
        # Convert to QPixmap and display
        img_data = pix.tobytes("ppm")
        qpixmap = QPixmap()
        qpixmap.loadFromData(img_data)
        
        # Set the pixmap to the label
        self.layout.set_pdf_content(qpixmap)

    def prev_page(self):
        if self.current_pdf and self.current_page > 0:
            self.current_page -= 1
            self.update_pdf_display()

    def next_page(self):
        if self.current_pdf and self.current_page < len(self.current_pdf) - 1:
            self.current_page += 1
            self.update_pdf_display()

    def zoom_in(self):
        self.zoom_factor *= 1.2
        self.update_pdf_display()

    def zoom_out(self):
        self.zoom_factor /= 1.2
        self.update_pdf_display()

    def scroll_up(self):
        scrollbar = self.layout.current_tab.scroll_area.verticalScrollBar()
        scrollbar.setValue(scrollbar.value() - self.scroll_speed)

    def scroll_down(self):
        scrollbar = self.layout.current_tab.scroll_area.verticalScrollBar()
        scrollbar.setValue(scrollbar.value() + self.scroll_speed)

    def toggle_continuous_scroll(self, enabled):
        self.continuous_scroll = enabled
        self.settings.setValue('continuous_scroll', enabled)
        
        if self.continuous_scroll:
            self.scroll_timer.start(50)  # Update every 50ms
        else:
            self.scroll_timer.stop()

    def update_scroll_speed(self, speed):
        self.scroll_speed = speed
        self.settings.setValue('scroll_speed', speed)

    def continuous_scroll_update(self):
        if self.continuous_scroll:
            scrollbar = self.layout.current_tab.scroll_area.verticalScrollBar()
            current_value = scrollbar.value()
            max_value = scrollbar.maximum()
            
            if current_value < max_value:
                scrollbar.setValue(current_value + self.scroll_speed // 10)
            else:
                # If we reach the bottom, go to next page
                self.next_page()
                scrollbar.setValue(0)

    def clear_recent_files(self):
        reply = QMessageBox.question(
            self, 
            "Clear History", 
            "Are you sure you want to clear your recent files history?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.recent_files = []
            self.settings.setValue('recent_files', [])
            self.layout.update_recent_files_list([])

    def filter_recent_files(self, text):
        filtered = [f for f in self.recent_files if text.lower() in os.path.basename(f).lower()]
        self.layout.update_recent_files_list(filtered)

    def show_open_dialog(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Open PDF File",
            "",
            "PDF Files (*.pdf)"
        )
        
        if file_name:
            self.open_pdf(file_name)

    def eventFilter(self, obj, event):
        if obj == self.layout.current_tab.scroll_area and event.type() == QWheelEvent.Type.Wheel:
            delta = event.angleDelta().y()
            self.scroll_threshold += delta
            self.scroll_timer.start(300)
            
            if abs(self.scroll_threshold) >= 120:
                if self.scroll_threshold > 0:
                    self.prev_page()
                else:
                    self.next_page()
                
                self.scroll_threshold = 0
            return True
        return super().eventFilter(obj, event)

    def reset_scroll_threshold(self):
        self.scroll_threshold = 0

    def resizeEvent(self, event: QResizeEvent):
        """Handle window resize events"""
        super().resizeEvent(event)
        # Ensure the layout is updated when the window is resized
        if hasattr(self, 'layout'):
            self.layout.parent.updateGeometry()

def main():
    app = QApplication(sys.argv)
    viewer = PDFViewer()
    viewer.show()
    
    # Open PDF file if provided as argument
    if len(sys.argv) > 1:
        viewer.open_pdf(sys.argv[1])
    
    # Start the application event loop
    return app.exec()

if __name__ == "__main__":
    sys.exit(main()) 
import sys
import fitz
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                            QHBoxLayout, QPushButton, QFileDialog, QLabel,
                            QScrollArea, QMenu, QGridLayout, QFrame, QLineEdit,
                            QSizePolicy, QMessageBox, QTabWidget, QSlider)
from PyQt6.QtCore import Qt, QTimer, QSettings, QSize
from PyQt6.QtGui import QPixmap, QImage, QWheelEvent, QAction, QIcon, QFont, QColor, QPalette
import qtawesome as qta

class PDFTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_doc = None
        self.current_page = 0
        self.zoom_factor = 1.0
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scroll_area.setObjectName("scroll-area")
        
        self.pdf_page_label = QLabel()
        self.pdf_page_label.setObjectName("pdf-page-label")
        self.pdf_page_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.scroll_area.setWidget(self.pdf_page_label)
        
        layout.addWidget(self.scroll_area)

class PDFViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SandFlea PDF Reader")
        self.setGeometry(100, 100, 1024, 768)
        self.setWindowIcon(qta.icon('fa5s.file-pdf', color='#4361ee'))
        
        script_dir = os.path.dirname(os.path.abspath(__file__))
        style_path = os.path.join(script_dir, 'styles.qss')
        
        try:
            with open(style_path, 'r') as f:
                self.setStyleSheet(f.read())
        except FileNotFoundError:
            print("Warning: styles.qss not found. Using default styling.")
        
        self.current_doc = None
        self.current_page = 0
        self.zoom_factor = 1.0
        self.scroll_threshold = 0
        self.scroll_timer = QTimer()
        self.scroll_timer.setSingleShot(True)
        self.scroll_timer.timeout.connect(self.reset_scroll_threshold)
        
        self.settings = QSettings('SandFleaPDFReader', 'Settings')
        self.continuous_scroll = self.settings.value('continuous_scroll', False, type=bool)
        self.scroll_speed = self.settings.value('scroll_speed', 50, type=int)
        self.scroll_timer = QTimer()
        self.scroll_timer.timeout.connect(self.continuous_scroll_update)
        
        self.settings = QSettings('SandFleaPDFReader', 'RecentFiles')
        self.recent_files = self.settings.value('recent_files', [])
        if self.recent_files is None:
            self.recent_files = []
        self.max_recent_files = 10
        
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.main_layout = QVBoxLayout(self.main_widget)
        self.main_layout.setSpacing(16)
        self.main_layout.setContentsMargins(24, 24, 24, 24)
        
        self.create_toolbar()
        
        self.content_widget = QWidget()
        self.main_layout.addWidget(self.content_widget)
        
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(0)
        
        self.create_dashboard()
        
        self.tab_widget = QTabWidget()
        self.tab_widget.setObjectName("pdf-tabs")
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.close_tab)
        self.content_layout.addWidget(self.tab_widget)
        self.tab_widget.hide()
        
        self.show_dashboard()
        
    def create_toolbar(self):
        toolbar = QFrame()
        toolbar.setObjectName("toolbar")
        toolbar_layout = QHBoxLayout(toolbar)
        toolbar_layout.setSpacing(12)
        toolbar_layout.setContentsMargins(12, 8, 12, 8)
        
        left_buttons = QHBoxLayout()
        left_buttons.setSpacing(8)
        
        self.open_button = QPushButton()
        self.open_button.setObjectName("icon-button")
        open_icon = qta.icon('fa5s.folder-open', color='white')
        self.open_button.setIcon(open_icon)
        self.open_button.setIconSize(QSize(18, 18))
        self.open_button.setToolTip("Open PDF")
        self.open_button.clicked.connect(self.show_open_dialog)
        left_buttons.addWidget(self.open_button)
        
        self.dashboard_button = QPushButton()
        self.dashboard_button.setObjectName("icon-button")
        dashboard_icon = qta.icon('fa5s.home', color='white')
        self.dashboard_button.setIcon(dashboard_icon)
        self.dashboard_button.setIconSize(QSize(18, 18))
        self.dashboard_button.setToolTip("Dashboard")
        self.dashboard_button.clicked.connect(self.show_dashboard)
        left_buttons.addWidget(self.dashboard_button)
        
        toolbar_layout.addLayout(left_buttons)
        toolbar_layout.addStretch(1)
        
        self.pdf_controls = QFrame()
        self.pdf_controls.setObjectName("pdf-controls")
        pdf_controls_layout = QHBoxLayout(self.pdf_controls)
        pdf_controls_layout.setSpacing(12)
        pdf_controls_layout.setContentsMargins(0, 0, 0, 0)
        
        nav_buttons = QHBoxLayout()
        nav_buttons.setSpacing(8)
        
        self.prev_button = QPushButton()
        self.prev_button.setObjectName("icon-button")
        prev_icon = qta.icon('fa5s.chevron-left', color='white')
        self.prev_button.setIcon(prev_icon)
        self.prev_button.setIconSize(QSize(18, 18))
        self.prev_button.setToolTip("Previous Page")
        self.prev_button.clicked.connect(self.prev_page)
        nav_buttons.addWidget(self.prev_button)
        
        self.next_button = QPushButton()
        self.next_button.setObjectName("icon-button")
        next_icon = qta.icon('fa5s.chevron-right', color='white')
        self.next_button.setIcon(next_icon)
        self.next_button.setIconSize(QSize(18, 18))
        self.next_button.setToolTip("Next Page")
        self.next_button.clicked.connect(self.next_page)
        nav_buttons.addWidget(self.next_button)
        
        pdf_controls_layout.addLayout(nav_buttons)
        
        self.page_counter_label = QLabel("Page: 0/0")
        self.page_counter_label.setObjectName("page-counter")
        self.page_counter_label.setFixedHeight(36)
        pdf_controls_layout.addWidget(self.page_counter_label)
        
        scroll_controls = QHBoxLayout()
        scroll_controls.setSpacing(4)
        
        self.scroll_up_button = QPushButton()
        self.scroll_up_button.setObjectName("icon-button")
        scroll_up_icon = qta.icon('fa5s.arrow-up', color='white')
        self.scroll_up_button.setIcon(scroll_up_icon)
        self.scroll_up_button.setIconSize(QSize(16, 16))
        self.scroll_up_button.setToolTip("Scroll Up")
        self.scroll_up_button.clicked.connect(self.scroll_up)
        scroll_controls.addWidget(self.scroll_up_button)
        
        self.scroll_down_button = QPushButton()
        self.scroll_down_button.setObjectName("icon-button")
        scroll_down_icon = qta.icon('fa5s.arrow-down', color='white')
        self.scroll_down_button.setIcon(scroll_down_icon)
        self.scroll_down_button.setIconSize(QSize(16, 16))
        self.scroll_down_button.setToolTip("Scroll Down")
        self.scroll_down_button.clicked.connect(self.scroll_down)
        scroll_controls.addWidget(self.scroll_down_button)
        
        self.continuous_scroll_button = QPushButton()
        self.continuous_scroll_button.setObjectName("icon-button")
        self.continuous_scroll_button.setIcon(qta.icon('fa5s.sync', color='white'))
        self.continuous_scroll_button.setIconSize(QSize(16, 16))
        self.continuous_scroll_button.setToolTip("Toggle Continuous Scroll")
        self.continuous_scroll_button.setCheckable(True)
        self.continuous_scroll_button.setChecked(self.continuous_scroll)
        self.continuous_scroll_button.clicked.connect(self.toggle_continuous_scroll)
        scroll_controls.addWidget(self.continuous_scroll_button)
        
        self.scroll_speed_slider = QSlider(Qt.Orientation.Horizontal)
        self.scroll_speed_slider.setObjectName("scroll-speed-slider")
        self.scroll_speed_slider.setMinimum(10)
        self.scroll_speed_slider.setMaximum(200)
        self.scroll_speed_slider.setValue(self.scroll_speed)
        self.scroll_speed_slider.setToolTip("Scroll Speed")
        self.scroll_speed_slider.valueChanged.connect(self.update_scroll_speed)
        self.scroll_speed_slider.setFixedWidth(100)
        scroll_controls.addWidget(self.scroll_speed_slider)
        
        pdf_controls_layout.addLayout(scroll_controls)
        
        zoom_controls = QHBoxLayout()
        zoom_controls.setSpacing(4)
        
        self.zoom_out_button = QPushButton()
        self.zoom_out_button.setObjectName("zoom-button")
        zoom_out_icon = qta.icon('fa5s.search-minus', color='white')
        self.zoom_out_button.setIcon(zoom_out_icon)
        self.zoom_out_button.setIconSize(QSize(16, 16))
        self.zoom_out_button.setToolTip("Zoom Out")
        self.zoom_out_button.clicked.connect(self.zoom_out)
        zoom_controls.addWidget(self.zoom_out_button)
        
        self.zoom_in_button = QPushButton()
        self.zoom_in_button.setObjectName("zoom-button")
        zoom_in_icon = qta.icon('fa5s.search-plus', color='white')
        self.zoom_in_button.setIcon(zoom_in_icon)
        self.zoom_in_button.setIconSize(QSize(16, 16))
        self.zoom_in_button.setToolTip("Zoom In")
        self.zoom_in_button.clicked.connect(self.zoom_in)
        zoom_controls.addWidget(self.zoom_in_button)
        
        pdf_controls_layout.addLayout(zoom_controls)
        toolbar_layout.addWidget(self.pdf_controls)
        self.pdf_controls.hide()
        self.main_layout.addWidget(toolbar)
        
    def create_dashboard(self):
        self.dashboard_widget = QFrame()
        dashboard_layout = QVBoxLayout(self.dashboard_widget)
        dashboard_layout.setSpacing(20)
        dashboard_layout.setContentsMargins(32, 32, 32, 32)
        
        header_layout = QHBoxLayout()
        header_layout.setSpacing(16)
        
        title_layout = QHBoxLayout()
        title_layout.setSpacing(12)
        
        title_icon = QLabel()
        title_icon_pixmap = qta.icon('fa5s.clock', color='#4361ee').pixmap(QSize(32, 32))
        title_icon.setPixmap(title_icon_pixmap)
        title_layout.addWidget(title_icon)
        
        title_label = QLabel("Recent Files")
        title_label.setObjectName("dashboard-title")
        title_label.setFont(QFont("Segoe UI", 24, QFont.Weight.Bold))
        title_layout.addWidget(title_label)
        title_layout.addStretch(1)
        
        header_layout.addLayout(title_layout)
        
        clear_button = QPushButton()
        clear_button.setObjectName("clear-history")
        clear_icon = qta.icon('fa5s.trash-alt', color='white')
        clear_button.setIcon(clear_icon)
        clear_button.setIconSize(QSize(16, 16))
        clear_button.setToolTip("Clear History")
        clear_button.clicked.connect(self.clear_recent_files)
        header_layout.addWidget(clear_button)
        
        dashboard_layout.addLayout(header_layout)
        
        search_container = QFrame()
        search_container.setObjectName("search-container")
        search_layout = QHBoxLayout(search_container)
        search_layout.setContentsMargins(12, 0, 12, 0)
        
        search_icon = QLabel()
        search_icon_pixmap = qta.icon('fa5s.search', color='#6c757d').pixmap(QSize(16, 16))
        search_icon.setPixmap(search_icon_pixmap)
        search_layout.addWidget(search_icon)
        
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Search files...")
        self.search_box.textChanged.connect(self.filter_recent_files)
        search_layout.addWidget(self.search_box)
        
        dashboard_layout.addWidget(search_container)
        
        files_container = QFrame()
        files_container.setObjectName("files-container")
        files_layout = QVBoxLayout(files_container)
        files_layout.setSpacing(2)
        files_layout.setContentsMargins(16, 16, 16, 16)
        
        self.recent_files_list = QVBoxLayout()
        self.recent_files_list.setSpacing(2)
        files_layout.addLayout(self.recent_files_list)
        
        dashboard_layout.addWidget(files_container)
        self.content_layout.addWidget(self.dashboard_widget)
        self.update_recent_files_list()

    def show_dashboard(self):
        self.dashboard_widget.show()
        self.tab_widget.hide()
        self.dashboard_button.setEnabled(False)
        self.pdf_controls.hide()
        
        self.prev_button.setEnabled(False)
        self.next_button.setEnabled(False)
        self.zoom_in_button.setEnabled(False)
        self.zoom_out_button.setEnabled(False)
        self.scroll_up_button.setEnabled(False)
        self.scroll_down_button.setEnabled(False)
        
    def show_pdf_viewer(self):
        self.dashboard_widget.hide()
        self.tab_widget.show()
        self.dashboard_button.setEnabled(True)
        
        if self.tab_widget.count() > 0:
            self.pdf_controls.show()
            self.update_buttons()
    
    def update_recent_files_list(self):
        for i in reversed(range(self.recent_files_list.count())): 
            self.recent_files_list.itemAt(i).widget().setParent(None)
        
        if not self.recent_files:
            no_files_container = QFrame()
            no_files_container.setObjectName("no-files-container")
            no_files_layout = QVBoxLayout(no_files_container)
            
            icon_label = QLabel()
            empty_icon = qta.icon('fa5s.folder-open', color='#6c757d')
            icon_label.setPixmap(empty_icon.pixmap(QSize(48, 48)))
            icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            no_files_layout.addWidget(icon_label)
            
            no_files_label = QLabel("No recent files")
            no_files_label.setObjectName("no-files")
            no_files_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            no_files_layout.addWidget(no_files_label)
            
            hint_label = QLabel("Click the folder icon to open a PDF file")
            hint_label.setObjectName("hint-text")
            hint_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            no_files_layout.addWidget(hint_label)
            
            self.recent_files_list.addWidget(no_files_container)
        else:
            for file_path in self.recent_files:
                file_link = self.create_file_link(file_path)
                self.recent_files_list.addWidget(file_link)

    def create_file_link(self, file_path):
        container = QFrame()
        container.setObjectName("file-link-container")
        layout = QHBoxLayout(container)
        layout.setContentsMargins(8, 0, 8, 0)
        layout.setSpacing(12)
        
        icon_label = QLabel()
        file_icon = qta.icon('fa5s.file-pdf', color='#4361ee')
        icon_label.setPixmap(file_icon.pixmap(QSize(16, 16)))
        layout.addWidget(icon_label)
        
        link = QLabel(os.path.basename(file_path))
        link.setProperty("class", "file-link")
        link.setCursor(Qt.CursorShape.PointingHandCursor)
        link.mousePressEvent = lambda e: self.open_file_from_link(file_path)
        layout.addWidget(link)
        
        layout.addStretch(1)
        return container

    def open_file_from_link(self, file_path):
        self.open_pdf(file_path)
        self.show_pdf_viewer()

    def eventFilter(self, obj, event):
        if obj == self.scroll_area and event.type() == QWheelEvent.Type.Wheel:
            self.handle_wheel_event(event)
            return True
        return super().eventFilter(obj, event)
    
    def handle_wheel_event(self, event):
        tab = self.get_current_tab()
        if not tab or not tab.current_doc:
            return
            
        delta = event.angleDelta().y()
        self.scroll_threshold += delta
        self.scroll_timer.start(300)
        
        if abs(self.scroll_threshold) >= 120:
            if self.scroll_threshold > 0:
                self.prev_page()
            else:
                self.next_page()
            
            self.scroll_threshold = 0
    
    def reset_scroll_threshold(self):
        self.scroll_threshold = 0
    
    def show_open_dialog(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Open PDF File",
            "",
            "PDF Files (*.pdf)"
        )
        
        if file_name:
            self.open_pdf(file_name)
            self.show_pdf_viewer()
        
    def open_pdf(self, file_name):
        if file_name:
            try:
                new_tab = PDFTab(self)
                new_tab.current_doc = fitz.open(file_name)
                
                tab_name = os.path.basename(file_name)
                self.tab_widget.addTab(new_tab, tab_name)
                self.tab_widget.setCurrentWidget(new_tab)
                
                self.update_page()
                self.update_buttons()
                self.pdf_controls.show()
                self.add_to_recent_files(file_name)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not open PDF file: {str(e)}")
    
    def add_to_recent_files(self, file_name):
        abs_path = os.path.abspath(file_name)
        
        if abs_path in self.recent_files:
            self.recent_files.remove(abs_path)
        
        self.recent_files.insert(0, abs_path)
        
        if len(self.recent_files) > self.max_recent_files:
            self.recent_files = self.recent_files[:self.max_recent_files]
        
        self.settings.setValue('recent_files', self.recent_files)
        self.update_recent_files_list()
    
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
            self.update_recent_files_list()
    
    def update_page(self):
        tab = self.get_current_tab()
        if tab and tab.current_doc:
            try:
                page = tab.current_doc[tab.current_page]
                pix = page.get_pixmap(matrix=fitz.Matrix(tab.zoom_factor, tab.zoom_factor))
                img = QImage(pix.samples, pix.width, pix.height, pix.stride, QImage.Format.Format_RGB888)
                pixmap = QPixmap.fromImage(img)
                tab.pdf_page_label.setPixmap(pixmap)
                self.page_counter_label.setText(f"Page: {tab.current_page + 1}/{len(tab.current_doc)}")
                tab.scroll_area.verticalScrollBar().setValue(0)
                tab.scroll_area.horizontalScrollBar().setValue(0)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error displaying page: {str(e)}")
    
    def update_buttons(self):
        tab = self.get_current_tab()
        if tab and tab.current_doc:
            self.prev_button.setEnabled(tab.current_page > 0)
            self.next_button.setEnabled(tab.current_page < len(tab.current_doc) - 1)
            self.zoom_in_button.setEnabled(True)
            self.zoom_out_button.setEnabled(True)
            self.scroll_up_button.setEnabled(True)
            self.scroll_down_button.setEnabled(True)
        else:
            self.prev_button.setEnabled(False)
            self.next_button.setEnabled(False)
            self.zoom_in_button.setEnabled(False)
            self.zoom_out_button.setEnabled(False)
            self.scroll_up_button.setEnabled(False)
            self.scroll_down_button.setEnabled(False)
    
    def prev_page(self):
        tab = self.get_current_tab()
        if tab and tab.current_doc and tab.current_page > 0:
            tab.current_page -= 1
            self.update_page()
            self.update_buttons()
    
    def next_page(self):
        tab = self.get_current_tab()
        if tab and tab.current_doc and tab.current_page < len(tab.current_doc) - 1:
            tab.current_page += 1
            self.update_page()
            self.update_buttons()
    
    def zoom_in(self):
        tab = self.get_current_tab()
        if tab:
            tab.zoom_factor *= 1.2
            self.update_page()
    
    def zoom_out(self):
        tab = self.get_current_tab()
        if tab:
            tab.zoom_factor /= 1.2
            self.update_page()

    def filter_recent_files(self):
        search_text = self.search_box.text().lower()
        
        for i in reversed(range(self.recent_files_list.count())): 
            self.recent_files_list.itemAt(i).widget().setParent(None)
        
        if not self.recent_files:
            no_files_container = QFrame()
            no_files_container.setObjectName("no-files-container")
            no_files_layout = QVBoxLayout(no_files_container)
            
            icon_label = QLabel()
            empty_icon = qta.icon('fa5s.folder-open', color='#6c757d')
            icon_label.setPixmap(empty_icon.pixmap(QSize(48, 48)))
            icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            no_files_layout.addWidget(icon_label)
            
            no_files_label = QLabel("No recent files")
            no_files_label.setObjectName("no-files")
            no_files_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            no_files_layout.addWidget(no_files_label)
            
            hint_label = QLabel("Click the folder icon to open a PDF file")
            hint_label.setObjectName("hint-text")
            hint_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            no_files_layout.addWidget(hint_label)
            
            self.recent_files_list.addWidget(no_files_container)
        else:
            for file_path in self.recent_files:
                if search_text in os.path.basename(file_path).lower():
                    file_link = self.create_file_link(file_path)
                    self.recent_files_list.addWidget(file_link)

    def close_tab(self, index):
        tab = self.tab_widget.widget(index)
        if tab and tab.current_doc:
            tab.current_doc.close()
        self.tab_widget.removeTab(index)
        
        if self.tab_widget.count() == 0:
            self.show_dashboard()
    
    def get_current_tab(self):
        return self.tab_widget.currentWidget()

    def scroll_up(self):
        tab = self.get_current_tab()
        if tab:
            scrollbar = tab.scroll_area.verticalScrollBar()
            scrollbar.setValue(scrollbar.value() - self.scroll_speed)

    def scroll_down(self):
        tab = self.get_current_tab()
        if tab:
            scrollbar = tab.scroll_area.verticalScrollBar()
            scrollbar.setValue(scrollbar.value() + self.scroll_speed)

    def toggle_continuous_scroll(self):
        self.continuous_scroll = self.continuous_scroll_button.isChecked()
        self.settings.setValue('continuous_scroll', self.continuous_scroll)
        
        if self.continuous_scroll:
            self.scroll_timer.start(50)  # Update every 50ms
        else:
            self.scroll_timer.stop()
    
    def update_scroll_speed(self, value):
        self.scroll_speed = value
        self.settings.setValue('scroll_speed', value)
    
    def continuous_scroll_update(self):
        if self.continuous_scroll:
            tab = self.get_current_tab()
            if tab:
                scrollbar = tab.scroll_area.verticalScrollBar()
                current_value = scrollbar.value()
                max_value = scrollbar.maximum()
                
                if current_value < max_value:
                    scrollbar.setValue(current_value + self.scroll_speed // 10)
                else:
                    # If we reach the bottom, go to next page
                    self.next_page()
                    scrollbar.setValue(0)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    viewer = PDFViewer()
    viewer.show()
    sys.exit(app.exec()) 
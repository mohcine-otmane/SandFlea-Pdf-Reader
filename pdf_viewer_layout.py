from PyQt6.QtWidgets import (QVBoxLayout, QHBoxLayout, QWidget, 
                             QPushButton, QLabel, QSlider, QScrollArea,
                             QTabWidget, QLineEdit, QFrame, QGridLayout)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont
import qtawesome as qta
import os

class PDFTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Create scroll area for PDF content
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scroll_area.setObjectName("pdf-view")
        
        # Create PDF content label
        self.pdf_label = QLabel()
        self.pdf_label.setObjectName("pdf-content")
        self.pdf_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.scroll_area.setWidget(self.pdf_label)
        
        layout.addWidget(self.scroll_area)

    def set_pdf_content(self, pixmap):
        self.pdf_label.setPixmap(pixmap)

class PDFViewerLayout:
    def __init__(self, parent):
        self.parent = parent
        self.setup_ui()

    def setup_ui(self):
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Create dashboard
        self.setup_dashboard()

        # Create PDF viewer
        self.setup_pdf_viewer()

        # Add everything to main layout
        main_layout.addWidget(self.dashboard)
        main_layout.addWidget(self.pdf_viewer)

        # Set the layout
        self.parent.setLayout(main_layout)

        # Initially show dashboard
        self.pdf_viewer.hide()

    def setup_dashboard(self):
        self.dashboard = QWidget()
        dashboard_layout = QVBoxLayout(self.dashboard)
        dashboard_layout.setContentsMargins(20, 20, 20, 20)
        dashboard_layout.setSpacing(20)

        # Title
        title = QLabel("SandFlea PDF Reader")
        title.setObjectName("dashboard-title")
        dashboard_layout.addWidget(title)

        # Search container
        search_container = QWidget()
        search_container.setObjectName("search-container")
        search_layout = QHBoxLayout(search_container)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search recent files...")
        self.search_input.setObjectName("search-input")
        
        self.open_button = QPushButton(qta.icon('fa5s.folder-open'), "Open PDF")
        self.open_button.setObjectName("open-button")
        
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.open_button)
        dashboard_layout.addWidget(search_container)

        # Recent files container
        self.files_container = QWidget()
        self.files_container.setObjectName("files-container")
        self.files_layout = QVBoxLayout(self.files_container)
        
        # Clear history button
        self.clear_history = QPushButton(qta.icon('fa5s.trash'), "Clear History")
        self.clear_history.setObjectName("clear-history")
        
        dashboard_layout.addWidget(self.files_container)
        dashboard_layout.addWidget(self.clear_history)
        dashboard_layout.addStretch()

    def setup_pdf_viewer(self):
        self.pdf_viewer = QWidget()
        viewer_layout = QVBoxLayout(self.pdf_viewer)
        viewer_layout.setContentsMargins(0, 0, 0, 0)
        viewer_layout.setSpacing(0)

        # Create PDF controls
        self.pdf_controls = QWidget()
        self.pdf_controls.setObjectName("pdf-controls")
        controls_layout = QHBoxLayout(self.pdf_controls)
        controls_layout.setContentsMargins(16, 8, 16, 8)
        controls_layout.setSpacing(8)

        # Navigation buttons
        self.prev_button = QPushButton(qta.icon('fa5s.chevron-left'), "")
        self.next_button = QPushButton(qta.icon('fa5s.chevron-right'), "")
        self.prev_button.setObjectName("pdf-nav-button")
        self.next_button.setObjectName("pdf-nav-button")

        # Page counter
        self.page_label = QLabel()
        self.page_label.setObjectName("page-counter")

        # Zoom controls
        self.zoom_in_button = QPushButton(qta.icon('fa5s.search-plus'), "")
        self.zoom_out_button = QPushButton(qta.icon('fa5s.search-minus'), "")
        self.zoom_in_button.setObjectName("pdf-nav-button")
        self.zoom_out_button.setObjectName("pdf-nav-button")

        # Scroll controls
        self.scroll_up_button = QPushButton(qta.icon('fa5s.arrow-up'), "")
        self.scroll_down_button = QPushButton(qta.icon('fa5s.arrow-down'), "")
        self.scroll_up_button.setObjectName("pdf-nav-button")
        self.scroll_down_button.setObjectName("pdf-nav-button")

        # Continuous scroll toggle
        self.continuous_scroll_button = QPushButton(qta.icon('fa5s.infinity'), "")
        self.continuous_scroll_button.setObjectName("pdf-nav-button")
        self.continuous_scroll_button.setCheckable(True)

        # Scroll speed slider
        self.scroll_speed_slider = QSlider(Qt.Orientation.Horizontal)
        self.scroll_speed_slider.setObjectName("scroll-speed-slider")
        self.scroll_speed_slider.setMinimum(10)
        self.scroll_speed_slider.setMaximum(100)
        self.scroll_speed_slider.setValue(50)

        # Dashboard button
        self.dashboard_button = QPushButton(qta.icon('fa5s.home'), "")
        self.dashboard_button.setObjectName("pdf-nav-button")

        # Add all controls
        controls_layout.addWidget(self.dashboard_button)
        controls_layout.addWidget(self.prev_button)
        controls_layout.addWidget(self.next_button)
        controls_layout.addWidget(self.page_label)
        controls_layout.addWidget(self.zoom_in_button)
        controls_layout.addWidget(self.zoom_out_button)
        controls_layout.addWidget(self.scroll_up_button)
        controls_layout.addWidget(self.scroll_down_button)
        controls_layout.addWidget(self.continuous_scroll_button)
        controls_layout.addWidget(self.scroll_speed_slider)
        controls_layout.addStretch()

        # Add controls to viewer
        viewer_layout.addWidget(self.pdf_controls)

        # Create tab widget
        self.tab_widget = QTabWidget()
        self.tab_widget.setObjectName("pdf-tabs")
        
        # Create initial PDF tab
        self.current_tab = PDFTab()
        self.tab_widget.addTab(self.current_tab, "No PDF Open")
        
        viewer_layout.addWidget(self.tab_widget)

    def show_dashboard(self):
        self.dashboard.show()
        self.pdf_viewer.hide()

    def show_pdf_viewer(self):
        self.dashboard.hide()
        self.pdf_viewer.show()

    def update_page_display(self, current_page, total_pages):
        self.page_label.setText(f"Page: {current_page}/{total_pages}")

    def set_pdf_content(self, pixmap):
        self.current_tab.set_pdf_content(pixmap)

    def add_pdf_tab(self, filename):
        tab_name = os.path.basename(filename)
        self.tab_widget.setTabText(0, tab_name)

    def update_recent_files_list(self, recent_files):
        # Clear existing items
        for i in reversed(range(self.files_layout.count())):
            self.files_layout.itemAt(i).widget().deleteLater()

        if not recent_files:
            no_files = QLabel("No recent files")
            no_files.setObjectName("no-files")
            hint = QLabel("Open a PDF file to get started")
            hint.setObjectName("hint-text")
            self.files_layout.addWidget(no_files)
            self.files_layout.addWidget(hint)
        else:
            for file_path in recent_files:
                file_name = os.path.basename(file_path)
                file_label = QLabel(file_name)
                file_label.setObjectName("file-link")
                self.files_layout.addWidget(file_label)

    def connect_signals(self, slots):
        """Connect layout signals to provided slot functions"""
        self.prev_button.clicked.connect(slots.get('prev_page', lambda: None))
        self.next_button.clicked.connect(slots.get('next_page', lambda: None))
        self.zoom_in_button.clicked.connect(slots.get('zoom_in', lambda: None))
        self.zoom_out_button.clicked.connect(slots.get('zoom_out', lambda: None))
        self.scroll_up_button.clicked.connect(slots.get('scroll_up', lambda: None))
        self.scroll_down_button.clicked.connect(slots.get('scroll_down', lambda: None))
        self.continuous_scroll_button.clicked.connect(slots.get('toggle_continuous_scroll', lambda: None))
        self.scroll_speed_slider.valueChanged.connect(slots.get('update_scroll_speed', lambda: None))
        self.dashboard_button.clicked.connect(slots.get('show_dashboard', lambda: None))
        self.clear_history.clicked.connect(slots.get('clear_recent_files', lambda: None))
        self.search_input.textChanged.connect(slots.get('filter_recent_files', lambda: None))
        self.open_button.clicked.connect(slots.get('open_pdf', lambda: None)) 
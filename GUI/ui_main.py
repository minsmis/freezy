import os
import sys

from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtWebEngineWidgets import *

import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import pandas as pd

import freezy
import ui_select_bodyparts
import ui_build_protocol
import ui_select_freezing_threshold
import ui_display_freezing_ratio


class MainWidget(QMainWindow):
    def __init__(self):
        super().__init__()

        self.init_parameters()  # init parameters
        self.init_thread()  # init thread
        self.init_main_ui()  # init main ui

    # %% inits
    def init_parameters(self):
        # Selected paths
        self.selected_paths = []

        # Bodyparts to extract
        self.x_bodypart = 'none'
        self.y_bodypart = 'none'

        # Default parameters
        self.windowSize = 15
        self.order = 4
        self.fps = 30
        self.pixelPerCm = 26

        # Freezing threshold
        self.freezing_threshold = ''

        # Protocol
        self.default_protocol = [120, 30, 30, 30, 30]
        self.protocol = []

        # Data
        self.route = []
        self.smoothed_route = []
        self.speed = []
        self.freezing_ratio = []

    def init_thread(self):
        # Event loop
        self.event_loop = QEventLoop(self)

    def init_main_ui(self):
        # Widget
        open_file_label = QLabel('1. Select path')  # Labels

        setup_smoothing_label = QLabel('2. Setup smoothing parameters')
        setup_smoothing_windowSize_label = QLabel('Window size:')
        setup_smoothing_order_label = QLabel('Order:')

        setup_compute_speed_label = QLabel('3. Setup speed computing parameters')
        setup_compute_speed_fps_label = QLabel('FPS:')
        setup_compute_speed_pixelPerCm_label = QLabel('Pixel/cm:')

        self.setup_smoothing_windowSize_lineEdit = QLineEdit()  # LineEdits
        self.setup_smoothing_windowSize_lineEdit.setPlaceholderText('window size')
        self.setup_smoothing_windowSize_lineEdit.setValidator(QIntValidator())
        self.setup_smoothing_windowSize_lineEdit.setText(str(self.windowSize))
        self.setup_smoothing_windowSize_lineEdit.textChanged.connect(self.action_update_windowSize)

        self.setup_smoothing_order_lineEdit = QLineEdit()
        self.setup_smoothing_order_lineEdit.setPlaceholderText('order')
        self.setup_smoothing_order_lineEdit.setValidator(QIntValidator())
        self.setup_smoothing_order_lineEdit.setText(str(self.order))
        self.setup_smoothing_order_lineEdit.textChanged.connect(self.action_update_order)

        self.setup_compute_speed_fps_lineEdit = QLineEdit()
        self.setup_compute_speed_fps_lineEdit.setPlaceholderText('fps')
        self.setup_compute_speed_fps_lineEdit.setValidator(QIntValidator())
        self.setup_compute_speed_fps_lineEdit.setText(str(self.fps))
        self.setup_compute_speed_fps_lineEdit.textChanged.connect(self.action_update_fps)

        self.setup_compute_speed_pixelPerCm_lineEdit = QLineEdit()
        self.setup_compute_speed_pixelPerCm_lineEdit.setPlaceholderText('pixel per cm')
        self.setup_compute_speed_pixelPerCm_lineEdit.setValidator(QIntValidator())
        self.setup_compute_speed_pixelPerCm_lineEdit.setText(str(self.pixelPerCm))
        self.setup_compute_speed_pixelPerCm_lineEdit.textChanged.connect(self.action_update_pixelPerCm)

        self.open_file_button = QPushButton('Select path')  # Buttons
        self.open_file_button.clicked.connect(self.action_select_paths)

        self.run_analysis_button = QPushButton('Run Analysis')
        self.run_analysis_button.clicked.connect(self.action_run_analysis)

        self.selected_path_table = QTableWidget(self)  # Tables
        self.selected_path_table.setColumnCount(1)
        self.selected_path_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.selected_path_table.setHorizontalHeaderLabels(['Selected paths'])

        self.speed_plot_webEngine = QWebEngineView()  # Plot: WebEngineViews
        self.freezing_ratio_plot_webEngine = QWebEngineView()

        # Layout
        path_layout = QVBoxLayout()
        path_layout.addWidget(open_file_label)
        path_layout.addWidget(self.open_file_button)
        path_layout.addWidget(self.selected_path_table)

        sub_analysis_setup_smoothing_layout = QHBoxLayout()
        sub_analysis_setup_smoothing_layout.addWidget(setup_smoothing_windowSize_label)
        sub_analysis_setup_smoothing_layout.addWidget(self.setup_smoothing_windowSize_lineEdit)
        sub_analysis_setup_smoothing_layout.addWidget(setup_smoothing_order_label)
        sub_analysis_setup_smoothing_layout.addWidget(self.setup_smoothing_order_lineEdit)

        sub_analysis_setup_compute_speed_layout = QHBoxLayout()
        sub_analysis_setup_compute_speed_layout.addWidget(setup_compute_speed_fps_label)
        sub_analysis_setup_compute_speed_layout.addWidget(self.setup_compute_speed_fps_lineEdit)
        sub_analysis_setup_compute_speed_layout.addWidget(setup_compute_speed_pixelPerCm_label)
        sub_analysis_setup_compute_speed_layout.addWidget(self.setup_compute_speed_pixelPerCm_lineEdit)

        analysis_setup_layout = QVBoxLayout()
        analysis_setup_layout.addWidget(setup_smoothing_label)
        analysis_setup_layout.addLayout(sub_analysis_setup_smoothing_layout)
        analysis_setup_layout.addWidget(setup_compute_speed_label)
        analysis_setup_layout.addLayout(sub_analysis_setup_compute_speed_layout)
        analysis_setup_layout.addWidget(self.run_analysis_button)

        plot_layout = QVBoxLayout()
        plot_layout.addWidget(self.speed_plot_webEngine)
        plot_layout.addWidget(self.freezing_ratio_plot_webEngine)

        # Frame
        path_frame = QFrame(self)
        path_frame.setFrameShape(QFrame.Shape.StyledPanel)
        path_frame.setFrameShadow(QFrame.Shadow.Sunken)
        path_frame.setLayout(path_layout)

        analysis_setup_frame = QFrame(self)
        analysis_setup_frame.setFrameShape(QFrame.Shape.StyledPanel)
        analysis_setup_frame.setFrameShadow(QFrame.Shadow.Sunken)
        analysis_setup_frame.setLayout(analysis_setup_layout)

        plot_frame = QFrame(self)
        plot_frame.setFrameShape(QFrame.Shape.StyledPanel)
        plot_frame.setFrameShadow(QFrame.Shadow.Sunken)
        plot_frame.setLayout(plot_layout)

        # Splitter
        horizontal_splitter = QSplitter(Qt.Orientation.Horizontal)
        horizontal_splitter.setChildrenCollapsible(False)
        horizontal_splitter.addWidget(path_frame)
        horizontal_splitter.addWidget(analysis_setup_frame)
        horizontal_splitter.setSizes([620, 404])

        vertical_splitter = QSplitter(Qt.Orientation.Vertical)
        vertical_splitter.setChildrenCollapsible(False)
        vertical_splitter.addWidget(horizontal_splitter)
        vertical_splitter.addWidget(plot_frame)
        vertical_splitter.setSizes([240, 620])

        # Main layout
        main_layout = QGridLayout(self)
        main_layout.addWidget(vertical_splitter)

        # Main Window widget
        main_widget = QWidget()
        main_widget.setLayout(main_layout)

        # Set central widget
        self.setCentralWidget(main_widget)

        # Menubar
        menu_bar = self.menuBar()
        menu_bar.setNativeMenuBar(False)
        self.file_menu = menu_bar.addMenu('&File')
        self.edit_menu = menu_bar.addMenu('&Edit')
        self.analysis_menu = menu_bar.addMenu('&Analysis')
        self.model_menu = menu_bar.addMenu('&Model')
        self.help_menu = menu_bar.addMenu('&Help')

        # Status bar
        self.statusBar()

        # Action
        self.action_open_file()  # Get file path

        # Show main widget
        self.setWindowTitle('Freezy: Analyzing fear behavior')
        self.resize(1024, 860)
        self.show()

    def closeEvent(self, event):
        message = QMessageBox.question(self, "Question", "Are you sure you want to quit?",
                                       QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                       QMessageBox.StandardButton.No)
        if message == QMessageBox.StandardButton.Yes:
            event.accept()  # Close window
        else:
            event.ignore()  # Ignore closure

    # %% Button actions
    def action_open_file(self):
        return

    def action_select_paths(self):
        # Open path selection dialog
        selected_paths = QFileDialog.getOpenFileNames(self, 'Select files', os.getcwd())

        # Make path lists
        self.selected_paths = list(selected_paths[0])

        # Display selected paths in table widget
        self.selected_path_table.setRowCount(len(self.selected_paths))
        [self.selected_path_table.setItem(i, 0, QTableWidgetItem(path)) for i, path in enumerate(self.selected_paths)]

    def action_update_windowSize(self):
        # Update changed text
        try:
            self.windowSize = int(self.setup_smoothing_windowSize_lineEdit.text())
        except:
            self.windowSize = 0  # Reset value

    def action_update_order(self):
        # Update changed text
        try:
            self.order = int(self.setup_smoothing_order_lineEdit.text())
        except:
            self.order = 0  # Reset value

    def action_update_fps(self):
        # Update changed text
        try:
            self.fps = int(self.setup_compute_speed_fps_lineEdit.text())
        except:
            self.fps = 0  # Reset value

    def action_update_pixelPerCm(self):
        # Update changed text
        try:
            self.pixelPerCm = int(self.setup_compute_speed_pixelPerCm_lineEdit.text())
        except:
            self.pixelPerCm = 0  # Reset value

    def action_run_analysis(self):

        # Check path
        if len(self.selected_paths) == 0:
            QMessageBox.warning(self, 'Path Error', 'Empty path.')
            return

        # Check parameter state
        if self.windowSize <= 0 or self.order <= 0 or self.fps <= 0 or self.pixelPerCm <= 0:
            QMessageBox.warning(self, 'Value Error', 'Unexpected parameter.')
            return

        # Reset parameters
        self.reset_parameters()

        # Run analysis
        # Read DLC coordinates
        ''' Now this application performs analysis for first selected data. '''
        dlc_coordinates = freezy.extract_data(self.selected_paths[0])

        # Select bodyparts
        ui_select_bodyparts.SelectBodypartsWidget(self, freezy.read_bodyparts(dlc_coordinates))
        if self.x_bodypart != 'none' and self.y_bodypart != 'none':  # Check unfilled bodyparts
            coordinates_x, coordinates_y = freezy.extract_coordinates(dlc_coordinates, self.x_bodypart, self.y_bodypart)
        else:
            return

        # Set protocol
        ui_build_protocol.BuildProtocolWidget(self)
        if not self.protocol:  # Check unfilled bodyparts
            return

            # Make 'route' with coordinates
        self.route = freezy.make_route(coordinates_x, coordinates_y)

        # Smooth route
        self.smoothed_route = freezy.smooth_route(self.route, window_size=self.windowSize)

        # Compute speed
        self.speed = freezy.compute_speed(self.smoothed_route, fps=self.fps, pixel_per_cm=self.pixelPerCm)

        # Select freezing threshold
        speed_distribution = freezy.compute_speed_distribution(self.speed)
        ui_select_freezing_threshold.SelectFreezingThresholdWidget(self, speed_distribution)
        if self.freezing_threshold == '':  # Check unfilled freezing threshold
            return

        # Detect freezing
        freeze_or_not = freezy.detect_freezing(self.speed, freezing_threshold=self.freezing_threshold)

        # Calculate freezing ratio for the protocol
        self.freezing_ratio = freezy.compute_freezing_ratio(freeze_or_not, self.protocol)

        # Display results
        self.plot_speed()
        self.plot_freezing_ratio()
        ui_display_freezing_ratio.DisplayFreezingRatioWidget(self, self.selected_paths, self.x_bodypart,
                                                             self.y_bodypart, self.windowSize, self.order, self.fps,
                                                             self.pixelPerCm, self.freezing_threshold, self.protocol,
                                                             self.route, self.smoothed_route, self.speed,
                                                             self.freezing_ratio)

    # %% Application management functions
    def exec_event_loop(self):
        self.event_loop.exec()

    def exit_event_loop(self):
        self.event_loop.exit()

    def close_widget(self, widget):
        widget.close()

    def reset_parameters(self):
        # Bodyparts to extract
        self.x_bodypart = 'none'
        self.y_bodypart = 'none'

        # Freezing threshold
        self.freezing_threshold = ''

        # Protocol
        self.default_protocol = [120, 30, 30, 30, 30]
        self.protocol = []

        # Data
        self.route = []
        self.smoothed_route = []
        self.speed = []
        self.freezing_ratio = []

    # %% Application utility functions
    def plot_route(self):
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=self.route[0], y=self.route[1], opacity=0.7, mode='lines+markers', name='Route'))
        fig.add_trace(
            go.Scatter(x=self.smoothed_route[0], y=self.smoothed_route[1], opacity=0.3, mode='lines+markers',
                       name='Smoothed route'))
        fig.update_xaxes(title='Coordinate X')
        fig.update_yaxes(title='Coordinate Y')
        fig.update_layout(margin=dict(l=20, r=20, t=20, b=20), legend=dict(yanchor='top', xanchor='right'))
        self.route_plot_webEngine.setHtml(fig.to_html(include_plotlyjs='cdn'))

    def plot_speed(self):
        fig = px.line(y=self.speed)
        fig.update_xaxes(title='Time (s)')
        fig.update_yaxes(title='Speed (cm/s)')
        fig.update_layout(margin=dict(l=20, r=20, t=20, b=20))
        self.speed_plot_webEngine.setHtml(fig.to_html(include_plotlyjs='cdn'))

    def plot_freezing_ratio(self):
        fig = go.Figure()
        fig.add_trace(go.Scatter(y=self.freezing_ratio, mode='lines+markers'))
        fig.update_xaxes(title='Protocol')
        fig.update_yaxes(title='Freezing (%)', range=[-5, 110], dtick=25)
        fig.update_layout(margin=dict(l=20, r=20, t=20, b=20))
        self.freezing_ratio_plot_webEngine.setHtml(fig.to_html(include_plotlyjs='cdn'))


# %% main executor
if __name__ == '__main__':
    app = QApplication(sys.argv)

    main_window = MainWidget()

    sys.exit(app.exec())

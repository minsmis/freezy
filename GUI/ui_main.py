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
import ui_select_freezing_threshold


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
        self.program_freezing_threshold = 0
        self.freezing_threshold = 0.3

        # Protocol
        self.protocol = [120, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30]

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

        setup_protocol_label = QLabel('4. Setup protocol')
        setup_protocol_protocol_label = QLabel('Protocol (s):')

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

        self.setup_protocol_lineEdit = QLineEdit()
        self.setup_protocol_lineEdit.setPlaceholderText('protocol Ex. [120, 30, 30, ...]')
        self.setup_protocol_lineEdit.setText(str(self.protocol))
        self.setup_protocol_lineEdit.textChanged.connect(self.action_update_protocol)

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

        sub_analysis_setup_protocol_layout = QHBoxLayout()
        sub_analysis_setup_protocol_layout.addWidget(setup_protocol_protocol_label)
        sub_analysis_setup_protocol_layout.addWidget(self.setup_protocol_lineEdit)

        analysis_setup_layout = QVBoxLayout()
        analysis_setup_layout.addWidget(setup_smoothing_label)
        analysis_setup_layout.addLayout(sub_analysis_setup_smoothing_layout)
        analysis_setup_layout.addWidget(setup_compute_speed_label)
        analysis_setup_layout.addLayout(sub_analysis_setup_compute_speed_layout)
        analysis_setup_layout.addWidget(setup_protocol_label)
        analysis_setup_layout.addLayout(sub_analysis_setup_protocol_layout)
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

        vertical_splitter = QSplitter(Qt.Orientation.Vertical)
        vertical_splitter.setChildrenCollapsible(False)
        vertical_splitter.addWidget(horizontal_splitter)
        vertical_splitter.addWidget(plot_frame)
        vertical_splitter.setStretchFactor(1, 10)

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
            event.accept()
        else:
            event.ignore()

    # %% Displaying widgets
    def display_freezing_ratio(self):
        # Display freezing ratio widget
        self.display_freezing_ratio_widget = QWidget()

        # Widgets
        display_freezing_ratio_path_label = QLabel('1. Path')  # Labels
        display_freezing_ratio_path_path_label = QLabel('Path:')

        display_freezing_ratio_smoothing_parameter_report_label = QLabel('2. Smoothing Parameters')
        display_freezing_ratio_smoothing_parameter_windowSize_label = QLabel('Window Size:')
        display_freezing_ratio_smoothing_parameter_order_label = QLabel('Order:')

        display_freezing_ratio_compute_speed_parameter_report_label = QLabel('3. Compute speed parameters')
        display_freezing_ratio_compute_speed_parameter_fps_label = QLabel('FPS:')
        display_freezing_ratio_compute_speed_parameter_pixelPerCm_label = QLabel('Pixel/cm:')

        display_freezing_ratio_protocol_label = QLabel('4. Protocol')
        display_freezing_ratio_protocol_protocol_label = QLabel('Protocol:')

        display_freezing_ratio_result_label = QLabel('Results')

        display_freezing_ratio_path_lineEdit = QLineEdit()  # LineEdits
        display_freezing_ratio_path_lineEdit.setText(str(self.selected_paths[0]))
        display_freezing_ratio_path_lineEdit.setReadOnly(True)

        display_freezing_ratio_smoothing_parameter_windowSize_lineEdit = QLineEdit()
        display_freezing_ratio_smoothing_parameter_windowSize_lineEdit.setText(str(self.windowSize))
        display_freezing_ratio_smoothing_parameter_windowSize_lineEdit.setReadOnly(True)

        display_freezing_ratio_smoothing_parameter_order_lineEdit = QLineEdit()
        display_freezing_ratio_smoothing_parameter_order_lineEdit.setText(str(self.order))
        display_freezing_ratio_smoothing_parameter_order_lineEdit.setReadOnly(True)

        display_freezing_ratio_compute_speed_parameter_fps_lineEdit = QLineEdit()
        display_freezing_ratio_compute_speed_parameter_fps_lineEdit.setText(str(self.fps))
        display_freezing_ratio_compute_speed_parameter_fps_lineEdit.setReadOnly(True)

        display_freezing_ratio_compute_speed_parameter_pixelPerCm_lineEdit = QLineEdit()
        display_freezing_ratio_compute_speed_parameter_pixelPerCm_lineEdit.setText(str(self.pixelPerCm))
        display_freezing_ratio_compute_speed_parameter_pixelPerCm_lineEdit.setReadOnly(True)

        display_freezing_ratio_protocol_protocol_lineEdit = QLineEdit()
        display_freezing_ratio_protocol_protocol_lineEdit.setText(str(self.protocol))
        display_freezing_ratio_protocol_protocol_lineEdit.setReadOnly(True)

        display_freezing_ratio_table = QTableWidget(self)  # Tables
        display_freezing_ratio_table.setColumnCount(2)
        display_freezing_ratio_table.setRowCount(len(self.protocol))
        display_freezing_ratio_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        display_freezing_ratio_table.setHorizontalHeaderLabels(['Protocol (s)', 'Freezing Ratio (%)'])
        [display_freezing_ratio_table.setItem(i, 0, QTableWidgetItem(str(duration)))
         for i, duration in enumerate(self.protocol)]
        [display_freezing_ratio_table.setItem(i, 1, QTableWidgetItem(str(freezing_ratio)))
         for i, freezing_ratio in enumerate(self.freezing_ratio)]

        display_freezing_ratio_save_button = QPushButton('Save')  # Buttons
        display_freezing_ratio_save_button.clicked.connect(self.action_save_freezing_ratio)

        display_freezing_ratio_cancel_button = QPushButton('Cancel')
        display_freezing_ratio_cancel_button.clicked.connect(lambda: self.display_freezing_ratio_widget.close())

        # Layout
        display_freezing_ratio_path_layout = QHBoxLayout()  # Path layout
        display_freezing_ratio_path_layout.addWidget(display_freezing_ratio_path_path_label)
        display_freezing_ratio_path_layout.addWidget(display_freezing_ratio_path_lineEdit)

        display_freezing_ratio_smoothing_parameter_layout = QHBoxLayout()  # Smoothing parameter layout
        display_freezing_ratio_smoothing_parameter_layout.addWidget(
            display_freezing_ratio_smoothing_parameter_windowSize_label)
        display_freezing_ratio_smoothing_parameter_layout.addWidget(
            display_freezing_ratio_smoothing_parameter_windowSize_lineEdit)
        display_freezing_ratio_smoothing_parameter_layout.addWidget(
            display_freezing_ratio_smoothing_parameter_order_label)
        display_freezing_ratio_smoothing_parameter_layout.addWidget(
            display_freezing_ratio_smoothing_parameter_order_lineEdit)

        display_freezing_ratio_compute_speed_layout = QHBoxLayout()  # Compute speed layout
        display_freezing_ratio_compute_speed_layout.addWidget(
            display_freezing_ratio_compute_speed_parameter_fps_label)
        display_freezing_ratio_compute_speed_layout.addWidget(
            display_freezing_ratio_compute_speed_parameter_fps_lineEdit)
        display_freezing_ratio_compute_speed_layout.addWidget(
            display_freezing_ratio_compute_speed_parameter_pixelPerCm_label)
        display_freezing_ratio_compute_speed_layout.addWidget(
            display_freezing_ratio_compute_speed_parameter_pixelPerCm_lineEdit)

        display_freezing_ratio_protocol_layout = QHBoxLayout()  # Protocol layout
        display_freezing_ratio_protocol_layout.addWidget(display_freezing_ratio_protocol_protocol_label)
        display_freezing_ratio_protocol_layout.addWidget(display_freezing_ratio_protocol_protocol_lineEdit)

        display_freezing_ratio_buttons_layout = QHBoxLayout()  # Buttons layout
        display_freezing_ratio_buttons_layout.addWidget(display_freezing_ratio_save_button)
        display_freezing_ratio_buttons_layout.addWidget(display_freezing_ratio_cancel_button)

        display_freezing_ratio_layout = QVBoxLayout()  # Largest layout
        display_freezing_ratio_layout.addWidget(display_freezing_ratio_path_label)
        display_freezing_ratio_layout.addLayout(display_freezing_ratio_path_layout)
        display_freezing_ratio_layout.addWidget(display_freezing_ratio_smoothing_parameter_report_label)
        display_freezing_ratio_layout.addLayout(display_freezing_ratio_smoothing_parameter_layout)
        display_freezing_ratio_layout.addWidget(display_freezing_ratio_compute_speed_parameter_report_label)
        display_freezing_ratio_layout.addLayout(display_freezing_ratio_compute_speed_layout)
        display_freezing_ratio_layout.addLayout(display_freezing_ratio_compute_speed_layout)
        display_freezing_ratio_layout.addWidget(display_freezing_ratio_protocol_label)
        display_freezing_ratio_layout.addLayout(display_freezing_ratio_protocol_layout)
        display_freezing_ratio_layout.addWidget(display_freezing_ratio_result_label)
        display_freezing_ratio_layout.addWidget(display_freezing_ratio_table)
        display_freezing_ratio_layout.addLayout(display_freezing_ratio_buttons_layout)

        # Set widget layout
        self.display_freezing_ratio_widget.setLayout(display_freezing_ratio_layout)

        # Show widget
        self.display_freezing_ratio_widget.setWindowTitle('Result Report: Freezing Ratio')
        self.display_freezing_ratio_widget.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.display_freezing_ratio_widget.resize(400, 700)
        self.display_freezing_ratio_widget.show()

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

    def action_update_protocol(self):
        # Update changed protocol
        try:
            self.protocol = eval(self.setup_protocol_lineEdit.text())
        except:
            self.protocol = []  # Reset value

    def action_run_analysis(self):
        # Check path
        if len(self.selected_paths) == 0:
            QMessageBox.warning(self, 'Path Error', 'Empty path.')
            return

        # Check parameter state
        if self.windowSize <= 0 or self.order <= 0 or self.fps <= 0 or self.pixelPerCm <= 0 or len(self.protocol) == 0:
            QMessageBox.warning(self, 'Value Error', 'Unexpected parameter.')
            return

        # Run analysis
        # Read DLC coordinates
        ''' Now this application performs analysis for first selected data. '''
        dlc_coordinates = freezy.extract_data(self.selected_paths[0])

        # Select bodyparts
        ui_select_bodyparts.SelectBodypartsWidget(self, freezy.read_bodyparts(dlc_coordinates))
        if self.x_bodypart != 'none' and self.y_bodypart != 'none':  # Proceed when bodyparts are selected.
            coordinates_x, coordinates_y = freezy.extract_coordinates(dlc_coordinates, self.x_bodypart, self.y_bodypart)
        else:
            self.exec_event_loop()  # Temporary pause until selected bodyparts are updated
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

        # Detect freezing
        freeze_or_not = freezy.detect_freezing(self.speed, freezing_threshold=self.freezing_threshold)

        # Calculate freezing ratio for the protocol
        self.freezing_ratio = freezy.compute_freezing_ratio(freeze_or_not, self.protocol)

        # Display results
        self.plot_speed()
        self.plot_freezing_ratio()
        self.display_freezing_ratio()

    def action_save_freezing_ratio(self):
        # Make dataframe
        setup_result = pd.DataFrame({
            'Path': self.selected_paths[0],
            'Bodypart (X)': self.x_bodypart,
            'Bodypart (Y)': self.y_bodypart,
            'Window Size': self.windowSize,
            'Order': self.order,
            'FPS': self.fps,
            'Picel/cm': self.pixelPerCm
        }, index=[0])
        data_result = pd.DataFrame({
            'Protocol (s)': self.protocol,
            'Freezing Ratio (%)': self.freezing_ratio
        })
        speed_result = pd.DataFrame({
            'Speed (cm/s)': self.speed
        })
        route_result = pd.DataFrame({
            'Route (X)': self.route[0],
            'Route (Y)': self.route[1],
            'Smoothed Route (X)': self.smoothed_route[0],
            'Smoothed Route (Y)': self.smoothed_route[1]
        })

        # Save file
        save_path = QFileDialog.getSaveFileName(self, 'Save File', os.path.dirname(self.selected_paths[0]),
                                                filter='Excel Files (*.xlsx)')
        with pd.ExcelWriter(save_path[0]) as writer:
            data_result.to_excel(writer, sheet_name='Data')
            speed_result.to_excel(writer, sheet_name='Speed')
            route_result.to_excel(writer, sheet_name='Route')
            setup_result.to_excel(writer, sheet_name='Setup')

    # %% Application management functions
    def exec_event_loop(self):
        self.event_loop.exec()

    def exit_event_loop(self):
        self.event_loop.exit()

    def close_widget(self, widget):
        widget.close()

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

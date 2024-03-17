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


class DisplayFreezingRatioWidget(QWidget):
    def __init__(self, main_widget_handle, selected_paths, x_bodypart, y_bodypart, windowSize, order, fps, pixelPerCm,
                 freezing_threshold, protocol, route, smoothed_route, speed, freezing_ratio):
        super().__init__()

        self.init_parameters(main_widget_handle, selected_paths, x_bodypart, y_bodypart, windowSize, order, fps,
                             pixelPerCm, freezing_threshold, protocol, speed, route, smoothed_route,
                             freezing_ratio)  # init parameters
        self.init_display_freezing_ratio()  # init display freezing ratio

    def init_parameters(self, main_widget_handle, selected_paths, x_bodypart, y_bodypart, windowSize, order, fps,
                        pixelPerCm, freezing_threshold, protocol, route, smoothed_route, speed, freezing_ratio):
        # Main widget handle
        self.main_widget_handle = main_widget_handle

        # Selected paths
        self.selected_paths = selected_paths

        # Bodyparts to extract
        self.x_bodypart = x_bodypart
        self.y_bodypart = y_bodypart

        # Default parameters
        self.windowSize = windowSize
        self.order = order
        self.fps = fps
        self.pixelPerCm = pixelPerCm

        # Freezing threshold
        self.freezing_threshold = freezing_threshold

        # Protocol
        self.protocol = protocol

        # Data
        self.route = route
        self.smoothed_route = smoothed_route
        self.speed = speed
        self.freezing_ratio = freezing_ratio

    def init_display_freezing_ratio(self):
        # Widgets
        display_freezing_ratio_path_label = QLabel('1. Path')  # Labels
        display_freezing_ratio_path_path_label = QLabel('Path:')

        display_freezing_ratio_smoothing_parameter_report_label = QLabel('2. Smoothing Parameters')
        display_freezing_ratio_smoothing_parameter_windowSize_label = QLabel('Window Size:')
        display_freezing_ratio_smoothing_parameter_order_label = QLabel('Order:')

        display_freezing_ratio_compute_speed_parameter_report_label = QLabel('3. Compute Speed Parameters')
        display_freezing_ratio_compute_speed_parameter_fps_label = QLabel('FPS:')
        display_freezing_ratio_compute_speed_parameter_pixelPerCm_label = QLabel('Pixel/cm:')

        display_freezing_ratio_protocol_label = QLabel('4. Protocol')
        display_freezing_ratio_protocol_protocol_label = QLabel('Protocol:')

        display_freezing_ratio_freezing_threshold_label = QLabel('5. Freezing Threshold')
        display_freezing_ratio_freezing_threshold_threshold_label = QLabel('Freezing Threshold: ')

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

        display_freezing_ratio_freezing_threshold_lineEdit = QLineEdit()
        display_freezing_ratio_freezing_threshold_lineEdit.setText(str(self.freezing_threshold))
        display_freezing_ratio_freezing_threshold_lineEdit.setReadOnly(True)

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
        display_freezing_ratio_cancel_button.clicked.connect(lambda: self.close())

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

        display_freezing_ratio_freezing_threshold_layout = QHBoxLayout()  # Freezing threshold layout
        display_freezing_ratio_freezing_threshold_layout.addWidget(
            display_freezing_ratio_freezing_threshold_threshold_label)
        display_freezing_ratio_freezing_threshold_layout.addWidget(display_freezing_ratio_freezing_threshold_lineEdit)

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
        display_freezing_ratio_layout.addWidget(display_freezing_ratio_freezing_threshold_label)
        display_freezing_ratio_layout.addLayout(display_freezing_ratio_freezing_threshold_layout)
        display_freezing_ratio_layout.addWidget(display_freezing_ratio_result_label)
        display_freezing_ratio_layout.addWidget(display_freezing_ratio_table)
        display_freezing_ratio_layout.addLayout(display_freezing_ratio_buttons_layout)

        # Set widget layout
        self.setLayout(display_freezing_ratio_layout)

        # Show widget
        self.setWindowTitle('Result Report: Freezing Ratio')
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.resize(450, 720)
        self.show()

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
            'Freezing Threshold (s)': self.freezing_threshold,
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

    def closeEvent(self, event):
        message = QMessageBox.question(self, "Question", "Are you sure want to quit?",
                                       QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                       QMessageBox.StandardButton.No)
        if message == QMessageBox.StandardButton.Yes:
            self.main_widget_handle.exit_event_loop()  # Release event loop
            event.accept()  # Close window
        else:
            event.ignore()  # Ignore closure

    def close_widget(self, widget):
        widget.close()

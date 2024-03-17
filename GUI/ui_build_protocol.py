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


class BuildProtocolWidget(QWidget):
    def __init__(self, main_widget_handle):
        super().__init__()

        self.init_parameters(main_widget_handle)  # init parameters
        self.init_build_protocol()  # init build protocol

    def init_parameters(self, main_widget_handle):
        # Main widget handle
        self.main_widget_handle = main_widget_handle

        # Protocols
        self.default_protocol = self.main_widget_handle.default_protocol
        self.protocol = self.main_widget_handle.protocol

        # Parameters
        self.total_duration = 0  # sec
        self.event_counts = 0

        self.baseline = 120  # sec
        self.conditioned_stimulus = 30  # sec
        self.inter_stimulus_interval = 30  # sec
        self.post_hold_duration = 30  # sec

        # Figure parameters
        self.event_display_value = 5
        self.event_display_width = 1
        self.x_list = []
        self.y_list = []

        # Preset figure
        self.fig = go.Figure()
        self.fig.update_xaxes(range=[0, 60], showgrid=True)
        self.fig.update_xaxes(title='Time (s)')
        self.fig.update_yaxes(range=[0, 10], showgrid=True)
        self.fig.update_yaxes(title='Protocol')
        self.fig.update_layout(margin=dict(l=20, r=20, t=20, b=20))

    def init_build_protocol(self):
        build_protocol_set_parameters_label = QLabel('1. Set protocol parameters')  # Labels
        build_protocol_baseline_label = QLabel('Set baseline duration [s]: ')
        build_protocol_conditioned_stimulus_label = QLabel('Set conditioned stimulus (CS) duration [s]: ')
        build_protocol_inter_stimulus_interval_label = QLabel('Set inter-stimulus interval (ITI) duration [s]: ')
        build_protocol_post_hold_duration_label = QLabel('Set post-hold duration duration [s]: ')
        build_protocol_build_protocol_label = QLabel('2. Build protocol')

        self.build_protocol_baseline_lineEdit = QLineEdit()  # LineEdit
        self.build_protocol_baseline_lineEdit.setText(str(self.baseline))
        self.build_protocol_baseline_lineEdit.setPlaceholderText('Set baseline duration [s].')
        self.build_protocol_baseline_lineEdit.setValidator(QIntValidator())
        self.build_protocol_baseline_lineEdit.textChanged.connect(self.action_update_baseline)

        self.build_protocol_conditioned_stimulus_lineEdit = QLineEdit()
        self.build_protocol_conditioned_stimulus_lineEdit.setText(str(self.conditioned_stimulus))
        self.build_protocol_conditioned_stimulus_lineEdit.setPlaceholderText(
            'Set conditioned stimulus (CS) duration [s].')
        self.build_protocol_conditioned_stimulus_lineEdit.setValidator(QIntValidator())
        self.build_protocol_conditioned_stimulus_lineEdit.textChanged.connect(self.action_update_conditioned_stimulus)

        self.build_protocol_inter_stimulus_interval_lineEdit = QLineEdit()
        self.build_protocol_inter_stimulus_interval_lineEdit.setText(str(self.inter_stimulus_interval))
        self.build_protocol_inter_stimulus_interval_lineEdit.setPlaceholderText(
            'Set inter-stimulus interval (ITI) duration [s].')
        self.build_protocol_inter_stimulus_interval_lineEdit.setValidator(QIntValidator())
        self.build_protocol_inter_stimulus_interval_lineEdit.textChanged.connect(
            self.action_update_inter_stimulus_interval)

        self.build_protocol_post_hold_duration_lineEdit = QLineEdit()
        self.build_protocol_post_hold_duration_lineEdit.setText(str(self.post_hold_duration))
        self.build_protocol_post_hold_duration_lineEdit.setPlaceholderText('Set post-hold duration duration [s].')
        self.build_protocol_post_hold_duration_lineEdit.setValidator(QIntValidator())
        self.build_protocol_post_hold_duration_lineEdit.textChanged.connect(self.action_update_baseline)

        self.protocol_plot_webEngine = QWebEngineView()  # Plot: WebEngineViews
        self.protocol_plot_webEngine.setHtml(
            self.fig.to_html(include_plotlyjs='cdn'))  # Include figure on WebEngineView

        self.build_protocol_add_protocol_button = QPushButton('Add Protocol')  # Buttons
        self.build_protocol_add_protocol_button.clicked.connect(self.action_add_protocol)

        self.build_protocol_reset_protocol_button = QPushButton('Reset Protocol')
        self.build_protocol_reset_protocol_button.clicked.connect(self.action_reset_protocol)

        self.build_protocol_set_protocol_button = QPushButton('Set Protocol')
        self.build_protocol_set_protocol_button.clicked.connect(self.action_set_protocol)

        self.build_protocol_cancel_protocol_button = QPushButton('Cancel')
        self.build_protocol_cancel_protocol_button.clicked.connect(self.action_cancel_protocol)

        # Sub-layout
        baseline_subLayout = QHBoxLayout()
        baseline_subLayout.addWidget(build_protocol_baseline_label)
        baseline_subLayout.addWidget(self.build_protocol_baseline_lineEdit)

        conditioned_stimulus_subLayout = QHBoxLayout()
        conditioned_stimulus_subLayout.addWidget(build_protocol_conditioned_stimulus_label)
        conditioned_stimulus_subLayout.addWidget(self.build_protocol_conditioned_stimulus_lineEdit)

        inter_stimulus_interval_subLayout = QHBoxLayout()
        inter_stimulus_interval_subLayout.addWidget(build_protocol_inter_stimulus_interval_label)
        inter_stimulus_interval_subLayout.addWidget(self.build_protocol_inter_stimulus_interval_lineEdit)

        post_hold_duration_subLayout = QHBoxLayout()
        post_hold_duration_subLayout.addWidget(build_protocol_post_hold_duration_label)
        post_hold_duration_subLayout.addWidget(self.build_protocol_post_hold_duration_lineEdit)

        build_protocol_subLayout = QHBoxLayout()
        build_protocol_subLayout.addWidget(self.build_protocol_add_protocol_button)
        build_protocol_subLayout.addWidget(self.build_protocol_reset_protocol_button)

        terminate_build_protocol_subLayout = QHBoxLayout()
        terminate_build_protocol_subLayout.addWidget(self.build_protocol_set_protocol_button)
        terminate_build_protocol_subLayout.addWidget(self.build_protocol_cancel_protocol_button)

        # Frame
        h_line_1 = QFrame(self)
        h_line_1.setFrameShape(QFrame.Shape.HLine)
        h_line_1.setFrameShadow(QFrame.Shadow.Sunken)

        h_line_2 = QFrame(self)
        h_line_2.setFrameShape(QFrame.Shape.HLine)
        h_line_2.setFrameShadow(QFrame.Shadow.Sunken)

        # Main layout
        build_protocol_layout = QVBoxLayout()
        build_protocol_layout.addWidget(build_protocol_set_parameters_label)
        build_protocol_layout.addLayout(baseline_subLayout)
        build_protocol_layout.addLayout(conditioned_stimulus_subLayout)
        build_protocol_layout.addLayout(inter_stimulus_interval_subLayout)
        build_protocol_layout.addLayout(post_hold_duration_subLayout)
        build_protocol_layout.addWidget(h_line_1)
        build_protocol_layout.addWidget(build_protocol_build_protocol_label)
        build_protocol_layout.addWidget(self.protocol_plot_webEngine)
        build_protocol_layout.addLayout(build_protocol_subLayout)
        build_protocol_layout.addWidget(h_line_2)
        build_protocol_layout.addLayout(terminate_build_protocol_subLayout)

        # Set widget layout
        self.setLayout(build_protocol_layout)

        # Show widget
        self.setWindowTitle('Build Protocol')
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.resize(1024, 720)
        self.show()

        # Start event loop
        self.main_widget_handle.exec_event_loop()  # Temporary pause until freezing threshold updated

    def closeEvent(self, event):
        self.main_widget_handle.exit_event_loop()  # Release event loop
        event.accept()  # Close window

    def close_widget(self, widget):
        widget.close()

    def action_update_baseline(self):
        # Update changed text
        try:
            self.baseline = int(self.build_protocol_baseline_lineEdit.text())
        except:
            self.baseline = 120  # sec

    def action_update_conditioned_stimulus(self):
        # Update changed text
        try:
            self.conditioned_stimulus = int(self.build_protocol_conditioned_stimulus_lineEdit.text())
        except:
            self.conditioned_stimulus = 30  # sec

    def action_update_inter_stimulus_interval(self):
        # Update changed text
        try:
            self.inter_stimulus_interval = int(self.build_protocol_inter_stimulus_interval_lineEdit.text())
        except:
            self.inter_stimulus_interval = 30  # sec

    def action_update_post_hold_duration(self):
        # Update changed text
        try:
            self.post_hold_duration = int(self.build_protocol_post_hold_duration_lineEdit.text())
        except:
            self.post_hold_duration = 30  # sec

    def action_add_protocol(self):
        # Add protocols
        if self.baseline > 0 and self.event_counts == 0:  # When baseline duration exists...
            # Update total duration
            self.total_duration += self.baseline
            self.protocol.append(self.baseline)

            # Increase event counts
            self.event_counts += 1

        # Add events
        self.fig.add_shape(type='rect',
                           x0=self.total_duration,
                           y0=self.event_display_value - self.event_display_width,
                           x1=self.total_duration + self.conditioned_stimulus,
                           y1=self.event_display_value + self.event_display_width,
                           line=dict(color='Grey', width=2),
                           fillcolor='LightGrey')

        self.protocol.append(self.conditioned_stimulus)
        self.protocol.append(self.inter_stimulus_interval)
        self.total_duration += self.conditioned_stimulus + self.inter_stimulus_interval

        self.fig.update_xaxes(range=[0, self.total_duration * 1.5], showgrid=True)
        self.protocol_plot_webEngine.setHtml(self.fig.to_html(include_plotlyjs='cdn'))  # Update plot

        # Increase event counts
        self.event_counts += 1

    def action_reset_protocol(self):
        # Reset protocol
        self.protocol = []

        # Reset total duration
        self.total_duration = 0  # sec

        # Reset event counts
        self.event_counts = 0

        # Reset figure
        self.fig = go.Figure()
        self.fig.update_xaxes(range=[0, 60], showgrid=True)
        self.fig.update_xaxes(title='Time (s)')
        self.fig.update_yaxes(range=[0, 10], showgrid=True)
        self.fig.update_yaxes(title='Protocol')
        self.fig.update_layout(margin=dict(l=20, r=20, t=20, b=20))

        # Reset figure on WebEngineView
        self.protocol_plot_webEngine.setHtml(self.fig.to_html(include_plotlyjs='cdn'))

    def action_set_protocol(self):
        # Update given protocol
        try:
            self.add_post_hold_duration()  # Add post-hold duration
            self.main_widget_handle.protocol = self.protocol
        except:
            self.main_widget_handle.protocol = self.default_protocol

        # Release event loop
        self.main_widget_handle.exit_event_loop()

        # Close widget
        self.close_widget(self)

    def action_cancel_protocol(self):
        self.close_widget(self)

    def add_post_hold_duration(self):
        # Add post-hold duration at the end of the protocol
        last_iti = self.protocol.pop()  # Remove last ITI
        self.total_duration -= last_iti

        self.protocol.append(self.post_hold_duration)  # Append post-hold duration
        self.total_duration += self.post_hold_duration

from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtWebEngineWidgets import *

import plotly.graph_objects as go

import freezy


class SelectFreezingThresholdWidget(QWidget):
    def __init__(self, main_widget_handle, speed_distribution):
        super().__init__()

        self.init_parameters(main_widget_handle, speed_distribution)  # init parameters
        self.init_select_freezing_threshold()  # init select freezing threshold

    def init_parameters(self, main_widget_handle, speed_distribution):
        self.main_widget_handle = main_widget_handle
        self.speed_distribution = speed_distribution

        # Freezing threshold
        self.freezing_threshold = self.main_widget_handle.freezing_threshold

    def init_select_freezing_threshold(self):
        # Parameters
        # speed_distribution [ndarr, 1D]: Return of the 'compute_speed_distribution'.

        # Estimate freezing threshold
        freezing_threshold_1 = freezy.estimate_freezing_threshold(self.speed_distribution, detection_threshold=0.01)
        freezing_threshold_5 = freezy.estimate_freezing_threshold(self.speed_distribution, detection_threshold=0.05)
        freezing_threshold_10 = freezy.estimate_freezing_threshold(self.speed_distribution, detection_threshold=0.1)
        freezing_threshold_20 = freezy.estimate_freezing_threshold(self.speed_distribution, detection_threshold=0.2)
        freezing_threshold_50 = freezy.estimate_freezing_threshold(self.speed_distribution, detection_threshold=0.5)

        # Figure
        fig = go.Figure()
        fig.add_trace(go.Scatter(y=self.speed_distribution, mode='lines'))
        fig.add_hline(y=freezing_threshold_1, line_dash='dash', line_color='green',
                      annotation_text='Superior 1% (Recommended)')
        fig.add_hline(y=freezing_threshold_5, line_dash='dash', line_color='blue', annotation_text='Superior 5%')
        fig.add_hline(y=freezing_threshold_10, line_dash='dash', line_color='red', annotation_text='Superior 10%')
        fig.add_hline(y=freezing_threshold_20, line_dash='dash', line_color='purple', annotation_text='Superior 20%')
        fig.add_hline(y=freezing_threshold_50, line_dash='dash', line_color='grey', annotation_text='Superior 50%')
        fig.update_xaxes(title='Timestamp (s)')
        fig.update_yaxes(title='Speed (cm/s)')
        fig.update_layout(margin=dict(l=20, r=20, t=20, b=20))

        # Widgets
        speed_distribution_plot_webEngine = QWebEngineView()  # Plot: WebEngineView
        speed_distribution_plot_webEngine.setHtml(fig.to_html(include_plotlyjs='cdn'))

        select_freezing_threshold_speed_distribution = QLabel('Speed distribution')  # Label
        select_freezing_threshold_estimation_label = QLabel('Freezing threshold estimation:')
        select_freezing_threshold_label = QLabel('Select threshold:')
        select_freezing_threshold_1_label = QLabel('Superior 1 %:')
        select_freezing_threshold_5_label = QLabel('Superior 5 %:')
        select_freezing_threshold_10_label = QLabel('Superior 10 %:')
        select_freezing_threshold_20_label = QLabel('Superior 20 %:')
        select_freezing_threshold_50_label = QLabel('Superior 50 %:')

        self.select_freezing_threshold_editField = QLineEdit()  # LineEdit
        self.select_freezing_threshold_editField.setPlaceholderText('Select freezing threshold.')
        self.select_freezing_threshold_editField.setText(str(self.freezing_threshold))
        self.select_freezing_threshold_editField.setValidator(QDoubleValidator())

        select_freezing_threshold_1_lineEdit = QLineEdit()
        select_freezing_threshold_1_lineEdit.setText(str(freezing_threshold_1))
        select_freezing_threshold_1_lineEdit.setReadOnly(True)

        select_freezing_threshold_5_lineEdit = QLineEdit()
        select_freezing_threshold_5_lineEdit.setText(str(freezing_threshold_5))
        select_freezing_threshold_5_lineEdit.setReadOnly(True)

        select_freezing_threshold_10_lineEdit = QLineEdit()
        select_freezing_threshold_10_lineEdit.setText(str(freezing_threshold_10))
        select_freezing_threshold_10_lineEdit.setReadOnly(True)

        select_freezing_threshold_20_lineEdit = QLineEdit()
        select_freezing_threshold_20_lineEdit.setText(str(freezing_threshold_20))
        select_freezing_threshold_20_lineEdit.setReadOnly(True)

        select_freezing_threshold_50_lineEdit = QLineEdit()
        select_freezing_threshold_50_lineEdit.setText(str(freezing_threshold_50))
        select_freezing_threshold_50_lineEdit.setReadOnly(True)

        select_freezing_threshold_button = QPushButton('Select Threshold')  # Button
        select_freezing_threshold_button.clicked.connect(self.action_update_freezing_threshold)

        # Frame
        h_line = QFrame(self)
        h_line.setFrameShape(QFrame.Shape.HLine)
        h_line.setFrameShadow(QFrame.Shadow.Sunken)

        # Layout
        select_freezing_threshold_subLayout = QHBoxLayout()
        select_freezing_threshold_subLayout.addWidget(select_freezing_threshold_label)
        select_freezing_threshold_subLayout.addWidget(self.select_freezing_threshold_editField)

        select_freezing_threshold_1_subLayout = QHBoxLayout()
        select_freezing_threshold_1_subLayout.addWidget(select_freezing_threshold_1_label)
        select_freezing_threshold_1_subLayout.addWidget(select_freezing_threshold_1_lineEdit)

        select_freezing_threshold_5_subLayout = QHBoxLayout()
        select_freezing_threshold_5_subLayout.addWidget(select_freezing_threshold_5_label)
        select_freezing_threshold_5_subLayout.addWidget(select_freezing_threshold_5_lineEdit)

        select_freezing_threshold_10_subLayout = QHBoxLayout()
        select_freezing_threshold_10_subLayout.addWidget(select_freezing_threshold_10_label)
        select_freezing_threshold_10_subLayout.addWidget(select_freezing_threshold_10_lineEdit)

        select_freezing_threshold_20_subLayout = QHBoxLayout()
        select_freezing_threshold_20_subLayout.addWidget(select_freezing_threshold_20_label)
        select_freezing_threshold_20_subLayout.addWidget(select_freezing_threshold_20_lineEdit)

        select_freezing_threshold_50_subLayout = QHBoxLayout()
        select_freezing_threshold_50_subLayout.addWidget(select_freezing_threshold_50_label)
        select_freezing_threshold_50_subLayout.addWidget(select_freezing_threshold_50_lineEdit)

        select_freezing_threshold_layout = QVBoxLayout()
        select_freezing_threshold_layout.addWidget(select_freezing_threshold_speed_distribution)
        select_freezing_threshold_layout.addWidget(speed_distribution_plot_webEngine)

        select_freezing_threshold_layout.addWidget(h_line)  # Horizontal line

        select_freezing_threshold_layout.addWidget(select_freezing_threshold_estimation_label)
        select_freezing_threshold_layout.addLayout(select_freezing_threshold_1_subLayout)
        select_freezing_threshold_layout.addLayout(select_freezing_threshold_5_subLayout)
        select_freezing_threshold_layout.addLayout(select_freezing_threshold_10_subLayout)
        select_freezing_threshold_layout.addLayout(select_freezing_threshold_20_subLayout)
        select_freezing_threshold_layout.addLayout(select_freezing_threshold_50_subLayout)

        select_freezing_threshold_layout.addWidget(h_line)  # Horizontal line

        select_freezing_threshold_layout.addLayout(select_freezing_threshold_subLayout)
        select_freezing_threshold_layout.addWidget(select_freezing_threshold_button)

        # Set widget layout
        self.setLayout(select_freezing_threshold_layout)

        # Show widget
        self.setWindowTitle('Select Freezing Threshold')
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.resize(720, 620)
        self.show()

        # Start event loop
        self.main_widget_handle.exec_event_loop()  # Temporary pause until freezing threshold updated

    def closeEvent(self, event):
        self.main_widget_handle.exit_event_loop()  # Release event loop
        event.accept()  # Close window

    def action_update_freezing_threshold(self):
        # Check unfilled freezing threshold
        if self.select_freezing_threshold_editField.text() == '':
            message = QMessageBox.warning(self, 'Warning',
                                          'Freezing threshold is empty. Are you sure to abort analysis?',
                                          QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                          QMessageBox.StandardButton.No)
            if message == QMessageBox.StandardButton.No:
                return
            if message == QMessageBox.StandardButton.Yes:
                self.close_widget(self)

        # Update freezing threshold
        self.freezing_threshold = float(self.select_freezing_threshold_editField.text())

        # Update freezing threshold in MainWindow
        self.main_widget_handle.freezing_threshold = self.freezing_threshold

        # Release event loop
        self.main_widget_handle.exit_event_loop()

        # Close widget
        self.close_widget(self)

    def close_widget(self, widget):
        widget.close()

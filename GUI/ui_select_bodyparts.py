from PyQt6.QtCore import *
from PyQt6.QtWidgets import *


class SelectBodypartsWidget(QWidget):
    def __init__(self, main_widget_handle, dlc_coordinates):
        super().__init__()

        self.init_parameters(main_widget_handle, dlc_coordinates)  # init parameters
        self.init_select_bodyparts()  # init select bodypart ui and actions

    def init_parameters(self, main_widget_handle, dlc_coordinates):
        # Set parameters
        self.main_widget_handle = main_widget_handle
        self.dlc_coordinates = dlc_coordinates

        # Bodyparts to extract
        self.x_bodypart = 'none'
        self.y_bodypart = 'none'

    def init_select_bodyparts(self):
        # Parameters
        # dlc_coordinates [DataFrame]: Return of 'extract_data'.

        # Widgets
        select_bodypart_x_coordinates_label = QLabel('Select X bodypart.')  # Labels
        select_bodypart_y_coordinates_label = QLabel('Select Y bodypart.')

        self.select_bodypart_x_coordinates_comboBox = QComboBox(self)  # ComboBox
        [self.select_bodypart_x_coordinates_comboBox.addItem(x_bodypart_item) for x_bodypart_item in
         self.dlc_coordinates]
        self.select_bodypart_y_coordinates_comboBox = QComboBox(self)
        [self.select_bodypart_y_coordinates_comboBox.addItem(y_bodypart_item) for y_bodypart_item in
         self.dlc_coordinates]

        select_bodypart_button = QPushButton('Done')  # Buttons
        select_bodypart_button.clicked.connect(self.action_select_bodyparts)

        # Layout
        select_bodypart_x_layout = QVBoxLayout()
        select_bodypart_x_layout.addWidget(select_bodypart_x_coordinates_label)
        select_bodypart_x_layout.addWidget(self.select_bodypart_x_coordinates_comboBox)

        select_bodypart_y_layout = QVBoxLayout()
        select_bodypart_y_layout.addWidget(select_bodypart_y_coordinates_label)
        select_bodypart_y_layout.addWidget(self.select_bodypart_y_coordinates_comboBox)

        sub_select_bodyparts_layout = QHBoxLayout()
        sub_select_bodyparts_layout.addLayout(select_bodypart_x_layout)
        sub_select_bodyparts_layout.addLayout(select_bodypart_y_layout)

        select_bodyparts_layout = QVBoxLayout()
        select_bodyparts_layout.addLayout(sub_select_bodyparts_layout)
        select_bodyparts_layout.addWidget(select_bodypart_button)

        # Set widget layout
        self.setLayout(select_bodyparts_layout)

        # Show widget
        self.setWindowTitle('Select Bodyparts')
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.resize(400, 100)
        self.show()

        # Start event loop
        self.main_widget_handle.exec_event_loop()  # Temporary pause until selected bodyparts are updated

    def closeEvent(self, event):
        self.main_widget_handle.exit_event_loop()  # Release event loop
        event.accept()  # Close window

    def action_select_bodyparts(self):
        # Update bodyparts
        self.x_bodypart = self.select_bodypart_x_coordinates_comboBox.currentText()
        self.y_bodypart = self.select_bodypart_x_coordinates_comboBox.currentText()

        # Update bodyparts in MainWindow
        self.main_widget_handle.x_bodypart = self.x_bodypart
        self.main_widget_handle.y_bodypart = self.y_bodypart

        # Release event loop
        self.main_widget_handle.exit_event_loop()

        # Close widget
        self.close_widget(self)

    def close_widget(self, widget):
        widget.close()

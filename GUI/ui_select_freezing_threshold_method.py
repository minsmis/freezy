from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout,
    QRadioButton, QPushButton, QLabel
)
from PyQt6.QtCore import Qt


class SelectFreezingThresholdModeDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.selected_mode = None  # 'auto', '1%', '5%'
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Freezing Threshold Selection")
        self.setWindowModality(Qt.WindowModality.ApplicationModal)

        label = QLabel("Select freezing threshold mode:")

        self.radio_auto = QRadioButton("Auto (recommended)")
        self.radio_1 = QRadioButton("Superior 1%")
        self.radio_5 = QRadioButton("Superior 5%")
        self.radio_manual = QRadioButton("Manual")

        self.radio_auto.setChecked(True)

        ok_button = QPushButton("OK")
        cancel_button = QPushButton("Cancel")

        ok_button.clicked.connect(self.accept_selection)
        cancel_button.clicked.connect(self.reject)

        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(self.radio_auto)
        layout.addWidget(self.radio_1)
        layout.addWidget(self.radio_5)
        layout.addWidget(self.radio_manual)

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(ok_button)
        button_layout.addWidget(cancel_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)
        self.resize(360, 180)

    def accept_selection(self):
        if self.radio_auto.isChecked():
            self.selected_mode = 'auto'
        elif self.radio_1.isChecked():
            self.selected_mode = 'superior_1'
        elif self.radio_5.isChecked():
            self.selected_mode = 'superior_5'
        elif self.radio_manual.isChecked():
            self.selected_mode = 'manual'

        self.accept()

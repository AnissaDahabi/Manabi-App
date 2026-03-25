from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QStackedWidget, QLabel, QPushButton
from PySide6.QtCore import Qt

class PageReservations(QMainWindow):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)

        self.label = QLabel("Liste des Utilisateurs")
        self.label.setStyleSheet("font-size: 20px; font-weight: bold; color: white;")
        self.layout.addWidget(self.label)
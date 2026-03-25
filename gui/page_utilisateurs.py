from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QStackedWidget, QLabel, QPushButton
from PySide6.QtCore import Qt

class PageUtilisateurs(QMainWindow):
    def __init__(self):
        super().__init__()

        container = QWidget()
        self.setCentralWidget(container)

        self.layout = QVBoxLayout(container)
        self.layout.setContentsMargins(20, 20, 20, 20)

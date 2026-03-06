from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QMainWindow, QStackedWidget, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
from PySide6.QtCore import Qt
from .page_afficher import PageAfficher

class MainWindow(QMainWindow):
    def __init__(self, curseur):
        super().__init__()
        self.curseur = curseur
        self.setWindowTitle("Manabi App")
        self.setGeometry(100, 100, 800, 600)

        self.pages = QStackedWidget()
        self.setCentralWidget(self.pages)

        # Page Accueil
        self.page_accueil = QWidget()
        acc_layout = QVBoxLayout(self.page_accueil)
        acc_layout.setContentsMargins(50, 50, 50, 50)

        label_accueil = QLabel("Bienvenue sur Manabi!")
        label_accueil.setAlignment(Qt.AlignCenter)
        acc_layout.addWidget(label_accueil)

        image = QLabel()
        pixmap = QPixmap("images/logoAccueil.png")
        image.setPixmap(pixmap.scaled(250, 250, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        image.setAlignment(Qt.AlignCenter)
        acc_layout.addWidget(image)

        btn_go = QPushButton("Afficher")
        btn_go.clicked.connect(lambda: self.pages.setCurrentIndex(1))
        acc_layout.addWidget(btn_go, alignment=Qt.AlignCenter)

        # Page Liste
        self.page_afficher = PageAfficher(self.curseur, self.pages, lambda: self.pages.setCurrentIndex(0))

        self.pages.addWidget(self.page_accueil)
        self.pages.addWidget(self.page_afficher)
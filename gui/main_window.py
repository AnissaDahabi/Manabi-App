from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtWidgets import QPushButton, QHBoxLayout

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Manabi - Révisions de Kanji")
        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        buttons_layout = QHBoxLayout()
        layout.addLayout(buttons_layout)

        bouton_afficher = QPushButton("Afficher")
        bouton_ajouter = QPushButton("Ajouter")
        bouton_modifier = QPushButton("Modifier")
        bouton_supprimer = QPushButton("Supprimer")

        buttons_layout.addWidget(bouton_afficher)
        buttons_layout.addWidget(bouton_ajouter)
        buttons_layout.addWidget(bouton_modifier)
        buttons_layout.addWidget(bouton_supprimer)

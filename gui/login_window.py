from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
)
from PySide6.QtCore import Qt

from services.login_service import verifier_connexion

class LoginWindow(QWidget):
    def __init__(self, on_success):
        super().__init__()
        self.on_success = on_success

        self.setWindowTitle("Manabi - Connexion")
        self.setFixedSize(400, 450)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setObjectName("loginWindow")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(16)
        layout.setAlignment(Qt.AlignCenter)

        kanji = QLabel("学")
        kanji.setObjectName("loginKanji")
        kanji.setAlignment(Qt.AlignCenter)
        layout.addWidget(kanji)

        titre = QLabel("Manabi Admin")
        titre.setObjectName("loginTitre")
        titre.setAlignment(Qt.AlignCenter)
        layout.addWidget(titre)

        sous_titre = QLabel("Connectez-vous pour accéder à la plateforme d'administration")
        sous_titre.setObjectName("loginSousTitre")
        sous_titre.setAlignment(Qt.AlignCenter)
        sous_titre.setWordWrap(True)
        layout.addWidget(sous_titre)

        self.input_email = QLineEdit()
        self.input_email.setPlaceholderText("Adresse email")
        self.input_email.setFixedHeight(40)
        layout.addWidget(self.input_email)

        self.input_password = QLineEdit()
        self.input_password.setPlaceholderText("Mot de passe")
        self.input_password.setEchoMode(QLineEdit.Password)
        self.input_password.setFixedHeight(40)
        self.input_password.returnPressed.connect(self.tenter_connexion)
        layout.addWidget(self.input_password)

        self.lbl_erreur = QLabel("")
        self.lbl_erreur.setObjectName("loginErreur")
        self.lbl_erreur.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.lbl_erreur)

        btn = QPushButton("Se connecter")
        btn.setObjectName("btnLogin")
        btn.setFixedHeight(42)
        btn.setCursor(Qt.PointingHandCursor)
        btn.clicked.connect(self.tenter_connexion)
        layout.addWidget(btn)

    def tenter_connexion(self):
        email = self.input_email.text().strip()
        password = self.input_password.text().strip()

        if not email or not password:
            self.lbl_erreur.setText("Veuillez remplir tous les champs.")
            return

        user = verifier_connexion(email, password)

        if user is None:
            self.lbl_erreur.setText("Email ou mot de passe incorrect.")
            self.input_password.clear()
        else:
            self.on_success(user)
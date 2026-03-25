from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QStackedWidget, QLabel, QPushButton
from PySide6.QtCore import Qt

from gui.page_utilisateurs import PageUtilisateurs
from gui.page_cours import PageCours
from gui.page_sessions import PageSessions
from gui.page_reservations import PageReservations

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Manabi Admin")
        self.resize(1100, 700)

        self.setup_ui()

        self.page_users = PageUtilisateurs()
        self.page_cours = PageCours()
        self.page_sessions = PageSessions()
        self.page_resas = PageReservations()

        self.content_stack.addWidget(self.page_users)
        self.content_stack.addWidget(self.page_cours)
        self.content_stack.addWidget(self.page_sessions)
        self.content_stack.addWidget(self.page_resas)

        self.btn_users.clicked.connect(lambda: self.naviguer(0, "Gestion des Utilisateurs", self.btn_users))
        self.btn_cours.clicked.connect(lambda: self.naviguer(1, "Gestion des Cours", self.btn_cours))
        self.btn_sessions.clicked.connect(lambda: self.naviguer(2, "Gestion des Sessions", self.btn_sessions))
        self.btn_reservations.clicked.connect(lambda: self.naviguer(3, "Gestion des Réservations", self.btn_reservations))

        self.naviguer(0, "Gestion des Utilisateurs", self.btn_users)

    def naviguer(self, index, titre, bouton):
        self.content_stack.setCurrentIndex(index)
        self.topbar_label.setText(titre)

        for b in [self.btn_users, self.btn_cours, self.btn_sessions, self.btn_reservations]:
            b.setChecked(False)
        bouton.setChecked(True)

    def setup_ui(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QHBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # sidebar
        self.sidebar = QWidget()
        self.sidebar.setObjectName("sideBar")
        self.sidebar.setFixedWidth(200)
        self.sidebar.setAttribute(Qt.WA_StyledBackground, True)

        self.sidebar_layout = QVBoxLayout(self.sidebar)
        self.sidebar_layout.setContentsMargins(10, 20, 10, 20)
        self.sidebar_layout.setSpacing(10)

        # logo et titre
        self.logo_label = QLabel("学")
        self.logo_label.setAlignment(Qt.AlignCenter)
        self.logo_label.setObjectName("logo")

        self.logo_title = QLabel("Manabi Admin")
        self.logo_title.setAlignment(Qt.AlignCenter)
        self.logo_title.setObjectName("title")

        self.sidebar_layout.addWidget(self.logo_label)
        self.sidebar_layout.addWidget(self.logo_title)

        # boutons
        self.btn_users = QPushButton("Utilisateurs")
        self.btn_cours = QPushButton("Cours")
        self.btn_sessions = QPushButton("Sessions")
        self.btn_reservations = QPushButton("Réservations")

        for b in [self.btn_users, self.btn_cours, self.btn_sessions, self.btn_reservations]:
            b.setCheckable(True)
            b.setCursor(Qt.PointingHandCursor)
            self.sidebar_layout.addWidget(b)

        self.sidebar_layout.addStretch()

        # main area
        self.main_area_widget = QWidget()
        self.main_area_layout = QVBoxLayout(self.main_area_widget)
        self.main_area_layout.setContentsMargins(20, 10, 20, 20)
        self.main_area_layout.setSpacing(10)

        # topbar
        self.topbar_widget = QWidget()
        self.topbar_layout = QHBoxLayout(self.topbar_widget)
        self.topbar_layout.setContentsMargins(0, 0, 0, 0)

        self.topbar_label = QLabel("Titre")
        self.topbar_label.setObjectName("topbarLabel")

        self.btn_ajouter = QPushButton("Ajouter")
        self.btn_ajouter.setObjectName("btnAjouter")
        self.btn_ajouter.setFixedSize(120, 40)
        self.btn_ajouter.setCursor(Qt.PointingHandCursor)

        self.topbar_layout.addWidget(self.topbar_label)
        self.topbar_layout.addStretch()
        self.topbar_layout.addWidget(self.btn_ajouter)

        self.content_stack = QStackedWidget()

        self.main_area_layout.addWidget(self.topbar_widget)
        self.main_area_layout.addWidget(self.content_stack)

        self.main_layout.addWidget(self.sidebar)
        self.main_layout.addWidget(self.main_area_widget)
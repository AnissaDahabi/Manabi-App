from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QHeaderView, QLabel, QLineEdit, QComboBox,
    QFrame, QMessageBox
)
from PySide6.QtCore import Qt

from models.user import User
from services.user_service import get_all_users, delete_user, create_user, update_user

ROLES = ["admin", "professeur", "eleve"]

BTN_ACTION_STYLE = """
    QPushButton {
        background-color: #c0392b;
        color: #FFF;
        font-family: 'DM Sans', sans-serif;
        font-size: 13px;
        font-weight: bold;
        border-radius: 20px;
        padding: 5px 15px;
        min-width: 110px;
        min-height: 32px;
        border: none;
    }
    QPushButton:hover { background-color: #922b21; }
    QPushButton:disabled { background-color: #ddd; color: #aaa; }
"""

BTN_GHOST_STYLE = """
    QPushButton {
        background-color: transparent;
        color: #8a8580;
        font-family: 'DM Sans', sans-serif;
        font-size: 13px;
        border-radius: 20px;
        padding: 5px 15px;
        min-width: 90px;
        min-height: 32px;
        border: 1px solid #E0DDD8;
    }
    QPushButton:hover { background-color: #f4f1ec; color: #2c2c2c; font-weight: normal; }
"""

LABEL_FORM_STYLE = "font-size: 12px; font-weight: bold; color: #8a8580; font-family: 'DM Sans', sans-serif;"

INPUT_STYLE = """
    QLineEdit, QComboBox {
        color: #2c2c2c;
        border: 1px solid #E0DDD8;
        border-radius: 8px;
        padding: 8px 12px;
        font-size: 13px;
        background: #faf9f7;
        font-family: 'DM Sans', sans-serif;
    }
    QLineEdit:focus, QComboBox:focus {
        border: 1px solid #c0392b;
        background: white;
    }
    QComboBox::drop-down { border: none; width: 20px; }
    QComboBox QAbstractItemView {
        background-color: #faf9f7;
        color: #2c2c2c;
        selection-background-color: #ECE0CF;
        border: 1px solid #E0DDD8;
    }
"""


def make_label(text):
    lbl = QLabel(text)
    lbl.setStyleSheet(LABEL_FORM_STYLE)
    return lbl


class PanneauUtilisateur(QFrame):
    """Panneau latéral de création / modification d'un utilisateur."""

    def __init__(self, parent_page):
        super().__init__()
        self.parent_page = parent_page
        self.user_data = None

        self.setObjectName("panneauUser")
        self.setFixedWidth(300)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet("""
            #panneauUser {
                background-color: #f4f1ec;
                border-left: 1px solid #E0DDD8;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        self.titre_label = QLabel("Ajouter un utilisateur")
        self.titre_label.setStyleSheet("""
            font-size: 15px;
            font-weight: bold;
            font-family: 'Noto Serif JP', Georgia, serif;
            color: #2c2c2c;
            padding-bottom: 4px;
        """)
        layout.addWidget(self.titre_label)

        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setStyleSheet("color: #E0DDD8;")
        layout.addWidget(sep)

        layout.addWidget(make_label("Nom"))
        self.input_nom = QLineEdit()
        self.input_nom.setPlaceholderText("Nom de famille")
        self.input_nom.setFixedHeight(38)
        self.input_nom.setStyleSheet(INPUT_STYLE)
        layout.addWidget(self.input_nom)

        layout.addWidget(make_label("Prénom"))
        self.input_prenom = QLineEdit()
        self.input_prenom.setPlaceholderText("Prénom")
        self.input_prenom.setFixedHeight(38)
        self.input_prenom.setStyleSheet(INPUT_STYLE)
        layout.addWidget(self.input_prenom)

        layout.addWidget(make_label("Email"))
        self.input_email = QLineEdit()
        self.input_email.setPlaceholderText("adresse@email.com")
        self.input_email.setFixedHeight(38)
        self.input_email.setStyleSheet(INPUT_STYLE)
        layout.addWidget(self.input_email)

        layout.addWidget(make_label("Mot de passe"))
        self.input_password = QLineEdit()
        self.input_password.setPlaceholderText("Laisser vide pour ne pas modifier")
        self.input_password.setEchoMode(QLineEdit.Password)
        self.input_password.setFixedHeight(38)
        self.input_password.setStyleSheet(INPUT_STYLE)
        layout.addWidget(self.input_password)

        layout.addWidget(make_label("Rôle"))
        self.combo_role = QComboBox()
        self.combo_role.addItems(ROLES)
        self.combo_role.setFixedHeight(38)
        self.combo_role.setStyleSheet(INPUT_STYLE)
        layout.addWidget(self.combo_role)

        self.lbl_erreur = QLabel("")
        self.lbl_erreur.setStyleSheet("color: #c0392b; font-size: 12px;")
        self.lbl_erreur.setWordWrap(True)
        layout.addWidget(self.lbl_erreur)

        layout.addStretch()

        btn_row = QHBoxLayout()
        btn_row.setSpacing(8)
        self.btn_annuler = QPushButton("Annuler")
        self.btn_annuler.setStyleSheet(BTN_GHOST_STYLE)
        self.btn_annuler.setCursor(Qt.PointingHandCursor)
        self.btn_annuler.clicked.connect(self.parent_page.fermer_panneau)
        self.btn_enregistrer = QPushButton("Enregistrer")
        self.btn_enregistrer.setStyleSheet(BTN_ACTION_STYLE)
        self.btn_enregistrer.setCursor(Qt.PointingHandCursor)
        self.btn_enregistrer.clicked.connect(self.enregistrer)
        btn_row.addWidget(self.btn_annuler)
        btn_row.addWidget(self.btn_enregistrer)
        layout.addLayout(btn_row)

    def ouvrir_creation(self):
        self.user_data = None
        self.titre_label.setText("Ajouter un utilisateur")
        self.input_nom.clear()
        self.input_prenom.clear()
        self.input_email.clear()
        self.input_password.clear()
        self.input_password.setPlaceholderText("Mot de passe")
        self.combo_role.setCurrentIndex(0)
        self.lbl_erreur.setText("")
        self.show()

    def ouvrir_modification(self, user_data):
        # user_data : id, nom, prenom, email, password, role
        self.user_data = user_data
        self.titre_label.setText("Modifier l'utilisateur")
        self.input_nom.setText(user_data[1])
        self.input_prenom.setText(user_data[2])
        self.input_email.setText(user_data[3])
        self.input_password.clear()
        self.input_password.setPlaceholderText("Laisser vide pour ne pas modifier")
        idx = self.combo_role.findText(user_data[5])
        self.combo_role.setCurrentIndex(idx if idx >= 0 else 0)
        self.lbl_erreur.setText("")
        self.show()

    def enregistrer(self):
        nom = self.input_nom.text().strip()
        prenom = self.input_prenom.text().strip()
        email = self.input_email.text().strip()
        password = self.input_password.text().strip()
        role = self.combo_role.currentText()

        if not nom or not prenom or not email:
            self.lbl_erreur.setText("Nom, prénom et email sont obligatoires.")
            return

        if self.user_data is None:
            if not password:
                self.lbl_erreur.setText("Le mot de passe est obligatoire à la création.")
                return
            create_user(User(None, nom, prenom, email, password, role))
        else:
            # Conserver l'ancien mot de passe si le champ est vide
            final_password = password if password else self.user_data[4]
            update_user(User(self.user_data[0], nom, prenom, email, final_password, role))

        self.parent_page.fermer_panneau()
        self.parent_page.charger_utilisateurs()


class PageUtilisateurs(QWidget):
    def __init__(self):
        super().__init__()

        self.selected_user_id = None
        self.selected_user_data = None
        self.users = []

        self.root_layout = QHBoxLayout(self)
        self.root_layout.setContentsMargins(0, 0, 0, 0)
        self.root_layout.setSpacing(0)

        # Zone gauche
        self.left_widget = QWidget()
        self.main_layout = QVBoxLayout(self.left_widget)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(16)

        # Tableau
        self.table = QTableWidget()
        self.table.setColumnCount(5)  # Nom, Prénom, Email, Rôle, ID caché
        self.table.setHorizontalHeaderLabels(["Nom", "Prénom", "Email", "Rôle", "ID"])

        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.setAlternatingRowColors(True)
        self.table.setShowGrid(False)
        self.table.horizontalHeader().setStretchLastSection(False)
        self.table.verticalHeader().setVisible(False)
        self.table.verticalHeader().setDefaultSectionSize(45)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)

        self.table.setColumnWidth(0, 180)
        self.table.setColumnWidth(1, 180)
        self.table.setColumnWidth(2, 300)
        self.table.setColumnWidth(3, 120)
        self.table.setColumnHidden(4, True)

        self.table.itemSelectionChanged.connect(self.on_selection_changed)
        self.main_layout.addWidget(self.table)

        # Boutons bas
        self.bottom_layout = QHBoxLayout()
        self.bottom_layout.setContentsMargins(0, 8, 0, 0)

        self.btn_modifier = QPushButton("Modifier")
        self.btn_modifier.setStyleSheet(BTN_ACTION_STYLE)
        self.btn_modifier.setCursor(Qt.PointingHandCursor)
        self.btn_modifier.setEnabled(False)
        self.btn_modifier.clicked.connect(self.modifier_selection)

        self.btn_supprimer = QPushButton("Supprimer")
        self.btn_supprimer.setStyleSheet(BTN_ACTION_STYLE)
        self.btn_supprimer.setCursor(Qt.PointingHandCursor)
        self.btn_supprimer.setEnabled(False)
        self.btn_supprimer.clicked.connect(self.supprimer_selection)

        self.bottom_layout.addStretch()
        self.bottom_layout.addWidget(self.btn_modifier)
        self.bottom_layout.addSpacing(40)
        self.bottom_layout.addWidget(self.btn_supprimer)
        self.bottom_layout.addStretch()
        self.main_layout.addLayout(self.bottom_layout)

        # Panneau latéral
        self.panneau = PanneauUtilisateur(self)
        self.panneau.hide()

        self.root_layout.addWidget(self.left_widget)
        self.root_layout.addWidget(self.panneau)

        self.charger_utilisateurs()

    def ajouter(self):
        self.table.clearSelection()
        self.panneau.ouvrir_creation()

    def fermer_panneau(self):
        self.panneau.hide()

    def charger_utilisateurs(self):
        self.users = get_all_users()
        self.table.setRowCount(0)

        for row_index, user in enumerate(self.users):
            self.table.insertRow(row_index)
            self.table.setItem(row_index, 0, QTableWidgetItem(user[1]))
            self.table.setItem(row_index, 1, QTableWidgetItem(user[2]))
            self.table.setItem(row_index, 2, QTableWidgetItem(user[3]))
            self.table.setItem(row_index, 3, QTableWidgetItem(user[5]))
            self.table.setItem(row_index, 4, QTableWidgetItem(str(user[0])))

        self.table.resizeRowsToContents()
        self.table.clearSelection()
        self.selected_user_id = None
        self.selected_user_data = None
        self._update_buttons()

    def on_selection_changed(self):
        row = self.table.currentRow()
        if row == -1 or row >= len(self.users):
            self.selected_user_id = None
            self.selected_user_data = None
        else:
            self.selected_user_id = self.users[row][0]
            self.selected_user_data = self.users[row]
        self._update_buttons()

    def _update_buttons(self):
        enabled = self.selected_user_id is not None
        self.btn_modifier.setEnabled(enabled)
        self.btn_supprimer.setEnabled(enabled)

    def modifier_selection(self):
        if self.selected_user_data is None:
            return
        self.panneau.ouvrir_modification(self.selected_user_data)

    def supprimer_selection(self):
        if self.selected_user_id is None:
            return
        confirm = QMessageBox.question(
            self, "Confirmer la suppression",
            f"Supprimer l'utilisateur « {self.selected_user_data[2]} {self.selected_user_data[1]} » ?",
            QMessageBox.Yes | QMessageBox.No
        )
        if confirm == QMessageBox.Yes:
            delete_user(self.selected_user_id)
            self.fermer_panneau()
            self.charger_utilisateurs()
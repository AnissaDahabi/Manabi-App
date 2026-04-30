from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QHeaderView, QLabel, QLineEdit, QTextEdit, QComboBox,
    QFrame, QMessageBox
)
from PySide6.QtCore import Qt

from models.cours import Cours
from services.cours_service import (
    get_cours_enrichis,
    get_cours_enrichis_by_prof,
    create_cours,
    update_cours,
    delete_cours,
)
from services.user_service import get_all_professeurs

NIVEAUX = ["N5", "N4", "N3", "N2", "N1"]


def make_label(text):
    lbl = QLabel(text)
    lbl.setObjectName("formLabel")
    return lbl


class PanneauCours(QFrame):
    """Panneau latéral de création / modification d'un cours."""

    def __init__(self, parent_page):
        super().__init__()
        self.parent_page = parent_page
        self.cours_data = None

        self.setObjectName("panneau")
        self.setFixedWidth(300)
        self.setAttribute(Qt.WA_StyledBackground, True)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        self.titre_label = QLabel("Ajouter un cours")
        self.titre_label.setObjectName("panneauTitre")
        layout.addWidget(self.titre_label)

        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setObjectName("panneauSep")
        layout.addWidget(sep)

        layout.addWidget(make_label("Intitulé"))
        self.input_intitule = QLineEdit()
        self.input_intitule.setPlaceholderText("Ex : Japonais N5")
        self.input_intitule.setFixedHeight(38)
        layout.addWidget(self.input_intitule)

        layout.addWidget(make_label("Niveau"))
        self.combo_niveau = QComboBox()
        self.combo_niveau.addItems(NIVEAUX)
        self.combo_niveau.setFixedHeight(38)
        layout.addWidget(self.combo_niveau)

        self.lbl_prof = make_label("Professeur")
        self.combo_prof = QComboBox()
        self.combo_prof.setFixedHeight(38)
        layout.addWidget(self.lbl_prof)
        layout.addWidget(self.combo_prof)

        layout.addWidget(make_label("Description"))
        self.input_description = QTextEdit()
        self.input_description.setPlaceholderText("Description du cours...")
        self.input_description.setFixedHeight(100)
        layout.addWidget(self.input_description)

        self.lbl_erreur = QLabel("")
        self.lbl_erreur.setObjectName("formErreur")
        self.lbl_erreur.setWordWrap(True)
        layout.addWidget(self.lbl_erreur)

        layout.addStretch()

        btn_row = QHBoxLayout()
        btn_row.setSpacing(8)
        self.btn_annuler = QPushButton("Annuler")
        self.btn_annuler.setObjectName("btnGhost")
        self.btn_annuler.setCursor(Qt.PointingHandCursor)
        self.btn_annuler.clicked.connect(self.parent_page.fermer_panneau)
        self.btn_enregistrer = QPushButton("Enregistrer")
        self.btn_enregistrer.setObjectName("btnAction")
        self.btn_enregistrer.setCursor(Qt.PointingHandCursor)
        self.btn_enregistrer.clicked.connect(self.enregistrer)
        btn_row.addWidget(self.btn_annuler)
        btn_row.addWidget(self.btn_enregistrer)
        layout.addLayout(btn_row)

    def ouvrir_creation(self, is_admin, professeurs):
        self.cours_data = None
        self.titre_label.setText("Ajouter un cours")
        self.input_intitule.clear()
        self.combo_niveau.setCurrentIndex(0)
        self.input_description.clear()
        self.lbl_erreur.setText("")
        self._charger_profs(professeurs, is_admin)
        self.show()

    def ouvrir_modification(self, cours_data, is_admin, professeurs):
        self.cours_data = cours_data
        self.titre_label.setText("Modifier le cours")
        self.input_intitule.setText(cours_data[1])
        idx = self.combo_niveau.findText(cours_data[2])
        self.combo_niveau.setCurrentIndex(idx if idx >= 0 else 0)
        self.input_description.setPlainText(cours_data[4] or "")
        self.lbl_erreur.setText("")
        self._charger_profs(professeurs, is_admin, selected_prof_id=cours_data[3])
        self.show()

    def _charger_profs(self, professeurs, is_admin, selected_prof_id=None):
        self.lbl_prof.setVisible(is_admin)
        self.combo_prof.setVisible(is_admin)
        if is_admin:
            self.combo_prof.clear()
            for prof in professeurs:
                self.combo_prof.addItem(f"{prof[2]} {prof[1]}", userData=prof[0])
            if selected_prof_id is not None:
                idx = self.combo_prof.findData(selected_prof_id)
                if idx >= 0:
                    self.combo_prof.setCurrentIndex(idx)

    def enregistrer(self):
        intitule = self.input_intitule.text().strip()
        if not intitule:
            self.lbl_erreur.setText("L'intitulé est obligatoire.")
            return
        prof_id = (
            self.combo_prof.currentData()
            if self.combo_prof.isVisible()
            else self.parent_page.user[0]
        )
        niveau = self.combo_niveau.currentText()
        description = self.input_description.toPlainText().strip()

        if self.cours_data is None:
            create_cours(Cours(None, intitule, niveau, prof_id, description))
        else:
            update_cours(Cours(self.cours_data[0], intitule, niveau, prof_id, description))

        self.parent_page.fermer_panneau()
        self.parent_page.charger_cours()


class PageCours(QWidget):
    def __init__(self, user=None):
        super().__init__()

        self.user = user
        self.is_admin = user is None or user[4] == 'admin'
        self.selected_cours_id = None
        self.selected_cours_data = None
        self.cours = []
        self.professeurs = []

        self.root_layout = QHBoxLayout(self)
        self.root_layout.setContentsMargins(0, 0, 0, 0)
        self.root_layout.setSpacing(0)

        self.left_widget = QWidget()
        self.main_layout = QVBoxLayout(self.left_widget)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(16)

        # Tableau — pas de colonne ID, on stocke l'id via self.cours
        self.table = QTableWidget()
        nb_cols = 4 if self.is_admin else 3
        self.table.setColumnCount(nb_cols)

        headers = ["Intitulé", "Niveau"]
        if self.is_admin:
            headers.append("Professeur")
        headers.append("Description")
        self.table.setHorizontalHeaderLabels(headers)

        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.setAlternatingRowColors(True)
        self.table.setShowGrid(False)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.verticalHeader().setVisible(False)
        self.table.verticalHeader().setDefaultSectionSize(45)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)

        self.table.setColumnWidth(0, 220)
        self.table.setColumnWidth(1, 120)
        if self.is_admin:
            self.table.setColumnWidth(2, 180)

        self.table.itemSelectionChanged.connect(self.on_selection_changed)
        self.main_layout.addWidget(self.table)

        # Boutons bas
        self.bottom_layout = QHBoxLayout()
        self.bottom_layout.setContentsMargins(0, 8, 0, 0)

        self.btn_modifier = QPushButton("Modifier")
        self.btn_modifier.setObjectName("btnAction")
        self.btn_modifier.setCursor(Qt.PointingHandCursor)
        self.btn_modifier.setEnabled(False)
        self.btn_modifier.clicked.connect(self.modifier_selection)

        self.btn_supprimer = QPushButton("Supprimer")
        self.btn_supprimer.setObjectName("btnAction")
        self.btn_supprimer.setCursor(Qt.PointingHandCursor)
        self.btn_supprimer.setEnabled(False)
        self.btn_supprimer.clicked.connect(self.supprimer_selection)

        self.bottom_layout.addStretch()
        self.bottom_layout.addWidget(self.btn_modifier)
        self.bottom_layout.addSpacing(40)
        self.bottom_layout.addWidget(self.btn_supprimer)
        self.bottom_layout.addStretch()
        self.main_layout.addLayout(self.bottom_layout)

        self.panneau = PanneauCours(self)
        self.panneau.hide()

        self.root_layout.addWidget(self.left_widget)
        self.root_layout.addWidget(self.panneau)

        self.charger_cours()

    def ajouter(self):
        self.table.clearSelection()
        self.panneau.ouvrir_creation(self.is_admin, self._get_professeurs())

    def fermer_panneau(self):
        self.panneau.hide()

    def _get_professeurs(self):
        if not self.professeurs:
            self.professeurs = get_all_professeurs()
        return self.professeurs

    def charger_cours(self):
        if self.is_admin:
            self.cours = get_cours_enrichis()
        else:
            self.cours = get_cours_enrichis_by_prof(self.user[0])

        self.table.setRowCount(0)
        for row_index, c in enumerate(self.cours):
            # c : id, intitule, niveau, prof_id, description, prof_nom, prof_prenom
            self.table.insertRow(row_index)
            col = 0
            self.table.setItem(row_index, col, QTableWidgetItem(c[1])); col += 1
            self.table.setItem(row_index, col, QTableWidgetItem(c[2])); col += 1
            if self.is_admin:
                self.table.setItem(row_index, col, QTableWidgetItem(f"{c[6]} {c[5]}")); col += 1
            self.table.setItem(row_index, col, QTableWidgetItem(c[4] or ""))

        self.table.resizeRowsToContents()
        self.table.clearSelection()
        self.selected_cours_id = None
        self.selected_cours_data = None
        self._update_buttons()

    def on_selection_changed(self):
        row = self.table.currentRow()
        if row == -1 or row >= len(self.cours):
            self.selected_cours_id = None
            self.selected_cours_data = None
        else:
            self.selected_cours_id = self.cours[row][0]
            self.selected_cours_data = self.cours[row]
        self._update_buttons()

    def _update_buttons(self):
        enabled = self.selected_cours_id is not None
        self.btn_modifier.setEnabled(enabled)
        self.btn_supprimer.setEnabled(enabled)

    def modifier_selection(self):
        if self.selected_cours_data is None:
            return
        self.panneau.ouvrir_modification(
            self.selected_cours_data, self.is_admin, self._get_professeurs()
        )

    def supprimer_selection(self):
        if self.selected_cours_id is None:
            return
        confirm = QMessageBox.question(
            self, "Confirmer la suppression",
            f"Supprimer le cours « {self.selected_cours_data[1]} » ?",
            QMessageBox.Yes | QMessageBox.No
        )
        if confirm == QMessageBox.Yes:
            delete_cours(self.selected_cours_id)
            self.fermer_panneau()
            self.charger_cours()
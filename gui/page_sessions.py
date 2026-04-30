from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QHeaderView, QLabel, QComboBox, QFrame, QMessageBox,
    QDateEdit, QTimeEdit
)
from PySide6.QtCore import Qt, QDate, QTime

from models.session import Session
from services.session_service import (
    get_all_sessions,
    create_session,
    update_session,
    delete_session,
)
from services.cours_service import get_cours_enrichis, get_cours_enrichis_by_prof


def make_label(text):
    lbl = QLabel(text)
    lbl.setObjectName("formLabel")
    return lbl


class PanneauSession(QFrame):
    """Panneau latéral de création / modification d'une session."""

    def __init__(self, parent_page):
        super().__init__()
        self.parent_page = parent_page
        self.session_data = None

        self.setObjectName("panneau")
        self.setFixedWidth(300)
        self.setAttribute(Qt.WA_StyledBackground, True)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        self.titre_label = QLabel("Ajouter une session")
        self.titre_label.setObjectName("panneauTitre")
        layout.addWidget(self.titre_label)

        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setObjectName("panneauSep")
        layout.addWidget(sep)

        layout.addWidget(make_label("Cours"))
        self.combo_cours = QComboBox()
        self.combo_cours.setFixedHeight(38)
        layout.addWidget(self.combo_cours)

        layout.addWidget(make_label("Date de la session"))
        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.setFixedHeight(38)
        self.date_edit.setDisplayFormat("dd/MM/yyyy")
        layout.addWidget(self.date_edit)

        layout.addWidget(make_label("Heure de début"))
        self.heure_debut = QTimeEdit()
        self.heure_debut.setTime(QTime(9, 0))
        self.heure_debut.setFixedHeight(38)
        self.heure_debut.setDisplayFormat("HH:mm")
        layout.addWidget(self.heure_debut)

        layout.addWidget(make_label("Heure de fin"))
        self.heure_fin = QTimeEdit()
        self.heure_fin.setTime(QTime(10, 0))
        self.heure_fin.setFixedHeight(38)
        self.heure_fin.setDisplayFormat("HH:mm")
        layout.addWidget(self.heure_fin)

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

    def _charger_cours(self, cours_list, selected_cours_id=None):
        self.combo_cours.clear()
        for c in cours_list:
            # c : id, intitule, niveau, prof_id, description, prof_nom, prof_prenom
            label = c[1]
            self.combo_cours.addItem(label, userData=c[0])
        if selected_cours_id is not None:
            idx = self.combo_cours.findData(selected_cours_id)
            if idx >= 0:
                self.combo_cours.setCurrentIndex(idx)

    def ouvrir_creation(self, cours_list):
        self.session_data = None
        self.titre_label.setText("Ajouter une session")
        self.date_edit.setDate(QDate.currentDate())
        self.heure_debut.setTime(QTime(9, 0))
        self.heure_fin.setTime(QTime(10, 0))
        self.lbl_erreur.setText("")
        self._charger_cours(cours_list)
        self.show()

    def ouvrir_modification(self, session_data, cours_list):
        # session_data : id, cours_id, prof_id, date_session, heure_debut, heure_fin,
        #                cours_intitule, prof_nom, prof_prenom
        self.session_data = session_data
        self.titre_label.setText("Modifier la session")
        self.lbl_erreur.setText("")
        self._charger_cours(cours_list, selected_cours_id=session_data[1])

        if session_data[3]:
            self.date_edit.setDate(QDate.fromString(str(session_data[3]), "yyyy-MM-dd"))

        if session_data[4]:
            h, m = str(session_data[4])[:5].split(":")
            self.heure_debut.setTime(QTime(int(h), int(m)))

        if session_data[5]:
            h, m = str(session_data[5])[:5].split(":")
            self.heure_fin.setTime(QTime(int(h), int(m)))

        self.show()

    def enregistrer(self):
        cours_id = self.combo_cours.currentData()
        if cours_id is None:
            self.lbl_erreur.setText("Veuillez sélectionner un cours.")
            return

        debut = self.heure_debut.time()
        fin = self.heure_fin.time()
        if fin <= debut:
            self.lbl_erreur.setText("L'heure de fin doit être après l'heure de début.")
            return

        date_session = self.date_edit.date().toString("yyyy-MM-dd")
        heure_debut = self.heure_debut.time().toString("HH:mm")
        heure_fin = self.heure_fin.time().toString("HH:mm")

        # Récupérer le prof_id depuis le cours sélectionné
        cours_list = self.parent_page.cours
        prof_id = None
        for c in cours_list:
            if c[0] == cours_id:
                prof_id = c[3]
                break

        if prof_id is None and self.parent_page.user:
            prof_id = self.parent_page.user[0]

        if self.session_data is None:
            create_session(Session(None, cours_id, prof_id, date_session, heure_debut, heure_fin))
        else:
            update_session(Session(self.session_data[0], cours_id, prof_id, date_session, heure_debut, heure_fin))

        self.parent_page.fermer_panneau()
        self.parent_page.charger_sessions()


class PageSessions(QWidget):
    def __init__(self, user=None):
        super().__init__()

        self.user = user
        self.is_admin = user is None or user[4] == 'admin'
        self.selected_session_id = None
        self.selected_session_data = None
        self.sessions = []
        self.cours = []

        self.root_layout = QHBoxLayout(self)
        self.root_layout.setContentsMargins(0, 0, 0, 0)
        self.root_layout.setSpacing(0)

        self.left_widget = QWidget()
        self.main_layout = QVBoxLayout(self.left_widget)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(16)

        # Tableau
        self.table = QTableWidget()
        nb_cols = 5 if self.is_admin else 4
        self.table.setColumnCount(nb_cols)

        headers = ["Cours", "Date", "Début", "Fin"]
        if self.is_admin:
            headers.insert(1, "Professeur")
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

        self.table.setColumnWidth(0, 230)
        if self.is_admin:
            self.table.setColumnWidth(1, 180)
            self.table.setColumnWidth(2, 110)
            self.table.setColumnWidth(3, 90)
        else:
            self.table.setColumnWidth(1, 110)
            self.table.setColumnWidth(2, 90)

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

        self.panneau = PanneauSession(self)
        self.panneau.hide()

        self.root_layout.addWidget(self.left_widget)
        self.root_layout.addWidget(self.panneau)

        self.charger_sessions()

    def ajouter(self):
        self.table.clearSelection()
        self.panneau.ouvrir_creation(self._get_cours())

    def fermer_panneau(self):
        self.panneau.hide()

    def _get_cours(self):
        if not self.cours:
            if self.is_admin:
                self.cours = get_cours_enrichis()
            else:
                self.cours = get_cours_enrichis_by_prof(self.user[0])
        return self.cours

    def charger_sessions(self):
        from services.session_service import get_sessions_enrichies, get_sessions_enrichies_by_prof

        if self.is_admin:
            self.sessions = get_sessions_enrichies()
        else:
            self.sessions = get_sessions_enrichies_by_prof(self.user[0])

        self.table.setRowCount(0)
        for row_index, s in enumerate(self.sessions):
            # s : id, cours_id, prof_id, date_session, heure_debut, heure_fin,
            #     cours_intitule, prof_nom, prof_prenom
            self.table.insertRow(row_index)
            col = 0
            self.table.setItem(row_index, col, QTableWidgetItem(s[6])); col += 1
            if self.is_admin:
                self.table.setItem(row_index, col, QTableWidgetItem(f"{s[8]} {s[7]}")); col += 1
            self.table.setItem(row_index, col, QTableWidgetItem(str(s[3]))); col += 1
            self.table.setItem(row_index, col, QTableWidgetItem(str(s[4])[:5])); col += 1
            self.table.setItem(row_index, col, QTableWidgetItem(str(s[5])[:5]))

        self.table.resizeRowsToContents()
        self.table.clearSelection()
        self.selected_session_id = None
        self.selected_session_data = None
        self._update_buttons()

    def on_selection_changed(self):
        row = self.table.currentRow()
        if row == -1 or row >= len(self.sessions):
            self.selected_session_id = None
            self.selected_session_data = None
        else:
            self.selected_session_id = self.sessions[row][0]
            self.selected_session_data = self.sessions[row]
        self._update_buttons()

    def _update_buttons(self):
        enabled = self.selected_session_id is not None
        self.btn_modifier.setEnabled(enabled)
        self.btn_supprimer.setEnabled(enabled)

    def modifier_selection(self):
        if self.selected_session_data is None:
            return
        self.panneau.ouvrir_modification(self.selected_session_data, self._get_cours())

    def supprimer_selection(self):
        if self.selected_session_id is None:
            return
        s = self.selected_session_data
        confirm = QMessageBox.question(
            self, "Confirmer la suppression",
            f"Supprimer la session du {s[3]} ({str(s[4])[:5]}–{str(s[5])[:5]}) pour « {s[6]} » ?",
            QMessageBox.Yes | QMessageBox.No
        )
        if confirm == QMessageBox.Yes:
            delete_session(self.selected_session_id)
            self.fermer_panneau()
            self.charger_sessions()
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QHeaderView, QLabel, QButtonGroup
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor

from services.reservation_service import (
    get_reservations_enrichies,
    get_reservations_enrichies_by_prof,
    confirmer_reservation,
    annuler_reservation,
)

STATUT_COULEURS = {
    'en attente': '#e67e22',
    'confirmee':  '#27ae60',
    'annulee':    '#c0392b',
}

STATUT_LABELS = {
    'en attente': 'En attente',
    'confirmee':  'Confirmée',
    'annulee':    'Annulée',
}


class PageReservations(QWidget):
    def __init__(self, user=None):
        super().__init__()

        self.user = user
        self.selected_reservation_id = None
        self.selected_statut = None
        self.filter_statut = None  # None = tout afficher
        self.toutes_reservations = []

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(16)

        # --- Barre de filtres ---
        self.filter_layout = QHBoxLayout()
        self.filter_layout.setSpacing(8)
        self.filter_layout.setContentsMargins(0, 0, 0, 0)

        self.filter_group = QButtonGroup(self)
        self.filter_group.setExclusive(True)

        self.btn_f_tous = QPushButton("Toutes")
        self.btn_f_tous.setObjectName("btnFiltreDefaut")

        self.btn_f_attente = QPushButton("En attente")
        self.btn_f_attente.setObjectName("btnFiltreAttente")

        self.btn_f_confirmees = QPushButton("Confirmées")
        self.btn_f_confirmees.setObjectName("btnFiltreConfirmees")

        self.btn_f_annulees = QPushButton("Annulées")
        self.btn_f_annulees.setObjectName("btnFiltreAnnulees")

        filtres = [
            (self.btn_f_tous,       None),
            (self.btn_f_attente,    'en attente'),
            (self.btn_f_confirmees, 'confirmee'),
            (self.btn_f_annulees,   'annulee'),
        ]

        for btn, statut in filtres:
            btn.setCheckable(True)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setProperty("statut_filtre", statut)
            self.filter_group.addButton(btn)
            self.filter_layout.addWidget(btn)

        self.btn_f_tous.setChecked(True)
        self.filter_group.buttonClicked.connect(self.on_filtre_changed)

        self.filter_layout.addStretch()
        self.main_layout.addLayout(self.filter_layout)

        # --- Tableau ---
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "Élève", "Cours", "Date session", "Horaire", "Date réservation", "Statut", "ID"
        ])

        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.setAlternatingRowColors(True)
        self.table.setShowGrid(False)
        self.table.horizontalHeader().setStretchLastSection(False)
        self.table.verticalHeader().setVisible(False)
        self.table.verticalHeader().setDefaultSectionSize(45)

        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        self.table.setColumnWidth(0, 150)  # Élève
        self.table.setColumnWidth(1, 200)  # Cours
        self.table.setColumnWidth(2, 120)  # Date session
        self.table.setColumnWidth(3, 100)  # Horaire
        self.table.setColumnWidth(4, 125)  # Date réservation
        self.table.setColumnWidth(5, 110)  # Statut
        self.table.setColumnHidden(6, True)  # ID caché

        self.table.itemSelectionChanged.connect(self.on_selection_changed)
        self.main_layout.addWidget(self.table)

        # --- Boutons ---
        self.bottom_layout = QHBoxLayout()
        self.bottom_layout.setContentsMargins(0, 8, 0, 0)

        self.btn_confirmer = QPushButton("Confirmer")
        self.btn_confirmer.setObjectName("btnConfirmer")
        self.btn_confirmer.setCursor(Qt.PointingHandCursor)
        self.btn_confirmer.setEnabled(False)
        self.btn_confirmer.clicked.connect(self.confirmer_selection)

        self.btn_annuler = QPushButton("Annuler")
        self.btn_annuler.setObjectName("btnAnnulerResa")
        self.btn_annuler.setCursor(Qt.PointingHandCursor)
        self.btn_annuler.setEnabled(False)
        self.btn_annuler.clicked.connect(self.annuler_selection)

        self.bottom_layout.addStretch()
        self.bottom_layout.addWidget(self.btn_confirmer)
        self.bottom_layout.addSpacing(40)
        self.bottom_layout.addWidget(self.btn_annuler)
        self.bottom_layout.addStretch()

        self.main_layout.addLayout(self.bottom_layout)

        self.charger_reservations()

    def charger_reservations(self):
        if self.user and self.user[4] == 'professeur':
            self.toutes_reservations = get_reservations_enrichies_by_prof(self.user[0])
        else:
            self.toutes_reservations = get_reservations_enrichies()

        self.appliquer_filtre()

    def on_filtre_changed(self, btn):
        self.filter_statut = btn.property("statut_filtre")
        self.appliquer_filtre()

    def appliquer_filtre(self):
        if self.filter_statut is None:
            self.reservations = self.toutes_reservations
        else:
            self.reservations = [r for r in self.toutes_reservations if r[8] == self.filter_statut]

        self.table.setRowCount(0)

        for row_index, resa in enumerate(self.reservations):
            # resa : id, nom, prenom, intitule, date_session, heure_debut, heure_fin, date_reservation, statut
            rid, nom, prenom, intitule, date_session, heure_debut, heure_fin, date_resa, statut = resa

            self.table.insertRow(row_index)

            eleve_item = QTableWidgetItem(f"{prenom} {nom}")
            cours_item = QTableWidgetItem(intitule)
            date_session_item = QTableWidgetItem(str(date_session))
            horaire_item = QTableWidgetItem(f"{str(heure_debut)[:5]} – {str(heure_fin)[:5]}")
            date_resa_item = QTableWidgetItem(str(date_resa))

            statut_label = STATUT_LABELS.get(statut, statut)
            statut_item = QTableWidgetItem(statut_label)
            statut_item.setTextAlignment(Qt.AlignCenter)
            couleur = STATUT_COULEURS.get(statut, '#ffffff')
            statut_item.setForeground(QColor(couleur))

            id_item = QTableWidgetItem(str(rid))

            self.table.setItem(row_index, 0, eleve_item)
            self.table.setItem(row_index, 1, cours_item)
            self.table.setItem(row_index, 2, date_session_item)
            self.table.setItem(row_index, 3, horaire_item)
            self.table.setItem(row_index, 4, date_resa_item)
            self.table.setItem(row_index, 5, statut_item)
            self.table.setItem(row_index, 6, id_item)

        self.table.resizeRowsToContents()
        self.table.clearSelection()
        self.selected_reservation_id = None
        self.selected_statut = None
        self._update_buttons()

    def on_selection_changed(self):
        row = self.table.currentRow()
        if row == -1 or row >= len(self.reservations):
            self.selected_reservation_id = None
            self.selected_statut = None
        else:
            self.selected_reservation_id = self.reservations[row][0]
            self.selected_statut = self.reservations[row][8]
        self._update_buttons()

    def _update_buttons(self):
        if self.selected_statut == 'en attente':
            self.btn_confirmer.setEnabled(True)
            self.btn_annuler.setEnabled(True)
        elif self.selected_statut == 'confirmee':
            self.btn_confirmer.setEnabled(False)
            self.btn_annuler.setEnabled(True)
        elif self.selected_statut == 'annulee':
            self.btn_confirmer.setEnabled(True)
            self.btn_annuler.setEnabled(False)
        else:
            self.btn_confirmer.setEnabled(False)
            self.btn_annuler.setEnabled(False)

    def confirmer_selection(self):
        if self.selected_reservation_id is None:
            return
        confirmer_reservation(self.selected_reservation_id)
        self.charger_reservations()

    def annuler_selection(self):
        if self.selected_reservation_id is None:
            return
        annuler_reservation(self.selected_reservation_id)
        self.charger_reservations()
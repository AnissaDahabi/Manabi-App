from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame
from PySide6.QtCore import Qt

from services.dashboard_service import get_stats_admin, get_stats_professeur

class StatCard(QFrame):
    def __init__(self, titre, valeur, status=None):
        super().__init__()
        self.setObjectName("statCard")
        if status:
            self.setProperty("status", status)
        self.setMinimumHeight(90)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 14, 16, 14)
        layout.setSpacing(6)

        lbl_valeur = QLabel(str(valeur))
        lbl_valeur.setObjectName("statValeur")
        lbl_valeur.setAlignment(Qt.AlignCenter)

        lbl_titre = QLabel(titre)
        lbl_titre.setObjectName("statTitre")
        lbl_titre.setAlignment(Qt.AlignCenter)

        layout.addWidget(lbl_valeur)
        layout.addWidget(lbl_titre)

def make_section(titre):
    lbl = QLabel(titre)
    lbl.setObjectName("sectionTitre")
    return lbl

def make_row(cards):
    row = QHBoxLayout()
    row.setSpacing(16)
    for card in cards:
        row.addWidget(card)
    return row

class PageDashboard(QWidget):
    def __init__(self, user):
        super().__init__()

        self.user = user
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(16)
        layout.setAlignment(Qt.AlignTop)

        role = user[4]

        if role == 'admin':
            stats = get_stats_admin()

            layout.addWidget(make_section("Vue d'ensemble"))
            layout.addLayout(make_row([
                StatCard("Élèves", stats['eleves']),
                StatCard("Professeurs", stats['professeurs']),
                StatCard("Cours", stats['cours']),
                StatCard("Sessions", stats['sessions']),
            ]))

            layout.addWidget(make_section("État des réservations"))
            layout.addLayout(make_row([
                StatCard("En attente", stats['attente'], "attente"),
                StatCard("Confirmées", stats['confirmees'], "confirmee"),
                StatCard("Annulées", stats['annulees'], "annulee"),
            ]))

        else:
            prof_id = user[0]
            stats = get_stats_professeur(prof_id)

            layout.addWidget(make_section("Mes cours et sessions"))
            layout.addLayout(make_row([
                StatCard("Mes cours", stats['cours']),
                StatCard("Mes sessions", stats['sessions']),
            ]))

            layout.addWidget(make_section("Mes réservations"))
            layout.addLayout(make_row([
                StatCard("En attente", stats['attente'], "attente"),
                StatCard("Confirmées", stats['confirmees'], "confirmee"),
                StatCard("Annulées", stats['annulees'], "annulee"),
            ]))

        layout.addStretch()
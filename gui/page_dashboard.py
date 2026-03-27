from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame
from PySide6.QtCore import Qt


class StatCard(QFrame):
    def __init__(self, titre, valeur, status_class=""):
        super().__init__()
        self.setObjectName("statCard")
        if status_class:
            self.setProperty("status", status_class)

        layout = QVBoxLayout(self)

        lbl_titre = QLabel(titre.upper())
        lbl_titre.setObjectName("statTitre")

        lbl_valeur = QLabel(str(valeur))
        lbl_valeur.setObjectName("statValeur")

        layout.addWidget(lbl_titre)
        layout.addWidget(lbl_valeur)


class PageDashboard(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(30)

        layout.addWidget(QLabel("Vue d'ensemble", objectName="sectionTitre"))

        gen_layout = QHBoxLayout()
        gen_layout.addWidget(StatCard("Élèves", 124))
        gen_layout.addWidget(StatCard("Professeurs", 12))
        gen_layout.addWidget(StatCard("Cours", 45))
        layout.addLayout(gen_layout)

        layout.addWidget(QLabel("État des réservations", objectName="sectionTitre"))

        res_layout = QHBoxLayout()
        res_layout.addWidget(StatCard("En attente", 8, "attente"))
        res_layout.addWidget(StatCard("Confirmées", 32, "confirmee"))
        res_layout.addWidget(StatCard("Annulées", 3, "annulee"))
        layout.addLayout(res_layout)

        layout.addStretch()
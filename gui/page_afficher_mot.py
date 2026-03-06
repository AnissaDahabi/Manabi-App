from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame, QSizePolicy
from PySide6.QtCore import Qt


class PageAfficherMot(QWidget):
    def __init__(self, curseur, id_mot, retour_callback):
        super().__init__()
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.curseur = curseur
        self.id_mot = id_mot

        main_layout = QHBoxLayout(self)

        # --- Sidebar ---
        sidebar_widget = QWidget()
        sidebar_widget.setObjectName("sidebar_widget")
        sidebar_widget.setFixedWidth(150)
        sidebar = QVBoxLayout(sidebar_widget)
        sidebar.addWidget(QLabel("Parcourir"))
        for niveau in ["JLPT N5", "JLPT N4", "JLPT N3", "JLPT N2", "JLPT N1"]:
            btn = QPushButton(niveau)
            btn.setFlat(True)
            sidebar.addWidget(btn)
        sidebar.addStretch()
        main_layout.addWidget(sidebar_widget)

        content_area = QVBoxLayout()

        # Header
        header_layout = QHBoxLayout()
        self.btn_retour = QPushButton("Retour")
        self.btn_retour.setObjectName("btn_retour")
        self.btn_retour.setFixedSize(100, 40)
        self.btn_retour.setCursor(Qt.PointingHandCursor)
        self.btn_retour.clicked.connect(retour_callback)
        header_layout.addWidget(self.btn_retour)
        header_layout.addStretch()
        content_area.addLayout(header_layout)

        # Card container
        card_container = QWidget()
        card_container.setObjectName("card_container")
        card_container_layout = QVBoxLayout(card_container)

        self.card = QFrame()
        self.card.setObjectName("card_mot")
        card_layout = QVBoxLayout(self.card)
        card_layout.setContentsMargins(0, 0, 0, 0)
        card_layout.setSpacing(15)

        self.label_kanji = QLabel()
        self.label_kanji.setObjectName("kanji_label")

        self.label_lecture_trad = QLabel()
        self.label_lecture_trad.setObjectName("lecture_trad")

        self.label_exemple = QLabel()
        self.label_exemple.setObjectName("exemple_label")
        self.label_exemple.setWordWrap(False)
        self.label_exemple.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        self.label_trad_exemple = QLabel()
        self.label_trad_exemple.setObjectName("trad_exemple_label")
        self.label_trad_exemple.setWordWrap(False)
        self.label_trad_exemple.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        self.label_niveau = QLabel()
        self.label_niveau.setObjectName("niveau_label")

        card_layout.addWidget(self.label_kanji, alignment=Qt.AlignCenter)
        card_layout.addWidget(self.label_lecture_trad, alignment=Qt.AlignCenter)
        card_layout.addWidget(self.label_exemple, alignment=Qt.AlignCenter)
        card_layout.addWidget(self.label_trad_exemple, alignment=Qt.AlignCenter)
        card_layout.addWidget(self.label_niveau, alignment=Qt.AlignCenter)

        card_container_layout.addWidget(self.card)
        content_area.addWidget(card_container)

        content_area.addStretch()

        actions_layout = QHBoxLayout()
        actions_layout.setAlignment(Qt.AlignCenter)
        actions_layout.setSpacing(20)

        self.btn_modifier = QPushButton("Modifier")
        self.btn_supprimer = QPushButton("Supprimer")
        self.btn_supprimer.setObjectName("btn_supprimer")

        actions_layout.addWidget(self.btn_modifier)
        actions_layout.addWidget(self.btn_supprimer)

        actions_layout.setContentsMargins(0, 0, 0, 20)

        content_area.addLayout(actions_layout)

        main_layout.addLayout(content_area)

        self.charger_mot()

    def charger_mot(self):
        self.curseur.execute(
            "SELECT kanji, lecture, traduction, exemple, traduction_exemple, niveau FROM mots WHERE id=?",
            (self.id_mot,)
        )
        mot = self.curseur.fetchone()
        if mot:
            self.label_kanji.setText(mot[0])
            self.label_lecture_trad.setText(f"{mot[1]}  -  {mot[2]}")
            self.label_exemple.setText(mot[3])
            self.label_trad_exemple.setText(mot[4])
            self.label_niveau.setText(f"Niveau : {mot[5]}")
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QHBoxLayout, QHeaderView
)
from PySide6.QtCore import Qt

from services.user_service import get_all_users, delete_user

BTN_STYLE = """
    QPushButton {
        background-color: #c0392b;
        color: #FFF;
        font-family: 'DM Sans', sans-serif;
        font-size: 14px;
        font-weight: bold;
        border-radius: 20px;
        padding: 5px 15px;
        min-width: 100px;
        min-height: 30px;
        border: none;
    }
    QPushButton:hover {
        background-color: #922b21;
    }
"""

class PageUtilisateurs(QWidget):
    def __init__(self):
        super().__init__()

        self.selected_user_id = None

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)

        self.table = QTableWidget()
        self.layout.addWidget(self.table)

        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Nom", "Prénom", "Email", "Rôle"])

        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)

        self.table.setAlternatingRowColors(True)
        self.table.setShowGrid(False)

        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.verticalHeader().setVisible(False)
        self.table.setMinimumHeight(0)
        self.table.setSizeAdjustPolicy(QTableWidget.AdjustToContents)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)

        self.table.setColumnWidth(0, 180)
        self.table.setColumnWidth(1, 180)
        self.table.setColumnWidth(2, 300)
        self.table.setColumnWidth(3, 120)

        self.table.verticalHeader().setDefaultSectionSize(45)
        self.table.itemSelectionChanged.connect(self.on_selection_changed)

        self.charger_utilisateurs()

        self.bottom_layout = QHBoxLayout()
        self.bottom_layout.setContentsMargins(0, 16, 0, 0)

        self.btn_edit = QPushButton("Modifier")
        self.btn_edit.setStyleSheet(BTN_STYLE)
        self.btn_edit.setCursor(Qt.PointingHandCursor)
        self.btn_edit.clicked.connect(self.modifier_selection)

        self.btn_delete = QPushButton("Supprimer")
        self.btn_delete.setStyleSheet(BTN_STYLE)
        self.btn_delete.setCursor(Qt.PointingHandCursor)
        self.btn_delete.clicked.connect(self.supprimer_selection)

        self.bottom_layout.addStretch()
        self.bottom_layout.addWidget(self.btn_edit)
        self.bottom_layout.addSpacing(40)
        self.bottom_layout.addWidget(self.btn_delete)
        self.bottom_layout.addStretch()

        self.layout.addLayout(self.bottom_layout)

    def charger_utilisateurs(self):
        users = get_all_users()

        self.table.setRowCount(0)

        for row_index, user in enumerate(users):
            self.table.insertRow(row_index)

            self.table.setItem(row_index, 0, QTableWidgetItem(user[1]))
            self.table.setItem(row_index, 1, QTableWidgetItem(user[2]))
            self.table.setItem(row_index, 2, QTableWidgetItem(user[3]))
            self.table.setItem(row_index, 3, QTableWidgetItem(user[5]))

        self.table.resizeRowsToContents()
        self.table.clearSelection()
        self.selected_user_id = None

    def on_selection_changed(self):
        row = self.table.currentRow()
        users = get_all_users()

        if row == -1 or row >= len(users):
            self.selected_user_id = None
        else:
            self.selected_user_id = users[row][0]

    def supprimer_selection(self):
        if self.selected_user_id is None:
            return
        delete_user(self.selected_user_id)
        self.charger_utilisateurs()

    def modifier_selection(self):
        if self.selected_user_id is None:
            return
        print("Modifier user :", self.selected_user_id)
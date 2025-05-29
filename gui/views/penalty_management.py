from collections.abc import Sequence

from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtWidgets import (
    QAbstractItemView,
    QComboBox,
    QFormLayout,
    QHBoxLayout,
    QHeaderView,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QTableView,
    QWidget,
)

from data.entities import Client, Fine, PenaltyAccounting, Rental
from gui.views.models import PenaltyAccountingTableModel


class PenaltyAccountingView(QWidget):
    accrue_request = Signal(int, int, list)

    def __init__(self, readonly: bool = False):
        super().__init__()
        self._readonly = readonly
        self._build_ui()

    def _build_ui(self):
        root = QHBoxLayout(self)

        form = QFormLayout()
        self.client_cb = QComboBox()
        self.rental_cb = QComboBox()
        self.fine_list = QListWidget()
        self.fine_list.setSelectionMode(QAbstractItemView.MultiSelection)

        form.addRow("Клиент:", self.client_cb)
        form.addRow("Аренда:", self.rental_cb)
        form.addRow("Штрафы:", self.fine_list)

        self.accrue_btn = QPushButton("Начислить штраф")
        self.accrue_btn.clicked.connect(self._on_accrue)
        form.addRow("", self.accrue_btn)
        root.addLayout(form, stretch=0)

        self._model = PenaltyAccountingTableModel([])
        self.table = QTableView()
        self.table.setModel(self._model)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        root.addWidget(self.table, stretch=1)

        self.client_cb.currentIndexChanged.connect(self._on_client_changed)

    def fill_clients(self, clients: Sequence[Client]):
        self.client_cb.clear()
        for c in clients:
            self.client_cb.addItem(c.full_name, c.id_client)

    def fill_rentals(self, rentals: Sequence[Rental]):
        self.rental_cb.clear()
        for r in rentals:
            label = f"#{r.id_rental} от {r.rental_date:%d.%m.%Y} ({r.status})"
            self.rental_cb.addItem(label, r.id_rental)

    def fill_fines(self, fines: Sequence[Fine]):
        self.fine_list.clear()
        for f in fines:
            item = QListWidgetItem(f"{f.reason} ({f.amount:.2f})")
            item.setData(Qt.UserRole, f.id_fine)
            self.fine_list.addItem(item)

    def show_penalties(self, rows: Sequence[PenaltyAccounting]):
        self._model.set_rows(list(rows))

    @Slot()
    def _on_client_changed(self):
        pass

    @Slot()
    def _on_accrue(self):
        id_client = self.client_cb.currentData()
        id_rental = self.rental_cb.currentData()
        fine_ids = [it.data(Qt.UserRole) for it in self.fine_list.selectedItems()]
        if id_client and id_rental and fine_ids:
            self.accrue_request.emit(id_client, id_rental, fine_ids)

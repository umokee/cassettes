from datetime import date, timedelta

from PySide6.QtCore import Signal, Slot
from PySide6.QtWidgets import (
    QAbstractItemView,
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSpinBox,
    QTableView,
    QVBoxLayout,
    QWidget,
)

from gui.views.models import RentalTableModel


class RentalManagementView(QWidget):
    opn_request = Signal(int, int, int, int)
    cls_request = Signal(int, str)

    def __init__(self, readonly: bool = False):
        super().__init__()
        self._readonly = readonly
        self._build_ui()

    @property
    def is_readonly(self) -> bool:
        return self._readonly

    def _build_ui(self):
        root = QHBoxLayout(self)

        form = QFormLayout()
        self.client_input = QComboBox()
        self.cassette_input = QComboBox()
        self.tariff_input = QComboBox()
        self.duration_input = QSpinBox()
        self.duration_input.setRange(1, 30)
        self.return_label = QLabel()

        form.addRow("Клиент:", self.client_input)
        form.addRow("Кассета:", self.cassette_input)
        form.addRow("Тариф:", self.tariff_input)
        form.addRow("Дней:", self.duration_input)
        form.addRow("Ожидаемый возврат:", self.return_label)

        self.open_btn = QPushButton("Оформить аренду")
        self.open_btn.clicked.connect(self._on_open_click)

        left = QVBoxLayout()
        left.addLayout(form)
        left.addWidget(self.open_btn)
        left.addStretch()

        self.duration_input.valueChanged.connect(self._update_expected_return)
        self._update_expected_return(self.duration_input.value())

        self._model = RentalTableModel([])
        self.table = QTableView()
        self.table.setModel(self._model)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.doubleClicked.connect(self._on_double_click)

        right = QVBoxLayout()
        right.addWidget(self.table)

        root.addLayout(left, 2)
        root.addLayout(right, 5)

        if self._readonly:
            for w in (
                self.client_input,
                self.cassette_input,
                self.tariff_input,
                self.duration_input,
                self.open_btn,
            ):
                w.setEnabled(False)
            self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
            self.table.setSelectionMode(QAbstractItemView.NoSelection)
            self.table.doubleClicked.disconnect()

    def set_clients(self, rows):
        self.client_input.clear()
        for c in rows:
            self.client_input.addItem(c.full_name, c.id_client)

    def set_cassettes(self, rows):
        self.cassette_input.clear()
        for c in rows:
            self.cassette_input.addItem(f"{c.id_cassette}: {c.title}", c.id_cassette)

    def set_tariffs(self, rows):
        self.tariff_input.clear()
        for t in rows:
            self.tariff_input.addItem(f"{t.name}: {t.coefficient}", t.id_tariff)

    def show_rentals(self, rows, cass_names, client_names):
        self._model.set_lookups(cass_names, client_names)
        self._model.set_rows(rows)

    @Slot()
    def _on_open_click(self):
        self.opn_request.emit(
            self.client_input.currentData(),
            self.cassette_input.currentData(),
            self.tariff_input.currentData(),
            self.duration_input.value(),
        )

    @Slot()
    def _on_double_click(self, idx):
        rid = self._model.rental_at(idx.row()).id_rental
        dlg = _ReturnDialog(self)
        if dlg.exec():
            self.cls_request.emit(rid, dlg.result_condition())

    def _update_expected_return(self, days: int):
        self.return_label.setText((date.today() + timedelta(days=days)).strftime("%d.%m.%Y"))


class _ReturnDialog(QDialog):
    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        self.cond_input = QComboBox()
        self.cond_input.addItems(["Хорошее", "Удовлетворительное", "Плохое"])
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        lay = QVBoxLayout(self)
        lay.addWidget(self.cond_input)
        lay.addWidget(buttons)

    def result_condition(self) -> str:
        return self.cond_input.currentText()

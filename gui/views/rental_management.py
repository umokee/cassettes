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


class _ReturnDialog(QDialog):
    """Небольшой диалог для выбора состояния кассеты при возврате."""

    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        self.setWindowTitle("Состояние кассеты после возврата")
        self.cond_cb = QComboBox()
        self.cond_cb.addItems(["Хорошее", "Удовлетворительное", "Плохое"])
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        lay = QVBoxLayout(self)
        lay.addWidget(self.cond_cb)
        lay.addWidget(buttons)

    def result_condition(self) -> str:
        return self.cond_cb.currentText()


class RentalManagementView(QWidget):
    #             client      cassette    tariff      days
    open_request = Signal(int, int, int, int)
    #             id_rental   condition_after
    close_request = Signal(int, str)

    def __init__(self, readonly: bool = False):
        super().__init__()
        self._readonly = readonly
        self._build_ui()

    # ------------------------------------------------------------------ UI
    def _build_ui(self):
        root = QHBoxLayout(self)

        # ---------- левая часть : оформление ----------
        form = QFormLayout()
        self.client_cb = QComboBox()
        self.cassette_cb = QComboBox()
        self.tariff_cb = QComboBox()
        self.duration_sb = QSpinBox()
        self.duration_sb.setRange(1, 30)
        self.exp_return_lbl = QLabel()

        form.addRow("Клиент:", self.client_cb)
        form.addRow("Кассета:", self.cassette_cb)
        form.addRow("Тариф:", self.tariff_cb)
        form.addRow("Дней:", self.duration_sb)
        form.addRow("Ожидаемый возврат:", self.exp_return_lbl)

        self.open_btn = QPushButton("Оформить аренду")
        self.open_btn.clicked.connect(self._on_open_click)

        left = QVBoxLayout()
        left.addLayout(form)
        left.addWidget(self.open_btn)
        left.addStretch()

        # обновляем дату при смене дней
        self.duration_sb.valueChanged.connect(self._update_expected_return)
        self._update_expected_return(self.duration_sb.value())

        # ---------- правая часть : текущие аренды ----------
        self._model = RentalTableModel([])
        self.table = QTableView()
        self.table.setModel(self._model)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.doubleClicked.connect(self._on_double_click)

        right = QVBoxLayout()
        right.addWidget(QLabel("Активные аренды (двойной клик — возврат)"))
        right.addWidget(self.table)

        root.addLayout(left, 2)
        root.addLayout(right, 5)

        if self._readonly:
            for w in (
                self.client_cb,
                self.cassette_cb,
                self.tariff_cb,
                self.duration_sb,
                self.open_btn,
            ):
                w.setEnabled(False)
            self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
            self.table.setSelectionMode(QAbstractItemView.NoSelection)
            self.table.doubleClicked.disconnect()

    # ---------------------------------------------------------------- public
    def fill_clients(self, rows):
        self.client_cb.clear()
        for c in rows:
            self.client_cb.addItem(c.full_name, c.id_client)

    def fill_cassettes(self, rows):
        self.cassette_cb.clear()
        for c in rows:
            self.cassette_cb.addItem(f"{c.id_cassette}: {c.title}", c.id_cassette)

    def fill_tariffs(self, rows):
        self.tariff_cb.clear()
        for t in rows:
            self.tariff_cb.addItem(t.name, t.id_tariff)

    def show_rentals(self, rows):
        self._model.set_rows(rows)

    # ---------------------------------------------------------------- slots
    @Slot()
    def _on_open_click(self):
        self.open_request.emit(
            self.client_cb.currentData(),
            self.cassette_cb.currentData(),
            self.tariff_cb.currentData(),
            self.duration_sb.value(),
        )

    @Slot()
    def _on_double_click(self, idx):
        rid = self._model.rental_at(idx.row()).id_rental
        dlg = _ReturnDialog(self)
        if dlg.exec():
            self.close_request.emit(rid, dlg.result_condition())

    # ---------------------------------------------------------------- helpers
    def _update_expected_return(self, days: int):
        self.exp_return_lbl.setText((date.today() + timedelta(days=days)).strftime("%d.%m.%Y"))

    # read-only флаг наружу (используют презентеры / policy)
    @property
    def is_readonly(self) -> bool:
        return self._readonly

from __future__ import annotations

from collections.abc import Sequence
from typing import Any

from PySide6.QtCore import QAbstractTableModel, QModelIndex, Qt

from data.entities import PenaltyAccounting


class PenaltyAccountingTableModel(QAbstractTableModel):
    _COLUMNS = ("Дата", "Аренда №", "Штраф", "Сумма")

    def __init__(self, rows: Sequence[PenaltyAccounting], fine_names: dict[int, str] | None = None):
        super().__init__()
        self._rows: list[PenaltyAccounting] = list(rows)
        self._fine_names = fine_names or {}

    def rowCount(self, parent: QModelIndex | None = None) -> int:
        return len(self._rows)

    def columnCount(self, parent: QModelIndex | None = None) -> int:
        return len(self._COLUMNS)

    def set_lookups(self, fine_names: dict[int, str]):
        self.beginResetModel()
        self._fine_names = fine_names
        self.endResetModel()

    def data(self, index: QModelIndex, role: int = Qt.DisplayRole) -> Any:
        if not index.isValid() or role != Qt.DisplayRole:
            return None
        p = self._rows[index.row()]
        col = index.column()
        if col == 0:
            return p.accrual_date.strftime("%d.%m.%Y")
        if col == 1:
            return p.id_rental
        if col == 2:
            return p.fine_reason or self._fine_names.get(p.id_fine, p.id_fine)
        if col == 3:
            return f"{p.accrual_amount:.2f}"
        return None

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = Qt.DisplayRole):
        if role != Qt.DisplayRole or orientation != Qt.Horizontal:
            return None
        if 0 <= section < len(self._COLUMNS):
            return self._COLUMNS[section]
        return None

    def set_rows(self, rows: list[PenaltyAccounting]):
        self.beginResetModel()
        self._rows = rows
        self.endResetModel()

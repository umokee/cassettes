from PySide6.QtCore import QAbstractTableModel, Qt

from data.entities import Rental


class RentalTableModel(QAbstractTableModel):
    _hdr = ["ID", "Кассета", "Клиент", "Дата", "Возврат", "Стоимость", "Статус"]

    def __init__(self, rows: list[Rental]):
        super().__init__()
        self._rows = rows

    def rowCount(self, parent=None):
        return len(self._rows)

    def columnCount(self, parent=None):
        return len(self._hdr)

    def data(self, idx, role=Qt.DisplayRole):
        if not idx.isValid() or role != Qt.DisplayRole:
            return None
        r = self._rows[idx.row()]
        return (
            r.id_rental,
            r.id_cassette,
            r.id_client,
            r.rental_date,
            r.return_date or "—",
            f"{r.rental_cost:.2f}",
            r.status,
        )[idx.column()]

    def headerData(self, i, o, role):
        return self._hdr[i] if o == Qt.Horizontal and role == Qt.DisplayRole else None

    def set_rows(self, rows):
        self.beginResetModel()
        self._rows = rows
        self.endResetModel()

    def rental_at(self, row):
        return self._rows[row]

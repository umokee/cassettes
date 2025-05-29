from PySide6.QtCore import QAbstractTableModel, Qt

from data.entities import Rental


class RentalTableModel(QAbstractTableModel):
    _hdr = ["ID", "Кассета", "Клиент", "Дата", "Возврат", "Стоимость", "Статус"]

    def __init__(
        self,
        rows: list[Rental],
        cassette_names: dict[int, str] | None = None,
        client_names: dict[int, str] | None = None,
    ):
        super().__init__()
        self._rows = list(rows)
        self._cassette_names = cassette_names or {}
        self._client_names = client_names or {}

    def rowCount(self, parent=None):
        return len(self._rows)

    def columnCount(self, parent=None):
        return len(self._hdr)

    def set_lookups(self, cassette_names: dict[int, str], client_names: dict[int, str]):
        self.beginResetModel()
        self._cassette_names = cassette_names
        self._client_names = client_names
        self.endResetModel()

    def data(self, idx, role=Qt.DisplayRole):
        if not idx.isValid() or role != Qt.DisplayRole:
            return None
        r = self._rows[idx.row()]
        return (
            r.id_rental,
            self._cassette_names.get(r.id_cassette, r.id_cassette),
            self._client_names.get(r.id_client,  r.id_client),
            str(r.rental_date),
            str(r.return_date),
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

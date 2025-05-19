from PySide6.QtCore import QAbstractTableModel, Qt

from data.entities import Tariff


class TariffTableModel(QAbstractTableModel):
    _headers = ["ID", "Название", "Коэффициент", "Тип тарифа", "Условия предоставления"]

    def __init__(self, rows: list[Tariff] | None = None):
        super().__init__()
        self._rows: list[Tariff] = rows or []

    def rowCount(self, parent=None):
        return len(self._rows)

    def columnCount(self, parent=None):
        return len(self._headers)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() or role != Qt.DisplayRole:
            return None
        t = self._rows[index.row()]
        return (t.id_tariff, t.name, t.coefficient, t.type, str(t.provision_condition))[
            index.column()
        ]

    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._headers[section]
        return super().headerData(section, orientation, role)

    def set_rows(self, rows: list[Tariff]):
        self.beginResetModel()
        self._rows = rows
        self.endResetModel()

    def tariff_id_at(self, row: int) -> int:
        return self._rows[row].id_tariff

    def tariff_at(self, row: int) -> Tariff:
        return self._rows[row]

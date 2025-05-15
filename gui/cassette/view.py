from typing import List

from PySide6.QtCore import QSortFilterProxyModel, Qt, Signal, Slot
from PySide6.QtWidgets import (
    QComboBox,
    QFormLayout,
    QFrame,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QTableView,
    QVBoxLayout,
    QWidget,
)

from data import Cassette, Genre
from gui import MultiSelectComboBox

from .model import CassetteModel


def hline() -> QFrame:
    line = QFrame()
    line.setFrameShape(QFrame.HLine)
    line.setFrameShadow(QFrame.Sunken)
    return line


class CassetteView(QWidget):

    add_request = Signal(str, str, str, list)
    del_request = Signal(int)
    upd_request = Signal(int, str, str, str, list)
    row_selected = Signal(int)

    def __init__(self) -> None:
        super().__init__()
        self._build_ui()

    def set_genres(self, genres: list[Genre]) -> None:
        self.genre_input.clear()
        for g in genres:
            self.genre_input.addItem(g.name, g.id_genre)

    def show_table(self, rows: List[Cassette]) -> None:
        self._model.set_rows(rows)
        self._proxy.invalidateFilter()

    def set_checked_genres(self, genres: list[Genre]) -> None:
        self.genre_input.setCheckedIds(genres)

    def _build_ui(self):
        root = QVBoxLayout()

        form = QFormLayout()
        self.title_input = QLineEdit()
        self.cond_input = QComboBox()
        self.cond_input.addItems(["Хорошо", "Плохо"])
        self.cost_input = QLineEdit()
        self.genre_input = MultiSelectComboBox()

        form.addRow("Название:", self.title_input)
        form.addRow("Состояние:", self.cond_input)
        form.addRow("Стоимость:", self.cost_input)
        form.addRow("Жанры:", self.genre_input)

        btn_box = QVBoxLayout()
        add_btn = QPushButton("Добавить кассету")
        del_btn = QPushButton("Удалить кассету")
        upd_btn = QPushButton("Изменить кассету")
        for b in (add_btn, del_btn, upd_btn):
            btn_box.addWidget(b)

        add_btn.clicked.connect(self._on_add_click)
        del_btn.clicked.connect(self._on_del_click)
        upd_btn.clicked.connect(self._on_upd_click)

        top = QHBoxLayout()
        top.addLayout(form, stretch=3)
        top.addLayout(btn_box, stretch=3)
        root.addLayout(top)
        root.addWidget(hline())

        filter = QHBoxLayout()
        self.filter_input = QLineEdit()
        self.filter_column = QComboBox()
        filter.addWidget(QLabel("Фильтр:"))
        filter.addWidget(self.filter_input, stretch=3)
        filter.addWidget(self.filter_column, stretch=1)
        root.addLayout(filter)

        self._model = CassetteModel([])
        self._proxy = QSortFilterProxyModel(self)
        self._proxy.setSourceModel(self._model)
        self._proxy.setFilterCaseSensitivity(Qt.CaseInsensitive)

        self.table = QTableView(model=self._proxy)
        self.table.setSelectionMode(QTableView.SingleSelection)
        self.table.setSelectionBehavior(QTableView.SelectRows)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.selectionModel().selectionChanged.connect(
            self._on_row_selected
        )
        root.addWidget(self.table, stretch=4)

        for i, header in enumerate(self._model._headers):
            self.filter_column.addItem(header, i)
        self.filter_input.textChanged.connect(self._apply_filter)
        self.filter_column.currentIndexChanged.connect(self._apply_filter)

        self.setLayout(root)

    @Slot()
    def _on_add_click(self) -> None:
        self.add_request.emit(
            self.title_input.text(),
            self.cond_input.currentText(),
            self.cost_input.text(),
            list(map(int, self.genre_input.currentData())),
        )
        self._clear()

    @Slot()
    def _on_del_click(self) -> None:
        selected = self.table.selectionModel().selectedRows()
        if not selected:
            return

        id_cassette = self._id_from_row(selected[0])
        self.del_request.emit(id_cassette)
        self._clear()

    @Slot()
    def _on_upd_click(self) -> None:
        selected = self.table.selectionModel().selectedRows()
        if not selected:
            return

        id_cassette = self._id_from_row(selected[0])
        self.upd_request.emit(
            id_cassette,
            self.title_input.text(),
            self.cond_input.currentText(),
            self.cost_input.text(),
            list(map(int, self.genre_input.currentData())),
        )
        self._clear()

    @Slot()
    def _apply_filter(self):
        self._proxy.setFilterFixedString(self.filter_input.text())
        self._proxy.setFilterKeyColumn(self.filter_column.currentData())

    def _on_row_selected(self):
        selected = self.table.selectionModel().selectedRows()
        if not selected:
            self._clear()
            return

        row = self._proxy.mapToSource(selected[0]).row()
        c = self._model._rows[row]
        self.title_input.setText(c.title)
        self.cond_input.setCurrentText(c.condition)
        self.cost_input.setText(str(c.rental_cost))
        self.row_selected.emit(c.id_cassette)

    def _id_from_row(self, proxy_index) -> int:
        row = self._proxy.mapToSource(proxy_index).row()
        return self._model.cassette_id_at(row)

    def _clear(self) -> None:
        self.title_input.clear()
        self.cost_input.clear()
        self.cond_input.setCurrentIndex(0)
        self.genre_input.setCurrentIndexes([])

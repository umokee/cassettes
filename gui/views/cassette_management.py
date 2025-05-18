from PySide6.QtCore import QSortFilterProxyModel, Qt, Signal, Slot
from PySide6.QtWidgets import (
    QAbstractItemView,
    QComboBox,
    QFormLayout,
    QFrame,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QPushButton,
    QTableView,
    QVBoxLayout,
    QWidget,
)

from data.entities import Cassette, Genre
from gui.views.models import CassetteTableModel
from gui.widgets import MultiSelectComboBox


class CassetteManagementView(QWidget):
    add_request = Signal(str, str, str, list)
    del_request = Signal(int)
    upd_request = Signal(int, str, str, str, list)
    sel_changed = Signal(int)
    not_readonly = Signal()

    def __init__(self, readonly: bool = False):
        super().__init__()
        self._readonly = readonly
        self._build_ui()

    @property
    def is_readonly(self) -> bool:
        return self._readonly

    def _build_ui(self):
        root = QVBoxLayout()

        filter = QHBoxLayout()
        self.filter_input = QLineEdit()
        self.filter_column = QComboBox()
        filter.addWidget(QLabel("Фильтр:"))
        filter.addWidget(self.filter_input, stretch=3)
        filter.addWidget(self.filter_column, stretch=1)

        self._model = CassetteTableModel([])
        self._proxy = QSortFilterProxyModel(self)
        self._proxy.setSourceModel(self._model)
        self._proxy.setFilterCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)

        self.table = QTableView()
        self.table.setModel(self._proxy)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        if not self._readonly:
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

            line = QFrame()
            line.setFrameShape(QFrame.Shape.HLine)
            line.setFrameShadow(QFrame.Shadow.Sunken)
            root.addWidget(line)

            self.table.selectionModel().selectionChanged.connect(self._on_sel_changed)

        root.addLayout(filter)
        root.addWidget(self.table, stretch=4)

        for i, header in enumerate(self._model._headers):
            self.filter_column.addItem(header, i)
        self.filter_input.textChanged.connect(self._apply_filter)
        self.filter_column.currentIndexChanged.connect(self._apply_filter)

        self.setLayout(root)

    @Slot()
    def _apply_filter(self):
        self._proxy.setFilterFixedString(self.filter_input.text())
        self._proxy.setFilterKeyColumn(self.filter_column.currentData())

    @Slot()
    def _on_sel_changed(self):
        cassette = self.get_selected_cassette()
        if cassette:
            self.sel_changed.emit(cassette.id_cassette)
        else:
            self._clear()

    @Slot()
    def _on_add_click(self):
        self.add_request.emit(
            self.title_input.text(),
            self.cond_input.currentText(),
            self.cost_input.text(),
            self.genre_input.currentData(),
        )
        self._clear()

    @Slot()
    def _on_del_click(self):
        id_cassette = self.get_selected_id()
        if id_cassette is not None:
            self.del_request.emit(id_cassette)
            self._clear()

    @Slot()
    def _on_upd_click(self):
        id_cassette = self.get_selected_id()
        if id_cassette is not None:
            self.upd_request.emit(
                id_cassette,
                self.title_input.text(),
                self.cond_input.currentText(),
                self.cost_input.text(),
                self.genre_input.currentData(),
            )
            self._clear()

    def _clear(self):
        self.title_input.clear()
        self.cost_input.clear()
        self.cond_input.setCurrentIndex(0)
        self.genre_input.setCurrentIndexes([])

    def set_genres(self, genres: list[Genre]):
        self.genre_input.clear()
        for g in genres:
            self.genre_input.addItem(g.name, g.id_genre)

    def show_table(self, rows: list[Cassette]):
        self._model.set_rows(rows)
        self._proxy.invalidateFilter()

    def set_form(self, c: Cassette):
        self.title_input.setText(c.title)
        self.cond_input.setCurrentText(c.condition)
        self.cost_input.setText(str(c.rental_cost))
        self.genre_input.setCheckedIds(list(c.genre_ids))

    def get_selected_id(self) -> int | None:
        selected = self.table.selectionModel().selectedRows()
        if not selected:
            return None
        row = self._proxy.mapToSource(selected[0]).row()
        return self._model.cassette_id_at(row)

    def get_selected_cassette(self) -> Cassette | None:
        selected = self.table.selectionModel().selectedRows()
        if not selected:
            return None
        row = self._proxy.mapToSource(selected[0]).row()
        return self._model.cassette_at(row)

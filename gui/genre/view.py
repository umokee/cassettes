from typing import List

from PySide6.QtCore import Qt, Signal, QSortFilterProxyModel
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout, QHBoxLayout, QFormLayout,
    QPushButton, QLineEdit, QTableView,
    QMessageBox, QHeaderView, QFrame, QLabel, QComboBox,
)
from data import Genre
from .model import GenreModel


class GenreView(QWidget):

    addRequested = Signal(str, str)
    deleteRequested = Signal(int)
    updateRequested = Signal(int, str, str)

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("SBC: Genres")
        self.resize(1000, 800)
        self._selected_id: int | None = None   
        self.build_ui()

    def show_table(self, rows: List[Genre]) -> None:
        self._model.set_rows(rows)
        self._proxy.invalidateFilter()

    def build_ui(self):
        root = QVBoxLayout()

        form_layout = QFormLayout()
        self.name_input = QLineEdit()
        self.description_input = QLineEdit()
        form_layout.addRow("Name:", self.name_input)
        form_layout.addRow("Description:", self.description_input)

        button_layout = QVBoxLayout()
        add_btn = QPushButton("Добавить жанр")
        delete_btn = QPushButton("Удалить жанр")
        update_btn = QPushButton("Изменить жанр")
        add_btn.clicked.connect(self._on_add_click)
        delete_btn.clicked.connect(self._on_delete_click)
        update_btn.clicked.connect(self._on_update_click)
        for w in (add_btn, delete_btn, update_btn):
            button_layout.addWidget(w)

        top_layout = QHBoxLayout()
        top_layout.addLayout(form_layout, stretch=3)
        top_layout.addLayout(button_layout, stretch=3)
        root.addLayout(top_layout)

        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        root.addWidget(line)

        filter_layout = QHBoxLayout()
        self.filter_input = QLineEdit()
        self.filter_column = QComboBox()
        filter_layout.addWidget(QLabel("Фильтр:"))
        filter_layout.addWidget(self.filter_input, stretch=3)
        filter_layout.addWidget(self.filter_column, stretch=1)
        root.addLayout(filter_layout)

        self._model = GenreModel([])
        self._proxy = QSortFilterProxyModel(self)
        self._proxy.setSourceModel(self._model)
        self._proxy.setFilterCaseSensitivity(Qt.CaseInsensitive)

        self.table = QTableView()
        self.table.setModel(self._proxy)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.selectionModel().selectionChanged.connect(self._on_selection_changed)
        root.addWidget(self.table, stretch=4)

        for col, header in enumerate(self._model._headers):
            self.filter_column.addItem(header, col)
        self.filter_column.currentIndexChanged.connect(self._on_filter_column)
        self.filter_input.textChanged.connect(self._on_filter_text)

        self.setLayout(root)

    
    def _on_add_click(self) -> None:
        self.addRequested.emit(self.name_input.text(), self.description_input.text())
        self._clear_inputs()

    def _on_delete_click(self) -> None:
        sel = self.table.selectionModel().selectedRows()
        if not sel:
            return
        for index in sel:
            gId = self._model.genre_id_at(index.row())
            self.deleteRequested.emit(gId)
        self._clear_inputs()

    def _on_update_click(self) -> None:
        if self._selected_id is None:
            return
        self.updateRequested.emit(self._selected_id, self.name_input.text(), self.description_input.text())
        self._clear_inputs()

    def _on_selection_changed(self, *_):
        sel = self.table.selectionModel().selectedRows()
        if not sel:
            self._selected_id = None
            return
        row  = sel[0].row()
        g = self._model._rows[row]
        self._selected_id = g.id_genre
        self.name_input.setText(g.name)
        self.description_input.setText(g.description)

    def _on_filter_text(self, text: str) -> None:
        self._proxy.setFilterFixedString(text)

    def _on_filter_column(self, idx: int) -> None:
        column = self.filter_column.itemData(idx)
        self._proxy.setFilterKeyColumn(column)
        
    def _clear_inputs(self) -> None:
        self.name_input.clear()
        self.description_input.clear()
        self._selected_id = None

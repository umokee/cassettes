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

from data.entities import ClientStatus
from gui.views.models import ClientStatusTableModel


class ClientStatusManagementView(QWidget):
    add_request = Signal(str, str)
    del_request = Signal(int)
    upd_request = Signal(int, str, str)
    sel_changed = Signal(int)

    def __init__(self, readonly: bool = False):
        super().__init__()
        self._readonly = readonly
        self._build_ui()

    def _build_ui(self):
        root = QVBoxLayout()

        filter = QHBoxLayout()
        self.filter_input = QLineEdit()
        self.filter_column = QComboBox()
        filter.addWidget(QLabel("Фильтр:"))
        filter.addWidget(self.filter_input, stretch=3)
        filter.addWidget(self.filter_column, stretch=1)

        self._model = ClientStatusTableModel([])
        self._proxy = QSortFilterProxyModel(self)
        self._proxy.setSourceModel(self._model)
        self._proxy.setFilterCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)

        self.table = QTableView()
        self.table.setModel(self._proxy)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        if not self._readonly:
            form = QFormLayout()
            self.name_input = QLineEdit()
            self.desc_input = QLineEdit()

            form.addRow("Название:", self.name_input)
            form.addRow("Описание:", self.desc_input)

            btn_box = QVBoxLayout()
            add_btn = QPushButton("Добавить статус")
            del_btn = QPushButton("Удалить статус")
            upd_btn = QPushButton("Изменить статус")
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
        status = self.get_selected_status()
        if status:
            self.sel_changed.emit(status.id_client_status)
        else:
            self._clear()

    @Slot()
    def _on_add_click(self):
        self.add_request.emit(self.name_input.text(), self.desc_input.text())
        self._clear()

    @Slot()
    def _on_del_click(self):
        status_id = self.get_selected_id()
        if status_id is not None:
            self.del_request.emit(status_id)
            self._clear()

    @Slot()
    def _on_upd_click(self):
        status_id = self.get_selected_id()
        if status_id is not None:
            self.upd_request.emit(status_id, self.name_input.text(), self.desc_input.text())
            self._clear()

    def _clear(self):
        self.name_input.clear()
        self.desc_input.clear()

    def show_table(self, rows: list[ClientStatus]):
        self._model.set_rows(rows)
        self._proxy.invalidateFilter()

    def set_form(self, cs: ClientStatus):
        self.name_input.setText(cs.name)
        self.desc_input.setText(cs.description)

    def get_selected_id(self) -> int | None:
        selected = self.table.selectionModel().selectedRows()
        if not selected:
            return None
        row = self._proxy.mapToSource(selected[0]).row()
        return self._model.status_id_at(row)

    def get_selected_status(self) -> ClientStatus | None:
        selected = self.table.selectionModel().selectedRows()
        if not selected:
            return None
        row = self._proxy.mapToSource(selected[0]).row()
        return self._model.status_at(row)

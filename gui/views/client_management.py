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

from data.entities import Client, ClientStatus
from gui.views.models import ClientTableModel


class ClientManagementView(QWidget):
    add_request = Signal(str, str, str, int)
    upd_request = Signal(int, str, str, str, int)
    sel_changed = Signal(int)

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

        self._model = ClientTableModel([])
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
            self.full_name_input = QLineEdit()
            self.login_input = QLineEdit()
            self.email_input = QLineEdit()
            self.status_input = QComboBox()

            form.addRow("ФИО:", self.full_name_input)
            form.addRow("Логин:", self.login_input)
            form.addRow("Email:", self.email_input)
            form.addRow("Cтатус:", self.status_input)

            btn_box = QVBoxLayout()
            add_btn = QPushButton("Добавить клиента")
            upd_btn = QPushButton("Изменить клиента")
            for b in (add_btn, upd_btn):
                btn_box.addWidget(b)

            add_btn.clicked.connect(self._on_add_click)
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
        client = self.get_selected_client()
        if client:
            self.sel_changed.emit(client.id_client)
        else:
            self._clear()

    @Slot()
    def _on_add_click(self):
        self.add_request.emit(
            self.full_name_input.text(),
            self.login_input.text(),
            self.email_input.text(),
            self.status_input.currentData(),
        )
        self._clear()

    @Slot()
    def _on_upd_click(self):
        client_id = self.get_selected_id()
        if client_id is not None:
            self.upd_request.emit(
                client_id,
                self.full_name_input.text(),
                self.login_input.text(),
                self.email_input.text(),
                self.status_input.currentData(),
            )
            self._clear()

    def _clear(self):
        self.full_name_input.clear()
        self.login_input.clear()
        self.email_input.clear()
        self.status_input.setCurrentIndex(0)

    def show_table(self, rows: list[Client]):
        self._model.set_rows(rows)
        self._proxy.invalidateFilter()

    def set_form(self, c: Client):
        self.full_name_input.setText(c.full_name)
        self.login_input.setText(c.login)
        self.email_input.setText(c.email)
        index = self.status_input.findText(c.status)
        self.status_input.setCurrentIndex(index)

    def set_statuses(self, statuses: list[ClientStatus]):
        self.status_input.clear()
        for s in statuses:
            self.status_input.addItem(s.name, s.id_client_status)

    def get_selected_id(self) -> int | None:
        selected = self.table.selectionModel().selectedRows()
        if not selected:
            return None
        row = self._proxy.mapToSource(selected[0]).row()
        return self._model.client_id_at(row)

    def get_selected_client(self) -> Client | None:
        selected = self.table.selectionModel().selectedRows()
        if not selected:
            return None
        row = self._proxy.mapToSource(selected[0]).row()
        return self._model.client_at(row)

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDockWidget,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QMainWindow,
    QSizePolicy,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from data.entities import Employee


class MainWindow(QMainWindow):
    def __init__(self, views: dict[str, QWidget], labels: dict[str, str]):
        super().__init__()
        self.setWindowTitle("SBC")
        self.resize(1200, 800)
        self._views = views

        self._stack = QStackedWidget()
        for view in views.values():
            self._stack.addWidget(view)

        self._nav_list = QListWidget()
        for section in views:
            self._nav_list.addItem(labels.get(section, section))

        self._nav_list.setCurrentRow(0)

        self._user_label = QLabel("Пользователь")
        self._user_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        nav_content = QWidget()
        nav_layout = QVBoxLayout(nav_content)
        nav_layout.setContentsMargins(0, 0, 0, 0)
        nav_layout.setSpacing(0)
        nav_layout.addWidget(self._user_label)
        nav_layout.addWidget(self._nav_list)

        nav_panel = QDockWidget("Навигация", self)
        nav_panel.setAllowedAreas(Qt.DockWidgetArea.LeftDockWidgetArea)
        nav_panel.setWidget(nav_content)
        nav_panel.setTitleBarWidget(QWidget())
        nav_panel.setMinimumWidth(200)
        nav_panel.setMaximumWidth(200)
        nav_panel.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding))
        nav_panel.setFeatures(
            QDockWidget.DockWidgetFeature.DockWidgetClosable
            | QDockWidget.DockWidgetFeature.DockWidgetMovable
        )

        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, nav_panel)

        central = QWidget()
        lay = QHBoxLayout(central)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.addWidget(self._stack)
        self.setCentralWidget(central)

        self._nav_list.currentRowChanged.connect(self._stack.setCurrentIndex)

    def set_current_employee(self, employee: Employee):
        self._user_label.setText(f"{employee.full_name}")

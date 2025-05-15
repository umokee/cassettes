from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDockWidget,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QMainWindow,
    QSizePolicy,
    QSplitter,
    QStackedWidget,
    QWidget,
)


class MainWindow(QMainWindow):

    def __init__(self, cassette: QWidget, genre: QWidget):
        super().__init__()
        self.setWindowTitle("SBC")
        self.resize(1200, 800)

        self._nav_panel = QDockWidget("Навигация", self)
        self._nav_panel.setAllowedAreas(Qt.LeftDockWidgetArea)
        self._nav_panel.setFeatures(QDockWidget.NoDockWidgetFeatures)
        FIXED_NAV_WIDTH = 180
        self._nav_panel.setMinimumWidth(FIXED_NAV_WIDTH)
        self._nav_panel.setMaximumWidth(FIXED_NAV_WIDTH)
        self._nav_panel.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)

        splitter = self.findChild(QSplitter)
        if splitter:
            splitter.setHandleWidth(0)
            for i in range(splitter.count()):
                splitter.setCollapsible(i, False)

        self._nav_list = QListWidget()
        self._nav_list.addItems(["Главная", "Cassettes", "Genres"])
        self._nav_panel.setWidget(self._nav_list)

        self._nav_panel.setTitleBarWidget(QWidget())
        self.addDockWidget(Qt.LeftDockWidgetArea, self._nav_panel)

        self._stack = QStackedWidget()
        self._stack.addWidget(QLabel("Главная страница"))
        self._stack.addWidget(cassette)
        self._stack.addWidget(genre)

        central = QWidget()
        lay = QHBoxLayout(central)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.addWidget(self._stack)
        self.setCentralWidget(central)

        self._nav_list.currentRowChanged.connect(self._stack.setCurrentIndex)
        self._nav_list.setCurrentRow(1)

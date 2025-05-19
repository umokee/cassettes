from PySide6.QtCore import QDate, QTime
from PySide6.QtWidgets import (
    QDateEdit,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QSpinBox,
    QTimeEdit,
    QVBoxLayout,
)

from data.entities import DateRange, Genre, TariffCondition, TimeRange
from gui.widgets import MultiSelectComboBox


class ProvisionConditionDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SBC")
        self._build_ui()
        self.reset()

    def _build_ui(self):
        layout = QVBoxLayout()

        form = QFormLayout()

        self.count_input = QSpinBox()
        self.count_input.setRange(0, 99)
        form.addRow("Кол-во применений:", self.count_input)

        self.genre_input = MultiSelectComboBox()
        form.addRow("Жанры:", self.genre_input)

        self.start_date = QDateEdit()
        self.end_date = QDateEdit()
        self.start_date.setCalendarPopup(True)
        self.end_date.setCalendarPopup(True)
        self.start_date.setDisplayFormat("dd.MM.yyyy")
        self.end_date.setDisplayFormat("dd.MM.yyyy")

        date_layout = QHBoxLayout()
        date_layout.addWidget(QLabel("C:"))
        date_layout.addWidget(self.start_date)
        date_layout.addWidget(QLabel("по:"))
        date_layout.addWidget(self.end_date)

        form.addRow("Диапазон действия:", date_layout)

        self.weekdays_input = MultiSelectComboBox()
        days = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]
        self.weekdays_input.addItems(days, list(range(1, 8)))
        form.addRow("Дни недели:", self.weekdays_input)

        self.time_start = QTimeEdit()
        self.time_end = QTimeEdit()

        time_layout = QHBoxLayout()
        time_layout.addWidget(QLabel("От:"))
        time_layout.addWidget(self.time_start)
        time_layout.addWidget(QLabel("До:"))
        time_layout.addWidget(self.time_end)
        form.addRow("Интервал времени суток:", time_layout)

        layout.addLayout(form)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        layout.addWidget(buttons)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        self.setLayout(layout)

    def reset(self):
        today = QDate.currentDate()
        self.count_input.setValue(0)
        self.genre_input.setCheckedIds([])
        self.weekdays_input.setCheckedIds([])
        self.start_date.setDate(today)
        self.end_date.setDate(today)
        self.time_start.setTime(QTime(0, 0))
        self.time_end.setTime(QTime(0, 0))

    def set_genres(self, genres: list[Genre]):
        self.genre_input.clear()
        for g in genres:
            self.genre_input.addItem(g.name, g.id_genre)

    def set_data(self, cond: TariffCondition):
        if cond.count_max is not None:
            self.count_input.setValue(cond.count_max)

        if cond.genres is not None:
            self.genre_input.setCheckedIds(list(cond.genres))

        if cond.dates is not None:
            if cond.dates.start:
                self.start_date.setDate(QDate.fromString(cond.dates.start, "yyyy-MM-dd"))
            if cond.dates.end:
                self.end_date.setDate(QDate.fromString(cond.dates.end, "yyyy-MM-dd"))

        if cond.times is not None:
            if cond.times.start:
                self.time_start.setTime(QTime.fromString(cond.times.start, "HH:mm"))
            if cond.times.end:
                self.time_end.setTime(QTime.fromString(cond.times.end, "HH:mm"))

    def get_data(self) -> TariffCondition:
        count = self.count_input.value() or None
        genres = self.genre_input.currentData() or None
        weekdays = self.weekdays_input.currentData() or None
        dates = None
        if self.date_from.date().isValid() and self.date_to.date().isValid():
            dates = DateRange(
                start=self.start_date.date().toString("yyyy-MM-dd"),
                end=self.end_date.date().toString("yyyy-MM-dd"),
            )
        times = None
        if self.time_from.time().isValid() and self.time_to.time().isValid():
            times = (
                TimeRange(
                    start=self.time_start.time().toString("HH:mm"),
                    end=self.time_end.time().toString("HH:mm"),
                ),
            )

        return TariffCondition(count, genres, dates, weekdays, times)

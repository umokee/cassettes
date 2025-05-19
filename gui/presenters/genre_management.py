from PySide6.QtCore import QObject, Slot
from PySide6.QtWidgets import QMessageBox

from app.services import GenreService
from gui.views import GenreManagementView


class GenreManagementPresenter(QObject):
    def __init__(self, view: GenreManagementView, genre_service: GenreService):
        super().__init__()
        self._view = view
        self._genre = genre_service
        self._connect_signals()
        self._refresh()

    def _connect_signals(self):
        self._view.add_request.connect(self._on_add)
        self._view.del_request.connect(self._on_del)
        self._view.upd_request.connect(self._on_upd)
        self._view.sel_changed.connect(self._on_sel)

    @Slot(int)
    def _on_sel(self, id_genre):
        try:
            genre = self._genre.get(id_genre)
            if genre:
                self._view.set_form(genre)
        except Exception as e:
            self._show_err(e)

    @Slot(str, str)
    def _on_add(self, name, desc):
        try:
            self._genre.add(name, desc)
            self._refresh()
        except Exception as e:
            self._show_err(e)

    @Slot(int)
    def _on_del(self, id_genre):
        try:
            self._genre.delete(id_genre)
            self._refresh()
        except Exception as e:
            self._show_err(e)

    @Slot(int, str, str)
    def _on_upd(self, id_genre, name, desc):
        try:
            self._genre.update(id_genre, name, desc)
            self._refresh()
        except Exception as e:
            self._show_err(e)

    def _refresh(self):
        try:
            genres = self._genre.get_all()
            self._view.show_table(genres)
        except Exception as e:
            self._show_err(e)

    def _show_err(self, e: Exception):
        QMessageBox.critical(self._view, "Ошибка", str(e), QMessageBox.StandardButton.Ok)

from PySide6.QtCore import QObject, Slot
from PySide6.QtWidgets import QMessageBox

from app.services import CassetteService, GenreService
from gui.views import CassetteManagementView


class CassetteManagementPresenter(QObject):
    def __init__(
        self,
        view: CassetteManagementView,
        cassette_service: CassetteService,
        genre_service: GenreService,
    ):
        super().__init__()
        self._view = view
        self._cassette = cassette_service
        self._genre = genre_service
        self._connect_signals()
        self._init_genres()
        self._refresh()

    def _connect_signals(self):
        self._view.add_request.connect(self._on_add)
        self._view.del_request.connect(self._on_del)
        self._view.upd_request.connect(self._on_upd)
        self._view.sel_changed.connect(self._on_sel)

    def _init_genres(self):
        if not self._view.is_readonly:
            try:
                genres = self._genre.get_all()
                self._view.set_genres(genres)
            except Exception as e:
                self._show_err(e)

    @Slot(int)
    def _on_sel(self, id_cassette: int):
        try:
            cassette = self._cassette.get(id_cassette)
            if cassette:
                self._view.set_form(cassette)
        except Exception as e:
            self._show_err(e)

    @Slot(str, str, str, list)
    def _on_add(self, title, cond, cost, genres):
        try:
            self._cassette.add(title, cond, cost, genres)
            self._refresh()
        except Exception as e:
            self._show_err(e)

    @Slot(int)
    def _on_del(self, id_cassette):
        try:
            self._cassette.delete(id_cassette)
            self._refresh()
        except Exception as e:
            self._show_err(e)

    @Slot(int, str, str, str, list)
    def _on_upd(self, id_cassette, title, cond, cost, genres):
        try:
            self._cassette.update(id_cassette, title, cond, cost, genres)
            self._refresh()
        except Exception as e:
            self._show_err(e)

    def _refresh(self):
        try:
            cassettes = self._cassette.get_all()
            self._view.show_table(cassettes)
        except Exception as e:
            self._show_err(e)

    def _show_err(self, e: Exception):
        QMessageBox.critical(self._view, "Ошибка", str(e), QMessageBox.StandardButton.Ok)

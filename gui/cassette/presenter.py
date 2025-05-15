from PySide6.QtCore import QObject, Slot
from PySide6.QtWidgets import QMessageBox

from usecases import (
    AddCassette,
    DeleteCassette,
    ListCassettes,
    ListGenres,
    ListGenresForCassette,
    SetCassetteGenres,
    UpdateCassette,
)

from .view import CassetteView


class CassettePresenter(QObject):
    def __init__(
        self,
        view: CassetteView,
        list_cassettes: ListCassettes,
        add_cassette: AddCassette,
        del_cassette: DeleteCassette,
        upd_cassette: UpdateCassette,
        list_genres: ListGenres,
        list_genres_for_casette: ListGenresForCassette,
        set_genres_for_cassette: SetCassetteGenres,
    ) -> None:
        super().__init__()
        self._v = view
        self._lc = list_cassettes
        self._ac = add_cassette
        self._dc = del_cassette
        self._uc = upd_cassette
        self._lg = list_genres
        self._lgc = list_genres_for_casette
        self._sgc = set_genres_for_cassette

        self._connect_signals()
        self.init_genres()
        self._refresh()

    def init_genres(self):
        self._v.set_genres(self._lg.execute())

    def _connect_signals(self):
        self._v.add_request.connect(self._on_add)
        self._v.del_request.connect(self._on_del)
        self._v.upd_request.connect(self._on_upd)
        self._v.row_selected.connect(self._on_row_selected)

    @Slot(str, str, str, list)
    def _on_add(self, title, cond, cost, genres):
        try:
            id_cassette = self._ac.execute(title, cond, float(cost))
            self._sgc.execute(id_cassette, genres)
            self._refresh()
        except Exception as e:
            self._show_err(e)

    @Slot(int)
    def _on_del(self, id_cassette: int):
        try:
            self._sgc.execute(id_cassette, [])
            self._dc.execute(id_cassette)
            self._refresh()
        except Exception as e:
            self._show_err(e)

    @Slot(int, str, str, str, list)
    def _on_upd(self, id_cassette, title, cond, cost, genres):
        try:
            self._uc.execute(id_cassette, title, cond, float(cost))
            self._sgc.execute(id_cassette, genres)
            self._refresh()
        except Exception as exc:
            self._show_err(exc)

    @Slot(int)
    def _on_row_selected(self, id_cassette: int):
        genres = self._lgc.execute(id_cassette)
        self._v.set_checked_genres(list(genres))

    def _refresh(self) -> None:
        self._v.show_table(self._lc.execute())

    def _show_err(self, e: Exception) -> None:
        QMessageBox.critical(self._v, "Ошибка", str(e), QMessageBox.Ok)

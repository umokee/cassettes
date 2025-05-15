from PySide6.QtCore import QObject, Slot
from .view import GenreView
from usecases import (
    ListGenres, AddGenre, DeleteGenre, UpdateGenre,
)


class GenrePresenter(QObject):
    def __init__(self, view: GenreView, list_g: ListGenres, add_g: AddGenre, del_g: DeleteGenre, upd_g: UpdateGenre) -> None:
        self._v = view
        self._list, self._add, self._del, self._upd = (
            list_g, add_g, del_g, upd_g
        )
        super().__init__()
        self._connect_signals()
        self.refresh()

    def _connect_signals(self):
        self._v.addRequested.connect(self._on_add)
        self._v.deleteRequested.connect(self._on_del)
        self._v.updateRequested.connect(self._on_upd)

    @Slot(str, str)
    def _on_add(self, name: str, description: str) -> None:
        try:
            self._add.execute(name, description)
        except Exception as exc:
            print(f"Add failed: {exc}")
        self.refresh()

    @Slot(int)
    def _on_del(self, id_genre: int) -> None:
        self._del.execute(id_genre)
        self.refresh()

    @Slot(int, str, str)
    def _on_upd(self, id_genre: int, name: str, description: str) -> None:
        self._upd.execute(id_genre, name, description)
        self.refresh()

    def refresh(self) -> None:
        self._v.show_table(self._list.execute())

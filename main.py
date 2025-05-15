import sys

from PySide6.QtWidgets import QApplication

from data import CassetteData, CassetteGenreData, Database, GenreData
from gui import (
    CassettePresenter,
    CassetteView,
    GenrePresenter,
    GenreView,
    MainWindow,
)
from usecases import (
    AddCassette,
    AddGenre,
    DeleteCassette,
    DeleteGenre,
    ListCassettes,
    ListGenres,
    ListGenresForCassette,
    SetCassetteGenres,
    UpdateCassette,
    UpdateGenre,
)


def main() -> None:
    app = QApplication(sys.argv)

    db = Database()
    c_data = CassetteData(db)
    g_data = GenreData(db)
    cg_data = CassetteGenreData(db)

    _c_view = CassetteView()
    _c_presenter = CassettePresenter(
        _c_view,
        ListCassettes(c_data),
        AddCassette(c_data),
        DeleteCassette(c_data),
        UpdateCassette(c_data),
        ListGenres(g_data),
        ListGenresForCassette(cg_data),
        SetCassetteGenres(cg_data),
    )

    _g_view = GenreView()
    _g_presenter = GenrePresenter(
        _g_view,
        ListGenres(g_data),
        AddGenre(g_data),
        DeleteGenre(g_data),
        UpdateGenre(g_data),
    )

    main_window = MainWindow(_c_view, _g_view)
    main_window.show()

    exit_code = app.exec()
    db.close()
    sys.exit(exit_code)


if __name__ == "__main__":
    main()

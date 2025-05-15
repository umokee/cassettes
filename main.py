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


def main():
    app = QApplication(sys.argv)

    db = Database()
    c_data = CassetteData(db)
    g_data = GenreData(db)
    cg_data = CassetteGenreData(db)

    cassette_view = CassetteView()
    genre_view = GenreView()

    list_cass_uc = ListCassettes(c_data)
    add_cass_uc = AddCassette(c_data)
    del_cass_uc = DeleteCassette(c_data)
    update_cass_uc = UpdateCassette(c_data)
    list_genres_uc = ListGenres(g_data)
    list_for_cas_uc = ListGenresForCassette(cg_data)
    set_genres_uc = SetCassetteGenres(cg_data)

    cassette_presenter = CassettePresenter(
        cassette_view,
        list_cass_uc,
        add_cass_uc,
        del_cass_uc,
        update_cass_uc,
        list_genres_uc,
        list_for_cas_uc,
        set_genres_uc,
    )

    genre_presenter = GenrePresenter(
        genre_view,
        ListGenres(g_data),
        AddGenre(g_data),
        DeleteGenre(g_data),
        UpdateGenre(g_data),
    )

    main_window = MainWindow(cassette_view, genre_view)
    main_window.show()

    exit_code = app.exec()
    db.close()
    sys.exit(exit_code)


if __name__ == "__main__":
    main()

from PySide6.QtCore import QObject, Slot
from PySide6.QtWidgets import QDialog, QMessageBox

from app.services import GenreService, TariffService, TariffTypeService
from data.entities import TariffCondition
from gui.views import ProvisionConditionDialog, TariffManagementView


class TariffManagementPresenter(QObject):
    def __init__(
        self,
        view: TariffManagementView,
        dialog: ProvisionConditionDialog,
        tariff_service: TariffService,
        type_service: TariffTypeService,
        genre_service: GenreService,
    ):
        super().__init__()
        self._view = view
        self._dialog = dialog
        self._tariff = tariff_service
        self._type = type_service
        self._genre = genre_service
        self._selected_condition: TariffCondition | None = None
        self._connect_signals()
        self._init_types()
        self._refresh()

    def _connect_signals(self):
        self._view.add_request.connect(self._on_add)
        self._view.del_request.connect(self._on_del)
        self._view.upd_request.connect(self._on_upd)
        self._view.sel_changed.connect(self._on_sel)
        self._view.opn_conds.connect(self._on_cond)
        self._view.clr_fields.connect(self._on_clear)

    def _init_types(self):
        if not self._view.is_readonly:
            try:
                types = self._type.get_all()
                self._view.set_types(types)
            except Exception as e:
                self._show_err(e)

    @Slot(int)
    def _on_sel(self, id_tariff):
        try:
            tariff = self._tariff.get(id_tariff)
            if tariff:
                self._view.set_form(tariff)
                self._selected_condition = tariff.provision_condition
        except Exception as e:
            self._show_err(e)

    @Slot(str, str, int)
    def _on_add(self, name, coeff, id_type):
        try:
            self._tariff.add(name, coeff, self._selected_condition or TariffCondition(), id_type)
            self._refresh()
        except Exception as e:
            self._show_err(e)

    @Slot(int)
    def _on_del(self, id_tariff):
        try:
            self._tariff.delete(id_tariff)
            self._refresh()
        except Exception as e:
            self._show_err(e)

    @Slot(int, str, str, int)
    def _on_upd(self, id_tariff, name, coeff, id_type):
        try:
            self._tariff.update(
                id_tariff, name, coeff, self._selected_condition or TariffCondition(), id_type
            )
            self._refresh()
        except Exception as e:
            self._show_err(e)

    @Slot()
    def _on_cond(self):
        try:
            genres = self._genre.get_all()
            self._dialog.set_genres(genres)
            self._dialog.set_data(self._selected_condition or TariffCondition())
            if self._dialog.exec() == QDialog.DialogCode.Accepted:
                self._selected_condition = self._dialog.get_data()
        except Exception as e:
            self._show_err(e)

    @Slot()
    def _on_clear(self):
        self._selected_condition = None
        self._dialog.reset()

    def _refresh(self):
        try:
            tariffs = self._tariff.get_all()
            self._view.show_table(tariffs)
        except Exception as e:
            self._show_err(e)

    def _show_err(self, e: Exception):
        QMessageBox.critical(self._view, "Ошибка", str(e), QMessageBox.StandardButton.Ok)

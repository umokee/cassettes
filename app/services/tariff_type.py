from collections.abc import Sequence

from data.entities import TariffType
from data.repo import TariffTypeRepository


class TariffTypeService:
    def __init__(self, repo: TariffTypeRepository):
        self._repo = repo

    def get_all(self) -> Sequence[TariffType]:
        return self._repo.list()

    def get(self, id_tariff_type: int) -> TariffType | None:
        return self._repo.get(id_tariff_type)

    def add(self, name: str, desc: str):
        self._validate(name, desc)
        self._repo.add(name, desc)

    def update(self, id_tariff_type: int, name: str, desc: str):
        self._validate(name, desc)
        self._repo.update(id_tariff_type, name, desc)

    def delete(self, id_tariff_type: int):
        self._repo.delete(id_tariff_type)

    def _validate(self, name: str, desc: str):
        if not name.strip():
            raise ValueError("Название типа тарифа не может быть пустым")
        if len(name) > 50:
            raise ValueError("Название типа тарифа слишком длинное (макс. 50 символов)")

        if desc.strip() and len(desc) > 300:
            raise ValueError("Описание типа тарифа слишком длинное (макс. 300 символов)")

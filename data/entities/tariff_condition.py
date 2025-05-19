import json
from dataclasses import asdict, dataclass, is_dataclass
from typing import Any


@dataclass
class TimeRange:
    start: str | None = None
    end: str | None = None


@dataclass
class DateRange:
    start: str | None = None
    end: str | None = None


@dataclass
class TariffCondition:
    count_max: int | None = None
    genres: list[int] | None = None
    dates: DateRange | None = None
    weekdays: list[int] | None = None
    times: TimeRange | None = None

    @classmethod
    def from_json(cls, value: str | dict[str, Any] | None) -> "TariffCondition":
        if not value:
            return cls()
        if isinstance(value, str):
            value = json.loads(value)

        def _load(dct, klass):
            return None if dct is None else klass(**dct)

        return cls(
            value.get("count_max"),
            value.get("genres"),
            _load(value.get("dates"), DateRange),
            value.get("weekdays"),
            _load(value.get("times"), TimeRange),
        )

    def to_json(self) -> str:
        def _serialize(obj: Any):
            if obj is None:
                return None
            if is_dataclass(obj):
                return {k: _serialize(v) for k, v in asdict(obj).items()}
            if isinstance(obj, (list, tuple, set)):
                return [_serialize(i) for i in obj]
            return obj

        prepared = {
            "count_max": self.count_max,
            "genres": _serialize(self.genres),
            "dates": _serialize(self.dates),
            "weekdays": _serialize(self.weekdays),
            "times": _serialize(self.times),
        }
        # выкидываем None-ключи
        prepared = {k: v for k, v in prepared.items() if v is not None}
        return json.dumps(prepared, ensure_ascii=False)

    def to_table(self, genre_names: dict[int, str] | None = None) -> str:
        parts: list[str] = []
        if self.count_max is not None:
            parts.append(f"до {self.count_max} касс.")
        if self.genres:
            names = (
                [genre_names.get(g, str(g)) for g in self.genres]
                if genre_names
                else map(str, self.genres)
            )
            parts.append(f"жанры: {', '.join(names)}")
        if self.weekdays:
            wd = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
            idx = []
            for v in self.weekdays:
                try:
                    idx.append(int(v))
                except (TypeError, ValueError):
                    continue
            if idx:
                parts.append("дни: " + ", ".join(wd[i - 1] for i in self.weekdays))
        if self.dates:
            parts.append(f"даты: {self.dates.start}‒{self.dates.end}")
        if self.times:
            parts.append(f"время: {self.times.start}‒{self.times.end}")
        return "; ".join(parts) if parts else "—"

    def __str__(self) -> str:
        return self.to_table()

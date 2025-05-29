import json
from dataclasses import asdict, dataclass
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
    def from_json(cls, src: str | dict[str, Any] | None) -> "TariffCondition":
        if not src:
            return cls()

        data = json.loads(src) if isinstance(src, str) else src

        return cls(
            data.get("count_max"),
            data.get("genres"),
            _load_dataclass(DateRange, data.get("dates")),
            data.get("weekdays"),
            _load_dataclass(TimeRange, data.get("times")),
        )

    def to_json(self) -> str:
        cleaned = _strip_none(asdict(self))
        return json.dumps(cleaned, ensure_ascii=False)


def _strip_none(obj: Any) -> Any:
    if obj is None:
        return None
    if isinstance(obj, list):
        return [_strip_none(i) for i in obj if i is not None]
    if isinstance(obj, dict):
        return {k: _strip_none(v) for k, v in obj.items() if v is not None}
    return obj


def _load_dataclass(klass, blob: dict | None):
    return None if blob is None else klass(**blob)

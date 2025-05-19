from dataclasses import dataclass
from typing import Any


@dataclass
class TimeRange:
    start: str | None
    end: str | None


@dataclass
class DateRange:
    start: str | None
    end: str | None
    time: TimeRange | None


@dataclass
class TariffCondition:
    count_max: int | None
    genres: list[int] | None
    dates: DateRange | None
    weekdays: list[int] | None
    time_day: list[TimeRange] | None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "TariffCondition":
        def load_timerange(obj):
            if obj is None:
                return None
            return TimeRange(start=obj.get("start"), end=obj.get("end"))

        def load_daterange(obj):
            if obj is None:
                return None
            return DateRange(
                start=obj.get("start"),
                end=obj.get("end"),
                time=load_timerange(obj.get("time")),
            )

        return cls(
            count_max=data.get("count_max"),
            genres=data.get("genres"),
            dates=load_daterange(data.get("dates")),
            weekdays=data.get("weekdays"),
            time_day=[load_timerange(t) for t in data.get("time_day", [])],
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "count_max": self.count_max,
            "genres": self.genres,
            "dates": {
                "start": self.dates.start if self.dates else None,
                "end": self.dates.end if self.dates else None,
                "time": {
                    "start": self.dates.time.start,
                    "end": self.dates.time.end,
                }
                if self.dates and self.dates.time
                else None,
            }
            if self.dates
            else None,
            "weekdays": self.weekdays,
            "time_day": [{"start": t.start, "end": t.end} for t in self.time_day]
            if self.time_day
            else None,
        }

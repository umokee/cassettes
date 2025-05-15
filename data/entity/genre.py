from dataclasses import dataclass


@dataclass(slots=True)
class Genre:
    id_genre: int
    name: str
    description: str

from dataclasses import dataclass


@dataclass(slots=True)
class Cassette:
    id_cassette: int
    title: str
    condition: str
    rental_cost: float
    genres: str

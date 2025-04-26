from dataclasses import dataclass
from typing import List, Optional
from uuid import UUID


@dataclass
class Person:
    id: UUID
    name: str


@dataclass
class FilmWork:
    id: UUID
    imdb_rating: Optional[float]
    title: str
    description: Optional[str]
    genres: List[str]
    directors: List[Person]
    actors: List[Person]
    writers: List[Person]
    directors_names: List[str]
    actors_names: List[str]
    writers_names: List[str]

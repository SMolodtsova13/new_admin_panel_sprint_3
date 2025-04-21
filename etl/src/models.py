from dataclasses import dataclass, field
from typing import List
from datetime import datetime


@dataclass
class Person:
    id: str
    name: str


@dataclass
class Genre:
    id: str
    name: str


@dataclass
class Filmwork:
    id: str
    title: str
    description: str
    imdb_rating: float
    genre: List[Genre] = field(default_factory=list)
    actors: List[Person] = field(default_factory=list)
    writers: List[Person] = field(default_factory=list)
    directors: List[Person] = field(default_factory=list)
    modified: datetime = None

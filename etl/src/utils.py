from typing import Generator, Iterable, TypeVar

T = TypeVar('T')


def chunked(iterable: Iterable[T], size: int) -> Generator[list[T], None, None]:
    """Делит iterable на куски по size элементов."""
    chunk = []
    for item in iterable:
        chunk.append(item)
        if len(chunk) == size:
            yield chunk
            chunk = []
    if chunk:
        yield chunk

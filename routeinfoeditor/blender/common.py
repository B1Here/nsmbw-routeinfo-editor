from typing import Iterable, TypeGuard, TypeVar

T = TypeVar("T")


def __is_defined__(obj: T | None) -> TypeGuard[T]:
    return obj is not None


def __split_if_contains__(text: str, sep: str) -> Iterable[str]:
    return (
        [text]
        if not text.__contains__(sep)
        else filter(lambda f: f.strip(), text.split(sep))
    )

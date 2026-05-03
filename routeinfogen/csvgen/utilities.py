from typing import TypeGuard, TypeVar

T = TypeVar('T')

def isDefined(obj: T | None) -> TypeGuard[T]:
    return obj is not None

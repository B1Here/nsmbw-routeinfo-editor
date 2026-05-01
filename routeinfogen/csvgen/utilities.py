from typing import TypeGuard, TypeVar

T = TypeVar('T')

def isDefined(obj: T | None) -> TypeGuard[T]:
    """Type guard to check if an object is not None.

    :param obj: The object to check.
    :return: True if the object is not None, False otherwise."""
    return obj is not None

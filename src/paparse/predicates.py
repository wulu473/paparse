from typing import Callable
from multimethod import isa


def issubclassof(superclass_type: type) -> Callable[[any], bool]:
    return lambda T: issubclass(T, superclass_type)


def islistofsubclass(superclass_type: type) -> Callable[[any], bool]:
    """Return a function which can check whether a type that is passed
    to the function is of type list[superclass_type]
    """
    def f(T):
        if not hasattr(T, "__origin__"):
            return False
        if not hasattr(T, "__args__"):
            return False
        if not issubclass(T.__origin__, list):
            return False
        if len(T.__args__) != 1:
            return False
        return issubclass(T.__args__[0], superclass_type)
    return f


def islistof(value_type: type) -> Callable[[any], bool]:
    def f(T):
        if not hasattr(T, "__origin__"):
            return False
        if not hasattr(T, "__args__"):
            return False
        if not issubclass(T.__origin__, list):
            return False
        if len(T.__args__) != 1:
            return False
        if not issubclass(value_type, T.__args__[0]):
            return False
        return True
    return f


def isdictof(key_type: type, value_type: type) -> Callable:
    def f(T):
        if not hasattr(T, "__origin__"):
            return False
        if not hasattr(T, "__args__"):
            return False
        if not issubclass(T.__origin__, dict):
            return False
        if len(T.__args__) != 2:
            return False
        if not issubclass(key_type, T.__args__[0]):
            return False
        if not issubclass(value_type, T.__args__[1]):
            return False
        return True
    return f


def isstr(T: type) -> bool:
    return issubclass(T, str)


def isint(T: type) -> bool:
    return issubclass(T, int)


def isfloat(T: type) -> bool:
    return issubclass(T, float)


def isoneof(type_list: list[type]) -> bool:
    return isa(*type_list)

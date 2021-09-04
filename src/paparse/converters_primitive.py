import seval

from typing import Iterable, Mapping
from multimethod import overload, isa

from .predicates import isoneof, isfloat, isint, isstr, islistof, isdictof

Primitives = [int, float, str]


@overload
def convert(data: isoneof(Primitives), T: isfloat) -> float:
    return T(seval.safe_eval(str(data)))


@overload
def convert(data: isoneof(Primitives), T: isint) -> int:  # noqa: F811
    return T(seval.safe_eval(str(data)))


@overload
def convert(data: isoneof(Primitives), T: isstr) -> str:  # noqa: F811
    return T(data)


@overload
def convert(data: isa(Iterable), T: islistof(Primitives)):  # noqa: F811
    return [convert(d_i, T.__args__[0]) for d_i in data]


@overload
def convert(data: isa(Mapping),  # noqa: F811
            T: isdictof(Primitives, Primitives)):
    return {convert(k, T.__args__[0]): convert(v, T.__args__[1])
            for k, v in data}

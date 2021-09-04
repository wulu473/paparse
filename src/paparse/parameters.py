import yaml
import re

from typing import Union, Callable

Scalar = Union[str, int, float]
Value = Union[str, float, int, list, dict]

DELIMITER = "."


def _modify_leaves(tree: Value, f: Callable[[Scalar], Scalar]):
    if isinstance(tree, list):
        return [_modify_leaves(v, f) for k, v in enumerate(tree)]
    if isinstance(tree, dict):
        return {k: _modify_leaves(v, f) for k, v in tree.items()}
    return f(tree)


def _substitute(value: str, substitutions: dict[str, str]):
    for old, new in substitutions.items():
        value = re.sub(fr"\${old}([^a-zA-Z_0-9])", fr"{new}\1", value)
        value = re.sub(fr"\${old}$", fr"{new}", value)
        value = re.sub(r"\$\{" + old + r"}", fr"{new}", value)
    return value


def _flatten(tree: Union[dict, list, str, int, float],
             _parent_key: str = "") -> dict[str, str]:
    tree_flattened: dict[str, str] = dict()
    if isinstance(tree, list):
        if _parent_key:
            _parent_key += DELIMITER
        for k, v in enumerate(tree):
            tree_flattened.update(_flatten(v, f"{_parent_key}{k}"))
    elif isinstance(tree, dict):
        if _parent_key:
            _parent_key += DELIMITER
        for k, v in tree.items():
            tree_flattened.update(_flatten(v, f"{_parent_key}{k}"))
    else:
        tree_flattened[_parent_key] = str(tree)
    return tree_flattened


class Parameters:
    def __init__(self, data: dict) -> None:
        self.data = _modify_leaves(data, str)
        self._perform_substitutions()

    @staticmethod
    def from_yaml(path: str) -> "Parameters":
        with open(path) as f:
            data = yaml.safe_load(f)
        assert isinstance(data, dict)
        return Parameters(data)

    def write_yaml(self, path: str) -> None:
        with open(path, "w+") as f:
            yaml.dump(self.data, f, default_flow_style="")

    def update(self, param: list[str], value: Value) -> None:
        pa = self.data
        for p in param[:-1]:
            if p.isdigit():
                p = int(p)
            pa = pa[p]
        pa[param[-1]] = str(value)
        self._perform_substitutions()

    def _perform_substitutions(self) -> None:
        subs = _flatten(self.data)
        self.data = _modify_leaves(self.data, lambda l: _substitute(l, subs))
        if subs != _flatten(self.data):
            self._perform_substitutions()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Parameters):
            raise TypeError()
        return self.data == other.data

    def __getitem__(self, key: str) -> Value:
        return self.data[key]

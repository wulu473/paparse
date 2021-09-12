from dataclasses import dataclass

from paparse import SimpleConfig


@dataclass
class _ConfigDummy(SimpleConfig):
    x: int


class TestSimpleConfig:
    def test_from_parameters(self):
        params = dict({"x": 1})

        cfg = _ConfigDummy.from_dict(params)

        assert cfg.x == 1

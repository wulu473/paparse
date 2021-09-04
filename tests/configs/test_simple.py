from dataclasses import dataclass

from paparse import SimpleConfig, Parameters


@dataclass
class _ConfigDummy(SimpleConfig):
    x: int


class TestSimpleConfig:
    def test_from_parameters(self):
        params = Parameters({"x": 1})

        cfg = _ConfigDummy.from_parameters(params)

        assert cfg.x == 1

from dataclasses import dataclass

from paparse import MultiActiveModuleConfig, SimpleConfig, Parameters


class _Base(MultiActiveModuleConfig):
    pass


@dataclass
class _A(_Base):
    x: int


@dataclass
class _B(_Base):
    y: int


@dataclass
class _RootConfig(SimpleConfig):
    modules: list[_Base]


class TestMultiActiveConfig:
    def test_from_parameters(self):

        params = Parameters({"modules": [
            {
                "module_name": "_A",
                "x": 3
            },
            {
                "module_name": "_A",
                "x": 4
            },
            {
                "module_name": "_B",
                "y": 2
            }]
        })
        cfg = _RootConfig.from_parameters(params)

        assert isinstance(cfg.modules[0], _A) is True
        assert isinstance(cfg.modules[1], _A) is True
        assert isinstance(cfg.modules[2], _B) is True

        assert cfg.modules[0].x == 3
        assert cfg.modules[1].x == 4
        assert cfg.modules[2].y == 2

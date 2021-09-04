from dataclasses import dataclass

from paparse import SingleActiveModuleConfig, SimpleConfig, Parameters


class _Base(SingleActiveModuleConfig):
    pass


@dataclass
class _A(_Base):
    x: int


@dataclass
class _B(_Base):
    y: int


@dataclass
class _RootConfig(SimpleConfig):
    module: _Base


class TestSingleActiveConfig:
    def test_from_parameters(self):

        params_a = Parameters(
            {
                "module":
                {
                    "module_name": "_A",
                    "x": 3
                }
            }
        )
        cfg = _RootConfig.from_parameters(params_a)

        assert isinstance(cfg.module, _A) is True
        assert cfg.module.x == 3

        params_b = Parameters(
            {
                "module":
                {
                    "module_name": "_B",
                    "y": 3
                }
            }
        )

        cfg = _RootConfig.from_parameters(params_b)

        assert isinstance(cfg.module, _B) is True
        assert cfg.module.y == 3

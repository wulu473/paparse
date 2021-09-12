from dataclasses import dataclass, field

from paparse import SimpleConfig
from paparse.configs import as_commented_dict

@dataclass
class _ConfigDummy2(SimpleConfig):
    x: int = field(metadata={"help": "This is a help string for the config2"})

@dataclass
class _ConfigDummy(SimpleConfig):
    x: int = field(metadata={
        "help": "This a help string for parameter x"
    })

    cfg: _ConfigDummy2 = field(metadata={
        "help": "This is a help string for a nested config"
    })

class TestSimpleConfig:
    def test_from_parameters(self):
        params = dict({"x": 1})

        cfg = _ConfigDummy.from_parameters(params)

        assert cfg.x == 1

    def test_commented_map(self):
        cfg = _ConfigDummy.from_parameters({
            "x": 2,
            "y": {
                "x": 3
            }
        })

        commented_dict = as_commented_dict(cfg)
        
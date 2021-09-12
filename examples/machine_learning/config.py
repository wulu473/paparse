import os

from dataclasses import dataclass

from paparse import SimpleConfig, MultiActiveModuleConfig


class MetricConfig(MultiActiveModuleConfig):
    pass


@dataclass
class AccuracyConfig(MetricConfig):
    threshold: float


@dataclass
class AreaUnderCurveConfig(MetricConfig):
    pass


@dataclass
class Config(SimpleConfig):
    metrics: list[MetricConfig]


if __name__ == "__main__":
    cfg = Config.from_yaml_file(
        os.path.join(os.path.dirname(__file__), "config.yaml"))

    assert type(cfg.metrics[0]) == AccuracyConfig
    assert cfg.metrics[0].threshold == 0.5
    assert type(cfg.metrics[1]) == AreaUnderCurveConfig

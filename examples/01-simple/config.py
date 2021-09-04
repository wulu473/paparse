import os

from dataclasses import dataclass

from paparse import SimpleConfig, Parameters


@dataclass
class TrainConfig(SimpleConfig):
    batch_size: int


@dataclass
class DataConfig(SimpleConfig):
    train_path: str


@dataclass
class Config(SimpleConfig):
    trainer: TrainConfig
    data: DataConfig


if __name__ == "__main__":
    params = Parameters.from_yaml(
        os.path.join(os.path.dirname(__file__), "config.yaml"))
    cfg = Config.from_parameters(params)

    assert cfg.trainer.batch_size == 5
    assert cfg.data.train_path == "some_path"

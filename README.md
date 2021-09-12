# Parameter Parse (paparse)

## Example

``` yaml
    trainer:
        batch_size: 5
    data:
        train_path: "some_path"
```

``` python
    @dataclass
    class Config(SimpleConfig):
```

``` python
    class EarlyTerminatorConfig(MultiActiveModuleConfig):
        pass

    @dataclass
    class IncreasingValueConfig(EarlyTerminatorConfig):
        patience:int
        metric:str

    @dataclass
    class TrainerConfig:
        early_terminators:list[EarlyTerminatorConfig]
    #   batch_size:int
    #   drop_remainder:bool
    #   ...
```
# Parameter Parse (paparse)

## Features

### Templating

``` yaml
{% set grad_accum_steps = 2 %}
Trainer:
    gradient_accumulation_steps: {{ grad_accum_steps }}
    eval_steps: {{ 100 / grad_accum_steps }}
```

## Example - Computational Fluid Dynamics

``` python
@datatclass
class ComputationalDomainConfig(SimpleConfig):
    x_min: list[float]
    x_max: list[float]
```

``` python
class FluxMethodConfig(SingleActiveModuleConfig):
    pass

@dataclass
class SLIC(FluxMethodConfig):
    limiter: LimiterEnum

@dataclass
class MUSCLHancock(SingleActiveModuleConfig):
    limiter: LimiterEnum
    riemann_solver: RiemannSolverEnum
```

``` python
class OutputConfig(MultipleActiveModuleConfig):
    pass

@dataclass
class GnuplotConfig(OutputConfig):
    file_path: str

@dataclass
class CSVConfig(OutputConfig):
    file_path: str
    delimiter: str
```

## Example - Machine Learning

Let's look at how we can use paparse for a typical ML setup.

Generally, we have a few basic config classes that every training run requires.
For instance, a `TrainerConfig` which stores parameters like batch size or gradient accumulation steps.

``` python
@dataclass
class TrainerConfig(SimpleConfig):
    batch_size: int
    gradient_accumulation_steps: int

@dataclass
class DataConfig(SimpleConfig):
    train_path: str
```

Configs like that can simply be defined as a simple dictionary in YAML

``` yaml
trainer:
    batch_size: 8
    gradient_accumulation_steps: 10
data:
    train_path: "some_path"
```

### Single active module

Often we want to be able to swap in and out different modules which have slightly different parameters.
For instance, we can use either SGD or Adam as an optimizer.
Both of them require slightly different parameters.

We can solve this by having a common `OptimizerConfig` class from which other optimizer configs should inherit

``` python
class OptimizerConfig:
    pass

@dataclass
class AdamConfig(OptimizerConfig):
    learning_rate: float
    beta_1: float = 0.9
    beta_2: float = 0.999

@dataclass
class SGDConfig(OptimizerConfig):
    learning_rate: float
```

We can specify which module we want to instantiate by passing the `module_name` parameter in the dictionary.
Additionally, we can also deactivate modules by passing `active: false`.
As the base class `SingleActiveModuleConfig` suggests only one active module is allowed.

``` yaml
optimizer:
    - module_name: Adam
      learning_rate: 1e-4
    - module_name: SGD
      active: false
      learning_rate: 1e-3
```

### Multiple active modules

Sometimes, we also want to have multiple active modules.
Revisiting our ML example, this could be when we want to terminate training runs early.

``` python
class EarlyTerminatorConfig(MultiActiveModuleConfig):
    pass

@dataclass
class IncreasingValueConfig(EarlyTerminatorConfig):
    patience:int
    metric:str

@dataclass
class ExceedingValueConfig(EarlyTerminatorConfig):
    value:float
    metric:str
```

```yaml
early_terminator:
    - module_name: IncreasingValue
      patience: 5
      metric: eval_loss
    - module_name: IncreasingValue
      patience: 5
      metric: eval_acc
    - module_name: ExceedingValue
      value: 10
      metric: epsilon
```


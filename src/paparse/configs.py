import inspect

from dataclasses import fields
from typing import TypeVar, Type

from multimethod import overload

from .exceptions import ConfigError
from .parameters import Parameters
from .converters_primitive import convert
from .predicates import issubclassof, isa, islistofsubclass


class AbstractConfig:
    def instance(self):
        """Create an instance of the class this configuration is associated to
        """
        raise NotImplementedError()

    @classmethod
    def from_dict(cls, data: dict[str, any]):
        """
        Create an instance of a config class from a dictionary of values
        """
        field_dict = dict()
        for field in fields(cls):
            if field.name in data:
                field_dict[field.name] = convert(data[field.name], field.type)
        return cls(**field_dict)


class ConfigFactory:
    def __init__(self, module):
        self.module = module

    def create(self, name):
        if hasattr(self.module, name):
            return getattr(self.module, name)
        elif hasattr(self.module, f"{name}Config"):
            return getattr(self.module, f"{name}Config")
        else:
            raise ConfigError(f"Cannot find '{name}' in name space "
                              f"'{self.module}'. Make sure that "
                              f"'{name}' lives in '{self.module}'")


class SingleActiveModuleConfig(AbstractConfig):
    pass


@overload
def convert(data: isa(dict),  # noqa: F811
            BaseConfig: issubclassof(SingleActiveModuleConfig)):
    base_name_space = inspect.getmodule(BaseConfig)
    try:
        module_name = data.pop("module_name")
    except KeyError:
        raise ConfigError("Cannot find key 'module_name' when creating "
                          f"{BaseConfig}.")

    try:
        Config = ConfigFactory(base_name_space).create(module_name)
    except AttributeError as e:
        raise ConfigError(f"Cannot find '{module_name}' in name space "
                          f"'{base_name_space}'. Make sure that "
                          f"'{module_name}' lives in '{base_name_space}'"
                          ) from e
    config = Config.from_dict(data)
    return config


class MultiActiveModuleConfig(AbstractConfig):
    pass


@overload
def convert(data: isa(list),  # noqa: F811
            BaseConfigList: islistofsubclass(MultiActiveModuleConfig)):
    BaseConfig = BaseConfigList.__args__[0]
    base_name_space = inspect.getmodule(BaseConfig)
    configs = []
    for data_i in data:
        assert isinstance(data_i, dict)
        try:
            module_name = data_i.pop("module_name")
        except KeyError:
            raise ConfigError("Cannot find key 'module_name' when creating "
                              f"{BaseConfig}.")

        try:
            Config = ConfigFactory(base_name_space).create(module_name)
        except AttributeError as e:
            raise ConfigError(f"Cannot find '{module_name}' in name space "
                              f"'{base_name_space}'. Make sure that "
                              f"'{module_name}' lives in '{base_name_space}'"
                              ) from e
        config_i = Config.from_dict(data_i)
        configs.append(config_i)
    return configs


T = TypeVar('T')


class SimpleConfig(AbstractConfig):
    @classmethod
    def from_parameters(cls: Type[T], parameters: Parameters) -> T:
        return convert(parameters.data, cls)


@overload
def convert(data: isa(dict), Config: issubclassof(SimpleConfig)):  # noqa: F811
    return Config.from_dict(data)

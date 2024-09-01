import inspect
import ruamel.yaml

from dataclasses import fields, asdict, is_dataclass
from typing import TypeVar, Type

from multimethod import overload
from ruamel.yaml.comments import CommentedMap
from pathlib import Path

from .exceptions import ConfigError
from .converters_primitive import convert
from .predicates import issubclassof, isa, islistofsubclass
from .parameters import read_templated_yaml_file

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
    
    def to_dict(self):
        """
        Convert the configuration instance to a dictionary.

        This method uses the `asdict` function from the `dataclasses` module
        to convert the instance of the configuration class into a dictionary
        where the keys are the field names and the values are the field values.

        Returns:
            dict: A dictionary representation of the configuration instance.
        """
        if not is_dataclass(self):
            raise TypeError(f"{self.__class__.__name__} is not a dataclass instance.")
        return asdict(self)

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
    """
    A configuration class that provides methods to read from and write to YAML files.

    This class extends the AbstractConfig class and provides additional functionality
    to handle YAML files, including reading from a YAML file and saving the configuration
    instance as a YAML file. The class can be converted to and from a dictionary representation
    which is useful for serialization and deserialization purposes.
    """
    
    @classmethod
    def from_yaml_file(cls: Type[T], path: str, context: dict = None) -> T:
        """
        Create an instance of the class from a YAML file.

        This method reads a YAML file, optionally processes it with a Jinja2 template
        using the provided context, and converts it into an instance of the class.

        Args:
            cls (Type[T]): The class type to instantiate.
            path (str): The file path to the YAML file.
            context (dict, optional): A dictionary of context variables to render the 
                                      Jinja2 template. Defaults to None.

        Returns:
            T: An instance of the class created from the YAML file data.

        Raises:
            ConfigError: If there is an issue with the configuration data.
        """
        return convert(read_templated_yaml_file(path, context=context), cls)

    def save_as_yaml_file(self, path: str):
        """
        Convert the configuration instance to a YAML file.

        This method converts the current configuration instance to a dictionary
        and then writes the dictionary to a YAML file.

        Args:
            path (str): The file path to the YAML file.

        Raises:
            ConfigError: If there is an issue with the configuration data.
        """
        yaml = ruamel.yaml.YAML()
        with open(path, 'w', encoding='utf-8') as f:
            yaml.dump(self.to_dict(), f)


@overload
def convert(data: isa(dict), Config: issubclassof(SimpleConfig)):  # noqa: F811
    """
    Convert a dictionary to a configuration instance.

    This function converts a given dictionary into an instance of the specified
    configuration class. The dictionary can be in one of two formats:
    
    1. A direct dictionary where all the parameters required by the Config class are present.
    2. A dictionary with a single element where the key is the name of the config (which must be a subclass of Config)
       and the value is a dictionary like in the first format.

    Args:
        data (dict): The dictionary containing configuration data.
        Config (Type[SimpleConfig]): The configuration class to instantiate.

    Returns:
        SimpleConfig: An instance of the configuration class created from the dictionary data.

    Raises:
        ConfigError: If the data cannot be converted to the specified configuration class.
    """
    try:
        return Config.from_dict(data)
    # TODO only catch specific errors
    except:
        pass

    if len(data) == 1:
        config_name = list(data.keys())[0]
        config_dict = list(data.values())[0]
        config_factory = ConfigFactory(Config)
        return config_factory.create(config_name).from_dict(config_dict)
    
    raise ConfigError(f"Cannot convert {data} to {Config}")

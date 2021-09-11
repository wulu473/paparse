import ruamel
from jinja2 import Template

def read_templated_yaml_str(templated_yaml_str: str, context: dict = None) -> dict:
    j2_template = Template(templated_yaml_str)
    yaml = ruamel.yaml.YAML()
    data = yaml.load(j2_template.render(context))
    return data

def read_templated_yaml_file(path: str, context: dict = None) -> dict:
    with open(path) as f:
        templated_yaml_str = f.read()
    return read_templated_yaml_str(templated_yaml_str, context=context)

def create_context_from_unknown_args(unknown_args: list) -> dict:
    if len(unknown_args) % 2 != 0:
        raise ValueError("Cannot create context from args. Odd length")
    return {k: v for k, v in zip(unknown_args[::2], unknown_args[1::2])}

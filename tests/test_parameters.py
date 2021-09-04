import os

from tempfile import TemporaryDirectory

from paparse.parameters import Parameters, _substitute, _flatten


class TestParameters:
    def test_read_write(self):
        params = Parameters({
            "module_a": "value_a",
            "param_list": ["1", "2", "3"]
        })

        with TemporaryDirectory() as temp_dir:
            params.write_yaml(os.path.join(temp_dir, "params.yaml"))
            params_read = Parameters.from_yaml(
                os.path.join(temp_dir, "params.yaml"))

        assert params_read == params

    def test_str_conversion(self):
        params_str = Parameters({
            "param_list": ["1", "2", "3"]
        })
        params_int = Parameters({
            "param_list": [1, 2, 3]
        })

        assert params_str == params_int

    def test_substitution(self):
        params = Parameters({
            "param_a": "1.0",
            "param_list": ["1", "2", "3*$param_a"]
        })
        assert params["param_list"][2] == "3*1.0"


class TestHelper:
    def test_flatten(self):
        tree = {
            "list": [
                {"param1": 0},
                {"param1": 1}
            ]
        }
        tree_flat = _flatten(tree)
        assert tree_flat["list.0.param1"] == "0"
        assert tree_flat["list.1.param1"] == "1"

    def test_substitution_str(self):
        assert _substitute("x$variable_1.",
                           {"variable_1": "value"}) == "xvalue."
        assert _substitute("x$variable_1y",
                           {"variable_1": "value"}) == "x$variable_1y"
        assert _substitute("x${variable_1}y",
                           {"variable_1": "value"}) == "xvaluey"

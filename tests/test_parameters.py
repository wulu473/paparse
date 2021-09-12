from paparse.parameters import read_templated_yaml_str


class TestParameters:
    def test_read_commented(self):
        YAML_STR = """
            {% set param_a = 100 %}

            module_a:
                param_1: 1.0 # help: This parameter does something
                param_2: {{ param_a / 10 }} # help: This parameter does something else
                param_3: {{ param_b * 10 }}
        """
        data = read_templated_yaml_str(YAML_STR, {"param_b": 10})
        assert data["module_a"]["param_1"] == 1.0
        assert data["module_a"]["param_2"] == 10
        assert data["module_a"]["param_3"] == 100
        

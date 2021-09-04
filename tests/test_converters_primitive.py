from paparse.converters_primitive import convert


def test_convert_int():
    assert convert("1", int) == 1


def test_convert_int_eval():
    assert convert("1*5", int) == 5


def test_convert_float():
    assert convert("0.5", float) == 0.5


def test_convert_float_eval():
    assert convert("0.5*0.5", float) == 0.25

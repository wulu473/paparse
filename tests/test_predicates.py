from paparse.predicates import issubclassof

def test_issubclassof():
    assert issubclassof(int)(int) is True
    assert issubclassof(object)(int) is True


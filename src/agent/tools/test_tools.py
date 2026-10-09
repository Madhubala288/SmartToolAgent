from agent.tools.calculator import calculator
def test_addition():
    assert calculator("10 + 5") == 15
def test_multiplication():
    assert calculator("6 * 7") == 42
def test_power():
    assert calculator("2 ** 3") == 8
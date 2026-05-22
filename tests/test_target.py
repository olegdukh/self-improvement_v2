from app.target_code import calculate


def test_calculate():
    assert calculate(2, 3) == 5

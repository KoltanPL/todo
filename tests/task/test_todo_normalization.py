import pytest

from src.task.task import Todo


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        ("Foo   Bar", "foo bar"),
        ("a\t\tB", "a b"),
        ("a\n\nB", "a b"),
        ("  foo  ", "foo"),
        ("single space", "single space"),
    ],
)
def test_normalize_collapses_whitespaces_and_lowercases(raw: str, expected: str) -> None:
    assert Todo._normalize(raw) == expected

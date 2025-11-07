from src.task.task import Todo


def test_tags_no_list_tags() -> None:
    t = Todo("Write test", tags=None)
    assert t.tags == []


def test_tags_list_tags() -> None:
    t = Todo("Write test", tags=["a\t\tB", "a\n\nB", "  foo  ", "Foo   Bar", "single space"])
    assert t.tags == ["a b", "foo", "foo bar", "single space"]


def test_add_tag_adds_unique_normalized_tag() -> None:
    t = Todo("Write test", tags=None)
    t.add_tag("  Foo   Bar  ")
    t.add_tag("foo bar")
    t.add_tag("  LEARNING Python  ")
    assert t.tags == ["foo bar", "learning python"]

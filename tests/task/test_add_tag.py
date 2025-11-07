from src.task.task import Todo


def test_add_tag() -> None:
    t = Todo("Write test", tags=None)

    t.add_tag("Learning Python")
    assert t.tags == ["learning python"]

    t.add_tag("  LEARNING Python  ")
    assert t.tags == ["learning python"]

    t.add_tag("FastAPI")
    assert t.tags == ["learning python", "fastapi"]

    t.add_tag("fastapi")
    assert t.tags == ["learning python", "fastapi"]

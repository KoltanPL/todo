from src.task.task import Todo


def test_remove_tag() -> None:
    t = Todo('Write test', tags=['learning python', 'fastapi'])
    t.remove_tag('fastapi')
    assert t.tags == ['learning python']


def test_remove_tag_non_existing_tag() -> None:
    t = Todo('Write test', tags=['learning python'])
    t.remove_tag('fastapi')
    assert t.tags == ['learning python']

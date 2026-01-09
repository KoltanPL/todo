import pytest

from src.schemas.guards.todo_list_dict_guard import is_todolist_dict


@pytest.mark.parametrize('value', [1, 1.0, True, None, False, [1, 2, 3], (1, 2, 3), 'John'])
def test_is_todolist_dict_returns_false_when_not_dict(value: object) -> None:
    assert is_todolist_dict(value) is False


def test_is_todolist_dict_returns_true_for_valid(valid_todo_list: dict[str, object]) -> None:
    assert is_todolist_dict(valid_todo_list) is True


def test_is_todolist_dict_returns_true_for_empty_tasks_list() -> None:
    my_todolist = {'tasks': []}

    assert is_todolist_dict(my_todolist) is True


def test_is_todolist_dict_returns_false_when_missing_tasks_key(valid_todo_dict: dict[str, object]) -> None:
    my_todolist_invalid = {'jobs': [valid_todo_dict]}

    assert is_todolist_dict(my_todolist_invalid) is False


def test_is_todolist_dict_returns_false_when_extra_key_present(valid_todo_list: dict[str, list]) -> None:
    valid_todo_list['extra'] = ['sth']

    assert is_todolist_dict(valid_todo_list) is False


def test_is_todolist_dict_returns_false_when_tasks_is_not_list() -> None:
    my_todolist = {'tasks': set()}

    assert is_todolist_dict(my_todolist) is False


def test_is_todolist_dict_returns_false_when_tasks_contains_non_dict(valid_todo_list: dict[str, list]) -> None:
    valid_todo_list['tasks'].append(1)

    assert is_todolist_dict(valid_todo_list) is False


def test_is_todolist_dict_returns_false_when_tasks_contains_invalid_todo(valid_todo_dict: dict[str, object]) -> None:
    del valid_todo_dict['description']

    assert is_todolist_dict(valid_todo_dict) is False


def test_is_todolist_dict_returns_false_when_tasks_mixed_valid_and_invalid(valid_todo_dict: dict[str, object]) -> None:
    invalid_todo = {**valid_todo_dict, 'idx': 'fa50210a-5e38-42e3-85c3-15d43c819515', 'extra': 42}
    my_todolist = {'tasks': [valid_todo_dict, invalid_todo]}

    assert is_todolist_dict(my_todolist) is False


def test_is_todolist_dict_returns_false_when_value_has_non_str_key() -> None:
    my_todo_dict = {42: 10}

    assert is_todolist_dict(my_todo_dict) is False

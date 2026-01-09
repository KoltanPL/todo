import pytest

from src.schemas.guards.todo_dict_guard import is_todo_dict


def test_is_todo_dict_returns_true_for_valid_dict_with_deadline_none(valid_todo_dict: dict[str, object]) -> None:
    assert is_todo_dict(valid_todo_dict) is True


def test_is_todo_dict_returns_true_for_valid_dict_with_deadline_str(valid_todo_dict: dict[str, object]) -> None:
    valid_todo_dict['deadline'] = '2026-03-19'

    assert is_todo_dict(valid_todo_dict) is True


@pytest.mark.parametrize('obj', [5, [1, 2, 3], (1, 2, 3), 'John'])
def test_is_todo_dict_returns_false_when_not_dict(obj: object) -> None:
    assert is_todo_dict(obj) is False


def test_is_todo_dict_returns_false_when_missing_key(valid_todo_dict: dict[str, object]) -> None:
    valid_todo_dict.pop('priority')

    assert is_todo_dict(valid_todo_dict) is False


def test_is_todo_dict_returns_false_when_extra_key_present(valid_todo_dict: dict[str, object]) -> None:
    valid_todo_dict['status_2'] = 'Diana'

    assert is_todo_dict(valid_todo_dict) is False


def test_is_todo_dict_returns_false_when_wrong_type_description(valid_todo_dict: dict[str, object]) -> None:
    valid_todo_dict['description'] = 5

    assert is_todo_dict(valid_todo_dict) is False

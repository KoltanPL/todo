import pytest

from src.cli.commands.remove_task import remove_task
from src.enums.priority_enum import PriorityEnum
from src.enums.status_enum import StatusEnum
from src.task.task import Todo


class DummyTodoList:
    def __init__(self, tasks: list[Todo]) -> None:
        self.tasks = tasks
        self.removed: list[object] = []

    def __len__(self) -> int:
        return len(self.tasks)

    def remove(self, idx: object) -> None:
        self.removed.append(idx)


def noop(*_: object, **__: object) -> None:
    return None


@pytest.fixture
def sample_task() -> Todo:
    """
    Provide a sample Todo object.

    Returns:
        Todo: Predefined task.
    """

    return Todo(
        description='Test',
        priority=PriorityEnum.HIGH,
        status=StatusEnum.TODO,
        deadline=None,
        tags=['x'],
    )


def test_remove_task_invalid_id(monkeypatch: pytest.MonkeyPatch) -> None:
    printed: list[tuple[object, ...]] = []

    def fake_print(*args: object, **kwargs: object) -> None:
        printed.append(args)

    def fake_prompt(_: str) -> str:
        return 'abc'

    monkeypatch.setattr('src.cli.commands.remove_task.typer.prompt', fake_prompt)
    monkeypatch.setattr('src.cli.commands.remove_task.console.print', fake_print)

    remove_task()

    assert any('Invalid task id.' in str(call) for call in printed)


def test_remove_task_out_of_range(monkeypatch: pytest.MonkeyPatch) -> None:
    printed: list[tuple[object, ...]] = []

    def fake_print(*args: object, **kwargs: object) -> None:
        printed.append(args)

    def fake_prompt(_: str) -> str:
        return '10'

    def fake_get() -> DummyTodoList:
        return DummyTodoList([])

    monkeypatch.setattr('src.cli.commands.remove_task.typer.prompt', fake_prompt)
    monkeypatch.setattr('src.cli.commands.remove_task.console.print', fake_print)
    monkeypatch.setattr('src.cli.commands.remove_task.get_todo_list', fake_get)

    remove_task()

    assert any('out of range' in str(call) for call in printed)


def test_remove_task_success(monkeypatch: pytest.MonkeyPatch, sample_task: Todo) -> None:
    todo_list = DummyTodoList([sample_task])

    def fake_prompt(_: str) -> str:
        return '1'

    def fake_get() -> DummyTodoList:
        return todo_list

    saved: dict[str, bool] = {'called': False}

    def fake_save() -> None:
        saved['called'] = True

    monkeypatch.setattr('src.cli.commands.remove_task.typer.prompt', fake_prompt)
    monkeypatch.setattr('src.cli.commands.remove_task.get_todo_list', fake_get)
    monkeypatch.setattr('src.cli.commands.remove_task.save_todo_list', fake_save)
    monkeypatch.setattr('src.cli.commands.remove_task.console.print', noop)

    remove_task()

    assert todo_list.removed == [sample_task.idx]
    assert saved['called'] is True

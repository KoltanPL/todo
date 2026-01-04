from datetime import UTC, date, datetime

from src.enums.priority_enum import PriorityEnum
from src.task.task import Todo
from src.todo_list.todo_list import TodoList


def test_sort_by_priority_ascending(todo_high_priority: Todo, todo_low_priority: Todo, todo_completed: Todo) -> None:
    my_todo_list = TodoList([todo_high_priority, todo_low_priority, todo_completed])

    priority_todo_list = my_todo_list.sort_by(key=lambda todo: todo.priority, reverse=False)

    assert priority_todo_list[0] is todo_low_priority
    assert priority_todo_list[1] is todo_completed
    assert priority_todo_list[2] is todo_high_priority


def test_sort_by_priority_descending(todo_high_priority: Todo, todo_low_priority: Todo, todo_completed: Todo) -> None:
    my_todo_list = TodoList([todo_high_priority, todo_low_priority, todo_completed])

    priority_todo_list = my_todo_list.sort_by(key=lambda todo: todo.priority, reverse=True)

    assert priority_todo_list[2] is todo_low_priority
    assert priority_todo_list[1] is todo_completed
    assert priority_todo_list[0] is todo_high_priority


def test_sort_by_deadline_none_last(todo_high_priority: Todo, todo_low_priority: Todo, todo_no_deadline: Todo) -> None:
    my_todo_list = TodoList([todo_high_priority, todo_low_priority, todo_no_deadline])

    tl = my_todo_list.sort_by(key=lambda todo: (todo.deadline is None, todo.deadline))

    assert [t.deadline for t in tl] == [date(2025, 12, 13), date(2026, 1, 10), None]


def test_sort_by_stable() -> None:
    t1 = Todo(description="Python")
    t2 = Todo(description="Java")

    my_todo_list = TodoList([t1, t2])

    tl = my_todo_list.sort_by(key=lambda todo: todo.priority)

    assert tl[0] is t1
    assert tl[1] is t2


def test_sort_by_does_not_mutate_original(todo_high_priority: Todo, todo_low_priority: Todo) -> None:
    todos = [todo_high_priority, todo_low_priority]
    my_todo_list = TodoList(todos)

    tl = my_todo_list.sort_by(key=lambda todo: todo.priority)

    assert tl[0] is todo_low_priority
    assert tl[1] is todo_high_priority
    assert my_todo_list.tasks == todos


def test_sort_by_many_priority_then_deadline(
    todo_high_priority: Todo, todo_low_priority: Todo, basic_todo: Todo
) -> None:
    my_todo_list = TodoList([todo_high_priority, todo_low_priority, basic_todo])

    tl = my_todo_list.sort_by_many(lambda todo: todo.priority, lambda todo: (todo.deadline is None, todo.deadline))

    assert [(t.priority, t.deadline) for t in tl] == [
        (PriorityEnum.LOW, date(2025, 12, 21)),
        (PriorityEnum.LOW, date(2026, 1, 10)),
        (PriorityEnum.HIGH, date(2025, 12, 13)),
    ]


def test_sort_by_many_created_at_then_priority_descending() -> None:
    dt1 = datetime(2025, 12, 11, 21, 30, 0, tzinfo=UTC)
    dt2 = datetime(2026, 1, 11, 21, 30, 0, tzinfo=UTC)

    t1 = Todo(description="Python", priority=PriorityEnum.MEDIUM, created_at=dt1)

    t2 = Todo(description="Python", priority=PriorityEnum.LOW, created_at=dt2)

    ml = TodoList([t1, t2])

    tl = ml.sort_by_many(lambda todo: todo.priority, lambda todo: todo.created_at, reverse=True)

    assert [(t.priority, t.created_at) for t in tl] == [(PriorityEnum.MEDIUM, dt1), (PriorityEnum.LOW, dt2)]

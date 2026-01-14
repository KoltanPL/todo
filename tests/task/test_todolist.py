from uuid import UUID

import pytest

from src.task.task import Todo
from src.todo_list.todo_list import TodoList


def test_todolist_tasks_is_not_iterable() -> None:
    with pytest.raises(TypeError, match=r"'int' object is not iterable"):
        TodoList(1000)  # type: ignore[arg-type]


def test_todolist_tasks_is_none() -> None:
    my_task_list = TodoList(None)

    assert my_task_list.tasks == []


def test_todolist_tasks_is_empty_list() -> None:
    my_task_list = TodoList([])

    assert isinstance(my_task_list.tasks, list)


def test_todolist_tasks_is_tuple(basic_todo: Todo) -> None:
    task_1 = Todo('Write tests', idx=UUID('931f66ba-99a0-484e-8b19-4866c2f51721'))
    task_2 = basic_todo

    my_task_list = TodoList((task_1, task_2))

    assert my_task_list.tasks[0] is task_1
    assert my_task_list.tasks[1] is task_2
    assert len(my_task_list.tasks) == 2
    assert isinstance(my_task_list.tasks, list)


def test_todolist_duplicate_ids(basic_todo: Todo) -> None:
    task_1 = Todo('Write tests', idx=UUID('931f66ba-99a0-484e-8b19-4866c2f51721'))
    task_2 = Todo('Learning python', idx=UUID('931f66ba-99a0-484e-8b19-4866c2f51721'))

    with pytest.raises(ValueError, match=r'Duplicate Todo index values detected'):
        TodoList([task_1, task_2, basic_todo])


def test_todolist_unique_tasks_in_order(basic_todo: Todo) -> None:
    task_1 = Todo('Write tests', idx=UUID('931f66ba-0000-484e-8b19-4866c2f51721'))
    task_2 = Todo('Learning python', idx=UUID('931f66ba-1111-484e-8b19-4866c2f51721'))
    task_3 = basic_todo

    my_task_list = TodoList([task_1, task_2, task_3])

    assert my_task_list.tasks == [task_1, task_2, task_3]
    assert my_task_list.tasks[0] is task_1
    assert my_task_list.tasks[1] is task_2
    assert my_task_list.tasks[2] is task_3
    assert len(my_task_list.tasks) == 3


def test_todolist_accepts_generator_input(basic_todo: Todo) -> None:
    task_1 = Todo('Write tests', idx=UUID('931f66ba-0000-484e-8b19-4866c2f51721'))
    task_2 = Todo('Learning python', idx=UUID('931f66ba-1111-484e-8b19-4866c2f51721'))
    task_3 = basic_todo

    res_gen = (task for task in [task_1, task_2, task_3])

    my_task_list = TodoList(res_gen)

    assert my_task_list.tasks[0] is task_1
    assert my_task_list.tasks[1] is task_2
    assert isinstance(my_task_list.tasks, list)
    assert isinstance(my_task_list.tasks[0], Todo)

    with pytest.raises(StopIteration):
        next(res_gen)


def test_todolist_accepts_empty_generator() -> None:
    res_gen = (x for x in [])

    my_task_list = TodoList(res_gen)

    assert my_task_list.tasks == []
    assert isinstance(my_task_list.tasks, list)

    with pytest.raises(StopIteration):
        next(res_gen)


def test_todolist_shallow_copy_semantics(basic_todo: Todo) -> None:
    task_1 = Todo('Write tests', idx=UUID('931f66ba-0000-484e-8b19-4866c2f51721'))
    task_2 = Todo('Learning python', idx=UUID('931f66ba-1111-484e-8b19-4866c2f51721'))
    task_3 = basic_todo

    task_list = [task_1, task_2, task_3]
    my_task_list = TodoList(task_list)

    assert my_task_list.tasks is not task_list
    assert my_task_list.tasks[0] is task_list[0]
    assert my_task_list.tasks[1] is task_list[1]
    assert len(my_task_list.tasks) == len(task_list)
    assert isinstance(my_task_list.tasks, list)


def test_todolist_reassign_tasks(basic_todo: Todo) -> None:
    task_1 = Todo('Write tests', idx=UUID('931f66ba-0000-484e-8b19-4866c2f51721'))
    task_2 = Todo('Learning python', idx=UUID('931f66ba-1111-484e-8b19-4866c2f51721'))

    my_list = TodoList([task_1])
    assert len(my_list.tasks) == 1
    assert my_list.tasks[0] is task_1

    my_list.tasks = [task_2, basic_todo]

    assert len(my_list.tasks) == 2
    assert my_list.tasks[0] is task_2
    assert my_list.tasks[1] is basic_todo
    assert task_1 not in my_list.tasks


def test_todolist_reassign_to_none(basic_todo: Todo) -> None:
    task_1 = Todo('Write tests', idx=UUID('931f66ba-0000-484e-8b19-4866c2f51721'))

    my_list = TodoList([task_1, basic_todo])
    assert len(my_list.tasks) == 2

    my_list.tasks = None

    assert my_list.tasks == []
    assert len(my_list.tasks) == 0
    assert isinstance(my_list.tasks, list)


def test_todolist_duplicates_on_reassign(basic_todo: Todo) -> None:
    task_1 = Todo('Write tests', idx=UUID('931f66ba-0000-484e-8b19-4866c2f51721'))
    task_1_duplicate = Todo('Learning python', idx=UUID('931f66ba-0000-484e-8b19-4866c2f51721'))

    my_list = TodoList([basic_todo])
    assert len(my_list.tasks) == 1

    with pytest.raises(ValueError, match=r'Duplicate Todo index values detected'):
        my_list.tasks = [task_1, task_1_duplicate]

    assert len(my_list.tasks) == 1
    assert my_list.tasks[0] is basic_todo


def test_todolist_external_mutation_affects_internal_list() -> None:
    task_1 = Todo('Write tests', idx=UUID('931f66ba-0000-484e-8b19-4866c2f51721'))
    task_2 = Todo('Learning python', idx=UUID('931f66ba-1111-484e-8b19-4866c2f51721'))

    my_list = TodoList([task_1])

    external_ref = my_list.tasks
    external_ref.append(task_2)

    assert len(my_list.tasks) == 2
    assert my_list.tasks[1] is task_2


def test_todolist_multiple_duplicates() -> None:
    task_1 = Todo('Write tests', idx=UUID('931f66ba-0000-484e-8b19-4866c2f51721'))
    task_2 = Todo('Learning python', idx=UUID('931f66ba-0000-484e-8b19-4866c2f51721'))
    task_3 = Todo('Code review', idx=UUID('931f66ba-1111-484e-8b19-4866c2f51721'))
    task_4 = Todo('Deploy', idx=UUID('931f66ba-1111-484e-8b19-4866c2f51721'))

    with pytest.raises(ValueError, match=r'Duplicate Todo index values detected'):
        TodoList([task_1, task_2, task_3, task_4])


def test_todolist_reassign_with_generator(basic_todo: Todo) -> None:
    task_1 = Todo('Write tests', idx=UUID('931f66ba-0000-484e-8b19-4866c2f51721'))
    task_2 = Todo('Learning python', idx=UUID('931f66ba-1111-484e-8b19-4866c2f51721'))

    my_list = TodoList([basic_todo])

    gen = (task for task in [task_1, task_2])
    my_list.tasks = gen

    assert len(my_list.tasks) == 2
    assert my_list.tasks[0] is task_1
    assert my_list.tasks[1] is task_2

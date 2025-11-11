from uuid import UUID

import pytest

from src.task.task import Todo, TodoList


def test_todolist_tasks_is_not_iterable() -> None:
    with pytest.raises(TypeError, match=r"Tasks must be an iterable object."):
        TodoList(1000)  # type: ignore[arg-type]


def test_todolist_tasks_is_none() -> None:
    my_task_list = TodoList(None)

    assert my_task_list.tasks == []


def test_todolist_tasks_is_empty_list() -> None:
    my_task_list = TodoList([])

    assert isinstance(my_task_list.tasks, list)


def test_todolist_tasks_is_tuple(basic_todo: Todo) -> None:
    task_1 = Todo("Write tests", idx=UUID("931f66ba-99a0-484e-8b19-4866c2f51721"))
    task_2 = basic_todo

    my_task_list = TodoList((task_1, task_2))

    assert my_task_list.tasks[0] is task_1
    assert my_task_list.tasks[1] is task_2
    assert len(my_task_list.tasks) == 2
    assert isinstance(my_task_list.tasks, list)


def test_todolist_tasks_is_string() -> None:
    with pytest.raises(TypeError, match=r"Each task in tasks must be a Todo instance class."):
        TodoList("Write tests")  # type: ignore[arg-type]


def test_todolist_invalid_task_in_tasks(basic_todo: Todo) -> None:
    with pytest.raises(TypeError, match=r"Each task in tasks must be a Todo instance class."):
        TodoList([basic_todo, 1000])  # type: ignore[arg-type]


def test_todolist_delete_duplicate_tasks(basic_todo: Todo) -> None:
    task_1 = Todo("Write tests", idx=UUID("931f66ba-99a0-484e-8b19-4866c2f51721"))
    task_2 = Todo("Learning python", idx=UUID("931f66ba-99a0-484e-8b19-4866c2f51721"))
    task_3 = basic_todo

    my_task_list = TodoList([task_1, task_2, task_3])

    assert my_task_list.tasks[0] is task_1
    assert my_task_list.tasks[1] is task_3
    assert len(my_task_list.tasks) == 2


def test_todolist_unique_tasks_in_order(basic_todo: Todo) -> None:
    task_1 = Todo("Write tests", idx=UUID("931f66ba-0000-484e-8b19-4866c2f51721"))
    task_2 = Todo("Learning python", idx=UUID("931f66ba-1111-484e-8b19-4866c2f51721"))
    task_3 = basic_todo

    my_task_list = TodoList([task_1, task_2, task_3])

    assert my_task_list.tasks == [task_1, task_2, task_3]
    assert my_task_list.tasks[0] is task_1
    assert my_task_list.tasks[1] is task_2
    assert my_task_list.tasks[2] is task_3
    assert len(my_task_list.tasks) == 3


def test_todolist_duplicate_task_does_not_overwrite_original() -> None:
    task_1 = Todo("Write tests", idx=UUID("931f66ba-99a0-484e-8b19-4866c2f51721"))
    task_2 = Todo("Learning python", idx=UUID("931f66ba-99a0-484e-8b19-4866c2f51721"))

    my_task_list = TodoList([task_1, task_2])

    assert my_task_list.tasks[0] is task_1
    assert len(my_task_list.tasks) == 1


def test_todolist_accepts_generator_input(basic_todo: Todo) -> None:
    task_1 = Todo("Write tests", idx=UUID("931f66ba-0000-484e-8b19-4866c2f51721"))
    task_2 = Todo("Learning python", idx=UUID("931f66ba-1111-484e-8b19-4866c2f51721"))
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


def test_todolist_input_list_not_mutated(basic_todo: Todo) -> None:
    task_1 = Todo("Write tests", idx=UUID("931f66ba-0000-484e-8b19-4866c2f51721"))
    task_2 = Todo("Learning python", idx=UUID("931f66ba-1111-484e-8b19-4866c2f51721"))
    task_3 = basic_todo

    task_list = [task_1, task_2, task_3, task_2]
    task_list_copy = task_list.copy()

    my_task_list = TodoList(task_list)

    assert task_list == task_list_copy
    assert my_task_list.tasks is not task_list


def test_todolist_shallow_copy_semantics(basic_todo: Todo) -> None:
    task_1 = Todo("Write tests", idx=UUID("931f66ba-0000-484e-8b19-4866c2f51721"))
    task_2 = Todo("Learning python", idx=UUID("931f66ba-1111-484e-8b19-4866c2f51721"))
    task_3 = basic_todo

    task_list = [task_1, task_2, task_3]
    my_task_list = TodoList(task_list)

    assert my_task_list.tasks is not task_list
    assert my_task_list.tasks[0] is task_list[0]
    assert my_task_list.tasks[1] is task_list[1]
    assert len(my_task_list.tasks) == len(task_list)
    assert isinstance(my_task_list.tasks, list)


def test_todolist_duplicate_in_the_middle(basic_todo: Todo) -> None:
    task_1 = Todo("Write tests", idx=UUID("931f66ba-0000-484e-8b19-4866c2f51721"))
    task_2 = Todo("Learning python", idx=UUID("931f66ba-1111-484e-8b19-4866c2f51721"))
    task_3 = basic_todo
    task_4 = Todo("Learning java", idx=UUID("931f66ba-2222-484e-8b19-4866c2f51721"))

    task_list = [task_1, task_2, task_1, task_3, task_4]
    my_task_list = TodoList(task_list)

    assert my_task_list.tasks[2] != task_list[2]
    assert my_task_list.tasks[0] == task_list[0]
    assert my_task_list.tasks[0] is task_list[0]
    assert my_task_list.tasks[1] is task_list[1]
    assert my_task_list.tasks[2] is task_list[3]
    assert my_task_list.tasks[3] is task_list[4]
    assert len(my_task_list.tasks) == 4
    assert my_task_list.tasks.count(task_list[2]) == 1

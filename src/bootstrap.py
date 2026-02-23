from datetime import date

from src.enums.priority_enum import PriorityEnum
from src.task.task import Todo
from src.todo_list.todo_list import TodoList


def bootstrap_tasks() -> TodoList:
    raw_tasks = [
        Todo('Improving Python', deadline=date(2027, 1, 2)),
        Todo('Learning Java', priority=PriorityEnum.HIGH),
        Todo('Clustering models'),
        Todo('SQL practice', tags=['SQL', 'Select', 'From']),
    ]
    return TodoList(raw_tasks)

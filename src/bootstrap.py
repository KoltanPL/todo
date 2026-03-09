from src.todo_list.todo_list import TodoList


def bootstrap_tasks() -> TodoList:
    with open('./temp/list_task.json', encoding='utf8') as file:
        content = file.read()

    return TodoList.from_json(content)

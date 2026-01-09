from typing import TypedDict


class TodoDict(TypedDict):
    description: str
    priority: int
    created_at: str
    deadline: str | None
    tags: list[str]
    status: str
    idx: str

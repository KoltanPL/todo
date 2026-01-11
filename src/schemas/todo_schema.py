from typing import TypedDict  # pragma: no cover


class TodoDict(TypedDict):  # pragma: no cover
    description: str  # pragma: no cover
    priority: int  # pragma: no cover
    created_at: str  # pragma: no cover
    deadline: str | None  # pragma: no cover
    tags: list[str]  # pragma: no cover
    status: str  # pragma: no cover
    idx: str  # pragma: no cover

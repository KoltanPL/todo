from collections import Counter
from typing import TYPE_CHECKING


if TYPE_CHECKING:  # pragma: no cover
    from collections.abc import Iterable

    from src.task.task import Todo


class TodoList:
    """Container class for managing a collection of unique `Todo` objects.

    This class accepts any iterable of `Todo` instances and constructs an
    internal list (`self.tasks`) that:

    * preserves the original order of elements from the input iterable,
    * removes duplicates based on each task's `idx` attribute,
    * performs strict validation to ensure that every element is a `Todo`
      instance,
    * prevents mutation of the original iterable by copying tasks into a
      new list.

    Parameters
    ----------
    tasks : Iterable[Todo] | None, optional
        Any iterable containing `Todo` objects (e.g., list, tuple, generator).
        If `None`, an empty task list is created.
        Duplicate tasks (same `idx`) are automatically removed, keeping only
        the first occurrence.

    Raises
    ------
    TypeError
        If `tasks` is not iterable.
        If any element inside the iterable is not an instance of `Todo`.

    Attributes
    ----------
    tasks : list[Todo]
        A new list containing unique tasks in their original order. This list
        is always a fresh shallow copy—modifying it does not affect the input.
    """

    def __init__(self, tasks: Iterable[Todo] | None = None) -> None:
        self.tasks = tasks

    @property
    def tasks(self) -> list[Todo]:
        return self._tasks

    @tasks.setter
    def tasks(self, value: Iterable[Todo] | None) -> None:
        if value is None:
            self._tasks = []
        else:
            items = list(value)
            self._unique_ids(items)
            self._tasks = items

    @staticmethod
    def _unique_ids(tasks: Iterable[Todo]) -> None:
        ids = [str(task.idx) for task in tasks]
        counter = Counter(ids)
        duplicates = [idx for idx, count in counter.items() if count > 1]

        if duplicates:
            raise ValueError(f"Duplicate Todo index values detected: {', '.join(duplicates)}.")

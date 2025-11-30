from collections import Counter
from typing import TYPE_CHECKING


if TYPE_CHECKING:  # pragma: no cover
    from collections.abc import Iterable
    from uuid import UUID

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
        """Initialize a TodoList with an optional collection of tasks.

        Args:
            tasks: An iterable of Todo objects. Defaults to None, which creates an empty list.

        Raises:
            TypeError: If tasks is not iterable.
            ValueError: If duplicate Todo UUIDs are detected in the input.
        """
        self.tasks = tasks

    @property
    def tasks(self) -> list[Todo]:
        """Get the list of tasks.

        Returns:
            A list of Todo objects managed by this TodoList.
        """
        return self._tasks

    @tasks.setter
    def tasks(self, value: Iterable[Todo] | None) -> None:
        """Set or replace the list of tasks.

        Args:
            value: An iterable of Todo objects, or None to clear all tasks.

        Raises:
            ValueError: If duplicate Todo UUIDs are detected in the input.
        """
        if value is None:
            self._tasks = []
        else:
            items = list(value)
            self._unique_ids(items)
            self._tasks = items

    @staticmethod
    def _unique_ids(tasks: Iterable[Todo]) -> None:
        """Validate that all tasks have unique UUIDs.

        Args:
            tasks: An iterable of Todo objects to validate.

        Raises:
            ValueError: If duplicate UUIDs are found, with details of the duplicates.
        """
        ids = [str(task.idx) for task in tasks]
        counter = Counter(ids)
        duplicates = [idx for idx, count in counter.items() if count > 1]

        if duplicates:
            raise ValueError(f"Duplicate Todo index values detected: {', '.join(duplicates)}.")

    def add(self, task: Todo) -> None:
        """Add a new task to the list.

        Args:
            task: The Todo object to add.

        Raises:
            ValueError: If the task's UUID already exists in the list.
        """
        self._unique_ids([*self.tasks, task])
        self.tasks.append(task)

    def remove(self, idx: UUID) -> None:
        """Remove a task from the list by its UUID.

        Args:
            idx: The UUID of the task to remove.

        Raises:
            ValueError: If no task with the given UUID exists.
        """
        tasks_len = len(self.tasks)

        self.tasks = [task for task in self.tasks if task.idx != idx]

        if len(self.tasks) == tasks_len:
            raise ValueError(f"Task with idx: {idx} not found.")

    def get(self, idx: UUID) -> Todo:
        """Retrieve a task by its UUID.

        Args:
            idx: The UUID of the task to retrieve.

        Returns:
            The Todo object with the matching UUID.

        Raises:
            ValueError: If no task with the given UUID exists.
        """
        for task in self.tasks:
            if task.idx == idx:
                return task

        raise ValueError(f"Task with idx: {idx} not found.")

from datetime import UTC, datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from src.enums.priority_enum import PriorityEnum
from src.enums.status_enum import StatusEnum


if TYPE_CHECKING:  # pragma: no cover
    from datetime import date


class Todo:
    """Represents a single to-do item with metadata such as description, priority, status, and deadlines.

    This class encapsulates both data and validation logic for creating and managing tasks.
    Each instance of :class:`Todo` is uniquely identified by a UUID and includes optional
    deadline, creation time, and tag information.

    Attributes:
        description (str): A short textual description of the task.
        priority (PriorityEnum): The priority level of the task (default: MEDIUM).
        created_at (datetime): The UTC timestamp when the task was created.
        deadline (date | None): The due date for the task. Must be after `created_at`.
        tags (list[str]): Optional list of tag strings categorizing the task.
        status (StatusEnum): The current workflow status (e.g., TODO, IN_PROGRESS, DONE).
        idx (UUID): A unique identifier for the task.
    """

    def __init__(
        self,
        description: str,
        priority: PriorityEnum = PriorityEnum.MEDIUM,
        created_at: datetime | None = None,
        deadline: date | None = None,
        tags: list[str] | None = None,
        status: StatusEnum = StatusEnum.TODO,
        idx: UUID | str | None = None,
    ) -> None:
        """Initialize a new :class:`Todo` instance.

        Args:
            description: A short text describing the task.
            priority: The task's priority level.
            created_at: The datetime when the task was created. Defaults to current UTC time if not provided.
            deadline: The date when the task is due. Must be later than `created_at`.
            tags: An optional list of tag strings.
            status: The initial workflow status of the task.
            idx: An optional unique identifier (UUID or UUID string). A new UUIDv4 is generated if omitted.

        Raises:
            ValueError: If the `description` length is less than 3 characters.
            ValueError: If the provided `deadline` is earlier than or equal to `created_at`.
            ValueError: If `idx` string is not a valid UUID format.
        """
        self.description = description
        self.priority = priority
        self.created_at = created_at if created_at is not None else datetime.now(tz=UTC)
        self.deadline = deadline
        self.tags = tags if tags is not None else []
        self.status = status
        self.idx = idx

    @property
    def description(self) -> str:
        """Get the textual description of the task.

        Returns:
            The task description as a string.
        """
        return self._description

    @description.setter
    def description(self, value: str) -> None:
        """Set the textual description of the task.

        The description must contain at least three non-whitespace characters.

        Args:
            value: The new task description.

        Raises:
            ValueError: If the description is shorter than 3 characters.
        """
        if len(value.strip()) < 3:
            raise ValueError(f"Description {value} must be at least 3 characters.")
        self._description = value.strip()

    @property
    def idx(self) -> UUID:
        """Get the unique identifier (UUID) of the task.

        Returns:
            The UUID associated with this task instance.
        """
        return self._idx

    @idx.setter
    def idx(self, value: UUID | str | None) -> None:
        """Set the unique identifier (UUID) of the task.

        Args:
            value: The UUID object, a valid UUID string, or None.

        Raises:
            ValueError: If the string cannot be parsed into a valid UUID.
        """
        if value is None:
            self._idx = uuid4()
        elif isinstance(value, str):
            self._idx = UUID(value, version=4)
        else:
            self._idx = value

    @property
    def deadline(self) -> date:
        """Get the task deadline.

        Returns:
            The task's deadline as a :class:`datetime.date` object, or None if not set.
        """
        return self._deadline

    @deadline.setter
    def deadline(self, value: date | None) -> None:
        """Set the task deadline.

        The deadline must be strictly later than the task's creation date.

        Args:
            value: A :class:`datetime.date` object or None to remove the deadline.

        Raises:
            ValueError: If `value` is earlier than to `created_at.date()`.
        """
        if value is None:
            self._deadline = None
        elif value < self.created_at.date():
            raise ValueError(f"Deadline {value} is invalid, date should be from the future.")
        self._deadline = value

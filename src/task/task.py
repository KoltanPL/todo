from datetime import UTC, datetime
import re
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from src.enums.priority_enum import PriorityEnum
from src.enums.status_enum import StatusEnum


if TYPE_CHECKING:  # pragma: no cover
    from collections.abc import Iterable
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
        self.tags = tags
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

    @property
    def tags(self) -> list[str]:
        """Get the list of tags assigned to the task.

        Returns:
            A list of normalized tag strings associated with the task.
        """
        return self._tags

    @tags.setter
    def tags(self, value: list[str] | None) -> None:
        """Set or update the list of tags for the task.

        Tags are automatically normalized (lowercased, stripped, and deduplicated).

        Args:
            value: A list of tag strings or None to clear all tags.
        """
        if value is None:
            self._tags = []
        else:
            self._tags = self._unique_values([self._normalize(tag) for tag in value])

    @staticmethod
    def _normalize(text: str) -> str:
        """Normalize text for consistent tag formatting.

        This method:
          * Converts text to lowercase,
          * Replaces multiple spaces, tabs, or newlines with a single space,
          * Strips leading and trailing whitespace.

        Args:
            text: The tag string to normalize.

        Returns:
            A normalized lowercase string with single spaces.
        """
        return re.sub(r"\s{2,}", " ", text).lower().strip()

    @staticmethod
    def _unique_values(values: Iterable[str]) -> list[str]:
        """Remove duplicates from an iterable while preserving order.

        Args:
            values: An iterable of strings.

        Returns:
            A list containing unique values in their original order.
        """
        seen: set[str] = set()
        out: list[str] = []

        for value in values:
            if value not in seen:
                seen.add(value)
                out.append(value)
        return out

    def add_tag(self, tag: str) -> None:
        """Add a single tag to the task.

        The tag will be normalized before insertion.
        If the tag already exists (case-insensitive), it will not be added again.

        Args:
            tag: The tag string to add.
        """
        tag_ = self._normalize(tag)
        if tag_ not in self.tags:
            self.tags.append(tag_)

    def remove_tag(self, tag: str) -> None:
        """Remove a tag from the task if it exists.

        The tag is normalized before removal, ensuring consistent comparison.

        Args:
            tag: The tag string to remove. If it does not exist, no action is taken.
        """
        tag_ = self._normalize(tag)
        if tag_ in self.tags:
            self.tags.remove(tag_)

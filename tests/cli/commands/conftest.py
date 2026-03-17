import pytest

from src.enums.priority_enum import PriorityEnum
from src.enums.status_enum import StatusEnum
from src.task.task import Todo


@pytest.fixture
def sample_task() -> Todo:
    """
    Provide a sample Todo object for testing.

    Returns:
        Todo: Predefined task with sample data.
    """
    return Todo(
        description='Test task',
        priority=PriorityEnum.HIGH,
        status=StatusEnum.TODO,
        deadline=None,
        tags=['python', 'cli'],
    )

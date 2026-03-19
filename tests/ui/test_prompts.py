from __future__ import annotations

from datetime import UTC, date, datetime

import pytest
import typer

from src.enums.priority_enum import PriorityEnum
from src.enums.status_enum import StatusEnum
from src.ui import prompts


class DummySelect:
    def __init__(self, answer: str | None) -> None:
        self._answer = answer

    def ask(self) -> str | None:
        return self._answer


def test_prompt_description_valid(monkeypatch: pytest.MonkeyPatch) -> None:
    values = iter(['a', 'ab', 'valid'])

    def fake_prompt(_: str) -> str:
        return next(values)

    printed: list[str] = []

    def fake_print(msg: str) -> None:
        printed.append(msg)

    monkeypatch.setattr('src.ui.prompts.typer.prompt', fake_prompt)
    monkeypatch.setattr('src.ui.prompts.console.print', fake_print)

    result = prompts.prompt_description()

    assert result == 'valid'
    assert any('at least 3' in msg for msg in printed)


def test_prompt_priority(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        'src.ui.prompts.questionary.select',
        lambda *_, **__: DummySelect('High'),
    )

    result = prompts.prompt_priority()

    assert result == PriorityEnum.HIGH


def test_prompt_priority_abort(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        'src.ui.prompts.questionary.select',
        lambda *_, **__: DummySelect(None),
    )

    with pytest.raises(typer.Abort):
        prompts.prompt_priority()


def test_prompt_status(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        'src.ui.prompts.questionary.select',
        lambda *_, **__: DummySelect('In Progress'),
    )

    result = prompts.prompt_status()

    assert result == StatusEnum.IN_PROGRESS


def test_prompt_status_abort(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        'src.ui.prompts.questionary.select',
        lambda *_, **__: DummySelect(None),
    )

    with pytest.raises(typer.Abort):
        prompts.prompt_status()


def test_prompt_deadline_no_deadline(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        'src.ui.prompts.questionary.select',
        lambda *_, **__: DummySelect('No deadline'),
    )

    assert prompts.prompt_deadline_graphical() is None


def test_prompt_deadline_today(monkeypatch: pytest.MonkeyPatch) -> None:
    fixed = datetime(2026, 1, 1, tzinfo=UTC)

    monkeypatch.setattr(
        'src.ui.prompts.questionary.select',
        lambda *_, **__: DummySelect('Today'),
    )
    monkeypatch.setattr('src.ui.prompts.datetime', type('X', (), {'now': lambda _: fixed}))

    result = prompts.prompt_deadline_graphical()

    assert result == fixed.date()


def test_prompt_deadline_tomorrow(monkeypatch: pytest.MonkeyPatch) -> None:
    fixed = datetime(2026, 1, 1, tzinfo=UTC)

    monkeypatch.setattr(
        'src.ui.prompts.questionary.select',
        lambda *_, **__: DummySelect('Tomorrow'),
    )
    monkeypatch.setattr('src.ui.prompts.datetime', type('X', (), {'now': lambda _: fixed}))

    result = prompts.prompt_deadline_graphical()

    assert result == date(2026, 1, 2)


def test_prompt_deadline_in_7_days(monkeypatch: pytest.MonkeyPatch) -> None:
    fixed = datetime(2026, 1, 1, tzinfo=UTC)

    monkeypatch.setattr(
        'src.ui.prompts.questionary.select',
        lambda *_, **__: DummySelect('In 7 days'),
    )
    monkeypatch.setattr('src.ui.prompts.datetime', type('X', (), {'now': lambda _: fixed}))

    result = prompts.prompt_deadline_graphical()

    assert result == date(2026, 1, 8)


def test_prompt_deadline_in_14_days(monkeypatch: pytest.MonkeyPatch) -> None:
    fixed = datetime(2026, 1, 1, tzinfo=UTC)

    monkeypatch.setattr(
        'src.ui.prompts.questionary.select',
        lambda *_, **__: DummySelect('In 14 days'),
    )
    monkeypatch.setattr('src.ui.prompts.datetime', type('X', (), {'now': lambda _: fixed}))

    result = prompts.prompt_deadline_graphical()

    assert result == date(2026, 1, 15)


def test_prompt_deadline_manual_valid(monkeypatch: pytest.MonkeyPatch) -> None:
    fixed = datetime(2026, 1, 1, tzinfo=UTC)

    monkeypatch.setattr(
        'src.ui.prompts.questionary.select',
        lambda *_, **__: DummySelect('Pick exact date (YYYY-MM-DD)'),
    )
    monkeypatch.setattr('src.ui.prompts.datetime', type('X', (), {'now': lambda _: fixed}))
    monkeypatch.setattr('src.ui.prompts.typer.prompt', lambda _: '2026-01-10')

    result = prompts.prompt_deadline_graphical()

    assert result == date(2026, 1, 10)


def test_prompt_deadline_manual_retry(monkeypatch: pytest.MonkeyPatch) -> None:
    fixed = datetime(2026, 1, 1, tzinfo=UTC)

    inputs = iter(['bad', '2025-01-01', '2026-01-10'])

    def fake_prompt(_: str) -> str:
        return next(inputs)

    monkeypatch.setattr(
        'src.ui.prompts.questionary.select',
        lambda *_, **__: DummySelect('Pick exact date (YYYY-MM-DD)'),
    )
    monkeypatch.setattr('src.ui.prompts.datetime', type('X', (), {'now': lambda _: fixed}))
    monkeypatch.setattr('src.ui.prompts.typer.prompt', fake_prompt)
    monkeypatch.setattr('src.ui.prompts.typer.echo', lambda _: None)

    result = prompts.prompt_deadline_graphical()

    assert result == date(2026, 1, 10)


def test_prompt_deadline_abort(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        'src.ui.prompts.questionary.select',
        lambda *_, **__: DummySelect(None),
    )

    with pytest.raises(typer.Abort):
        prompts.prompt_deadline_graphical()


def test_prompt_tags_empty(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr('src.ui.prompts.typer.prompt', lambda *_, **__: '')

    assert prompts.prompt_tags() == []


def test_prompt_tags_values(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr('src.ui.prompts.typer.prompt', lambda *_, **__: 'a, b , c')

    assert prompts.prompt_tags() == ['a', 'b', 'c']


def test_prompt_menu(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        'src.ui.prompts.questionary.select',
        lambda *_, **__: DummySelect('X'),
    )

    result = prompts.prompt_menu(['X', 'Y'])

    assert result == 'X'

import importlib
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    import pytest


def test_main_registers_commands(monkeypatch: pytest.MonkeyPatch) -> None:
    calls: list[object] = []

    def fake_register(app: object) -> None:
        calls.append(app)

    monkeypatch.setattr('src.cli.registry.register_commands', fake_register)

    module = importlib.import_module('src.main')
    importlib.reload(module)

    assert len(calls) >= 1


def test_main_executes_app(monkeypatch: pytest.MonkeyPatch) -> None:
    called: dict[str, bool] = {'run': False}

    class DummyApp:
        def __call__(self) -> None:
            called['run'] = True

    def fake_typer(*args: object, **kwargs: object) -> DummyApp:
        return DummyApp()

    def fake_register(app: object) -> None:
        pass

    monkeypatch.setattr('typer.Typer', fake_typer)
    monkeypatch.setattr('src.cli.registry.register_commands', fake_register)

    module = importlib.import_module('src.main')
    importlib.reload(module)

    module.app()

    assert called['run'] is True

"""Tests for CLI module imports."""


def test_cli_imports() -> None:
    """Verify that cli module can be imported without executing the loop."""
    from mtg_engine import cli

    assert hasattr(cli, "main")
    assert hasattr(cli, "run_game_loop")
    assert hasattr(cli, "print_state")
    assert hasattr(cli, "print_actions")


def test_game_import() -> None:
    """Verify that game module can be imported."""
    from mtg_engine.engine import game

    assert hasattr(game, "Game")


def test_cli_creates_game() -> None:
    """Verify that Game can be created from CLI context."""
    from mtg_engine.engine.game import Game

    g = Game.new()
    assert g is not None
    assert g.state.players[0].life == 20

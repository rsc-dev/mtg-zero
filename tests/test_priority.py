"""Tests for priority and turn advancement mechanics."""

from mtg_engine.engine.actions import Action, ActionType
from mtg_engine.engine.game import Game


class TestPriorityAndTurns:
    """Tests for priority passing and turn advancement."""

    def test_empty_stack_pass_advances_turn(self) -> None:
        """Test that passing with empty stack advances the turn.

        Scenario:
        - Start at turn 1, active_player 0, priority_player 0
        - Both players pass with empty stack
        - Turn should increment, active_player should swap
        - priority_player should equal active_player
        - pass_streak should reset
        """
        g = Game.new()

        # Record initial state
        initial_turn = g.state.turn
        initial_active = g.state.active_player

        assert initial_turn == 1
        assert initial_active == 0
        assert g.state.priority_player == 0
        assert g.state.stack.is_empty()

        # P0 passes
        g.apply(Action(ActionType.PASS))
        assert g.state.pass_streak == 1
        assert g.state.priority_player == 1
        assert g.state.turn == 1  # Turn hasn't changed yet

        # P1 passes (with empty stack -> turn advances)
        g.apply(Action(ActionType.PASS))

        # Verify turn advancement
        assert g.state.turn == 2
        assert g.state.active_player == 1  # Swapped from 0 to 1
        assert g.state.priority_player == 1  # Equals active_player
        assert g.state.pass_streak == 0  # Reset

    def test_priority_switches_after_cast(self) -> None:
        """Test that priority switches to opponent after casting."""
        g = Game.new()

        assert g.state.priority_player == 0

        g.apply(Action(ActionType.CAST_A))
        assert g.state.priority_player == 1

        g.apply(Action(ActionType.CAST_B))
        assert g.state.priority_player == 0

    def test_priority_switches_after_pass(self) -> None:
        """Test that priority switches after passing."""
        g = Game.new()

        assert g.state.priority_player == 0

        g.apply(Action(ActionType.PASS))
        assert g.state.priority_player == 1

        # Cast to reset pass_streak and prevent turn advancement
        g.apply(Action(ActionType.CAST_A))
        assert g.state.priority_player == 0

    def test_priority_returns_to_active_after_resolution(self) -> None:
        """Test that priority returns to active player after stack resolution."""
        g = Game.new()

        # P0 is active, casts a spell
        g.apply(Action(ActionType.CAST_A))  # Priority to P1

        # Both pass to resolve
        g.apply(Action(ActionType.PASS))  # P1 passes, priority to P0
        g.apply(Action(ActionType.PASS))  # P0 passes, stack resolves

        # After resolution, priority should be with active player (P0)
        assert g.state.active_player == 0
        assert g.state.priority_player == 0

    def test_pass_streak_resets_on_cast(self) -> None:
        """Test that pass_streak resets when a spell is cast."""
        g = Game.new()

        # P0 passes
        g.apply(Action(ActionType.PASS))
        assert g.state.pass_streak == 1

        # P1 casts instead of passing
        g.apply(Action(ActionType.CAST_A))
        assert g.state.pass_streak == 0

    def test_multiple_turn_advancements(self) -> None:
        """Test multiple consecutive turn advancements."""
        g = Game.new()

        assert g.state.turn == 1
        assert g.state.active_player == 0

        # Turn 1 -> 2
        g.apply(Action(ActionType.PASS))
        g.apply(Action(ActionType.PASS))
        assert g.state.turn == 2
        assert g.state.active_player == 1

        # Turn 2 -> 3
        g.apply(Action(ActionType.PASS))
        g.apply(Action(ActionType.PASS))
        assert g.state.turn == 3
        assert g.state.active_player == 0

        # Turn 3 -> 4
        g.apply(Action(ActionType.PASS))
        g.apply(Action(ActionType.PASS))
        assert g.state.turn == 4
        assert g.state.active_player == 1

"""Tests for stack resolution mechanics."""

from mtg_engine.engine.actions import Action, ActionType
from mtg_engine.engine.game import Game


class TestStackResolution:
    """Tests for LIFO stack resolution."""

    def test_stack_lifo_resolution(self) -> None:
        """Test that stack resolves in LIFO order.

        Scenario:
        - P0 casts A (3 damage)
        - P1 casts B (2 damage)
        - Both pass -> B resolves first, P0 takes 2 damage (20 -> 18)
        - Both pass -> A resolves, P1 takes 3 damage (20 -> 17)
        - Stack should be empty at the end
        """
        g = Game.new()

        # Verify starting state
        assert g.state.players[0].life == 20
        assert g.state.players[1].life == 20
        assert g.state.priority_player == 0

        # P0 casts A (goes on stack, priority passes to P1)
        g.apply(Action(ActionType.CAST_A))
        assert len(g.state.stack) == 1
        assert g.state.priority_player == 1

        # P1 casts B (goes on stack on top of A, priority passes to P0)
        g.apply(Action(ActionType.CAST_B))
        assert len(g.state.stack) == 2
        assert g.state.priority_player == 0

        # Verify stack order: B is on top (will resolve first)
        assert g.state.stack.peek().name == "B"

        # P0 passes (pass_streak = 1)
        g.apply(Action(ActionType.PASS))
        assert g.state.pass_streak == 1
        assert g.state.priority_player == 1

        # P1 passes (pass_streak = 2, triggers resolution of B)
        g.apply(Action(ActionType.PASS))

        # B resolved: P0 (opponent of P1 who cast B) takes 2 damage
        assert g.state.players[0].life == 18
        assert g.state.players[1].life == 20
        assert len(g.state.stack) == 1  # Only A remains
        assert g.state.pass_streak == 0
        assert g.state.priority_player == g.state.active_player

        # Now resolve A
        # P0 passes
        g.apply(Action(ActionType.PASS))
        assert g.state.pass_streak == 1

        # P1 passes (triggers resolution of A)
        g.apply(Action(ActionType.PASS))

        # A resolved: P1 (opponent of P0 who cast A) takes 3 damage
        assert g.state.players[0].life == 18
        assert g.state.players[1].life == 17
        assert g.state.stack.is_empty()
        assert g.state.pass_streak == 0

    def test_multiple_spells_same_player(self) -> None:
        """Test stack when same player casts multiple spells."""
        g = Game.new()

        # P0 casts A, then P1 passes priority back, P0 casts A again
        g.apply(Action(ActionType.CAST_A))  # P0 casts, priority to P1
        g.apply(Action(ActionType.PASS))  # P1 passes, priority to P0
        g.apply(Action(ActionType.CAST_A))  # P0 casts again, priority to P1

        assert len(g.state.stack) == 2

        # Both pass to resolve top A
        g.apply(Action(ActionType.PASS))  # P1 passes
        g.apply(Action(ActionType.PASS))  # P0 passes -> resolve

        assert g.state.players[1].life == 17  # P1 took 3 damage
        assert len(g.state.stack) == 1

        # Both pass to resolve bottom A
        g.apply(Action(ActionType.PASS))
        g.apply(Action(ActionType.PASS))

        assert g.state.players[1].life == 14  # P1 took another 3 damage
        assert g.state.stack.is_empty()

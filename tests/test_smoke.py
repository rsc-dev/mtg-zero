"""Smoke tests to verify the test setup works."""

import mtg_engine
from mtg_engine.engine.actions import (
    Action,
    ActionType,
    action_from_input,
    action_label,
)
from mtg_engine.engine.phases import Phase
from mtg_engine.engine.stack import Stack, StackItem
from mtg_engine.engine.state import GameState, PlayerState, new_game


def test_import_succeeds() -> None:
    """Verify that mtg_engine can be imported."""
    assert mtg_engine.__version__ == "0.1.0"


class TestPhase:
    """Tests for Phase enum."""

    def test_main_phase_exists(self) -> None:
        """Phase.MAIN must exist."""
        assert Phase.MAIN is not None

    def test_all_phases_exist(self) -> None:
        """All expected phases should exist."""
        assert Phase.BEGIN is not None
        assert Phase.MAIN is not None
        assert Phase.COMBAT is not None
        assert Phase.END is not None

    def test_str_representation(self) -> None:
        """Phase should have a human-readable string representation."""
        assert str(Phase.MAIN) == "Main"
        assert str(Phase.BEGIN) == "Begin"


class TestAction:
    """Tests for Action and ActionType."""

    def test_action_types_exist(self) -> None:
        """All action types should exist."""
        assert ActionType.CAST_A is not None
        assert ActionType.CAST_B is not None
        assert ActionType.PASS is not None

    def test_action_construction(self) -> None:
        """Action can be constructed with an ActionType."""
        action = Action(ActionType.PASS)
        assert action.type == ActionType.PASS

    def test_action_from_input_valid(self) -> None:
        """action_from_input parses valid inputs."""
        assert action_from_input("a") == Action(ActionType.CAST_A)
        assert action_from_input("b") == Action(ActionType.CAST_B)
        assert action_from_input("p") == Action(ActionType.PASS)

    def test_action_from_input_case_insensitive(self) -> None:
        """action_from_input is case-insensitive."""
        assert action_from_input("A") == Action(ActionType.CAST_A)
        assert action_from_input("P") == Action(ActionType.PASS)

    def test_action_from_input_invalid(self) -> None:
        """action_from_input returns None for invalid input."""
        assert action_from_input("x") is None
        assert action_from_input("") is None
        assert action_from_input("cast") is None

    def test_action_label(self) -> None:
        """action_label returns human-readable labels."""
        assert action_label(Action(ActionType.CAST_A)) == "Cast Spell A"
        assert action_label(Action(ActionType.CAST_B)) == "Cast Spell B"
        assert action_label(Action(ActionType.PASS)) == "Pass"


class TestStack:
    """Tests for StackItem and Stack."""

    def test_stack_item_construction(self) -> None:
        """StackItem can be constructed with required fields."""
        item = StackItem(name="Lightning Bolt", controller=0, damage_to_opponent=3)
        assert item.name == "Lightning Bolt"
        assert item.controller == 0
        assert item.damage_to_opponent == 3

    def test_stack_empty_on_creation(self) -> None:
        """A new Stack should be empty."""
        stack = Stack()
        assert stack.is_empty()
        assert len(stack) == 0
        assert stack.peek() is None

    def test_stack_push_and_peek(self) -> None:
        """push adds an item, peek returns it without removing."""
        stack = Stack()
        item = StackItem(name="Shock", controller=1, damage_to_opponent=2)
        stack.push(item)

        assert not stack.is_empty()
        assert len(stack) == 1
        assert stack.peek() == item
        assert len(stack) == 1  # peek doesn't remove

    def test_stack_push_and_pop(self) -> None:
        """pop removes and returns the top item."""
        stack = Stack()
        item = StackItem(name="Shock", controller=1, damage_to_opponent=2)
        stack.push(item)

        popped = stack.pop()
        assert popped == item
        assert stack.is_empty()

    def test_stack_lifo_order(self) -> None:
        """Stack follows LIFO order."""
        stack = Stack()
        item1 = StackItem(name="First", controller=0, damage_to_opponent=1)
        item2 = StackItem(name="Second", controller=1, damage_to_opponent=2)

        stack.push(item1)
        stack.push(item2)

        assert stack.pop() == item2  # Last in, first out
        assert stack.pop() == item1

    def test_stack_describe_top_first(self) -> None:
        """describe returns items top-first."""
        stack = Stack()
        item1 = StackItem(name="Bottom", controller=0, damage_to_opponent=1)
        item2 = StackItem(name="Top", controller=1, damage_to_opponent=2)

        stack.push(item1)
        stack.push(item2)

        desc = stack.describe()
        assert len(desc) == 2
        assert "Top" in desc[0]
        assert "Bottom" in desc[1]


class TestState:
    """Tests for PlayerState and GameState."""

    def test_player_state_construction(self) -> None:
        """PlayerState can be constructed with life total."""
        player = PlayerState(life=20)
        assert player.life == 20

    def test_new_game_defaults(self) -> None:
        """new_game creates a valid initial game state."""
        game = new_game()

        assert game.turn == 1
        assert game.active_player == 0
        assert game.priority_player == 0
        assert game.phase == Phase.MAIN
        assert game.pass_streak == 0
        assert len(game.players) == 2
        assert game.players[0].life == 20
        assert game.players[1].life == 20
        assert game.stack.is_empty()

    def test_new_game_custom_life(self) -> None:
        """new_game respects custom starting life."""
        game = new_game(starting_life=40)
        assert game.players[0].life == 40
        assert game.players[1].life == 40

    def test_opponent(self) -> None:
        """opponent returns the other player's index."""
        game = new_game()
        assert game.opponent(0) == 1
        assert game.opponent(1) == 0

    def test_clone_shallow(self) -> None:
        """clone_shallow creates an independent copy."""
        game = new_game()
        game.stack.push(StackItem(name="Spell", controller=0, damage_to_opponent=3))

        clone = game.clone_shallow()

        # Basic values should match
        assert clone.turn == game.turn
        assert clone.active_player == game.active_player
        assert clone.phase == game.phase
        assert clone.players[0].life == game.players[0].life

        # But they should be independent objects
        clone.players[0].life = 10
        assert game.players[0].life == 20  # Original unchanged

        clone.stack.push(StackItem(name="Another", controller=1, damage_to_opponent=2))
        assert len(game.stack) == 1  # Original unchanged
        assert len(clone.stack) == 2

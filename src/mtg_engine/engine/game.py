"""Game class - orchestrates a Magic: The Gathering game."""

from __future__ import annotations

from mtg_engine.engine.actions import Action, ActionType
from mtg_engine.engine.stack import StackItem
from mtg_engine.engine.state import GameState, new_game


class GameInvariantError(Exception):
    """Raised when a game invariant is violated."""

    pass


class Game:
    """Orchestrates a Magic: The Gathering game.

    This class manages the game loop, legal actions, and state transitions.
    Currently implements a simplified version with MAIN phase only.

    Attributes:
        state: The current game state.
    """

    def __init__(self, state: GameState) -> None:
        """Initialize a game with the given state.

        Args:
            state: The initial game state.
        """
        self.state: GameState = state

    @classmethod
    def new(cls, starting_life: int = 20) -> Game:
        """Create a new game with default initial state.

        Args:
            starting_life: Starting life total for each player.

        Returns:
            A new Game instance ready to play.
        """
        return cls(new_game(starting_life))

    def legal_actions(self) -> list[Action]:
        """Return all legal actions for the player with priority.

        Currently, all actions are always legal (no mana/timing restrictions).

        Returns:
            A list of legal actions.
        """
        return [
            Action(ActionType.CAST_A),
            Action(ActionType.CAST_B),
            Action(ActionType.PASS),
        ]

    def apply(self, action: Action) -> None:
        """Apply an action to the game state.

        This method implements the core game rules for action resolution:

        **Casting a spell (CAST_A or CAST_B):**
        1. Push the spell onto the stack
        2. Reset pass_streak to 0
        3. Pass priority to the opponent

        **Passing priority (PASS):**
        1. Increment pass_streak
        2. Pass priority to the opponent
        3. If pass_streak reaches 2 (both players passed consecutively):
           - If stack is non-empty: resolve the top item
             - Pop the top spell from the stack
             - Deal its damage to the controller's opponent
             - Reset pass_streak to 0
             - Priority returns to the active player
           - If stack is empty: advance to next turn
             - Increment turn counter
             - Swap active player
             - Reset pass_streak to 0
             - Priority goes to the new active player

        Args:
            action: The action to apply.

        Raises:
            GameInvariantError: If the action results in an invalid game state.
        """
        state = self.state
        priority_player = state.priority_player

        match action.type:
            case ActionType.CAST_A:
                state.stack.push(
                    StackItem(
                        name="A",
                        controller=priority_player,
                        damage_to_opponent=3,
                    )
                )
                state.pass_streak = 0
                state.priority_player = state.opponent(priority_player)

            case ActionType.CAST_B:
                state.stack.push(
                    StackItem(
                        name="B",
                        controller=priority_player,
                        damage_to_opponent=2,
                    )
                )
                state.pass_streak = 0
                state.priority_player = state.opponent(priority_player)

            case ActionType.PASS:
                state.pass_streak += 1
                state.priority_player = state.opponent(priority_player)

                if state.pass_streak >= 2:
                    if not state.stack.is_empty():
                        # Resolve the top item on the stack
                        item = state.stack.pop()
                        opponent = state.opponent(item.controller)
                        state.players[opponent].life -= item.damage_to_opponent
                        state.pass_streak = 0
                        state.priority_player = state.active_player
                    else:
                        # Advance to next turn
                        state.turn += 1
                        state.active_player = state.opponent(state.active_player)
                        state.pass_streak = 0
                        state.priority_player = state.active_player

        self._assert_invariants()

    def _assert_invariants(self) -> None:
        """Check that game state invariants hold.

        Invariants checked:
        - priority_player is 0 or 1
        - active_player is 0 or 1
        - players list has exactly 2 elements
        - pass_streak is 0 or 1 (never 2+ after apply completes)
        - turn is positive

        Raises:
            GameInvariantError: If any invariant is violated.
        """
        state = self.state

        if state.priority_player not in (0, 1):
            raise GameInvariantError(
                f"priority_player must be 0 or 1, got {state.priority_player}"
            )

        if state.active_player not in (0, 1):
            raise GameInvariantError(
                f"active_player must be 0 or 1, got {state.active_player}"
            )

        if len(state.players) != 2:
            raise GameInvariantError(
                f"players list must have exactly 2 elements, got {len(state.players)}"
            )

        if state.pass_streak not in (0, 1):
            raise GameInvariantError(
                f"pass_streak must be 0 or 1 after apply, got {state.pass_streak}"
            )

        if state.turn < 1:
            raise GameInvariantError(f"turn must be positive, got {state.turn}")

    def is_over(self) -> bool:
        """Check if the game is over.

        Returns:
            True if any player has life <= 0.
        """
        return any(p.life <= 0 for p in self.state.players)

    def winner(self) -> int | None:
        """Determine the winner of the game.

        Returns:
            The index of the winning player (the one with life > 0),
            or None if the game is not over or both players are at <= 0 life.
        """
        if not self.is_over():
            return None

        p0_alive = self.state.players[0].life > 0
        p1_alive = self.state.players[1].life > 0

        if p0_alive and not p1_alive:
            return 0
        elif p1_alive and not p0_alive:
            return 1
        else:
            # Both dead or neither dead (shouldn't happen if is_over is true)
            return None

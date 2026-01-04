"""Game state representation."""

from dataclasses import dataclass, field

from mtg_engine.engine.phases import Phase
from mtg_engine.engine.stack import Stack


@dataclass
class PlayerState:
    """State for a single player.

    Attributes:
        life: The player's current life total.
    """

    life: int


@dataclass
class GameState:
    """Complete state of a Magic: The Gathering game.

    Attributes:
        turn: Current turn number (starts at 1).
        active_player: Index of the player whose turn it is (0 or 1).
        priority_player: Index of the player who currently has priority (0 or 1).
        phase: Current phase of the turn.
        pass_streak: Number of consecutive passes across both players.
            Resets when a player takes a non-pass action.
        players: List of player states (always length 2).
        stack: The game stack.
    """

    turn: int
    active_player: int
    priority_player: int
    phase: Phase
    pass_streak: int
    players: list[PlayerState]
    stack: Stack = field(default_factory=Stack)

    def opponent(self, p: int) -> int:
        """Return the opponent's index for a given player.

        Args:
            p: Player index (0 or 1).

        Returns:
            The opponent's index (1 if p is 0, 0 if p is 1).
        """
        return 1 - p

    def clone_shallow(self) -> "GameState":
        """Create a shallow copy of the game state.

        Note: This creates new list/Stack objects but does not deep-copy
        the StackItems or PlayerState objects within them. For immutable
        StackItems this is fine; PlayerState may need attention if mutated.

        Returns:
            A new GameState with copied containers.
        """
        new_stack = Stack()
        new_stack._items = list(self.stack._items)
        return GameState(
            turn=self.turn,
            active_player=self.active_player,
            priority_player=self.priority_player,
            phase=self.phase,
            pass_streak=self.pass_streak,
            players=[PlayerState(life=p.life) for p in self.players],
            stack=new_stack,
        )


def new_game(starting_life: int = 20) -> GameState:
    """Create a new game state with default initial values.

    Args:
        starting_life: Starting life total for each player. Defaults to 20.

    Returns:
        A fresh GameState ready to begin a game.
    """
    return GameState(
        turn=1,
        active_player=0,
        priority_player=0,
        phase=Phase.MAIN,
        pass_streak=0,
        players=[PlayerState(life=starting_life), PlayerState(life=starting_life)],
        stack=Stack(),
    )

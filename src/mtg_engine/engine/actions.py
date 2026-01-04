"""Player actions and action handling."""

from dataclasses import dataclass
from enum import Enum, auto


class ActionType(Enum):
    """Types of actions a player can take.

    For the initial prototype:
    - CAST_A: Cast spell A (placeholder for a damage spell)
    - CAST_B: Cast spell B (placeholder for another damage spell)
    - PASS: Pass priority
    """

    CAST_A = auto()
    CAST_B = auto()
    PASS = auto()


@dataclass(frozen=True, slots=True)
class Action:
    """A player action.

    Attributes:
        type: The type of action being taken.
    """

    type: ActionType


# Mapping from input characters to action types
_INPUT_MAP: dict[str, ActionType] = {
    "a": ActionType.CAST_A,
    "b": ActionType.CAST_B,
    "p": ActionType.PASS,
}

# Mapping from action types to human-readable labels
_LABEL_MAP: dict[ActionType, str] = {
    ActionType.CAST_A: "Cast Spell A",
    ActionType.CAST_B: "Cast Spell B",
    ActionType.PASS: "Pass",
}


def action_from_input(s: str) -> Action | None:
    """Parse a user input string into an Action.

    Args:
        s: User input string. Accepts "a", "b", or "p" (case-insensitive).

    Returns:
        The corresponding Action, or None if input is invalid.

    Examples:
        >>> action_from_input("a")
        Action(type=<ActionType.CAST_A: 1>)
        >>> action_from_input("X")
        None
    """
    action_type = _INPUT_MAP.get(s.strip().lower())
    if action_type is None:
        return None
    return Action(action_type)


def action_label(a: Action) -> str:
    """Return a human-readable label for an action.

    Args:
        a: The action to describe.

    Returns:
        A string describing the action.

    Examples:
        >>> action_label(Action(ActionType.PASS))
        'Pass'
    """
    return _LABEL_MAP[a.type]

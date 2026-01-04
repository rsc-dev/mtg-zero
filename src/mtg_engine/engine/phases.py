"""Turn phases and steps."""

from enum import Enum, auto


class Phase(Enum):
    """Phases of a Magic: The Gathering turn.

    For the initial prototype, we define a simplified set of phases.
    The full turn structure includes more granular steps within each phase.
    """

    BEGIN = auto()
    MAIN = auto()
    COMBAT = auto()
    END = auto()

    def __str__(self) -> str:
        """Return a human-readable name for the phase."""
        return self.name.capitalize()

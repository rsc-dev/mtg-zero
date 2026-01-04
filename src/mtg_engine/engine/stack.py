"""The stack - spells and abilities waiting to resolve."""

from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class StackItem:
    """An item on the stack (spell or ability).

    Attributes:
        name: Display name for this stack item.
        controller: Index of the player who controls this item (0 or 1).
        damage_to_opponent: Amount of damage this deals to opponent on resolution.
    """

    name: str
    controller: int
    damage_to_opponent: int


@dataclass
class Stack:
    """The game stack where spells and abilities wait to resolve.

    Items are stored in LIFO order. The last item pushed is the first to resolve.
    The internal list stores items with index 0 being the bottom of the stack.
    """

    _items: list[StackItem] = field(default_factory=list)

    def push(self, item: StackItem) -> None:
        """Push an item onto the top of the stack.

        Args:
            item: The stack item to add.
        """
        self._items.append(item)

    def pop(self) -> StackItem:
        """Remove and return the top item from the stack.

        Returns:
            The top stack item.

        Raises:
            IndexError: If the stack is empty.
        """
        return self._items.pop()

    def peek(self) -> StackItem | None:
        """Return the top item without removing it.

        Returns:
            The top stack item, or None if the stack is empty.
        """
        if self._items:
            return self._items[-1]
        return None

    def is_empty(self) -> bool:
        """Check if the stack is empty.

        Returns:
            True if the stack has no items, False otherwise.
        """
        return len(self._items) == 0

    def __len__(self) -> int:
        """Return the number of items on the stack."""
        return len(self._items)

    def describe(self) -> list[str]:
        """Return a description of all stack items, top-first.

        Returns:
            A list of strings describing each item, with the top of the
            stack first (index 0) and bottom last.
        """
        return [
            f"{item.name} (P{item.controller}, {item.damage_to_opponent} dmg)"
            for item in reversed(self._items)
        ]

"""Command-line interface for MTG Engine."""

from mtg_engine.engine.actions import action_from_input, action_label
from mtg_engine.engine.game import Game


def print_state(game: Game) -> None:
    """Print the current game state."""
    state = game.state

    print()
    print("=" * 50)
    print(f"Turn {state.turn} | Phase: {state.phase}")
    print(f"Active Player: P{state.active_player} | Priority: P{state.priority_player}")
    print("-" * 50)
    print(f"P0 Life: {state.players[0].life}")
    print(f"P1 Life: {state.players[1].life}")
    print("-" * 50)

    if state.stack.is_empty():
        print("Stack: (empty)")
    else:
        print("Stack (top first):")
        for desc in state.stack.describe():
            print(f"  - {desc}")

    print("=" * 50)


def print_actions(game: Game) -> None:
    """Print available actions."""
    print(f"\nP{game.state.priority_player}'s turn to act:")
    print("  [a] Cast Spell A (3 damage)")
    print("  [b] Cast Spell B (2 damage)")
    print("  [p] Pass priority")
    print("  [q] Quit game")


def run_game_loop(game: Game) -> None:
    """Run the main game loop."""
    while not game.is_over():
        print_state(game)
        print_actions(game)

        try:
            user_input = input("\n> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGame aborted.")
            return

        if user_input.lower() == "q":
            print("Game quit by user.")
            return

        action = action_from_input(user_input)
        if action is None:
            print(f"Invalid input '{user_input}'. Use: a, b, p, or q")
            continue

        print(f"P{game.state.priority_player} -> {action_label(action)}")
        game.apply(action)

    # Game over
    print_state(game)
    winner = game.winner()
    if winner is not None:
        print(f"\n*** GAME OVER: Player {winner} wins! ***\n")
    else:
        print("\n*** GAME OVER: Draw! ***\n")


def main() -> None:
    """Entry point for the CLI."""
    print("MTG Engine - Minimal Prototype")
    print("Two players, MAIN phase only")
    print("Spell A deals 3 damage, Spell B deals 2 damage")
    print()

    game = Game.new()
    run_game_loop(game)


if __name__ == "__main__":
    main()

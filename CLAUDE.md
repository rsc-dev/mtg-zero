Magic: The Gathering Simulation Engine (Python, uv)

Core Purpose & Vision: This project aims to develop a Magic: The Gathering (MTG) simulation engine in Python that enforces the full official rules of the game. The long-term vision is a robust engine capable of simulating complete MTG games with full rules enforcement, from turn structure and the stack to complex card interactions. The engine will start as a command-line tool for two-player games, but it is designed with extensibility in mind. Future extensions will include AI players (for testing and training through self-play simulations) and potentially a graphical or web-based UI on top of the core engine. Ultimately, the project aspires to be a faithful rules engine for MTG, usable for AI research or as the backend for playable MTG applications, mirroring the capabilities of established engines like XMage/Forge but in Python.

Primary Constraints & Stack:

Language: Python (targeting Python 3.x). This ensures ease of development and integration with AI/ML tools in the future. We prioritize pure Python standard libraries and self-contained logic for portability and clarity.

Package Manager: uv (Astral’s ultra-fast Python project manager) will manage dependencies and environments
medium.com
. The project will use a pyproject.toml for configuration, and uv will handle package installation, lockfiles, and virtual environment management. All contributors should use uv to ensure consistent environments.

Project Scope: Full MTG rules enforcement from the outset. We will not simplify the turn structure or ignore the stack/priority system – these core rules must be implemented correctly in the first prototype. The Comprehensive Rules (provided in /docs) will serve as the primary requirements reference.

Dependencies: Keep external dependencies minimal. Aside from uv and possibly testing frameworks, the engine should rely on standard Python libraries. If needed, use lightweight libraries for specific tasks (e.g. a finite state machine library or a parser generator), but only if they significantly speed up development without bloating the project.

Performance: While Python is not as fast as low-level languages, the engine should be efficient enough to handle many simulated games (for AI training). We may consider optimizations (caching results, using Python’s data model effectively) and later possibly integrate with faster libraries (e.g. use of NumPy for simulations or even Rust extensions) if needed. However, clarity and correctness take priority over premature optimization in early phases.

Development Phases & Priorities: We will approach development in incremental phases. Each phase focuses on expanding the engine’s capabilities while maintaining correct rules enforcement:

Phase 1 – Core Engine Foundation (Highest Priority): Build the fundamental game loop and rule enforcement. This includes the turn structure (beginning phase, main phases, combat, ending phase), the priority system for players to act or pass, and the concept of the stack for spells/abilities. By the end of Phase 1, the engine should support two players playing a very basic game with simple cards, with all steps of a turn and the stack resolution working according to the rules. The focus is on rules framework rather than a large card pool.

Phase 2 – Expand Card Types & Actions: Introduce more card types (creatures, sorceries, instants, enchantments, etc.) and implement their behaviors. Add support for combat (declaring attackers/blockers, combat damage steps) and spell abilities (e.g. enter-the-battlefield effects, simple activated abilities). Ensure the engine can handle common keywords or mechanics (flying, trample, etc.) in a basic way. Priority remains on game mechanics correctness – e.g., the stack must resolve in LIFO order, and timing restrictions must be enforced (instants vs sorcery speed).

Phase 3 – Comprehensive Rules & Advanced Mechanics: Tackle the more complex aspects of MTG rules. This includes continuous effects and the layer system, replacement and prevention effects, triggered abilities (with an event system), and handling of corner cases from the Comprehensive Rules. The engine’s architecture should already anticipate these (tracking all game events and state changes to derive effects). This phase will also expand the card pool and abilities, aiming for broad coverage of rules so that most standard cards could be represented.

Phase 4 – AI Player and Simulations: With a solid rules engine, integrate an AI component. Provide an API for AI agents to query game state and make decisions. Initial AI might be simple (random or rule-based), then progress to more sophisticated algorithms (Monte Carlo Tree Search, reinforcement learning, etc.). The engine should support running many games in succession (headless) for training. This phase might also involve optimizing performance (e.g., simplifying game state copying for simulations).

Phase 5 – UI/Visualization Layer (Future Vision): Although not an immediate goal, the design should allow plugging in a visualization (terminal UI or GUI). By this phase, the engine could be used as a backend for a player-facing application. We might build a minimal GUI or web interface to play the game using the engine, demonstrating that the core handles all rule logic (so the UI can be relatively dumb). This phase will emphasize modularity (separating the engine from any UI concerns via a clear API).

Each phase builds upon the previous, and all rules enforced in earlier phases must remain correct as new features are added. A guiding principle is to never introduce shortcuts that violate the MTG comprehensive rules, even if it means more upfront work. For example, even in Phase 1 with limited cards, we will implement the priority pass system properly (players alternating priority and requiring two consecutive passes to resolve the stack) rather than skipping it, to avoid a refactor later.

Short-Term Deliverables: In the immediate term, the goal is to deliver a working prototype of a two-player game that enforces the turn structure and priority rules:

A command-line application where two players (initially human via text input, or scripted AI) can play a few turns of Magic with a small test deck. It should handle phases (untap, upkeep, draw, main, combat, etc.), allow playing spells (perhaps just basic creatures or a simple spell) by paying mana costs, and manage a stack for at least instant spells or simple abilities.

The prototype must enforce legality: e.g. players can only cast spells when they have priority and the game is in an appropriate phase, lands can be played only during their main phase when stack is empty (land play rules), etc. If a player tries an illegal action, the engine should prevent it.

Implement a basic priority passing mechanism. For example, if both players consecutively choose “Pass” (do nothing) while the stack is empty, the phase should advance. If a spell is on the stack and both pass, the spell resolves. This ensures the fundamental flow of Magic turns is respected.

Include a minimal set of cards to demonstrate the rules engine. For instance, one or two creature cards and one sorcery or instant. The cards can have very simple effects (a creature with no abilities, an instant that deals damage to a player or creature) so we can test the stack and resolution. The exact card details are less important than making sure the engine can support their play.

Logging or output that clearly shows the progression of the game (phase changes, actions taken, changes to life totals, etc.) to verify that rules are followed. This could be as simple as text log statements. (In future, this logging can help debug and also serve as training data for AI.)

Documentation in the repository (possibly within this CLAUDE.md or separate) describing how to run the prototype, the rules supported, and examples of a turn-by-turn playthrough.

This first deliverable is essentially a skeleton of the game: not many card types or abilities, but the skeleton must be structurally identical to a full rules game. Think of it as implementing the game’s “operating system” with one or two sample “applications” (cards). Once this skeleton is proven, new cards and mechanics can be added in subsequent milestones without rewriting core logic.

Modular Structure & Architecture:

We plan a modular architecture to manage the complexity of MTG. Key modules (and likely Python packages or directories) in the project might include:

Game State & Core Logic: This module will define classes for the overall game (Game), players (Player), and fundamental zones (Library, Hand, Battlefield, Graveyard, Stack, etc.). It will manage the turn order and phase transitions. A state machine approach will be used for the turn structure: the game can be in a certain state (phase/step and active player) and transitions to the next state according to the rules. For example, after the second main phase, move to the ending phase, etc., cycling turn by turn. A finite-state machine or explicit step logic can ensure no phase is skipped and players get priority at the correct times.

Card Definitions: We will represent cards as objects or data structures. Each card has properties (name, mana cost, type, text, etc.), possibly loaded from an external data file or defined in code. To handle card abilities/effects, we need a way to represent what happens when the card is played or when its ability is used. A straightforward approach is an object-oriented design where each card (or card class) implements its specific effects in a method. For example, a class LightningBoltCard(Card) might have a method resolve(target) that applies 3 damage to the target. However, hardcoding thousands of cards is not scalable. In the long term, we may adopt a data-driven approach: representing card abilities in a structured format (like an Abstract Syntax Tree for effects). For instance, “Lightning Bolt deals 3 damage to target creature or player” can be represented as a structured effect: [This card] as source, Deal 3 damage action, and Target: creature or player as a parameter
reddit.com
. Designing a flexible ability schema or scripting language will be important so that new cards can be added without modifying core code for each one. (It’s known that to fully support all cards, one either manually encodes each card’s effect or builds a parser for card text
reddit.com
; we may start with manual definitions for a small set, then work toward a semi-automated approach.)

Zone Management: Each zone (hand, battlefield, etc.) can be a class or simply a list within a Player or Game class. The rules for moving cards between zones (draw from library to hand, play card from hand to stack, resolve from stack to battlefield/graveyard, etc.) will be encapsulated in functions or methods. For clarity, we might create a Zone base class or use simple structures initially (e.g. player.library as a list of cards, game.stack as a list of spell objects). Abstractions will help, for example an interface to query any zone for certain cards (useful for targeting and effects).

The Stack & Actions: The stack is central to Magic’s turn structure. We will model the stack as a list (or stack data structure) of spells or abilities that have been played and not yet resolved. Each entry on the stack will likely be an object containing the effect to execute when it resolves, the source card, chosen targets, and any other needed data (like mana paid, etc.). We will implement pushing to the stack when a spell/ability is activated, and a mechanism to resolve the top object when appropriate (i.e. when both players pass priority in succession). The engine will enforce that only spells/abilities can go on the stack and that players can only add to the stack when they have priority. We will also include a special action for “Pass Priority” that players can take when they choose to do nothing
github.com
. (In the command-line interface, this might be a menu option or command like "pass".)

Priority and Turn Order: We will explicitly model priority – which player is allowed to act at a given moment. The Game state will track whose turn it is and who currently has priority. At most times, priority alternates between players whenever an action is taken. The engine will provide a function to get all legal actions for the player with priority at any given state (e.g., cast a spell, activate an ability, or pass)
github.com
. By computing legal moves, we also set the stage for AI integration (AI can choose from the same moves a human could). When both players consecutively choose Pass (and the stack is empty), the game state will advance to the next step or phase; if the stack is not empty and both pass, the top of the stack resolves. This logic enforces timing rules exactly as in paper Magic.

Event System (for Triggers & Continuous Effects): As the game evolves, we need to broadcast events (like “a creature entered the battlefield” or “a player lost life”) so that triggered abilities and continuous effects can respond. An event-driven architecture will likely be employed in later phases: parts of the code can subscribe to events or query the game state to apply continuous effects. For example, when a creature enters the battlefield, we check if any permanent has an ability “Whenever a creature enters, do X” and if so, put that ability on the stack. Similarly, continuous effects (like an anthem giving all creatures +1/+1) can be handled by evaluating a set of active effects each time the relevant part of state is used (or by modifying properties dynamically in the entity). Designing a clean way to manage these effects is crucial. We might maintain a list of ongoing effects and apply them in the correct layer order per MTG rules when determining characteristics of objects. This system is complex, so it will be built up in Phase 3 with careful reference to the Comprehensive Rules (like the layers system for continuous effects).

Data Models & Abstractions: We will define data classes (using Python’s dataclass or similar) for key concepts: Card, Player, Game, Mana (to represent mana pools and costs), Effect/Ability, etc. Using dataclasses can make the code cleaner (auto-generating init, etc.) and help with equality checks (which might be useful for game state comparison or undo). We will also likely need enumerations or constants for things like card types, phases, step names, colors of mana, etc., to avoid using string literals everywhere. This adds clarity and reduces bugs.

Modularity and Extensibility: Given the vastness of MTG’s card pool, the engine should be built to allow adding new cards and mechanics without monolithic changes. We will strive to separate the rules logic (which rarely changes, aside from new mechanics) from the card definitions (which constantly expand). One possible architectural choice is a plugin system for cards: for example, have a directory or module where each new card or set can be added as a class or script that registers itself with the engine. This way, contributors can add new cards by writing new modules, with the core engine unchanged. (This approach is used in projects like XMage, which has a plugin-based architecture for cards
delftswa.gitbooks.io
.) In Python, this could be achieved by having the engine dynamically load card classes from a “cards” package, or by reading card data from files. We’ll weigh whether a data-driven approach (reading card abilities from JSON/YAML) or a code-driven approach (subclassing a Card class for each card) is better initially – likely we start code-driven for flexibility, then move to data-driven once patterns emerge.

Best Practices & Code Organization: The project will follow Python best practices: clear naming conventions (maybe CamelCase for classes, snake_case for functions/variables), type hinting for clarity, and unit tests for critical pieces (especially the rules enforcement logic). We plan to organize the repository with a logical structure:

A top-level package (e.g., mtgengine or mtg_sim) containing submodules like core (game state, rules), cards (card definitions/data), ai (AI players, when added), and possibly ui (if/when a interface is added).

A command-line entry point script (e.g., main.py or using a console script entrypoint in pyproject.toml) that sets up a game, loads decks, and runs the game loop.

The /docs folder will continue to hold reference materials (the MTG Comprehensive Rules text, design notes like this CLAUDE.md, etc.). We might also add documentation in Markdown or Sphinx format to explain how the engine works and how to contribute cards or AI modules.

Use of version control and issue tracking to manage the scope (e.g., treat each new rule or card implemented as an issue/feature to tackle).

Testing: It’s vital to test such a complex engine. We will include a test suite (perhaps using pytest) to verify rules. For example, tests for simple scenarios: casting a spell and seeing it resolve properly, combat damage calculations, edge cases (like what happens if a creature with 0 toughness enters, etc.). Writing tests also forces clarity in the API (we should be able to set up a game state and step through it in tests easily).

Architecture Recommendations: We strongly recommend an approach that is state-driven and event-driven:

Use a Finite State Machine (FSM) for handling turn phases and steps. Each phase (Beginning, Main1, Combat phases, Main2, End) can be a state with defined transitions. This makes the turn sequence explicit and helps ensure the priority sequence is correctly implemented at each step. We can implement the FSM either through a library or via a simple loop/switch in code that advances the phase state.

Implement an event system for game actions. Magic is effectively an event-based game (spells cast, damage dealt, objects changing zones all can cause other effects). By modeling this with events (even just by calling handler functions in response to state changes), we make it easier to add triggered abilities and replacement effects later. For instance, when a spell is cast, fire an event “spell_cast” with details; when a creature dies, fire “creature_died”, etc. In Phase 1 these events might not have any listeners, but building the mechanism early means Phase 3 (triggers) will plug into a prepared system.

Consider an Entity-Component-System (ECS) approach for flexibility. In an ECS, game entities (cards, players, etc.) are composed of components that provide data or behavior. For example, a creature card might have components like CreatureType, Power/Toughness, Abilities, etc. This can make it easier to add new abilities by just adding new components or systems that process components. However, ECS can add complexity and might be overkill in Python. We will evaluate if a lighter OOP approach suffices. Possibly, a hybrid: core game flow is procedural/OOP, but use composition for card abilities (each ability could be an object or component attached to a card).

Track Full Game State: From day one, the engine will maintain a comprehensive representation of game state and history. Every action taken (cast spell, draw card, combat damage event) should be recorded or at least be derivable from the game state. This is important for two reasons: (1) some cards’ effects depend on past actions (e.g., Storm count cares about how many spells were cast in the turn; a card might ask “how many creatures died this turn?” etc.), so having a log of events or a way to compute these from state is crucial
reddit.com
. (2) It enables implementing undo or rollback if we ever need to (especially useful for AI simulations or testing, where you might explore alternate game branches). A holistic game state approach, rather than minimal state, ensures we don’t paint ourselves into a corner when a new card demands some piece of information. Modern advice for MTG engines is to track everything and derive specific counts as needed (even if not immediately needed)
reddit.com
 – this avoids having to refactor state tracking when a new mechanic arrives.

Layered Rule Enforcement: Magic’s rules have many layers (both in terms of the comprehensive rules and continuous effects layers). Our engine design should layer complexity in implementation. Basic rule enforcement (turn order, priority, mana payment) at the lowest layer; on top of that, build combat rules; on top of that, state-based actions and continuous effects. By separating concerns, we can ensure that, for example, state-based actions (like a creature with 0 toughness dying, or a player losing if their life <= 0) are checked at the correct times. A possible design is to have a function check_state_based_actions(game_state) that is called whenever appropriate (e.g., after any spell/ability resolves, or at certain points in phases) to handle these automatically. Continuous effects can be handled by computing a “modified state” when needed (like when calculating a creature’s power, apply all effects in the proper layer order).

Documentation & Rule Mapping: Because the MTG Comprehensive Rules are our spec, we will maintain documentation mapping which sections of the rules have been implemented or need special handling. For instance, note which rule covers priority (e.g., rule 117 in comprehensive rules) and ensure our code covers those cases. This helps in coverage and in onboarding new contributors who can see, e.g., “rule 508 (combat damage assignment) is implemented in CombatPhase.handle_damage()”.

In summary, the architecture is designed to be robust, extensible, and clear. By Phase 1’s completion, we should have a well-structured codebase that can grow in complexity without requiring fundamental redesign. The engine will treat the rules as first-class requirements – where possible, we directly reflect rule definitions in code structure. For example, since the rules define steps and priority passing, our code will have corresponding structures (classes or states) for those. By adhering closely to MTG’s rules from the start, we ensure the simulation’s integrity and reduce technical debt when expanding features (it’s much harder to add proper priority later if you started without it). The outcome will be a Pythonic yet faithful realization of MTG’s engine, suitable for both playing and experimenting (AI or otherwise) with the greatest strategic depth Magic has to offer.

Development Plan with Milestones and Technical Guidance

To build this MTG simulation engine, we will follow a milestone-driven development plan. Each milestone corresponds to a set of features (aligned with the phases in the CLAUDE.md vision) and is broken down into actionable tasks. The plan also provides technical guidance for implementation, including suggested abstractions, data models, and any pertinent libraries or tools. We assume an Agile-like iterative approach – each milestone results in a usable (if partial) product that can be tested and validated before moving on.

Milestone 1: Initial Engine Foundation – Basic turn structure, priority, and simple actions

Objective: Implement the minimal core of the game engine that can play through turns with two players, enforcing phases and priority. This milestone delivers a command-line prototype where two players can play land cards and maybe a simple spell, with the engine handling turn progression correctly.

Key Tasks:

Project Setup: Initialize the Python project using uv. Run uv init to create a new project scaffold (pyproject.toml, etc.), and organize the repository structure. Create a base package (e.g., mtgengine/) with submodules for core game logic. Include the Comprehensive Rules text in /docs for reference.

Rule Parsing (Initial Reference): (Note: This is not about parsing card text yet, but understanding the rules.) As a development exercise, parse the turn structure and phase order from the comprehensive rules. This can be done manually by reading the rules or by writing a small script to extract the list of phases/steps from the rules text in /docs. The goal is to produce an authoritative list of phases and the order in which priority is given. Hard-code this sequence into the engine (e.g., an enum for Phase and maybe a data structure for turn order).

Game State Model: Design the primary classes: Game, Player, and Card (base class).

Game will hold the overall state: which turn it is, current phase/step, stack, players, etc. It will also have methods like start_game() (to initialize the game and maybe perform opening steps like draw initial hands), and advance_phase() or next_phase() to move the state machine.

Player will contain player-specific info: library (deck), hand, graveyard, life total, available mana, etc., and methods for actions a player can take (draw a card, play a card from hand, etc.). It should also track whether the player has priority at a given time and whether they have taken certain actions (like land played this turn).

Card will represent a card in abstract. For now, it might simply hold properties (name, type, mana_cost, etc.). We might subclass Card into specific types later (CreatureCard, SpellCard etc.), but at this stage we can start with one class and a field for type.

Use Python dataclass for these to simplify initialization and readability. Define str or similar for debugging output of game state.

Zones Implementation: Create data structures for zones:

For each Player: a list for library (perhaps shuffle it on game start), a list for hand, a list for graveyard, a list for exile (we may not need exile in M1, but include for completeness), and a list for battlefield (permanents in play). Also a counter for how many lands played this turn, etc.

For the Game: a stack (could be a list) for spells/abilities on the stack. Possibly also a pointer/reference to the active stack object being resolved (if any).

Implement basic operations: draw (move top card from library to hand), play card (move card from hand to stack or battlefield depending on type, after paying costs), resolve card (move from stack to battlefield or graveyard as appropriate). Initially, focus on land and simple spells: e.g., land goes from hand to battlefield (no cost), spell goes from hand to stack then to graveyard on resolution.

Enforce zone size rules (e.g., library becomes empty -> that player loses, though that can be a later state-based check).

Priority System & Turn Loop: Implement the turn cycle as a loop or state machine:

Represent phases: perhaps as an enum or set of constants (BEGIN_STEP, UPKEEP, DRAW, MAIN1, COMBAT_BEGIN, declare_attackers, etc., MAIN2, END). We might not implement every step in detail in M1 (combat steps can be stubbed or simplified if no combat yet), but structure should allow them.

Write a function or loop in Game.start_game() or Game.run() that controls the flow:

Beginning of turn: untap, upkeep, draw (for active player).

Main phase: give priority to active player first.

During any phase where players can act, loop: determine the player with priority. Present them with possible actions (casting a spell, playing land, or passing). You might implement a simple CLI input to choose an action.

If player acts (casts a spell), put it on stack, subtract mana (for now, you could simplify mana as always available if lands not implemented yet, or implement a basic land/mana system where lands in play can be tapped for mana).

Switch priority to the other player after an action is taken (priority passes after a spell/ability is added to stack).

If an action was taken, allow the other player a chance to respond (their turn in the loop with priority).

If both players consecutively choose “Pass”, then:

If the stack is not empty: pop the top of stack and resolve it (apply its effect). After resolution, check state-based effects (if any) and then return to priority sequence with the active player (who gets priority again in that same phase).

If the stack is empty: the phase/step ends. Move to the next phase, and give priority to the appropriate player for that phase (usually active player on main phases, etc.).

Continue until the End phase of the turn, then switch active player and go to next turn.

End conditions: check if a player has lost (life <= 0, or tried to draw from empty library). In M1, implement a basic life check (someone hits 0 or less life = game over) for win condition.

The above logic is complex, but we can simplify in M1 by having very limited actions: essentially, the only actions might be “play a land, if not yet played one this turn”, “cast a sorcery (only in main phase when stack empty) if you have mana”, or “pass”. With just those, the priority loop is easier to test. We will expand this loop as more actions become possible.

Use this opportunity to ensure that the structure aligns with rules: e.g., you must give priority after a spell is cast, even if in practice our test might have no instants to cast in response. Hard-code priority passing logic now.

Mana and Costs: Introduce a simple mana system:

In M1, it might be enough to allow playing a land card that produces one mana, and an example spell that costs one mana of that type.

Implement a ManaPool for each player (could be just an integer or a dict of color -> amount). When lands are tapped, add mana to the pool; when casting a spell, deduct mana from pool equal to cost. For simplicity, you could skip implementing different colors in M1 and just use generic mana or one color to ensure the mechanic works. The structure, however, should allow multiple colors (e.g., define a Mana class or use collections.Counter for mana).

Ensure that when casting a spell, the player has enough mana in their pool and has the right timing (e.g., sorcery only on their main phase when stack is empty, which you’ll enforce by only listing it as legal move at those times).

Input/Output Mechanics: Implement a basic CLI for the game:

While the core engine should be UI-agnostic, for testing and demonstration we need a way to play. You can put a simple loop in main.py that prints the game state (whose turn, current phase, life totals, cards in hand, etc.) and then asks the active player for an action. Since initially it’s two real players via CLI, alternate prompting Player 1 and Player 2.

Example: Game.get_legal_actions(player) returns a list of actions (could be represented as strings or small Action objects). These might include "Play [CardName] from hand", "Pass", etc. Print these options with numbers and let the user type a choice. Then call the appropriate engine method to execute that choice (game.play_card(card) or game.pass_priority() etc.).

Manage the flow so that it’s clear when one turn ends and another begins (print a separator or summary at end of turn).

Testing Milestone 1: Before concluding this milestone, test the prototype thoroughly with a couple of scripted scenarios:

For example, simulate a simple turn where Player 1 plays a land, then perhaps another land next turn (ensuring the one-land-per-turn rule), or Player 1 casts a dummy spell dealing damage to Player 2 and verify life is reduced and the spell goes to graveyard. Since we have minimal variety, these tests ensure the skeleton works.

Write unit tests for critical functions: e.g., Game.advance_phase() (does it correctly go Beginning->Main1->Combat, etc.), Game.add_to_stack() and Game.resolve_top_of_stack().

Ensure that illegal actions are prevented: e.g., if player tries to cast a spell without enough mana or at an illegal time, the action should not appear in legal actions or should be rejected with an error message.

Technical Guidance (Milestone 1):

Aim for clarity over completeness. Hardcode things like phase order and even card behaviors if needed, but do so in a way that can be extended (e.g., a dictionary or list for phases that we can add to).

Use a simple design for the priority loop first. It’s okay if it’s a series of if/else or a while True loop that breaks when the game ends. In later refactors, we might encapsulate it differently, but early on, make it work correctly.

Leverage Python’s features: e.g., use Enum for phase names for readability, use @dataclass for Card/Player, and perhaps use NamedTuple or simple classes for actions if that helps.

No external library is strictly needed in M1, aside from uv for setup. The logic can all be plain Python. If you want to use a finite state machine library like transitions for phase management, you can, but given the simplicity of our phase progression, it might be overkill. Similarly, an event library isn’t needed yet; we can just call functions directly for triggers when we implement them later.

Keep the Comprehensive Rules handy to double-check details (like what exactly happens in beginning phase or how priority passes). Since our rule enforcement must be accurate, it’s worth verifying our logic against the official rules. For example, confirm that both players get priority in each phase except the untap and cleanup, etc., to not miss something.

Folder structure at M1: Perhaps:

mtgengine/core.py (or multiple files like game.py, player.py, card.py splitting classes) containing the main classes and logic.

mtgengine/cards.py could list the test cards (e.g., define classes or data for the sample cards like a simple creature or spell).

mtgengine/__init__.py to make it a package.

main.py at project root (or a tiny wrapper in mtgengine/__main__.py to allow python -m mtgengine usage). This will run a sample game.

tests/ directory for test cases.

Documentation: update CLAUDE.md if needed to reflect any deviations, and maybe add a README.md summarizing the project and how to run it (the user instructions for the prototype).

Milestone 1 Deliverable: Basic playable CLI Magic game with extremely limited cards but full turn and priority rules. The maintainers should verify that the turn sequence and priority passing align with MTG rules before proceeding.

Milestone 2: Expanded Gameplay Features – More card types, combat, and rule coverage

Objective: Build upon the core by introducing additional gameplay elements: creature combat, a wider range of card types (creature, instant), and basic abilities. This milestone will transform the engine from a skeleton into a more feature-complete game, albeit with a limited card pool. We’ll also improve the abstractions for cards and effects to handle a variety of outcomes.

Key Tasks:

Implement Creature Cards and Combat:

Define a Creature subclass of Card or include creature-specific fields in the Card class (like power, toughness, abilities, summoning_sickness flag, etc.).

Update the gameplay loop to incorporate the Combat Phase steps properly: Beginning of Combat, Declare Attackers, Declare Blockers, Combat Damage, End of Combat.

Allow the active player (attacker) to declare attackers in their Combat phase. This means presenting a choice of which creatures (from their battlefield) will attack and whom (if there are multiple opponents or planeswalkers, but for 1v1 it’s always the other player). Since combining all attackers at once can be complex, consider simplifying by letting the player choose attackers one by one or as a set. You can generate all legal combinations of attackers, as one open-source project did
github.com
, but for now a simpler approach: let player choose each creature to attack with in turn (or choose “no more attackers” when done).

Then, for the defending player, prompt to declare blockers. For each attacking creature, the defender can assign one of their creatures to block (or none). If multiple blockers per attacker are allowed, implement that (Magic allows any number of blockers to gang-block one attacker). This may require choosing sets of blockers – you can simplify initial implementation by limiting to one blocker per attacker to get the system running, then expand later.

Compute combat damage: Each attacking creature that isn’t blocked deals damage to the defending player; blocked creatures deal damage to the blockers and vice versa. Use the power/toughness stats. Include the concept of lethal damage (if damage >= toughness, creature dies). Mark creatures as destroyed and move them to graveyard after damage (this can be done via a state-based action check right after combat damage step).

Include combat-related abilities if possible: e.g., basic keywords like First Strike (means you need to split damage step into first-strike and normal), but that could be deferred. Trample, etc., can be later. Initially, handle straightforward combat.

Ensure summoning sickness rule: creatures that enter the battlefield this turn shouldn’t be allowed to attack or tap for abilities (unless they have Haste). So mark creatures with a turn-entered timestamp or flag.

Add Instant Spells and Stack Interaction:

Introduce an Instant card type and allow instants to be cast at appropriate times (any time a player has priority). This means during the other player’s turn or during combat, etc. The engine’s priority system from M1 should already allow it, but now we must actually have a card to test it.

Example: Add a simple instant like “Shock” (deal 2 damage to target creature or player). This involves selecting a target when casting. Thus, extend the action model to support targeting: when a player chooses to cast Shock, the engine should ask which target (list legal targets: e.g., any creature on battlefield or the opponent player). Implement a way to carry this choice – perhaps the action can be a compound structure like (“cast Shock”, target=X). You might implement this by having the cast_spell(card, target=None) method accept a target parameter, or by having a separate step in the input: choose the spell, then if it requires target, list targets.

Update the Stack resolution to handle spells with targets and effects: when resolving Shock on the stack, it should apply 2 damage to the chosen target (subtract life or creature’s toughness accordingly). If a creature’s toughness falls to 0 or below, mark it for death (state-based action to destroy it).

Test stack interactions: e.g., Player A casts a creature on main phase, Player B responds with Shock targeting that creature on the stack (meaning the creature isn’t in play yet, but if Shock says any target, maybe target player instead in this case). Or an instant war like Shock vs a larger instant. This ensures that the stack LIFO order is working: the last cast instant resolves first
github.com
.

Enrich Card and Effect Representation:

At this stage, our card implementation might become more complex. We should think about a cleaner way to represent card abilities. For each card, define its effects either in code or data. Possibilities:

Use a class hierarchy: e.g., class Shock(Card): def resolve(self, target): target.take_damage(2).

Or use a data-driven approach: define a dictionary or JSON for the card that includes something like {"effect": {"type": "damage", "amount": 2, "target": "creature_or_player"}}. Then have a generic function to execute effects from such data. This is an early form of creating that “AST” of card text
reddit.com
.

Another approach is to encode effects as a sequence of functions or lambdas. For now, perhaps go with the simplest: code methods per card, since we only have a few cards. But keep in mind the structure should allow scaling. Maybe define a base SpellCard class that takes a function or something representing its on-resolve effect.

Include ability to handle continuous effects in a rudimentary way. For example, if we add a “Glorious Anthem” card (“Creatures you control get +1/+1”), we would need a way to continuously modify stats. This might be too early, but plan for it by designing how you might apply such effects (perhaps maintain a list of active effects in game state).

Implement simple activated abilities for permanents. For instance, give a creature an activated ability “{T}: Deal 1 damage to any target” (just as a test). This means representing abilities similar to instants but tied to a card on the battlefield. You can treat it like casting a spell: if a creature has an ability, if the player has priority they can activate it, pay costs (tapping the creature, maybe mana), and put an ability object on stack. The stack/resolution logic is the same. This will test that the engine can handle abilities vs spells uniformly (likely by having a common interface for “StackItem” that spells and abilities both implement).

Game State Persistence & Logging: As complexity grows, consider improving how game state is handled:

Perhaps implement a GameState snapshot mechanism (to copy the state for AI simulations or for undo, not used by players but internally). Python’s copy module or writing a custom copy method might be necessary because of the interconnected objects. Mark this as an area for future optimization.

Add more detailed logging of events: it might be useful for debugging to have a log entry each time something happens (spell cast, damage dealt, life changed, phase change). Ensure this can be toggled or is not too verbose by default.

Include some detection for draws or stalemates (though unlikely in our limited scenario, but if both players somehow do nothing, how to end?). In Magic, a game can draw if both lose simultaneously or through certain card effects – not a priority now, but keep in mind.

Testing Milestone 2: Create tests and example scenarios:

Combat test: e.g., Player A with a 3/3 creature attacks, Player B blocks with a 2/2, ensure B’s creature dies and A’s survives with 1 damage marked (and gets cleared after turn). Test multi-blockers if implemented.

Instant timing test: e.g., Player A casts a 2/2 creature, Player B responds with Shock to deal 2 damage to that creature before it resolves (actually, a creature spell isn’t on battlefield yet, so B can’t target it unless the spell specifically says target spell or something – better scenario: Player A casts a creature, it resolves and is on battlefield, then B on their turn tries to Shock it). Ensure correct results.

Land and mana test: attempt to cast a spell without enough mana to ensure it’s forbidden. Ensure land play is only once per turn.

General sanity: simulate a couple of full turns with mixed actions to see no rule is violated (no second land drop, no casting sorcery on opponent’s turn, etc.).

Technical Guidance (Milestone 2):

Refine Structure: As new features are added, consider splitting code into more modules for clarity. E.g., phases.py to handle phase logic or constants, combat.py for combat resolutions, actions.py to define Action classes or logic for casting/activating, etc. A clean separation might be to keep the Game class high-level and delegate specifics (like a CombatPhaseHandler class).

Leverage Patterns: The event-driven approach becomes more useful now. Implement a simple publish/subscribe mechanism: e.g., within Game, have a method trigger_event(event_type, data) that when called will look for any listeners (perhaps certain card abilities or global checks). For now, you can manually call the effects (like after damage is dealt, manually check if any creature has a “dies” trigger), but as triggers grow, a generic system is beneficial.

No heavy new dependencies: You can continue using just Python. If you need a parsing library for any reason (maybe to parse card text or more complex effect logic), you might use lark or parsimonious, but it’s probably not necessary yet since we’re mostly hardcoding abilities. Keep it simple.

Data for Cards: It might be a good time to think about loading card definitions from a file. For example, maintain a JSON file for the test cards (with fields for name, type, power, toughness, mana_cost, etc., and maybe a simplified representation of effect). You can then write a small loader that creates Card objects from this. This will make adding new cards easier (especially if multiple people contribute, they can just edit the JSON). It also sets the stage for possibly one day using a database of real cards.

AI Stubs: Though AI is planned for later, you can start adding hooks to make AI integration easier. For instance, define the interface of a Player’s decision-making: currently it’s human via input, but you could allow plugging in a strategy function or class that picks from get_legal_actions. Maybe implement a trivial AI that always passes or random legal move, just to test the engine doesn’t require human input (useful for automated tests). This will be expanded in Milestone 4.

Folder conventions: By now, likely structure could be:

mtgengine/ with submodules:

core/ (maybe game.py, player.py, stack.py, zones.py inside),

cards/ (if using code classes, have one file per card type or per group; if using data, have data files and maybe a cards/card_library.py to load them),

logic/ or mechanics/ (for combat, actions, effects),

ai/ (possibly empty or basic AI classes).

Keep tests organized similarly (maybe mirror structure under tests/).

Use naming that makes sense to contributors. Add docstrings to key classes and methods now, since things are getting complex.

The codebase at this point should be able to handle the majority of core gameplay scenarios for basic cards. It might not yet support things like complex stack interactions (counterspells, etc.), but it should enforce rules correctly for what it does support. We should refrain from adding “placeholder” shortcuts that break rules (e.g., don’t implement direct damage to player as ignoring the stack “just to make it easier” – do it via a spell on stack). If any such simplifications were made in M1, M2 is the time to remove them if possible.

Milestone 3: Advanced Rule Coverage – Triggers, Continuous Effects, Keywords, and Comprehensive Rules Compliance

Objective: Extend the engine to cover the more intricate aspects of MTG rules, bringing it closer to a truly comprehensive engine. This includes triggered abilities (and thus an event system), continuous effects with layering, more keywords (flying, trample, etc.), stack abilities like counterspells, and state-based actions. Essentially, polish the rules enforcement to cover corner cases and most mechanics, at least in a generic sense.

Key Tasks:

Event/Trigger System: Finalize an event dispatch mechanism within the engine.

Define a set of event types (e.g., "SPELL_CAST", "CREATURE_DIED", "CREATURE_ETB" [entered the battlefield], "LIFE_GAINED", etc.).

When certain actions happen in the game logic, generate events. For example, after a spell is cast (and put on stack), you might trigger a "SPELL_CAST" event with data about the spell. When a permanent enters battlefield, trigger an "ENTERED_BATTLEFIELD" event.

Allow cards to register listeners for events. For instance, a creature card with a “When this creature enters the battlefield, do X” ability would register a listener for the "ENTERED_BATTLEFIELD" event (filtered to events where the subject is that card). When the event fires, it should create a new ability on the stack (triggered abilities themselves go on the stack).

This likely means representing triggered abilities similarly to instants: perhaps as a class TriggeredAbility that knows its effect and possibly who controlled it. When triggered, instantiate one and push to stack.

Key challenge: timing of triggers – according to rules, triggered abilities trigger immediately when the event happens, but wait to be put on stack until a player would next get priority. Our engine can simulate this by queuing triggers and then pushing them on the stack at the appropriate time (usually right after state-based actions are checked).

Start with simple triggers (like a creature with “when ETB, draw a card” or “when dies, deal damage”) to ensure system works.

Continuous Effects and Layer System: Implement a system for continuous effects:

Continuous effects are those that modify game state as long as some condition holds or within a duration (like “creatures you control get +1/+1” or “target creature gets -2/-2 until end of turn”).

We should maintain a list of active continuous effects in the Game state. Each effect would have:

a scope (what it affects: e.g., all creatures you control, or a specific object),

a modification (change to apply: e.g., +1/+1 to power/toughness, or “cannot block”),

duration (until end of turn, as long as source is on battlefield, etc.).

Many continuous effects are linked to a card or ability. E.g., an enchantment on the battlefield granting a buff creates a continuous effect as long as it’s in play; a spell like “Giant Growth” creates a temporary effect until end of turn. We need to apply these effects when relevant:

At minimum, ensure that when calculating a creature’s power/toughness, all applicable effects are summed. If multiple effects apply to the same stat, follow the layer ordering (power/toughness modifications layer).

Also handle continuous effects that grant or remove abilities (e.g., “target creature loses flying”). This implies when checking if a creature can block (flying vs non-flying), consult effects.

The comprehensive rules define layers and timestamps for effects. For now, implement a simplified version: e.g., handle effects by categories (one for changing P/T, one for color/type changes, etc.). If an effect’s timestamp matters (one effect says +1/+1, another says -1/-1 later, they both apply; if dependency conflicts, follow typical last-in rule for same layer). This is quite complex, but aim to get the structure right: maybe sort effects by an order (layer and timestamp) each time we evaluate state.

State-Based Actions (SBAs): Code a function to handle SBAs, which include things like:

A creature with 0 or less toughness is destroyed.

A player with 0 or less life loses.

If a player has attempted to draw from empty library, they lose (if that’s how we implement it).

If both players have 0 life due to some event, game is draw (rare case).

Limit of 7 cards in hand at cleanup (for discard; this may require implementing discard step).

etc.
Call this SBA check after any significant action resolves or at appropriate times in phases. The rules have a specific timing for SBAs (after any event, before triggers are put on stack).

Keywords: Implement a few evergreen keywords to test continuous effects and combat interactions: Flying (only creatures with flying or reach can block those with flying – check in block legality), Trample (excess damage to player if creature is blocked – handle in damage assignment), Vigilance (doesn’t tap to attack – just don’t tap that creature when it attacks), Deathtouch (any amount of damage is lethal – in damage resolution, if a creature with deathtouch deals damage, kill the target), Lifelink (damage causes life gain – an event when damage dealt can handle that).

These can be implemented via flags on creatures and small hooks in combat resolution or damage handling. For example, after combat damage is assigned, if attacker has lifelink and dealt 3 damage, increase attacker controller’s life by 3.

Use the event system for some: e.g., a generic event “DAMAGE_DEALT” could be emitted for lifelink or other effects to listen.

Comprehensive Rules Audit: Take the Comprehensive Rules document and identify any major rule that is not yet handled:

Mulligans (maybe out of scope unless we simulate entire game start; could implement a simple mulligan rule for completeness).

The stack interaction nuances: e.g., counterspells (allow a spell that targets another spell on stack to “counter” it, meaning remove it from stack with no effect). We should implement at least a basic counterspell card to test this. That means when resolving a counterspell, we need to find the target spell on stack and remove it (and not execute it). Make sure the engine can handle removing non-top stack items (or specify that a counterspell can only target top? Actually in Magic, you can target any spell on stack. So allow removing an item from middle of stack; the remaining above it still resolve as normal).

Exile zone: by now, implement moving cards to exile if a spell effect says so (just like another graveyard but separate).

Protection ability (e.g., “Protection from red” – might skip detailed protection rules for now as they are complex).

Copies of cards or effects (could be future).

If possible, implement the notion of stacked triggers properly and ensure priority sequence even when triggers occur.

End of turn cleanup: ensure that temporary continuous effects end when they should (you may need to mark effects with “until end of turn” and remove them in cleanup), and clear any “damage marked on creatures” at end of turn, remove summoning sickness at next upkeep, etc.

Performance Considerations: With more complex state, think about performance:

If we plan on running AI simulations later, the engine might need to create and evaluate thousands of game states. Profile the code (maybe using Python’s cProfile) on a series of random games to find slow spots. Typical culprits: copying game state (which we might do for simulation), checking all effects in a naive way, etc.

We may refactor some parts for efficiency. For example, if our continuous effects system recomputes all stats from scratch frequently, consider caching values and invalidating cache only when relevant changes occur.

However, clarity is still priority; optimize only if needed, and in obvious places (like if our event system ends up checking dozens of triggers frequently, ensure it’s not too slow).

Testing Milestone 3: This milestone is heavy on rules, so lots of tests:

Trigger tests: e.g., card “When X enters battlefield, you gain 5 life” – simulate playing it and see life increase and no other time. Also test that if two such creatures enter (or one enters under some condition), triggers stack properly.

Continuous effect tests: have an “anthem” effect (all creatures +1/+1) and verify a 2/2 becomes 3/3, and if the effect source is removed, the creature goes back to 2/2. Test an “until end of turn” buff (Giant Growth: +3/+3 EOT) is applied and then removed after cleanup.

Combat with keywords: e.g., a 1/1 deathtouch can kill a 8/8 in block, lifelink gives life, trample deals leftover damage.

Counterspell test: one player casts a spell, other counters it, ensure the first spell does not resolve. Also test if counters and triggers interplay properly (like counter a spell that had a trigger on cast, the trigger should still happen since spell was cast).

Edge cases: test multiple triggers trying to go on stack at once (e.g., two creatures with same trigger event). They should all go on stack in AP/NAP order (Active Player / Non-Active Player order if simultaneous). Implementing AP/NAP ordering might be advanced, but at least ensure all triggers appear.

State-based actions: kill a creature with 0 toughness by an effect, ensure it dies immediately (doesn’t linger until end of turn). Test lethal damage assignment leads to death, etc.

Technical Guidance (Milestone 3):

By now, consider using more formal representations for complex logic. For example, for parsing or validating card text, maybe not needed, but for verifying rules, you might rely more on the rule text. It could help to annotate code with rule references (like a comment “// 704.5: state-based actions for creature death” etc.).

If the event/trigger handling gets complicated, ensure to keep it organized. Perhaps have an EventManager class or similar to manage listeners and dispatch, instead of scattering that logic.

You might consider introducing a dependency for structured data, e.g., pydantic for card schema validation if loading from JSON, or a parsing library if writing a mini DSL for card effects. Use sparingly.

Keep user documentation updated. At this stage, one could write a README or User Guide explaining how to play the game via the CLI, listing implemented features and known limitations. Since the engine is nearing comprehensiveness, external testers might try it; documentation helps them and ensures we haven’t missed explaining any rule nuance.

Code maintenance: the codebase will be quite large now. Ensure proper separation of concerns: e.g., the code that decides legal actions should probably be in one place (maybe Game or a separate module), the code for resolving effects in another. Avoid very long functions – break them into helpers.

Potential Library Use: If managing game complexity is getting unwieldy, we might consider introducing libraries:

A finite state machine library (like transitions) could formalize phase transitions and make it easier to visualize or verify the state machine. This is optional, as our manual implementation might suffice.

If writing lots of repeated code for similar card effects, consider a rules engine or expression evaluator. For instance, a library that can take a structured expression (like a mini-language for card effects) and execute it. However, such generality might be beyond our timeline. A simpler approach: use Python’s dynamic features to our advantage (maybe store effect logic as small lambda functions or method references in card data).

No external AI library yet – we’ll likely use plain Python or simple algorithms for AI in the next milestone.

Milestone 3 Deliverable: An engine that in principle could support most real MTG cards, given definitions. We might not have all cards implemented, but the rules framework can handle complex interactions. This deliverable is likely a version 1.0 of the rules engine. It should be possible to simulate games with moderately complex cards and see correct outcomes as per MTG rules. Documentation should list which mechanics are supported. We should also ensure that adding a new card is now a matter of adding data or a small piece of code, not changing the core engine (this tests our modularity).

Milestone 4: AI Integration and Simulation at Scale – Intelligent agents and bulk simulation capabilities

Objective: Leverage the completed rules engine to introduce AI players and the ability to run many games for AI training or statistical analysis. Ensure the engine can be used as a backend for non-interactive play (no CLI prompts, but driven by AI or scripts). Also consider any optimizations or adjustments needed for the AI use-case.

Key Tasks:

AI Player Interface: Define an interface for an AI agent to interact with the game. For example, create an abstract base class AIPlayer with a method like choose_action(game_state, legal_actions) that returns one of the provided actions. The Player class (or the game loop) should be able to hand over decision-making to an AI implementation if the player is flagged as AI.

Implement a couple of simple AI agents:

RandomAI (chooses a random legal action, useful baseline and for testing).

Perhaps a HeuristicAI (favors attacking if possible, or casting spells at first chance, just a simple hardcoded logic).

These will help test that the game can run without user input and without pausing.

The AI should be able to run the game loop to completion on its own. E.g., simulate 100 games between two RandomAIs to see if engine remains stable.

Self-Play Simulation Tools: Develop scripts or functions to run many games in succession, possibly in parallel.

For example, an entry point or script simulate.py where one can specify two AI agents and number of games, and it will loop and maybe collect statistics (like how many wins for each).

Ensure that game state is properly reset between games and no memory leaks occur (game objects from finished games should be garbage-collected).

If performance is an issue in many simulations, consider using multiprocessing or threading. However, Python GIL might limit multi-threading, so multi-process via the multiprocessing module or using an async approach could be considered if needed. This might not be critical unless aiming for thousands of games quickly.

Reinforcement Learning Integration (optional): If the goal includes training an AI via reinforcement learning, set up hooks for that:

Provide a way for an external RL algorithm to interface. Possibly define the game in OpenAI Gym environment style (i.e., a reset() and step(action) function for the game environment). This could allow using existing libraries (like Stable Baselines or custom training loops) to train an AI.

Ensure the game state can be encoded in a learning-friendly format (maybe a vector or a set of features) – this is a big task and likely beyond scope for now, but planning the interface is helpful.

Alternatively, support saving game logs of self-play in a format that can be analyzed to derive strategies.

Optimization and Profiling: Running AIs will stress test the engine. Profile in scenarios of many games:

Identify bottlenecks. If, say, the event system or continuous effect evaluation is slow, consider optimizing (perhaps by simplifying some checks or using more efficient data structures).

If copying state for lookahead is too slow, consider implementing a more efficient game state clone (maybe using __slots__ or other tricks to reduce overhead, or writing a C extension if absolutely needed for critical parts).

However, since Python will be inherently limited for huge simulations, it might be acceptable if we manage say tens of games per second. If needed, some computationally heavy parts (like determining legal moves in very complex states) could be optimized or cached.

AI Evaluation and Improvement: After initial AI integration, we might attempt a simple experiment:

e.g., use Monte Carlo Tree Search (MCTS) with the engine. Write an MCTS that can use the engine to simulate random playouts (hence the importance of fast game copy or reset). See if it can improve decision-making beyond Random.

Or train a model (even a very basic one) to play, though that might be long-term.

These are optional but help validate that the engine works for AI usage.

Testing Milestone 4:

Run automated self-play games and assert no crashes or inconsistent states. For instance, do 10 random games and ensure each ends with one winner or a draw, and no rule violations occurred (we might not have an easy way to detect rule violations except the engine internally preventing them).

Test AI decisions: ensure that AI never tries an illegal action (shouldn’t if we only feed legal actions). If we create a scenario where one action clearly leads to winning (like an AI can deal lethal damage vs pass), test that a non-random AI takes it (if using heuristics).

Memory test: run a large number of games in a loop and monitor memory usage to ensure we don’t have a major leak (some leftover global state or un-freed references).

Technical Guidance (Milestone 4):

Integrating AI might require slight refactoring of the game loop. Ideally, we separate the engine from the input method. The engine should expose a function like game.get_legal_actions() and game.take_action(action) which updates the game state. Then a higher-level loop can call these for either a human or AI. This way, the AI can operate by just calling these functions without any need for input prompts or text parsing.

Consider representing actions in a machine-friendly way (not just as text). Perhaps define an Action class or namedtuple for actions with fields like type (play, attack, pass, etc.), card (if any), targets (if any). This will be easier for an AI to handle than parsing strings. You can still map these to user-friendly descriptions for CLI, but internally use objects.

Use seeds for randomness (shuffling, random AI) to allow reproducibility in tests and training.

As we might incorporate reinforcement learning, keep the dependencies minimal but you may introduce some if needed for convenience: e.g., numpy for vectorized computations (if encoding state or doing many random sims), or an RL library for environment handling. These are more acceptable now that core engine is done, but ensure they don’t interfere with core logic.

Maintain clear separation: The AI code (policies, training loops, etc.) should reside perhaps in mtgengine/ai/ subpackage or outside the engine package, using the engine via its public API. This keeps the engine generic and avoids accidental bias or cheat (AI reading internal state it shouldn’t, etc.).

Update documentation to include how to use the AI: for example, instructions to run a sample AI-vs-AI game, or how to plug in a custom AI. Possibly provide an example of a very basic ML agent or how one would gather data from the engine.

With this milestone complete, the project is ready for either research use (AI experiments) or further extension (maybe adding thousands of cards, or a UI). Prioritize ensuring the engine is stable and correct, as a wrong rule can mislead an AI training on it. It might be wise to publish a set of regression tests that cover known tricky interactions so that any future changes (or performance tweaks) do not break core functionality.

Milestone 5: UI/UX and Extended Usability – Optional/Future: Visual interface and large-scale card integration

(This milestone is more forward-looking and may not be fully executed within the initial development cycle. It outlines how the project could expand beyond the core engine.)

Objective: Create a user-friendly layer on top of the engine and integrate a broad set of real MTG cards, turning the engine from a developer tool into an application or service that end-users (or a wider community) could engage with.

Key Ideas:

Visualization/UI: Develop a simple graphical interface or web interface for the game. This could be a desktop app (using a library like pygame or PyQt) or a web app (using a framework like Flask/Django for a web server and JS for client, or a terminal-based GUI with rich text).

A minimal approach is to use a library like rich or blessed to make a nicer text UI (colored text, card symbols, etc.). This keeps things simple but more pleasant.

A full approach might involve showing a window with zones, cards (text or images), etc. Given the complexity, maybe reuse existing card image resources or just use text.

The key is that this UI layer should use the engine’s public API and not contain game logic. It just reflects state and sends player inputs to the engine.

Large Card Pool & Data Integration: Expand the card database:

Incorporate a source of real card data, such as MTG JSON or Wizards’ data. Perhaps use an existing dataset (MTG JSON provides structured data for all cards). This could greatly accelerate adding cards: we’d parse the dataset and for each card, see if our engine supports its mechanics, then either automatically add it if simple or mark it as unsupported if it has unique mechanics.

Possibly write a parser for card text to our internal effect format. This is a monumental task (as discussed earlier, translating English text to code or AST is complex
reddit.com
). We might limit scope by focusing on a specific set (like implement all cards of a core set manually to prove coverage).

Alternatively, allow community contributions where adding a card is as easy as writing a small Python class or JSON entry.

Ensure the engine can handle the volume of cards (perhaps lazily load card definitions when needed, etc., to not slow startup).

Networking/Multiplayer: If there's interest, consider making the engine playable over a network (client-server model). This would require separating the engine (server side) from a client UI and synchronizing state. This is how XMage works (server enforcing rules, clients send actions). Implementing this would involve serialization of game actions and states, and careful security to not allow cheating. Likely out of initial scope, but possible future direction for a community-driven platform.

Continuous Testing and QA: With many cards and possibly users, set up CI for running the test suite on each change, and maybe incorporate some form of property-based testing or fuzzing (random games) to catch regressions. The comprehensive nature of the engine makes it critical to have automated checks for rule correctness.

Technical Guidance (Milestone 5 and beyond):

For UI, choosing a technology is key. A quick win is text UI (since we already have CLI). For a graphical UI, web might be easier to reach many users (one could even run the engine server-side and have a JS client). Python’s async features could help if building a server.

For card data, if using MTG JSON, use requests or include a snapshot of the JSON. Write a parser that maps fields to our Card class. We still need a way to handle the rules text; perhaps start by mapping keywords (e.g., if card has “Flying” in text, set flying flag; parse numeric effects like “draw 2 cards” as effect type draw with quantity 2, etc.). This could cover a subset of simple cards automatically. Complex cards would need hand-written logic.

Possibly develop a scripting DSL for card abilities as part of the engine. For instance, a mini-language or configuration that can express common effects (damage, heal, draw, modify stat, etc.) and conditional logic (“if X, then Y”). This could then be used to encode many card texts without writing Python for each. It’s an ambitious but valuable tool if the project grows.

Keep dependency philosophy: we might allow more dependencies in a UI layer (for example, Flask or PyQt), but the core engine should remain lightweight and isolated.

Community and Contribution: As the project grows, encourage contributions by documenting how to add new cards or mechanics. Perhaps set up a template or guide, e.g., “to add a new card, do X”. If plugin architecture is in use, ensure it’s easy to register new plugins.

Monitor performance with the expanded scope. If thousands of cards loaded, ensure initialization is not too slow (maybe load on demand). If games with complex interactions are slow, consider optimizations or even transpiling critical parts to faster languages (Cython, Rust via FFI, etc.), but only if necessary.

Remain vigilant that all new features respect the core mission: simulate full MTG rules accurately. It can be tempting to cut corners for an obscure mechanic, but those corners often affect gameplay. The comprehensive rules text should remain our ultimate test – we can periodically pick random rules from it and ask “does the engine handle this?” and if not, decide if it must (some rules are about multiplayer or formats, which might not apply if we focus on 1v1).

Deliverable for Milestone 5: This would result in a more user-friendly MTG simulator, possibly akin to a minimal clone of Magic Arena (minus the fancy graphics). Achieving all of M5 is a huge effort, but each sub-goal can be taken one at a time. By the end, the project would have not just an engine but an application or at least a service (AI training platform, etc.). This is beyond the initial deliverables, but outlines a path for the project to continue growing.

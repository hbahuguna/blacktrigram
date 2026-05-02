{
  "file_path": "tests/unit/combat/test_combat_screen_input.py",
  "code": "import pytest
from unittest.mock import Mock

# --- Mocking the GameState and handleCombatInput function ---
# This section simulates the behavior of the TypeScript function and its dependencies
# in a Python environment for testing purposes.

class MockGameState:
    \"\"\"
    A mock game state object to simulate the state managed by CombatScreen3D.
    \"\"\"
    def __init__(self):
        self.is_combat_active = False
        self.is_menu_open = False
        self.player_position = {'x': 0, 'y': 0, 'z': 0}
        self.player_stamina = 100
        self.last_action_performed = None
        self.menu_toggle_calls = 0
        self.action_perform_calls = 0
        self.move_player_calls = 0

    def toggle_menu(self):
        self.is_menu_open = not self.is_menu_open
        self.menu_toggle_calls += 1

    def perform_action(self):
        \"\"\" Simulates performing a combat action. \"\"\"
        if self.is_combat_active and not self.is_menu_open and self.player_stamina >= 10:
            self.last_action_performed = \"attack\"
            self.player_stamina -= 10
            self.action_perform_calls += 1
            return True
        return False

    def move_player(self, direction):
        \"\"\" Simulates player movement. \"\"\"
        if self.is_combat_active and not self.is_menu_open:
            if direction == 'forward':
                self.player_position['z'] += 1
            elif direction == 'backward':
                self.player_position['z'] -= 1
            elif direction == 'left':
                self.player_position['x'] -= 1
            elif direction == 'right':
                self.player_position['x'] += 1
            self.last_action_performed = f\"move_{direction}\"
            self.move_player_calls += 1
            return True
        return False

# This function is a Python representation of the target TypeScript function `handleCombatInput`.
# It processes a mock keyboard event and updates the mock game state.
def handle_combat_input(event: dict, game_state: MockGameState) -> bool:
    \"\"\"
    Simulates the handleCombatInput function, processing keyboard input
    and updating the game state based on combat and menu constraints.
    Returns True if the input was handled, False otherwise.
    \"\"\"
    key = event.get('key')

    # Always allow menu toggle
    if key == 'Escape':
        game_state.toggle_menu()
        return True

    # If menu is open, no other inputs should be processed
    if game_state.is_menu_open:
        return False

    # If combat is not active, no combat-related inputs should be processed
    if not game_state.is_combat_active:
        return False

    # Handle combat actions and movement
    if key == 'w':
        return game_state.move_player('forward')
    elif key == 's':
        return game_state.move_player('backward')
    elif key == 'a':
        return game_state.move_player('left')
    elif key == 'd':
        return game_state.move_player('right')
    elif key == 'Enter':
        return game_state.perform_action()

    return False # Input not handled by this function


# --- Pytest Test Cases for handleCombatInput ---

@pytest.fixture
def game_state():
    \"\"\"Provides a fresh MockGameState for each test.\"\"\"
    return MockGameState()

@pytest.mark.parametrize(\"initial_menu_state, expected_menu_state\", [
    (False, True),
    (True, False)
])
def test_escape_key_toggles_menu_regardless_of_combat_state(game_state, initial_menu_state, expected_menu_state):
    \"\"\"
    Tests that the 'Escape' key correctly toggles the menu state,
    irrespective of whether combat is active or not.
    \"\"\"
    game_state.is_menu_open = initial_menu_state
    game_state.is_combat_active = False # Test with combat inactive
    event = {'key': 'Escape'}

    handled = handle_combat_input(event, game_state)
    assert handled is True
    assert game_state.is_menu_open == expected_menu_state
    assert game_state.menu_toggle_calls == 1

    game_state.is_menu_open = initial_menu_state # Reset for combat active
    game_state.is_combat_active = True # Test with combat active
    game_state.menu_toggle_calls = 0 # Reset call count
    handled = handle_combat_input(event, game_state)
    assert handled is True
    assert game_state.is_menu_open == expected_menu_state
    assert game_state.menu_toggle_calls == 1


@pytest.mark.parametrize(\"key, direction, initial_pos, expected_pos\", [
    ('w', 'forward', {'x': 0, 'y': 0, 'z': 0}, {'x': 0, 'y': 0, 'z': 1}),
    ('s', 'backward', {'x': 0, 'y': 0, 'z': 0}, {'x': 0, 'y': 0, 'z': -1}),
    ('a', 'left', {'x': 0, 'y': 0, 'z': 0}, {'x': -1, 'y': 0, 'z': 0}),
    ('d', 'right', {'x': 0, 'y': 0, 'z': 0}, {'x': 1, 'y': 0, 'z': 0}),
])
def test_movement_keys_move_player_when_combat_active_and_menu_closed(game_state, key, direction, initial_pos, expected_pos):
    \"\"\"
    Tests that movement keys (W, A, S, D) correctly move the player
    when combat is active and the menu is closed.
    \"\"\"
    game_state.is_combat_active = True
    game_state.is_menu_open = False
    game_state.player_position = initial_pos.copy()
    event = {'key': key}

    handled = handle_combat_input(event, game_state)
    assert handled is True
    assert game_state.player_position == expected_pos
    assert game_state.last_action_performed == f\"move_{direction}\"
    assert game_state.move_player_calls == 1


@pytest.mark.parametrize(\"key\", ['w', 's', 'a', 'd', 'Enter'])
def test_combat_inputs_ignored_when_menu_is_open(game_state, key):
    \"\"\"
    Tests that combat-related inputs (movement, action) are ignored
    when the menu is open, even if combat is active.
    \"\"\"
    game_state.is_combat_active = True
    game_state.is_menu_open = True
    initial_pos = game_state.player_position.copy()
    initial_stamina = game_state.player_stamina
    event = {'key': key}

    handled = handle_combat_input(event, game_state)
    assert handled is False
    assert game_state.player_position == initial_pos # No movement
    assert game_state.player_stamina == initial_stamina # No stamina change
    assert game_state.last_action_performed is None
    assert game_state.move_player_calls == 0
    assert game_state.action_perform_calls == 0


@pytest.mark.parametrize(\"key\", ['w', 's', 'a', 'd', 'Enter'])
def test_combat_inputs_ignored_when_combat_is_inactive(game_state, key):
    \"\"\"
    Tests that combat-related inputs are ignored when combat is inactive,
    even if the menu is closed.
    \"\"\"
    game_state.is_combat_active = False
    game_state.is_menu_open = False
    initial_pos = game_state.player_position.copy()
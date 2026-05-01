import pytest
from unittest.mock import Mock

# --- Mocking the target function and its dependencies for pytest ---
# In a real Python project, this would be an import from the actual source.
# For this exercise, we're creating a conceptual Python equivalent to test.

class MockGameState:
    """A mock game state to track changes made by handle_combat_input."""
    def __init__(self):
        self.player_stance = "neutral"
        self.menu_open = False
        self.last_action = None
        self.action_history = []

    def set_stance(self, stance: str):
        self.player_stance = stance

    def toggle_menu(self):
        self.menu_open = not self.menu_open

    def perform_action(self, action_type: str):
        self.last_action = action_type
        self.action_history.append(action_type)

def handle_combat_input(event: dict, game_state: MockGameState):
    """
    Conceptual Python equivalent of the handleCombatInput function from TSX.
    Processes keyboard input events to orchestrate player combat actions,
    stance switches, and menu toggles.
    """
    key = event.get("key")
    if not key:
        return

    if key == "a": # Example: Attack action
        game_state.perform_action("attack")
    elif key == "d": # Example: Defend action
        game_state.perform_action("defend")
    elif key == "s": # Example: Switch Stance
        if game_state.player_stance == "neutral":
            game_state.set_stance("aggressive")
        else:
            game_state.set_stance("neutral")
    elif key == "Escape" or key == "m": # Example: Toggle Menu
        game_state.toggle_menu()
    # Other keys are ignored, simulating no action

# --- Pytest tests for handle_combat_input ---

@pytest.fixture
def game_state_fixture():
    """Provides a fresh MockGameState for each test."""
    return MockGameState()

def test_handle_combat_input_attack_action(game_state_fixture):
    """Tests that pressing 'a' triggers an attack action."""
    event = {"key": "a"}
    handle_combat_input(event, game_state_fixture)
    assert game_state_fixture.last_action == "attack"
    assert "attack" in game_state_fixture.action_history

def test_handle_combat_input_defend_action(game_state_fixture):
    """Tests that pressing 'd' triggers a defend action."""
    event = {"key": "d"}
    handle_combat_input(event, game_state_fixture)
    assert game_state_fixture.last_action == "defend"
    assert "defend" in game_state_fixture.action_history

def test_handle_combat_input_stance_switch(game_state_fixture):
    """Tests that pressing 's' correctly switches player stance."""
    # Initial stance is neutral
    assert game_state_fixture.player_stance == "neutral"

    # Press 's' once: neutral -> aggressive
    event = {"key": "s"}
    handle_combat_input(event, game_state_fixture)
    assert game_state_fixture.player_stance == "aggressive"

    # Press 's' again: aggressive -> neutral
    handle_combat_input(event, game_state_fixture)
    assert game_state_fixture.player_stance == "neutral"

def test_handle_combat_input_toggle_menu_escape(game_state_fixture):
    """Tests that pressing 'Escape' toggles the menu state."""
    # Initial menu state is closed
    assert not game_state_fixture.menu_open

    # Press 'Escape' once: closed -> open
    event = {"key": "Escape"}
    handle_combat_input(event, game_state_fixture)
    assert game_state_fixture.menu_open

    # Press 'Escape' again: open -> closed
    handle_combat_input(event, game_state_fixture)
    assert not game_state_fixture.menu_open

def test_handle_combat_input_toggle_menu_m_key(game_state_fixture):
    """Tests that pressing 'm' also toggles the menu state."""
    assert not game_state_fixture.menu_open

    event = {"key": "m"}
    handle_combat_input(event, game_state_fixture)
    assert game_state_fixture.menu_open

    handle_combat_input(event, game_state_fixture)
    assert not game_state_fixture.menu_open

def test_handle_combat_input_irrelevant_key_no_action(game_state_fixture):
    """Tests that an irrelevant key press does not change game state."""
    initial_stance = game_state_fixture.player_stance
    initial_menu_state = game_state_fixture.menu_open
    initial_last_action = game_state_fixture.last_action

    event = {"key": "z"} # An arbitrary irrelevant key
    handle_combat_input(event, game_state_fixture)

    assert game_state_fixture.player_stance == initial_stance
    assert game_state_fixture.menu_open == initial_menu_state
    assert game_state_fixture.last_action == initial_last_action
    assert not game_state_fixture.action_history # No actions should have been recorded

def test_handle_combat_input_empty_event_no_error(game_state_fixture):
    """Tests that an empty event dictionary does not cause errors and no state change."""
    initial_stance = game_state_fixture.player_stance
    initial_menu_state = game_state_fixture.menu_open

    event = {}
    handle_combat_input(event, game_state_fixture)

    assert game_state_fixture.player_stance == initial_stance
    assert game_state_fixture.menu_open == initial_menu_state
    assert game_state_fixture.last_action is None
    assert not game_state_fixture.action_history

def test_handle_combat_input_event_without_key_no_error(game_state_fixture):
    """Tests that an event without a 'key' field does not cause errors and no state change."""
    initial_stance = game_state_fixture.player_stance
    initial_menu_state = game_state_fixture.menu_open

    event = {"keyCode": 65} # Example of an event with other fields but no 'key'
    handle_combat_input(event, game_state_fixture)

    assert game_state_fixture.player_stance == initial_stance
    assert game_state_fixture.menu_open == initial_menu_state
    assert game_state_fixture.last_action is None
    assert not game_state_fixture.action_history
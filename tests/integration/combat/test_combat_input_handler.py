import pytest

# Mock CombatState class to simulate game state
class MockCombatState:
    def __init__(self):
        self.stance = "neutral"
        self.is_menu_open = False
        self.current_action = None
        self.player_health = 100
        self.enemy_health = 100

    def set_stance(self, new_stance: str):
        self.stance = new_stance

    def toggle_menu(self):
        self.is_menu_open = not self.is_menu_open

    def perform_action(self, action_type: str):
        self.current_action = action_type
        if action_type == "attack":
            self.enemy_health -= 10 # Simulate damage

    def __repr__(self):
        return f"Stance: {self.stance}, Menu Open: {self.is_menu_open}, Action: {self.current_action}, Enemy Health: {self.enemy_health}"

# Mock handleCombatInput function based on the summary
def handle_combat_input(event: dict, combat_state: MockCombatState):
    """
    Simulates the handleCombatInput function from CombatScreen3D.tsx.
    Processes keyboard input events to orchestrate player combat actions,
    stance switches, and menu toggles.
    """
    key = event.get("key")
    event_type = event.get("type", "keydown") # Default to keydown

    if event_type == "keydown":
        # If menu is open, only allow menu-related inputs
        if combat_state.is_menu_open:
            if key == "Escape":
                combat_state.toggle_menu()
            # Other menu navigation keys could be handled here
            return

        # Handle combat actions and stance switches when menu is closed
        if key == "q":
            combat_state.set_stance("left_guard")
        elif key == "e":
            combat_state.set_stance("right_guard")
        elif key == " ": # Spacebar for attack
            combat_state.perform_action("attack")
        elif key == "Escape":
            combat_state.toggle_menu()
        # Add more combat actions/stances as needed
    elif event_type == "keyup":
        # Future: Handle keyup events for releasing actions, etc.
        pass


@pytest.fixture
def initial_combat_state():
    """Provides a fresh MockCombatState for each test."""
    return MockCombatState()


def test_initial_state(initial_combat_state):
    """Verifies the initial state of the combat system."""
    assert initial_combat_state.stance == "neutral"
    assert not initial_combat_state.is_menu_open
    assert initial_combat_state.current_action is None
    assert initial_combat_state.enemy_health == 100


def test_stance_switch_left_guard(initial_combat_state):
    """Tests that pressing 'q' switches to left guard stance."""
    event = {"key": "q", "type": "keydown"}
    handle_combat_input(event, initial_combat_state)
    assert initial_combat_state.stance == "left_guard"
    assert not initial_combat_state.is_menu_open


def test_stance_switch_right_guard(initial_combat_state):
    """Tests that pressing 'e' switches to right guard stance."""
    event = {"key": "e", "type": "keydown"}
    handle_combat_input(event, initial_combat_state)
    assert initial_combat_state.stance == "right_guard"
    assert not initial_combat_state.is_menu_open


def test_perform_attack_action(initial_combat_state):
    """Tests that pressing spacebar triggers an attack and reduces enemy health."""
    event = {"key": " ", "type": "keydown"}
    initial_combat_state.enemy_health = 50 # Set initial health for clear change
    handle_combat_input(event, initial_combat_state)
    assert initial_combat_state.current_action == "attack"
    assert initial_combat_state.enemy_health == 40 # 50 - 10
    assert not initial_combat_state.is_menu_open


def test_toggle_menu_open(initial_combat_state):
    """Tests that pressing 'Escape' opens the menu."""
    event = {"key": "Escape", "type": "keydown"}
    handle_combat_input(event, initial_combat_state)
    assert initial_combat_state.is_menu_open
    assert initial_combat_state.stance == "neutral" # Stance should not change


def test_toggle_menu_close(initial_combat_state):
    """Tests that pressing 'Escape' closes the menu when it's open."""
    initial_combat_state.toggle_menu() # Manually open menu
    assert initial_combat_state.is_menu_open

    event = {"key": "Escape", "type": "keydown"}
    handle_combat_input(event, initial_combat_state)
    assert not initial_combat_state.is_menu_open


def test_combat_actions_ignored_when_menu_open(initial_combat_state):
    """Tests that combat actions are ignored when the menu is open."""
    initial_combat_state.toggle_menu() # Open menu
    assert initial_combat_state.is_menu_open

    # Try to change stance
    event_q = {"key": "q", "type": "keydown"}
    handle_combat_input(event_q, initial_combat_state)
    assert initial_combat_state.stance == "neutral" # Should remain neutral

    # Try to attack
    event_space = {"key": " ", "type": "keydown"}
    initial_combat_state.enemy_health = 100
    handle_combat_input(event_space, initial_combat_state)
    assert initial_combat_state.current_action is None # Should not perform action
    assert initial_combat_state.enemy_health == 100 # Health should not change
    assert initial_combat_state.is_menu_open # Menu should still be open


def test_unknown_key_does_nothing(initial_combat_state):
    """Tests that an unhandled key press does not alter the state."""
    original_stance = initial_combat_state.stance
    original_menu_state = initial_combat_state.is_menu_open
    original_action = initial_combat_state.current_action
    original_enemy_health = initial_combat_state.enemy_health

    event = {"key": "z", "type": "keydown"}
    handle_combat_input(event, initial_combat_state)

    assert initial_combat_state.stance == original_stance
    assert initial_combat_state.is_menu_open == original_menu_state
    assert initial_combat_state.current_action == original_action
    assert initial_combat_state.enemy_health == original_enemy_health


def test_keyup_event_no_action_by_default(initial_combat_state):
    """Tests that a keyup event, by default, does not trigger actions."""
    original_stance = initial_combat_state.stance
    original_menu_state = initial_combat_state.is_menu_open
    original_action = initial_combat_state.current_action

    event = {"key": "q", "type": "keyup"}
    handle_combat_input(event, initial_combat_state)

    assert initial_combat_state.stance == original_stance
    assert initial_combat_state.is_menu_open == original_menu_state
    assert initial_combat_state.current_action == original_action

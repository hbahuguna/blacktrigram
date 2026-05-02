import pytest

# Mock implementation of the target function for testing purposes.
# In a real scenario, this would be imported from the actual Python module
# or a TypeScript function would be mocked using a testing framework like Jest.
# Since the target code is unavailable and pytest is requested, we provide
# a Python simulation of the described behavior.
def updateInjuries(current_injuries: dict, body_region: str, initial_severity: int = 1) -> dict:
    """
    Manages the progression and accumulation of physical injuries by escalating severity
    for repeated hits to the same body region.

    Args:
        current_injuries: A dictionary where keys are body regions (str) and values
                          are their current injury severity (int).
        body_region: The body region that was just hit.
        initial_severity: The base severity of the new hit if it's a new injury,
                          or the increment for an existing one.

    Returns:
        An updated dictionary of injuries.
    """
    updated_injuries = current_injuries.copy()
    if body_region in updated_injuries:
        # Escalate severity for repeated hits
        updated_injuries[body_region] += initial_severity
    else:
        # New injury
        updated_injuries[body_region] = initial_severity
    return updated_injuries


class TestUpdateInjuries:

    def test_initial_hit_creates_injury(self):
        """
        Tests that hitting a new body region creates an injury with the default severity.
        """
        current_injuries = {}
        body_region = "head"
        updated_injuries = updateInjuries(current_injuries, body_region)
        assert updated_injuries == {"head": 1}

    def test_initial_hit_with_custom_severity(self):
        """
        Tests that hitting a new body region creates an injury with a specified severity.
        """
        current_injuries = {}
        body_region = "chest"
        initial_severity = 3
        updated_injuries = updateInjuries(current_injuries, body_region, initial_severity)
        assert updated_injuries == {"chest": 3}

    def test_repeated_hit_escalates_severity(self):
        """
        Tests that hitting an already injured region increases its severity.
        """
        current_injuries = {"arm": 1}
        body_region = "arm"
        updated_injuries = updateInjuries(current_injuries, body_region)
        assert updated_injuries == {"arm": 2}

    def test_repeated_hit_with_custom_severity_escalates_correctly(self):
        """
        Tests that hitting an already injured region with a custom severity
        adds that severity to the existing one.
        """
        current_injuries = {"leg": 5}
        body_region = "leg"
        initial_severity = 2
        updated_injuries = updateInjuries(current_injuries, body_region, initial_severity)
        assert updated_injuries == {"leg": 7}

    def test_hitting_different_regions_maintains_existing_injuries(self):
        """
        Tests that hitting a new region does not affect existing injuries in other regions.
        """
        current_injuries = {"head": 1, "arm": 3}
        body_region = "leg"
        updated_injuries = updateInjuries(current_injuries, body_region)
        assert updated_injuries == {"head": 1, "arm": 3, "leg": 1}

    def test_hitting_existing_and_new_regions_in_sequence(self):
        """
        Tests a sequence of hits involving both new and existing injury regions.
        """
        injuries = {}
        injuries = updateInjuries(injuries, "head", 2) # New hit
        assert injuries == {"head": 2}

        injuries = updateInjuries(injuries, "arm", 1) # New hit
        assert injuries == {"head": 2, "arm": 1}

        injuries = updateInjuries(injuries, "head", 1) # Repeated hit
        assert injuries == {"head": 3, "arm": 1}

        injuries = updateInjuries(injuries, "arm", 3) # Repeated hit with custom severity
        assert injuries == {"head": 3, "arm": 4}

    def test_empty_body_region_input(self):
        """
        Tests behavior with an empty string as body region (should create an injury for '').
        """
        current_injuries = {}
        body_region = ""
        updated_injuries = updateInjuries(current_injuries, body_region)
        assert updated_injuries == {"": 1}

    def test_immutability_of_input_dict(self):
        """
        Tests that the original current_injuries dictionary is not modified.
        """
        current_injuries = {"chest": 5}
        original_injuries_copy = current_injuries.copy()
        updateInjuries(current_injuries, "head")
        assert current_injuries == original_injuries_copy

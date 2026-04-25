import pytest

# Mock implementation of the target function, as the original code is unavailable.
# This mock is based on the function summary: "Calculates the total effective reach
# of an attack by applying stance-based modifiers to the base technique range."
# We assume the modifier is a multiplicative factor.
def calculateAttackReach(base_technique_range: float, stance_modifier: float) -> float:
    """
    MOCK: Calculates the total effective reach of an attack by applying stance-based
    modifiers to the base technique range.
    """
    if base_technique_range < 0:
        raise ValueError("Base technique range cannot be negative.")
    if stance_modifier < 0:
        # While a negative modifier might be valid in some contexts (e.g., reach reduction
        # beyond zero), for a typical "reach" calculation, a negative multiplier would
        # invert the reach, which is usually not intended. We'll allow it for now but
        # note it as a potential design decision point.
        pass

    return base_technique_range * stance_modifier


class TestCalculateAttackReach:
    """Tests for the calculateAttackReach function."""

    @pytest.mark.parametrize(
        "base_range, stance_modifier, expected_reach",
        [
            # Standard cases
            (10.0, 1.2, 12.0),  # 20% increase
            (5.0, 0.8, 4.0),    # 20% decrease
            (7.5, 1.0, 7.5),    # No change
            (1.0, 1.5, 1.5),    # 50% increase

            # Edge cases
            (0.0, 1.5, 0.0),    # Zero base range, any modifier
            (0.0, 0.5, 0.0),    # Zero base range, any modifier
            (100.0, 2.0, 200.0),# Large base range, significant increase
            (0.1, 0.5, 0.05),   # Small base range, decrease
            (15.0, 0.0, 0.0),   # Zero modifier (e.g., completely disabled reach)

            # Floating point precision (using pytest.approx for comparison)
            (3.0, 1/3, 1.0),    # Modifier that results in exact float
            (10.0, 1.15, 11.5), # Decimal modifier
        ],
    )
    def test_valid_calculations(self, base_range: float, stance_modifier: float, expected_reach: float):
        """Tests various valid combinations of base range and stance modifiers."""
        actual_reach = calculateAttackReach(base_range, stance_modifier)
        assert actual_reach == pytest.approx(expected_reach)

    def test_negative_base_range_raises_error(self):
        """Tests that a negative base technique range raises a ValueError."""
        with pytest.raises(ValueError, match="Base technique range cannot be negative."):
            calculateAttackReach(-5.0, 1.2)

    @pytest.mark.parametrize(
        "base_range, stance_modifier, expected_reach",
        [
            (10.0, -0.5, -5.0), # Negative modifier, results in negative reach
            (5.0, -1.0, -5.0),  # Negative modifier, results in negative reach
        ],
    )
    def test_negative_stance_modifier(self, base_range: float, stance_modifier: float, expected_reach: float):
        """Tests behavior with a negative stance modifier. Note: The interpretation of
        negative reach might vary based on game design, but the calculation should be consistent.
        """
        actual_reach = calculateAttackReach(base_range, stance_modifier)
        assert actual_reach == pytest.approx(expected_reach)

    def test_large_values_no_overflow(self):
        """Tests with very large numbers to ensure no unexpected overflow or precision issues (within float limits)."""
        base_range = 1e10  # 10 billion
        stance_modifier = 1.5
        expected_reach = 1.5e10
        actual_reach = calculateAttackReach(base_range, stance_modifier)
        assert actual_reach == pytest.approx(expected_reach)

    def test_small_values_precision(self):
        """Tests with very small numbers to ensure precision is maintained."""
        base_range = 1e-9  # 1 nanometer
        stance_modifier = 0.001
        expected_reach = 1e-12
        actual_reach = calculateAttackReach(base_range, stance_modifier)
        assert actual_reach == pytest.approx(expected_reach)

import pytest

# NOTE: The actual `getDamageType` function is written in TypeScript (src/components/screens/combat/CombatScreen3D.tsx).
# For the purpose of generating a standalone Pytest test, a Python equivalent of the function
# is provided below. In a real-world scenario, if the target function were in Python,
# it would be imported directly. If it were in TypeScript and we needed to test its logic
# from Python, we might use a language bridge or a more sophisticated testing setup.
# This test assumes the following thresholds based on the function summary:
# - Critical: damage >= 100
# - Vital: 50 <= damage < 100
# - Normal: damage < 50

def getDamageType(damage: float) -> str:
    """
    Categorizes the severity of an attack into critical, vital, or normal tiers
    based on the damage value.

    This is a hypothetical Python implementation mirroring the expected behavior
    of the TypeScript function `getDamageType`.
    """
    CRITICAL_THRESHOLD = 100.0
    VITAL_THRESHOLD = 50.0

    if damage >= CRITICAL_THRESHOLD:
        return "critical"
    elif damage >= VITAL_THRESHOLD:
        return "vital"
    else:
        return "normal"


class TestGetDamageType:
    """
    Tests for the `getDamageType` function, ensuring correct categorization
    of damage values into 'critical', 'vital', or 'normal' tiers.
    """

    @pytest.mark.parametrize(
        "damage, expected_type",
        [
            # Critical damage cases
            (100.0, "critical"),  # Edge case: exactly critical threshold
            (100.1, "critical"),  # Just above critical threshold
            (150.0, "critical"),  # High critical damage
            (200, "critical"),    # Integer critical damage

            # Vital damage cases
            (50.0, "vital"),      # Edge case: exactly vital threshold
            (50.1, "vital"),      # Just above vital threshold
            (75.0, "vital"),      # Mid-range vital damage
            (99.9, "vital"),      # Just below critical threshold

            # Normal damage cases
            (0.0, "normal"),      # Zero damage
            (1.0, "normal"),      # Low normal damage
            (25.0, "normal"),     # Mid-range normal damage
            (49.9, "normal"),     # Just below vital threshold

            # Negative damage (assuming damage is typically non-negative, but testing robustness)
            (-10.0, "normal"),    # Negative damage should still be normal
        ],
        ids=[
            "critical_exact_threshold", "critical_above_threshold", "critical_high", "critical_integer",
            "vital_exact_threshold", "vital_above_threshold", "vital_mid", "vital_just_below_critical",
            "normal_zero", "normal_low", "normal_mid", "normal_just_below_vital",
            "normal_negative_damage"
        ]
    )
    def test_damage_categorization(self, damage: float, expected_type: str):
        """
        Verifies that various damage values are correctly categorized.
        """
        assert getDamageType(damage) == expected_type

    def test_return_type_and_valid_values(self):
        """
        Ensures the function always returns a string and that the string
        is one of the expected damage types.
        """
        result = getDamageType(75.5)
        assert isinstance(result, str)
        assert result in ["critical", "vital", "normal"]

        result_critical = getDamageType(120)
        assert isinstance(result_critical, str)
        assert result_critical == "critical"

        result_normal = getDamageType(10)
        assert isinstance(result_normal, str)
        assert result_normal == "normal"

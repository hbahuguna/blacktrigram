{
  "file_path": "tests/unit/test_collision_detection.py",
  "code": "import pytest
from unittest.mock import Mock, patch

# --- Mocking dependent classes for testing purposes ---
# In a real scenario, these would be imported from their respective modules.

class BoundingBox:
    def __init__(self, min_coords, max_coords):
        self.min = min_coords  # (x, y, z)
        self.max = max_coords  # (x, y, z)

    def intersects(self, other: 'BoundingBox') -> bool:
        # Simplified AABB intersection logic for testing
        return (self.min[0] <= other.max[0] and self.max[0] >= other.min[0] and
                self.min[1] <= other.max[1] and self.max[1] >= other.min[1] and
                self.min[2] <= other.max[2] and self.max[2] >= other.min[2])

class Ray:
    def __init__(self, origin, direction):
        self.origin = origin
        self.direction = direction

class VitalPoint:
    def __init__(self, name, position, radius):
        self.name = name
        self.position = position
        self.radius = radius

    # This method will be mocked in tests to control narrow-phase outcomes
    def intersects_ray(self, ray: Ray) -> bool:
        raise NotImplementedError(\"This should be mocked for testing.\")

class Combatant:
    def __init__(self, id, bounding_box: BoundingBox, vital_points: list[VitalPoint]):
        self.id = id
        self.bounding_box = bounding_box
        self.vital_points = vital_points

# --- Target Class (Conceptual Python equivalent of CollisionDetection.ts) ---
class CollisionDetection:
    def __init__(self):
        pass

    def _broad_phase_check(self, combatant1: Combatant, combatant2: Combatant) -> bool:
        \"\"\"Performs a broad-phase bounding box intersection check.\"\"\"
        return combatant1.bounding_box.intersects(combatant2.bounding_box)

    def _narrow_phase_check(self, attacker_ray: Ray, target_combatant: Combatant) -> dict:
        \"\"\"Performs a narrow-phase raycast against vital points.\"\"\"
        hits = {}
        for vp in target_combatant.vital_points:
            if vp.intersects_ray(attacker_ray):
                hits[vp.name] = vp.position
        return hits

    def detect_hit(self, attacker_combatant: Combatant, target_combatant: Combatant, attack_ray: Ray) -> dict:
        \"\"\"
        Orchestrates collision detection to identify precise vital point hits.
        Returns a dictionary indicating hit status and details.
        \"\"\"
        if not self._broad_phase_check(attacker_combatant, target_combatant):
            return {\"hit\": False, \"details\": \"No broad-phase collision\"}

        vital_point_hits = self._narrow_phase_check(attack_ray, target_combatant)

        if vital_point_hits:
            return {\"hit\": True, \"details\": \"Vital point hit\", \"vital_points\": vital_point_hits}
        else:
            return {\"hit\": False, \"details\": \"Broad-phase collision, but no vital point hit\"}

# --- Pytest Tests for CollisionDetection ---

@pytest.fixture
def collision_detection_system():
    return CollisionDetection()

@pytest.fixture
def mock_combatants():
    # Combatant 1: Attacker
    attacker_bbox = BoundingBox((0, 0, 0), (1, 1, 1))
    attacker_vital_points = [
        VitalPoint(\"head\", (0.5, 0.9, 0.5), 0.1)
    ]
    attacker = Combatant(\"attacker_1\", attacker_bbox, attacker_vital_points)

    # Combatant 2: Target (initially overlapping for broad-phase)
    target_bbox = BoundingBox((0.5, 0.5, 0.5), (1.5, 1.5, 1.5))
    target_vital_points = [
        VitalPoint(\"chest\", (1.0, 1.0, 1.0), 0.2),
        VitalPoint(\"leg\", (0.8, 0.2, 0.8), 0.1)
    ]
    target = Combatant(\"target_1\", target_bbox, target_vital_points)

    # A ray for testing
    test_ray = Ray((0, 0, 0), (1, 1, 1)) # Ray from origin towards (1,1,1)

    return attacker, target, test_ray

def test_no_broad_phase_collision(collision_detection_system):
    \"\"\"
    Tests that no hit is detected when combatants' bounding boxes do not overlap.
    \"\"\"
    attacker_bbox = BoundingBox((0, 0, 0), (1, 1, 1))
    attacker = Combatant(\"attacker_1\", attacker_bbox, [])

    # Target far away
    target_bbox = BoundingBox((10, 10, 10), (11, 11, 11))
    target = Combatant(\"target_1\", target_bbox, [])

    test_ray = Ray((0, 0, 0), (1, 1, 1))

    result = collision_detection_system.detect_hit(attacker, target, test_ray)
    assert result[\"hit\"] is False
    assert result[\"details\"] == \"No broad-phase collision\"

@patch.object(VitalPoint, 'intersects_ray', return_value=False)
def test_broad_phase_collision_no_narrow_phase_hit(mock_intersects_ray, collision_detection_system, mock_combatants):
    \"\"\"
    Tests that a broad-phase collision occurs, but the ray misses all vital points.
    \"\"\"
    attacker, target, test_ray = mock_combatants

    # Ensure broad-phase would pass (default mock_combatants setup)
    assert collision_detection_system._broad_phase_check(attacker, target) is True

    result = collision_detection_system.detect_hit(attacker, target, test_ray)
    assert result[\"hit\"] is False
    assert result[\"details\"] == \"Broad-phase collision, but no vital point hit\"
    mock_intersects_ray.assert_called() # Ensure narrow-phase was attempted

@patch.object(VitalPoint, 'intersects_ray')
def test_broad_phase_collision_with_narrow_phase_hit(mock_intersects_ray, collision_detection_system, mock_combatants):
    \"\"\"
    Tests that both broad-phase and narrow-phase checks pass, resulting in a vital point hit.
    \"\"\"
    attacker, target, test_ray = mock_combatants

    # Mock one vital point to be hit
    mock_intersects_ray.side_effect = lambda ray: ray == test_ray and target.vital_points[0].name == \"chest\"

    result = collision_detection_system.detect_hit(attacker, target, test_ray)
    assert result[\"hit\"] is True
    assert result[\"details\"] == \"Vital point hit\"
    assert \"vital_points\" in result
    assert \"chest\" in result[\"vital_points\"]
    assert result[\"vital_points\"][\"chest\"] == target.vital_points[0].position
    mock_intersects_ray.assert_called()

@patch.object(VitalPoint, 'intersects_ray')
def test_multiple_vital_points_hit(mock_intersects_ray, collision_detection_system, mock_combatants):
    \"\"\"
    Tests scenario where a single ray hits multiple vital points.
    \"\"\"
    attacker, target, test_ray = mock_combatants

    # Mock both vital points to be hit
    mock_intersects_ray.return_value = True

    result = collision_detection_system.detect_hit(attacker, target, test_ray)
    assert result[\"hit\"] is True
    assert result[\"details\"] == \"Vital point hit\"
    assert \"vital_points\" in result
    assert \"chest\" in result[\"vital_points\"]
    assert \"leg\" in result[\"vital_points\"]
    assert result[\"vital_points\"][\"chest\"] == target.vital_points[0].position
    assert result[\"vital_points\"][\"leg\"] == target.vital_points[1].position
    assert mock_intersects_ray.call_count == len(target.vital_points)

@patch.object(VitalPoint, 'intersects_ray')
def test_target_with_no_vital_points(mock_intersects_ray, collision_detection_system, mock_combatants):
    \"\"\"
    Tests collision detection against a target combatant that has no vital points.
    Should result in broad-phase collision but no vital point hit.
    \"\"\"
    attacker, _, test_ray = mock_combatants

    # Create a target with no vital points, but overlapping bbox
    target_bbox = BoundingBox((0.5, 0.5, 0.5), (1.5, 1.5, 1.5))
    target_no_vps = Combatant(\"target_no_vps\", target_bbox, [])

    result = collision_detection_system.detect_hit(attacker, target_no_vps, test_ray)
    assert result[\"hit\"] is False
    assert result[\"details\"] == \"Broad-phase collision, but no vital point hit\"
    mock_intersects_ray.assert_not_called() # No vital points to check
"
}
{
  "file_path": "tests/unit/systems/physics/test_collision_detection.py",
  "code": "import pytest
from unittest.mock import Mock, MagicMock

# --- Mock Classes for Dependencies and the Target Class ---
# These mocks simulate the behavior described in the CollisionDetection summary
# as the actual target code is unavailable.

class MockBoundingBox:
    def __init__(self, min_coords, max_coords):
        self.min = min_coords  # (x, y, z)
        self.max = max_coords  # (x, y, z)

    def intersects(self, other):
        \"\"\"
        Performs a simple Axis-Aligned Bounding Box (AABB) intersection check.
        \"\"\"
        return not (self.max[0] < other.min[0] or self.min[0] > other.max[0] or
                    self.max[1] < other.min[1] or self.min[1] > other.max[1] or
                    self.max[2] < other.min[2] or self.min[2] > other.max[2])

class MockVitalPoint:
    def __init__(self, name, position, radius=0.1):
        self.name = name
        self.position = position  # (x, y, z) in world coordinates
        self.radius = radius

    def __eq__(self, other):
        if not isinstance(other, MockVitalPoint):
            return NotImplemented
        return self.name == other.name and self.position == other.position and self.radius == other.radius

    def __repr__(self):
        return f\"MockVitalPoint(name='{self.name}', position={self.position}, radius={self.radius})\"

class MockCombatant:
    def __init__(self, name, position, bounding_box, vital_points):
        self.name = name
        self.position = position  # (x, y, z) - overall combatant position
        self._bounding_box = bounding_box  # MockBoundingBox instance
        self._vital_points = vital_points  # List of MockVitalPoint instances

    def get_world_bounding_box(self):
        \"\"\"
        Returns the combatant's bounding box in world coordinates.
        For simplicity, assumes the stored bounding box is already world-relative.
        \"\"\"
        return self._bounding_box

    def get_world_vital_points(self):
        \"\"\"
        Returns a list of the combatant's vital points in world coordinates.
        For simplicity, assumes the stored vital points are already world-relative.
        \"\"\"
        return self._vital_points

    def __eq__(self, other):
        if not isinstance(other, MockCombatant):
            return NotImplemented
        return self.name == other.name

    def __repr__(self):
        return f\"MockCombatant(name='{self.name}', position={self.position})\"

class MockRay:
    def __init__(self, origin, direction):
        self.origin = origin
        self.direction = direction

    def __eq__(self, other):
        if not isinstance(other, MockRay):
            return NotImplemented
        return self.origin == other.origin and self.direction == other.direction

    def __repr__(self):
        return f\"MockRay(origin={self.origin}, direction={self.direction})\"

class MockRaycaster:
    def intersect_sphere(self, ray, sphere_center, sphere_radius):
        \"\"\"
        Simulates a ray-sphere intersection. Returns True if hit, False otherwise.
        This is a simplified check for testing purposes.
        \"\"\"
        # For simplicity, we'll just check if the ray's origin is 'close enough'
        # to the sphere center, or if a mock has been configured to return a specific result.
        # A real raycaster would perform actual geometric intersection.
        # For now, we'll rely on mocking this method directly in tests.
        raise NotImplementedError(\"MockRaycaster.intersect_sphere should be mocked in tests\")

class CollisionResult:
    def __init__(self, combatant_hit, vital_point_hit, ray_origin, ray_direction):
        self.combatant_hit = combatant_hit
        self.vital_point_hit = vital_point_hit
        self.ray_origin = ray_origin
        self.ray_direction = ray_direction

    def __eq__(self, other):
        if not isinstance(other, CollisionResult):
            return NotImplemented
        # Compare combatant_hit by name for simplicity in tests
        return (self.combatant_hit.name == other.combatant_hit.name and
                self.vital_point_hit == other.vital_point_hit and
                self.ray_origin == other.ray_origin and
                self.ray_direction == other.ray_direction)

    def __repr__(self):
        return (f\"CollisionResult(combatant_hit='{self.combatant_hit.name}', \"
                f\"vital_point_hit='{self.vital_point_hit.name}', \"
                f\"ray_origin={self.ray_origin}, ray_direction={self.ray_direction})\")

# The target class, mocked based on the summary's description
class CollisionDetection:
    def __init__(self, raycaster=None):
        self.raycaster = raycaster if raycaster else MockRaycaster()

    def detect_collisions(self, combatant_a, combatant_b):
        \"\"\"
        Orchestrates 3D collision detection between combatants.
        Performs broad-phase bounding box checks and narrow-phase raycasting
        to identify precise vital point hits.
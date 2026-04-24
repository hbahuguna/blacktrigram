import pytest

# --- System Under Test (SUT) Mock --- #
# As the original TypeScript code is unavailable, we'll create a Python
# equivalent based on the function's summary to make the tests standalone and executable.

class MockVector3:
    """Mock for a 3D vector class."""
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    def set(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

class MockQuaternion:
    """Mock for a quaternion class for rotation."""
    def __init__(self, x=0, y=0, z=0, w=1):
        self.x = x
        self.y = y
        self.z = z
        self.w = w

    def set(self, x, y, z, w):
        self.x = x
        self.y = y
        self.z = z
        self.w = w

class MockBox:
    """Mock for a box geometry."""
    def __init__(self):
        self.position = MockVector3()
        self.size = MockVector3()

class MockSphere:
    """Mock for a sphere geometry."""
    def __init__(self):
        self.position = MockVector3()
        self.radius = 0

class MockRay:
    """Mock for a ray used in raycasting."""
    def __init__(self):
        self.origin = MockVector3()
        self.direction = MockVector3()

# This dictionary represents the global cache that the function will populate.
GEOMETRY_CACHE = {}

def initializeGeometryCache(size: int):
    """
    Pre-allocates and caches geometric shapes to optimize raycasting performance
    and minimize memory allocations during high-frequency collision checks.
    """
    global GEOMETRY_CACHE

    if not isinstance(size, int) or size < 0:
        raise ValueError("Cache size must be a non-negative integer.")

    # The function is expected to clear and re-populate the cache on each call.
    GEOMETRY_CACHE = {
        "boxes": [MockBox() for _ in range(size)],
        "spheres": [MockSphere() for _ in range(size)],
        "rays": [MockRay() for _ in range(size)],
        "vectors": [MockVector3() for _ in range(size * 3)],  # Assume more vectors are needed
        "quaternions": [MockQuaternion() for _ in range(size)]
    }

# --- Pytest Tests --- #

@pytest.fixture(autouse=True)
def reset_cache_before_each_test():
    """Ensures a clean state for each test by resetting the cache."""
    global GEOMETRY_CACHE
    GEOMETRY_CACHE.clear()
    yield
    GEOMETRY_CACHE.clear()

@pytest.mark.parametrize("cache_size", [1, 10, 100])
def test_initialization_with_positive_size(cache_size):
    """Verify that the cache is populated correctly for various positive sizes."""
    # Act
    initializeGeometryCache(cache_size)

    # Assert
    assert "boxes" in GEOMETRY_CACHE
    assert "spheres" in GEOMETRY_CACHE
    assert "rays" in GEOMETRY_CACHE
    assert "vectors" in GEOMETRY_CACHE
    assert "quaternions" in GEOMETRY_CACHE

    assert len(GEOMETRY_CACHE["boxes"]) == cache_size
    assert len(GEOMETRY_CACHE["spheres"]) == cache_size
    assert len(GEOMETRY_CACHE["rays"]) == cache_size
    assert len(GEOMETRY_CACHE["vectors"]) == cache_size * 3
    assert len(GEOMETRY_CACHE["quaternions"]) == cache_size

    assert all(isinstance(item, MockBox) for item in GEOMETRY_CACHE["boxes"])
    assert all(isinstance(item, MockSphere) for item in GEOMETRY_CACHE["spheres"])

def test_initialization_with_zero_size():
    """Verify that initializing with size 0 results in empty lists in the cache."""
    # Act
    initializeGeometryCache(0)

    # Assert
    assert len(GEOMETRY_CACHE["boxes"]) == 0
    assert len(GEOMETRY_CACHE["spheres"]) == 0
    assert len(GEOMETRY_CACHE["rays"]) == 0
    assert len(GEOMETRY_CACHE["vectors"]) == 0
    assert len(GEOMETRY_CACHE["quaternions"]) == 0

def test_reinitialization_clears_and_repopulates():
    """Verify that calling the function again correctly replaces the old cache."""
    # Arrange: Initialize with a first size
    initializeGeometryCache(10)
    # Store references to prove they are replaced
    first_box_id = id(GEOMETRY_CACHE["boxes"][0])
    assert len(GEOMETRY_CACHE["boxes"]) == 10

    # Act: Re-initialize with a different size
    initializeGeometryCache(5)

    # Assert: The cache is now the new size
    assert len(GEOMETRY_CACHE["boxes"]) == 5
    assert len(GEOMETRY_CACHE["spheres"]) == 5

    # Assert: The objects are new instances, not just a truncated list
    second_box_id = id(GEOMETRY_CACHE["boxes"][0])
    assert first_box_id != second_box_id

def test_cached_objects_have_default_values():
    """Verify that the pre-allocated objects are in a clean, default state."""
    # Arrange
    cache_size = 1

    # Act
    initializeGeometryCache(cache_size)

    # Assert
    # Check a box
    box = GEOMETRY_CACHE["boxes"][0]
    assert isinstance(box, MockBox)
    assert box.position.x == 0 and box.position.y == 0 and box.position.z == 0
    assert box.size.x == 0 and box.size.y == 0 and box.size.z == 0

    # Check a sphere
    sphere = GEOMETRY_CACHE["spheres"][0]
    assert isinstance(sphere, MockSphere)
    assert sphere.position.x == 0 and sphere.position.y == 0 and sphere.position.z == 0
    assert sphere.radius == 0

    # Check a quaternion
    quat = GEOMETRY_CACHE["quaternions"][0]
    assert isinstance(quat, MockQuaternion)
    assert quat.x == 0 and quat.y == 0 and quat.z == 0 and quat.w == 1

@pytest.mark.parametrize("invalid_size", [-1, -10, 1.5, "five"])
def test_initialization_with_invalid_size_raises_error(invalid_size):
    """Verify that non-integer or negative sizes raise a ValueError."""
    with pytest.raises(ValueError, match="Cache size must be a non-negative integer."):
        initializeGeometryCache(invalid_size)

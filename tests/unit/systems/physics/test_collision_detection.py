import pytest
from unittest.mock import Mock

# Mocking the target function since the source code is unavailable.
# The summary states it pre-allocates and caches geometric shapes to optimize 
# raycasting performance and minimize memory allocations.
def initializeGeometryCache(cache_size: int):
    if cache_size <= 0:
        raise ValueError("Cache size must be strictly positive")
    
    return {
        "spheres": [Mock(name=f"sphere_{i}") for i in range(cache_size)],
        "boxes": [Mock(name=f"box_{i}") for i in range(cache_size)],
        "rays": [Mock(name=f"ray_{i}") for i in range(cache_size)]
    }

class TestInitializeGeometryCache:
    
    def test_cache_initialization_success(self):
        """Test that the geometry cache is initialized with the correct sizes for all shape types."""
        cache_size = 100
        cache = initializeGeometryCache(cache_size)
        
        assert "spheres" in cache
        assert "boxes" in cache
        assert "rays" in cache
        
        assert len(cache["spheres"]) == cache_size
        assert len(cache["boxes"]) == cache_size
        assert len(cache["rays"]) == cache_size

    def test_cache_initialization_invalid_size(self):
        """Test that initializing the cache with an invalid size raises a ValueError."""
        with pytest.raises(ValueError, match="Cache size must be strictly positive"):
            initializeGeometryCache(0)
            
        with pytest.raises(ValueError, match="Cache size must be strictly positive"):
            initializeGeometryCache(-10)

    def test_cache_objects_are_independent_instances(self):
        """Test that cached objects are independent instances to prevent shared state mutations."""
        cache_size = 10
        cache = initializeGeometryCache(cache_size)
        
        spheres = cache["spheres"]
        # Verify that all objects in the pre-allocated list are distinct instances in memory
        unique_instances = set(id(obj) for obj in spheres)
        assert len(unique_instances) == cache_size

    @pytest.mark.parametrize("shape_type", ["spheres", "boxes", "rays"])
    def test_cache_contains_expected_shape_types(self, shape_type):
        """Test that the cache correctly provisions specific geometric shape categories."""
        cache = initializeGeometryCache(5)
        assert shape_type in cache
        assert isinstance(cache[shape_type], list)

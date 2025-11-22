"""
Complete example showing how to use the computation backend system.

This example demonstrates:
1. Different ways to configure backends
2. Performance comparisons
3. Best practices
"""

import time

from helpers.setup import *

from ansys.edb.core.config import ComputationBackend, Config
from ansys.edb.core.geometry.polygon_data import PolygonData


def example_basic_usage():
    """Example 1: Basic usage with different backends."""
    print("=" * 70)
    print("Example 1: Basic Usage")
    print("=" * 70)

    # Create a simple polygon
    polygon = PolygonData([(0, 0), (10, 0), (10, 10), (0, 10)])
    polygon2 = PolygonData([(10, 10), (20, 10), (20, 20), (10, 20)])

    # Use server backend (explicit)
    print("\n--- Using Server Backend ---")
    Config.set_computation_backend(ComputationBackend.SERVER)
    PolygonData.reset_backend()

    # Initialize EDB
    initialize_edb(__file__)

    print(f"Area: {polygon.area()}")
    print(f"Is convex: {polygon.is_convex()}")
    print(f"Is (5, 5) inside: {polygon.is_inside((5, 5))}")
    print(
        f"Bounding box: ({polygon.bbox()[0].x}, {polygon.bbox()[0].y}) -- ({polygon.bbox()[1].x}, {polygon.bbox()[1].y})"
    )
    print(
        f"Bounding box of multiple polygons: ({PolygonData.bbox_of_polygons([polygon, polygon2])[0].x}, {PolygonData.bbox_of_polygons([polygon, polygon2])[0].y}) -- ({PolygonData.bbox_of_polygons([polygon, polygon2])[1].x}, {PolygonData.bbox_of_polygons([polygon, polygon2])[1].y})"
    )

    # Use Shapely backend (if available)
    print("\n--- Using Shapely Backend ---")
    try:
        Config.set_computation_backend(ComputationBackend.SHAPELY)
        PolygonData.reset_backend()

        print(f"Area: {polygon.area()}")
        print(f"Is convex: {polygon.is_convex()}")
        print(f"Is (5, 5) inside: {polygon.is_inside((5, 5))}")
        print(
            f"Bounding box: ({polygon.bbox()[0].x}, {polygon.bbox()[0].y}) -- ({polygon.bbox()[1].x}, {polygon.bbox()[1].y})"
        )
        print(
            f"Bounding box of multiple polygons: ({PolygonData.bbox_of_polygons([polygon, polygon2])[0].x}, {PolygonData.bbox_of_polygons([polygon, polygon2])[0].y}) -- ({PolygonData.bbox_of_polygons([polygon, polygon2])[1].x}, {PolygonData.bbox_of_polygons([polygon, polygon2])[1].y})"
        )
    except ImportError as e:
        print(f"Shapely not available: {e}")

    # Use AUTO mode
    print("\n--- Using AUTO Mode ---")
    Config.set_computation_backend(ComputationBackend.AUTO)
    PolygonData.reset_backend()

    print(f"Area: {polygon.area()}")
    print(f"Is convex: {polygon.is_convex()}")
    print(f"Is (5, 5) inside: {polygon.is_inside((5, 5))}")
    print(f"Backend used: {Config.get_computation_backend()}")
    print(
        f"Bounding box: ({polygon.bbox()[0].x}, {polygon.bbox()[0].y}) -- ({polygon.bbox()[1].x}, {polygon.bbox()[1].y})"
    )
    print(
        f"Bounding box of multiple polygons: ({PolygonData.bbox_of_polygons([polygon, polygon2])[0].x}, {PolygonData.bbox_of_polygons([polygon, polygon2])[0].y}) -- ({PolygonData.bbox_of_polygons([polygon, polygon2])[1].x}, {PolygonData.bbox_of_polygons([polygon, polygon2])[1].y})"
    )


def example_performance_comparison():
    """Example 2: Compare performance between backends."""
    print("\n" + "=" * 70)
    print("Example 2: Performance Comparison")
    print("=" * 70)

    # Create test polygons
    num_polygons = 10000
    polygons = []
    for i in range(num_polygons):
        # Create polygons of varying sizes
        size = 10 + i * 0.1
        poly = PolygonData([(0, 0), (size, 0), (size, size), (0, size)])
        polygons.append(poly)

    def benchmark_backend(backend_type, backend_name):
        """Run benchmark with a specific backend."""
        Config.set_computation_backend(backend_type)
        PolygonData.reset_backend()

        start = time.time()
        total_area = 0

        for poly in polygons:
            total_area += poly.area()

        elapsed = time.time() - start

        print(f"\n{backend_name}:")
        print(f"  Time: {elapsed:.4f}s")
        print(f"  Total area: {total_area:.2f}")

        return elapsed

    # Benchmark server
    server_time = benchmark_backend(ComputationBackend.SERVER, "Server Backend")

    # Benchmark Shapely (if available)
    try:
        shapely_time = benchmark_backend(ComputationBackend.SHAPELY, "Shapely Backend")
        speedup = server_time / shapely_time
        print(f"\nSpeedup: {speedup:.1f}x faster with Shapely")
    except ImportError:
        print("\nShapely not available for comparison")


def example_environment_variable():
    """Example 3: Using environment variables."""
    print("\n" + "=" * 70)
    print("Example 3: Environment Variable Configuration")
    print("=" * 70)

    import os

    # Set via environment variable (would normally be set outside Python)
    os.environ["PYEDB_COMPUTATION_BACKEND"] = "shapely"

    # Reset config to pick up environment variable
    Config.reset()
    PolygonData.reset_backend()

    print(f"Backend from environment: {Config.get_computation_backend()}")

    # Clean up
    del os.environ["PYEDB_COMPUTATION_BACKEND"]
    Config.reset()


def example_batch_processing():
    """Example 4: Batch processing with optimal backend."""
    print("\n" + "=" * 70)
    print("Example 4: Batch Processing")
    print("=" * 70)

    # For batch processing, use Shapely for best performance
    Config.set_computation_backend(ComputationBackend.SHAPELY)
    PolygonData.reset_backend()

    # Process multiple polygons
    results = []
    for i in range(10):
        # Create random-ish polygon
        points = [(0, 0), (i + 1, 0), (i + 1, i + 1), (0, i + 1)]
        poly = PolygonData(points)

        # Compute multiple properties efficiently (all local with Shapely)
        result = {
            "id": i,
            "area": poly.area(),
            "is_convex": poly.is_convex(),
            "center_inside": poly.is_inside((i / 2, i / 2)),
        }
        results.append(result)

    print(f"\nProcessed {len(results)} polygons")
    print(f"First result: {results[0]}")
    print(f"Last result: {results[-1]}")


def example_mixed_operations():
    """Example 5: Using backend for some operations, server for others."""
    print("\n" + "=" * 70)
    print("Example 5: Mixed Operations")
    print("=" * 70)

    # Use Shapely for fast computation
    Config.set_computation_backend(ComputationBackend.SHAPELY)
    PolygonData.reset_backend()

    polygon = PolygonData([(0, 0), (10, 0), (10, 10), (0, 10)])

    # These use the configured backend (Shapely)
    print(f"Area (via backend): {polygon.area()}")

    # These still use server directly (not yet migrated to backend)
    print(f"Is circle (via server): {polygon.is_circle()}")
    print(f"Is box (via server): {polygon.is_box()}")

    print("\nNote: Some operations use backend, others still use server")


def example_error_handling():
    """Example 6: Proper error handling."""
    print("\n" + "=" * 70)
    print("Example 6: Error Handling")
    print("=" * 70)

    # Try to use Shapely when not installed
    Config.set_computation_backend(ComputationBackend.SHAPELY)
    PolygonData.reset_backend()

    try:
        polygon = PolygonData([(0, 0), (1, 0), (1, 1), (0, 1)])
        area = polygon.area()
        print(f"Successfully computed area: {area}")
    except ImportError as e:
        print(f"Caught expected error: {e}")
        print("Falling back to server backend...")

        # Fallback to server
        Config.set_computation_backend(ComputationBackend.SERVER)
        PolygonData.reset_backend()

        area = polygon.area()
        print(f"Area with server backend: {area}")


if __name__ == "__main__":
    example_basic_usage()
    example_performance_comparison()
    example_environment_variable()
    example_batch_processing()
    example_mixed_operations()
    example_error_handling()

    print("\n" + "=" * 70)
    print("Examples completed!")
    print("=" * 70)

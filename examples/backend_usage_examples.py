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
from ansys.edb.core.geometry.arc_data import ArcData
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

    # Create test polygons with arcs
    num_arc_polygons = 10000
    arc_polygons = []
    for i in range(num_arc_polygons):
        # Create rounded rectangles of varying sizes
        size = 10 + i * 0.1
        arc1 = ArcData((0, 0), (size, 0), height=0.5)
        arc2 = ArcData((size, 0), (size, size), height=0.5)
        arc3 = ArcData((size, size), (0, size), height=0.5)
        arc4 = ArcData((0, size), (0, 0), height=0.5)
        arc_poly = PolygonData(arcs=[arc1, arc2, arc3, arc4])
        arc_polygons.append(arc_poly)

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

    def benchmark_backend_with_arcs(backend_type, backend_name):
        """Run benchmark with arc polygons using a specific backend."""
        Config.set_computation_backend(backend_type)
        PolygonData.reset_backend()

        start = time.time()
        total_area = 0

        for poly in arc_polygons:
            total_area += poly.area()

        elapsed = time.time() - start

        print(f"\n{backend_name} (Arc Polygons):")
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

    # Benchmark arc polygons
    print(f"\n--- Arc Polygon Performance ({num_arc_polygons} polygons) ---")
    server_arc_time = benchmark_backend_with_arcs(ComputationBackend.SERVER, "Server Backend")

    try:
        shapely_arc_time = benchmark_backend_with_arcs(ComputationBackend.SHAPELY, "Shapely Backend")
        speedup_arcs = server_arc_time / shapely_arc_time
        if speedup_arcs > 1:
            print(f"\nSpeedup (Arc Polygons): {speedup_arcs:.1f}x faster with Shapely")
        else:
            slowdown = shapely_arc_time / server_arc_time
            print(f"\nSlowdown (Arc Polygons): {slowdown:.1f}x SLOWER with Shapely")
            print("Note: Shapely doesn't natively support arcs. Arc polygons must be")
            print("      tessellated (converted to many line segments) before Shapely")
            print("      can process them, which adds significant overhead.")
            print("      For arc polygons, the Server backend is recommended.")
    except ImportError:
        print("\nShapely not available for arc polygon comparison")


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


def example_polygon_with_arcs():
    """Example 7: Working with polygons that contain arcs."""
    print("\n" + "=" * 70)
    print("Example 7: Polygon with Arcs")
    print("=" * 70)

    # Initialize EDB
    initialize_edb(__file__)

    # Create a simple polygon with straight edges
    simple_poly = PolygonData([(0, 0), (10, 0), (10, 5), (0, 5)])
    print(f"\nSimple polygon area: {simple_poly.area()}")
    print(f"Has arcs: {simple_poly.has_arcs()}")

    # Create a polygon with arcs using ArcData
    # This creates a rounded rectangle - a rectangle with rounded corners
    arc1 = ArcData((0, 0), (2, 0), height=0.5)  # Bottom edge with arc
    arc2 = ArcData((2, 0), (2, 2), height=0.0)  # Right edge (straight)
    arc3 = ArcData((2, 2), (0, 2), height=0.5)  # Top edge with arc
    arc4 = ArcData((0, 2), (0, 0), height=0.0)  # Left edge (straight)

    rounded_poly = PolygonData(arcs=[arc1, arc2, arc3, arc4])
    print(f"\nRounded polygon area: {rounded_poly.area():.4f}")
    print(f"Has arcs: {rounded_poly.has_arcs()}")
    print(f"Number of arc segments: {len(rounded_poly.arc_data)}")

    # Create a polygon with a circular arc segment
    # This creates a "pie slice" shape
    arc_points = [(0, 0), (5, 0), (5, 5), (0, 5)]
    arc_poly = PolygonData(arc_points)
    # Make one edge curved by reconstructing with arc
    curved_arc = ArcData((5, 0), (0, 5), height=2.0)  # Curved edge
    pie_slice = PolygonData(
        arcs=[
            ArcData((0, 0), (5, 0), height=0),  # Bottom straight
            curved_arc,  # Curved right side
            ArcData((0, 5), (0, 0), height=0),  # Left straight
        ]
    )
    print(f"\nPie slice polygon area: {pie_slice.area():.4f}")
    print(f"Has arcs: {pie_slice.has_arcs()}")

    # Test backend operations on arc polygons
    print("\n--- Testing Backend Operations on Arc Polygons ---")

    # Use AUTO backend
    Config.set_computation_backend(ComputationBackend.AUTO)
    PolygonData.reset_backend()

    print(f"Is (1, 1) inside rounded polygon: {rounded_poly.is_inside((1, 1))}")
    print(f"Is convex (rounded): {rounded_poly.is_convex()}")

    # Convert arc polygon to polygon without arcs (tessellated)
    tessellated = rounded_poly.without_arcs(max_chord_error=0.01)
    print(f"\nTessellated polygon (no arcs):")
    print(f"  Has arcs: {tessellated.has_arcs()}")
    print(f"  Number of points: {len(tessellated.points)}")
    print(f"  Area: {tessellated.area():.4f}")

    # Perform operations with arc polygons
    simple_square = PolygonData([(0.5, 0.5), (1.5, 0.5), (1.5, 1.5), (0.5, 1.5)])
    intersection = PolygonData.intersect(rounded_poly, simple_square)
    print(f"\nIntersection with square:")
    print(f"  Number of resulting polygons: {len(intersection)}")
    if len(intersection) > 0:
        print(f"  First result area: {intersection[0].area():.4f}")


if __name__ == "__main__":
    example_basic_usage()
    example_performance_comparison()
    example_environment_variable()
    example_batch_processing()
    example_mixed_operations()
    example_error_handling()
    example_polygon_with_arcs()

    print("\n" + "=" * 70)
    print("Examples completed!")
    print("=" * 70)

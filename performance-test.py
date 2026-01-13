"""Performance testing script for polygon operations across different computation backends.

This module benchmarks and profiles the convex_hull operation using different backends
(SERVER, SHAPELY, BUILD123D) to identify performance bottlenecks.
"""
import cProfile
from io import StringIO
import os
import pstats

from ansys.edb.core.config import ComputationBackend, Config
from ansys.edb.core.geometry.arc_data import ArcData
from ansys.edb.core.session import launch_session
from tests.backends.utils.fixtures import create_polygon

os.environ["ANSYSEM_EDB_EXE_DIR"] = r"C:\Program Files\ANSYS Inc\v262\AnsysEM"
if "ANSYSEM_EDB_EXE_DIR" in os.environ:
    EXE_DIR = os.environ["ANSYSEM_EDB_EXE_DIR"]
else:
    EXE_DIR = None
session = launch_session(EXE_DIR)

# Define a test polygon with arcs
polygon_def = {
    "data": [
        ArcData((0, 0), (10, 0), height=-5.0),
        ArcData((10, 0), (10, 10), height=0.0),
        ArcData((10, 10), (0, 10), height=5.0),
        ArcData((0, 10), (0, 0), height=0.0),
    ]
}

# Number of iterations for performance testing
NUM_ITERATIONS = 1000

print(f"Performance test: Computing area {NUM_ITERATIONS} times")
print("=" * 60)

# Test each backend
backends = [ComputationBackend.SERVER, ComputationBackend.SHAPELY, ComputationBackend.BUILD123D]

for backend in backends:
    Config.set_computation_backend(backend)

    # Create polygon with the selected backend
    polygon = create_polygon(polygon_def)

    # Profile the move operation
    print(f"\n{backend.name} Backend:")
    print("Running profiler to identify bottleneck...")

    profiler = cProfile.Profile()
    profiler.enable()

    for _ in range(NUM_ITERATIONS):
        polygon.convex_hull([polygon])

    profiler.disable()

    # Print basic profiling results to console
    s = StringIO()
    ps = pstats.Stats(profiler, stream=s)
    ps.sort_stats("cumulative")
    ps.print_stats(20)
    print(s.getvalue())

    # Save detailed profiling data to file
    profile_filename = f"profile_{backend.name.lower()}.prof"
    profiler.dump_stats(profile_filename)
    print(f"\nProfile data saved to: {profile_filename}")

print("\n" + "=" * 60)

# Generate HTML visualization
print("\n" + "=" * 60)
print("Generating HTML visualization...")

# try:
#     # Try to import snakeviz
#     import snakeviz

#     for backend in backends:
#         profile_filename = f"profile_{backend.name.lower()}.prof"
#         print(f"\nOpening {profile_filename} in browser with snakeviz...")
#         print("(Close the browser tab when done to continue)")

#         # Open snakeviz in browser
#         subprocess.run([sys.executable, "-m", "snakeviz", profile_filename])

# except ImportError:
#     print("\nsnakeviz not installed. Installing it now...")
#     subprocess.run([sys.executable, "-m", "pip", "install", "snakeviz"])
#     print("\nTo view the profile data in your browser, run:")
#     for backend in backends:
#         profile_filename = f"profile_{backend.name.lower()}.prof"
#         print(f"  python -m snakeviz {profile_filename}")
# except Exception as e:
#     print(f"\nCouldn't automatically open visualization: {e}")
#     print("\nTo view the profile data in your browser, run:")
#     for backend in backends:
#         profile_filename = f"profile_{backend.name.lower()}.prof"
#         print(f"  python -m snakeviz {profile_filename}")

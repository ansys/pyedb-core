"""Installation file for the ansys-api-edb-v1 package"""

import glob
import os
import re

from setuptools import setup
from setuptools.command.develop import develop

install_requires = ["grpcio==1.39.0", "grpcio-tools==1.39.0", "protobuf>=3.20,<4"]

# Get the long description from the README file
HERE = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(HERE, "README.rst"), encoding="utf-8") as fd:
    long_description = fd.read()

desc = "python gRPC interface package for ansys-api-edb-v1"


def compile_proto():
    """Compile proto files."""
    package_name = "ansys.api.edb.v1"
    proto_dir = os.path.join(os.getcwd(), *package_name.split("."))
    proto_files = os.path.join(proto_dir, "*.proto")
    out_dir = proto_dir

    # import grpc_tools

    cmds = [
        "python",
        "-m grpc_tools.protoc",
        f"-I {proto_dir}",
        f"--python_out={out_dir}",
        f"--grpc_python_out={out_dir}",
        proto_files,
    ]
    cmd = " ".join(cmds)
    os.system(cmd)

    replace_imports(package_name)


def replace_imports(package_name):
    """Replace relative imports from auto-generated pb2 files with absolute imports."""
    root = os.path.join(os.getcwd(), *package_name.split("."))
    files_path = os.path.join(root, "*.py")
    files = glob.glob(files_path, recursive=True)
    source = {}
    for filename in files:
        relative_path = filename.replace(root, "")
        module_name = ".".join(re.split(r"\\|/", relative_path))
        module_name = module_name.rstrip(".py")
        module_name = module_name.strip(".")
        source[module_name] = open(filename).read()

    packages = set()
    for module_name in source:
        find_str = "import %s" % module_name
        repl_str = "import %s.%s" % (package_name, module_name)
        packages.add(package_name)

        for mod_name, mod_source in source.items():
            source[mod_name] = mod_source.replace(find_str, repl_str)

    for module_name, module_source in source.items():
        relative_module_path = module_name.split(".")
        relative_module_path[-1] = "%s.py" % relative_module_path[-1]
        filename = os.path.join(root, *relative_module_path)

        with open(filename, "w") as f:
            f.write(module_source)


class CustomDevelopCommand(develop):
    """Custom command that also compiles proto files on editable mode."""

    def run(self):
        """Compile proto files before proceeding."""
        compile_proto()
        develop.run(self)


setup(
    name="ansys-api-edb-v1",
    packages=["ansys.api.edb.v1"],
    version="0.0.0",
    license="MIT",
    url="https://github.com/pyansys/",
    author="Ansys Inc.",
    author_email="support@ansys.com",
    description=desc,
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires=">=3.5.*",
    install_requires=install_requires,
    cmdclass={"develop": CustomDevelopCommand},
)

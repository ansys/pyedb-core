# Copyright (C) 2024 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""A pre-commit hook script for cleaning Jupyter notebooks by resetting execution counts, removing outputs, and removing metadata."""  # noqa: E501

import argparse
import json
from pathlib import Path
import sys


def _clean_notebook(path: Path, leave_outputs: bool):
    """Clean an ipynb file and return True if it was modified, None on error, otherwise False."""
    modified = False
    try:
        with open(path) as input_file:
            data = json.load(input_file)
        execution_order = 1
        if "metadata" in data and data["metadata"]:
            data["metadata"] = {}
            modified = True
        for cell in data["cells"]:
            if "execution_count" in cell:
                if leave_outputs:
                    if cell["execution_count"] != execution_order:
                        cell["execution_count"] = execution_order
                        modified = True
                    execution_order += 1
                else:
                    if cell["execution_count"] is not None:
                        cell["execution_count"] = None
                        modified = True
            if "metadata" in cell and cell["metadata"]:
                cell["metadata"] = {}
                modified = True
            if not leave_outputs and "outputs" in cell and cell["outputs"]:
                cell["outputs"] = []
                modified = True
        if modified:
            print(path)
            with open(path, "w") as output_file:
                json.dump(data, output_file, indent=1)
    except Exception as e:
        print("Unexpected exception: {}".format(e))
        return None
    return modified


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--leave-outputs", action="store_true", default=False, help="leave cell outputs as-is"
    )
    parser.add_argument("files", help="ipynb files to process", nargs=argparse.REMAINDER)
    arguments = parser.parse_args()
    files_modified = False
    for file in arguments.files:
        path = Path(file)
        if not path.is_file() or path.suffix != ".ipynb":
            continue
        result = _clean_notebook(path, arguments.leave_outputs)
        if result is None:
            print("_clean_notebook failed on {}".format(path))
            sys.exit(2)
        files_modified = result

    sys.exit(int(files_modified))

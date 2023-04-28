"""A pre-commit hook script for cleaning Jupyter notebooks by resetting execution counts, removing outputs, and removing metadata."""  # noqa: E501

import json
from pathlib import Path
import sys


def _clean_notebook(path: Path):
    """Clean an ipynb file and return True if it was modified, None on error, otherwise False."""
    result = False
    try:
        with open(path) as input_file:
            data = json.load(input_file)
        for cell in data["cells"]:
            if "execution_count" in cell and cell["execution_count"] is not None:
                cell["execution_count"] = None
                result = True
            if "metadata" in cell and cell["metadata"]:
                cell["metadata"] = {}
                result = True
            if "outputs" in cell and cell["outputs"]:
                cell["outputs"] = []
                result = True
        if result:
            print(path)
            with open(path, "w") as output_file:
                json.dump(data, output_file, indent=1)
    except Exception as e:
        print("Unexpected exception: {}".format(e))
        return None
    return result


if __name__ == "__main__":
    files_modified = False
    for file in sys.argv[1:]:
        path = Path(file)
        if not path.is_file() or path.suffix != ".ipynb":
            continue
        result = _clean_notebook(path)
        if result is None:
            print("_clean_notebook failed")
            sys.exit(2)
        files_modified = result

    sys.exit(int(files_modified))

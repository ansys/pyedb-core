#!/bin/bash

# Helper function for printing colored text
function print_colored_text() {
  BEGIN_FORMAT='\033['
  END_FORMAT='\033[0m'
  COLOR=""
  if [[ "$1" == "red" ]]; then
    COLOR='0;31'
  elif [[ "$1" == "green" ]]; then
    COLOR='0;32'
  fi
  echo -e "${BEGIN_FORMAT}${COLOR}m${2}${END_FORMAT}"
}

# Helper function for printing error messages
function print_error_msg() {
  print_colored_text "red" "$1"
}

# Helper function for printing info messages
function print_info_msg() {
  print_colored_text "green" "$1"
}

# Check if the ansys-api-edb repository exists
if [[ -z ${ANSYS_API_EDB_REPO_PATH} ]]; then
  print_error_msg "Please set the environment variable ANSYS_API_EDB_REPO_PATH to the path of the ansys-api-edb repository on your system."
  exit 1
fi

# Make sure the ansys-api-edb repo path is the proper format
cleaned_ansys_api_edb_repo_path=$(echo "$ANSYS_API_EDB_REPO_PATH" | tr '\\' '/')

# check if the virtual environment exists
VENV_DIR="venv"
VENV_EXISTS=false
if [ -d "$VENV_DIR" ]; then
  VENV_EXISTS=true
fi

# Create the virtual environment if it doesn't exist
if $VENV_EXISTS; then
  print_info_msg "python virtual environment already exists and will be reused"
else
  print_info_msg "Creating new python virtual environment..."
  python -m venv $VENV_DIR
fi

# Set the python venv directory
PY_DIR="$VENV_DIR/Scripts/"
if [[ "$OSTYPE" == linux-gnu ]]; then
  PY_DIR="$VENV_DIR/bin"
fi

# install proto parser utils if needed
proto_parser_utils_dir=$cleaned_ansys_api_edb_repo_path/proto_parser
if [ "$VENV_EXISTS" = false ]; then
  print_info_msg "Installing proto parser utils package in python virtual environment..."
  "$PY_DIR/pip" install $proto_parser_utils_dir

  # Clean up proto parser utils build artifacts
  print_info_msg "Cleaning up proto parser utils build artifacts..."
  rm -rf $proto_parser_utils_dir/ansys_api_edb_proto_parser.egg-info $proto_parser_utils_dir/build
fi

# Run the script
print_info_msg "Parsing proto files..."
"$PY_DIR/python" generate_rpc_info.py

# Run pre-commit hooks on the rpc_info.py files
print_info_msg "Running pre-commit hooks..."
pre-commit run --files ../../src/ansys/edb/core/inner/rpc_info.py

# Done
print_info_msg "Finished parsing proto files"
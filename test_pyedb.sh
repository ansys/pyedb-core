#!/bin/bash

current_script_dir=$(dirname $0)
pushd ${current_script_dir}
current_script_dir=${PWD}

isWindows=true
isLinux=false
# Set up the python virtual environment
if [[ "$(uname -s)" = "Linux" ]]; then
  isWindows=false
  isLinux=true
  python3 -m venv .venv && source .venv/bin/activate
else
  python -m venv .venv && source .venv/Scripts/activate
fi

# Set up the .env.test file so we know where to find the install
env_test=${current_script_dir}/.env.test
if [ ! -f "${env_test}" ]; then
  echo "Creating ${env_test} file"
  cp .env.test.example "${env_test}" -rp
  if [[ -z "${RPC_SERVER_ROOT}" ]]; then
    if ${isWindows} && [[ ! -z "${ANSYSEM_ROOT231}" ]]; then
      RPC_SERVER_ROOT="${ANSYSEM_ROOT231}"
    else
      echo "***[ERROR]: Environment variable \$RPC_SERVER_ROOT is not set. Please add this to ${env_test} ***";
      exit 1
    fi
  fi
  if ${isWindows}; then
    RPC_SERVER_ROOT="${RPC_SERVER_ROOT//\\//}/"
  fi
  sed -i "s|RPC_SERVER_ROOT|RPC_SERVER_ROOT=${RPC_SERVER_ROOT}|g" "${env_test}"
fi

# Run tox
python -m pip install --upgrade -r requirements/requirements_tox.txt
python -m tox -e test

popd

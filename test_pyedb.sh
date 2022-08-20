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
# Need the -r to make tox recompile proto files, since they are typically changed commit-to-commit and sometimes we end
# up with failing tests
python -m tox -re test

popd

# Post reports to ARM
junit_xml=${current_script_dir}/junit/test-results.xml
if [[ -f "${junit_xml}" ]]; then
  RPC_SERVER_ROOT="$(grep RPC_SERVER_ROOT "${env_test}" | sed -e 's/RPC_SERVER_ROOT=//'g )"
  if ${isWindows}; then
    arm_dir=//smb.cdcislcore.ansys.com/ARM/ARM
    RPC_SERVER_ROOT="${RPC_SERVER_ROOT//\\//}/"
  else
    arm_dir=/nfs/cdcisldev/ARM/ARM
  fi
  junit_to_arm=${arm_dir}/SharedTools/ReportConversion/JUnitToARM/JUnitToARM.py
  output=${current_script_dir}/junit/ARMResults
  report_list_xml=${output}/ARM_report_list.xml
  arm_settings_src=${current_script_dir}/tests/utils/arm_settings.xml
  arm_settings=${output}/arm_settings.xml
  rm -rf ${output}
  mkdir -p ${output}
  echo "Creating ARM settings file"
  if ${isWindows}; then
    output_win_style="$(cygpath -w ${output})"
    output_win_style="${output_win_style//\\//}/"
    sed "s|@@WORKING_DIR@@|${output_win_style}|g" "${arm_settings_src}" > "${arm_settings}"
  else
    sed "s|@@WORKING_DIR@@|${output}|g" "${arm_settings_src}" > "${arm_settings}"
  fi
  echo "Creating ARM reports"
  python ${junit_to_arm} --junit_xml=${junit_xml} --product=EDT_LAYOUT --install="${RPC_SERVER_ROOT}" --output=${output} --suite=pyedb --report_list_xml=${report_list_xml} >> ${output}/JUnitToARM.log
  post_report_path="java -cp ${arm_dir}/ARMRoot/TestHarness/ARM.TestHarness.jar com.ansys.arm.ReportPoster"
  echo "Posting ARM reports"
  ${post_report_path} --settings ${arm_settings} --file ${report_list_xml} >> ${output}/ARMreportPoster.log
  # -h: Don't show filename; sort -u: Show unique lines
  grep "Queue Run:" ${output}/*/*.post -h | sort -u
fi

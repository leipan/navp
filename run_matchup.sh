#!/bin/bash
BASE_PATH=$(dirname "${BASH_SOURCE}")
BASE_PATH=$(cd "${BASE_PATH}"; pwd)

# source environment
source $HOME/verdi/bin/activate

echo "##########################################" 1>&2
echo -n "Running WVCC matchup: " 1>&2
date 1>&2
cd $HOME/data
python $BASE_PATH/../CrIS_VIIRS_collocation-master/code_test_QY.py
STATUS=$?
echo -n "Finished running WVCC matchup: " 1>&2
date 1>&2
if [ $STATUS -ne 0 ]; then
  echo "Failed to run WVCC matchup." 1>&2
  cat code_test.log 1>&2
  echo "{}"
  exit $STATUS
fi

#!/bin/bash
BASE_PATH=$(dirname "${BASH_SOURCE}")
BASE_PATH=$(cd "${BASE_PATH}"; pwd)

# source environment
source $HOME/verdi/bin/activate

echo "##########################################"
echo -n "Running WVCC matchup: "
date
cd $HOME/data
python $BASE_PATH/../CrIS_VIIRS_collocation-master/code_test_QY.py
STATUS=$?
echo -n "Finished running WVCC matchup: "
date
if [ $STATUS -ne 0 ]; then
  echo "Failed to run WVCC matchup."
  exit $STATUS
fi

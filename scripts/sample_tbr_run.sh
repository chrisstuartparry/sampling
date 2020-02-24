#!/bin/bash

export SINGULARITY_TMPDIR=/share/rcifdata/pmanek/singularity/tmpdir
export SINGULARITY_CACHEDIR=/share/rcifdata/pmanek/singularity/cache
export MAIN_DIR=/share/rcifdata/pmanek/fusion
export TIME_SPIN_UP=5 # seconds
export RUN_NO=0
export BATCH_NO=$1 ; shift # TODO: make clear that this is a parameter
export RUN_DIR=${MAIN_DIR}/data/run${RUN_NO}
export IMAGE_NAME=tbr26.sif

set -e

cp ${MAIN_DIR}/images/${IMAGE_NAME} /tmp/${IMAGE_NAME}

cd /tmp
source ${MAIN_DIR}/sampling/venv/bin/activate

echo "Running simulation server"
singularity exec /tmp/${IMAGE_NAME} python3 /app/simple_sphere_TBR_study/flask_api_for_tbr_simulation.py &

echo "Sleeping ${TIME_SPIN_UP} seconds"
sleep ${TIME_SPIN_UP}

echo "Collecting samples"
python ${MAIN_DIR}/sampling/scripts/run_sim_job.py --batch ${BATCH_NO} --in-dir ${RUN_DIR} --out-dir ${RUN_DIR}

echo "Stopping simulation server"
kill %1
wait < <(jobs -p)

deactivate

rm -f /tmp/${IMAGE_NAME}
echo "Done"

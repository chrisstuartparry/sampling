#!/bin/bash
#SBATCH -p RCIF
#SBATCH -N 1
#SBATCH -c 40
#SBATCH --time=04:00:00
#SBATCH --array=0-99

export OMP_NUM_THREADS=$SLURM_JOB_CPUS_PER_NODE

srun -n1 ~/fusion/sample_tbr_run.sh $SLURM_ARRAY_TASK_ID

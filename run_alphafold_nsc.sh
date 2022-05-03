#!/bin/bash
#SBATCH --gpus 1
#SBATCH -t 480


module load Anaconda/2021.05-nsc1
module load buildenv-gcccuda/11.4-8.3.1-bare

export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/software/sse/manual/CUDA/11.4.2_470.57.02/lib64/
export XLA_FLAGS=--xla_gpu_cuda_data_dir=$CUDA_PATH
export PATH="/proj/wallner-b/apps/hmmer-3.2.1/bin/:/proj/wallner-b/apps/hhsuite/bin/:/proj/wallner-b/apps/kalign/src/:$PATH"

# See https://github.com/huggingface/transformers/issues/14907 for jax update
export TF_FORCE_UNIFIED_MEMORY=1
export XLA_PYTHON_CLIENT_MEM_FRACTION=10.0
echo $XLA_FLAGS

conda activate /proj/wallner-b/users/x_bjowa/.conda/envs/alphafold/
which python
nvidia-smi
echo Running CMD: python /proj/wallner-b/apps/alphafoldv2.1.0/run_alphafold.py $@
python /proj/wallner-b/apps/alphafoldv2.1.0/run_alphafold.py $@


#!/bin/bash
## Notes: run as bash
[ ! -d app/zlog ] && mkdir app/zlog
# Note: pass the gpu_id as the only one argument to this .sh, such as: 
# bash run_colabfold.sh 0
if [ $# -ne 1 ]; then echo 'args num is not 1'; exit 1; fi
export CUDA_VISIBLE_DEVICES=$1
nohup python run.py \
> app/ColabFold_batch.log 2>&1 &

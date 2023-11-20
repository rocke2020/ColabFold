#!/bin/bash
## Notes: run as bash
[ ! -d app/zlog ] && mkdir app/zlog
gpu_id=1
export CUDA_VISIBLE_DEVICES=$gpu_id
nohup python app/colabFold_batch_runner.py \
> app/ColabFold_batch-gpu_id$gpu_id.log 2>&1 &

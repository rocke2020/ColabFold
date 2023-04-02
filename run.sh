[ ! -d app/zlog ] && mkdir app/zlog
if [ $# -eq 2 ]; then echo 'args num is not 2'; exit 1; fi
export CUDA_VISIBLE_DEVICES=$1
# [ -f app/af_out/1awr_C_I/log.log ] && rm app/af_out/1awr_C_I/log.log
[ -d app/af_out/1awr_C_I ] && sudo rm -rf app/af_out/1awr_C_I
nohup python run.py \
> app/zlog/AlphaFold2_batch.log 2>&1 &

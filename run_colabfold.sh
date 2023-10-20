[ ! -d app/zlog ] && mkdir app/zlog
export CUDA_VISIBLE_DEVICES=$1
# [ -f app/af_out/1awr_C_I/log.log ] && rm app/af_out/1awr_C_I/log.log
# [ -d app/af_out/1awr_C_I ] && sudo rm -rf app/af_out/1awr_C_I
# [ -d app/af_out/pos_complex_in_one_seq ] && sudo rm -rf app/af_out/pos_complex_in_one_seq
nohup python run.py \
> app/AlphaFold2_batch.log 2>&1 &

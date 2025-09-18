#!/bin/bash
for i in {1..10}
do
    nohup python -u auto_eval.py \
        --process_dir ../results/subset100_batch${i} \
        --api_model gpt-4.1-2025-04-14\
        --max_attached_imgs 20 > subset100_batch${i}_evaluation.log &
done
#!/bin/bash
for i in {1..10}
do
    nohup python -u auto_eval.py \
        --process_dir ../results/.__data__subset50_batch${i} \
        --api_model gpt-4.1-2025-04-14\
        --max_attached_imgs 15 > subset50_batch${i}_evaluation.log &
done
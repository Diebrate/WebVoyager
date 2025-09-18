#!/bin/bash
for i in {1..10}
do
    nohup python -u run.py \
        --test_file ./data/subset100.jsonl \
        --headless \
        --max_iter 20 \
        --max_attached_imgs 3 \
        --temperature 1 \
        --fix_box_color \
        --api_model gpt-4.1-2025-04-14 \
        --seed ${i} > logs/subset100_batch_${i}.log \
        --batch_id ${i} &
done
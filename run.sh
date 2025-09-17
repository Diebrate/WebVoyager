#!/bin/bash
nohup python -u run.py \
    --test_file ./data/subset.jsonl \
    --headless \
    --max_iter 15 \
    --max_attached_imgs 3 \
    --temperature 1 \
    --fix_box_color \
    --api_model gpt-4.1-2025-04-14 \
    --seed 42 > test_tasks.log &

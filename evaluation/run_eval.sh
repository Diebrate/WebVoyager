#!/bin/bash
nohup python -u auto_eval.py \
    --process_dir ../results/20250905_12_22_59 \
    --api_model gpt-4o \
    --max_attached_imgs 15 > evaluation.log &
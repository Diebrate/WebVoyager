#!/bin/bash
nohup python -u auto_eval.py \
    --process_dir ../results/tasks_test_batch0 \
    --api_model gpt-4o \
    --max_attached_imgs 15 > tasks_test__batch0_evaluation.log &
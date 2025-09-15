import json
import pathlib
import re

import numpy as np

np.random.seed(1234)

ROOT_PATH = pathlib.Path(__file__).parent
DATA_PATH = ROOT_PATH / 'data'
EVAL_PATH = ROOT_PATH / 'evaluation'

def load_json(file_name):
    with open(DATA_PATH / file_name, 'r') as f:
        return json.load(f)
    
def save_json(data, file_name):
    with open(DATA_PATH / file_name, 'w') as f:
        json.dump(data, f, indent=4)

def load_jsonl(file_name):
    data = []
    with open(DATA_PATH / file_name, 'r') as f:
        for line in f:
            data.append(json.loads(line))
    return data

def save_jsonl(data, file_name):
    with open(DATA_PATH / file_name, 'w') as f:
        for entry in data:
            f.write(json.dumps(entry) + '\n')

def sample_jsonl(input_file, output_file, sample_size):
    data = load_jsonl(input_file)
    sampled_data = np.random.choice(data, size=sample_size, replace=False)
    save_jsonl(sampled_data, output_file)

def parse_evaluation_log_to_jsonl(log_path, output_jsonl_path, return_results=False):
    with open(log_path, 'r') as f:
        lines = f.readlines()

    results = []
    task_type = None
    task_id = None
    success = None

    for line in lines:
        # Match the start of a task block
        m = re.match(r'-+ \.\./results/([^/]+)/task([A-Za-z0-9 ]+)--(\d+) ', line)
        if m:
            job_name = m.group(1).strip()
            task_type = m.group(2).strip()
            task_id = m.group(3).strip()
            success = None  # Reset for new task
        elif 'Auto_eval_res: 1' in line:
            success = 1
        elif 'Auto_eval_res: 0' in line or 'Not find answer for' in line:
            success = 0

        # If we have all fields, save the result
        if task_type and task_id and success is not None:
            results.append({
                "task_type": task_type,
                "task_id": task_id,
                "success": success
            })
            interaction_path = ROOT_PATH / 'results' / job_name / f'task{task_type}--{task_id}' / 'interact_messages.json'
            interactions = extract_confidence_completion(interaction_path)
            results[-1]["interactions"] = interactions
            task_type = None
            task_id = None
            success = None

    if return_results:
        return results
    # Write to JSONL
    with open(output_jsonl_path, 'w') as f:
        for entry in results:
            f.write(json.dumps(entry) + '\n')

def extract_confidence_completion(json_path):
    with open(json_path, 'r') as f:
        messages = json.load(f)
    interactions = []
    for msg in messages:
        if msg.get("role") == "assistant":
            content = msg.get("content", "")
            # Try to extract Confidence and Completion from the text
            try:
                # Use regex or simple parsing
                conf_line = next(line for line in content.split('\n') if line.strip().startswith("Confidence:"))
                comp_line = next(line for line in content.split('\n') if line.strip().startswith("Completion:"))
                confidence = float(conf_line.split(":", 1)[1].strip())
                completion = float(comp_line.split(":", 1)[1].strip())
                interactions.append({"confidence": confidence, "completion": completion, "probability": msg.get("prob", None)})
            except Exception:
                continue
    return interactions

def parse_batch_output(batch_name, size, output_jsonl_path):
    results = []
    for i in range(1, size + 1):
        log_path = EVAL_PATH / f"{batch_name}_batch{i}_evaluation.log"
        if not log_path.exists():
            continue
        tmp = parse_evaluation_log_to_jsonl(log_path, None, return_results=True)
        if not tmp:
            continue
        if not results:
            results = tmp.copy()
            for res in results:
                res["success"] = [res["success"]]
                res["interactions"] = [res["interactions"]]
            continue
        for res, entry in zip(results, tmp):
            res["success"].append(entry["success"])
            res["interactions"].append(entry["interactions"])
    with open(output_jsonl_path, 'w') as f:
        for entry in results:
            f.write(json.dumps(entry) + '\n')

import argparse
import sys
import os
import json

TASKS_FILE = "tasks.json"

def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, "r") as file:
        return json.load(file)

def save_task(tasks):
    with open(TASKS_FILE, "w") as file:
        json.dump(tasks, file, indent=2)

parser = argparse.ArgumentParser()
parser.add_argument("task", type=str, nargs="?", help="Task to add")
parser.add_argument("-l", "--list", action="store_true", help="List all tasks")
args = parser.parse_args()

if len(sys.argv) == 1:
    parser.print_help(sys.stderr)
    sys.exit(1)

if args.list:
    tasks = load_tasks()
    for task in tasks:
        status = "x" if task["done"] else " "
        print(f"{status} {task['id']}: {task['task']}")
    sys.exit(0)
elif args.task:
    tasks = load_tasks()
    if len(tasks) == 0:
        new_id = 1
    else:
        new_id = tasks[-1]["id"] + 1
    tasks.append({"id": new_id, "task": args.task, "done": False})
    save_task(tasks)

    print(f"Task {args.task} added with ID of {new_id}")

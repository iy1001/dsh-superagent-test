#!/usr/bin/env python3
"""A small task tracker CLI.

Tasks are stored in ``tasks.json`` in the current working directory.
Each task has an integer ``id``, a ``title``, a ``status`` (``open`` or
``done``) and an ISO 8601 ``created`` timestamp.
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone

TASKS_FILE = "tasks.json"


def load_tasks(path=TASKS_FILE):
    """Load the task list from ``path``.

    Returns an empty list when the file does not exist or is empty.
    """
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as handle:
        content = handle.read().strip()
    if not content:
        return []
    return json.loads(content)


def save_tasks(tasks, path=TASKS_FILE):
    """Write ``tasks`` to ``path`` as JSON."""
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(tasks, handle, indent=2)
        handle.write("\n")


def next_id(tasks):
    """Return the next available integer task id."""
    if not tasks:
        return 1
    return max(task["id"] for task in tasks) + 1


def add_task(title, path=TASKS_FILE):
    """Add a new open task with ``title`` and return it."""
    tasks = load_tasks(path)
    task = {
        "id": next_id(tasks),
        "title": title,
        "status": "open",
        "created": datetime.now(timezone.utc).isoformat(),
    }
    tasks.append(task)
    save_tasks(tasks, path)
    return task


def list_tasks(path=TASKS_FILE):
    """Return all tasks in storage order."""
    return load_tasks(path)


def mark_done(task_id, path=TASKS_FILE):
    """Mark the task with ``task_id`` done.

    Returns the updated task, or ``None`` when no such task exists.
    """
    tasks = load_tasks(path)
    for task in tasks:
        if task["id"] == task_id:
            task["status"] = "done"
            save_tasks(tasks, path)
            return task
    return None


def remove_task(task_id, path=TASKS_FILE):
    """Remove the task with ``task_id``.

    Returns the removed task, or ``None`` when no such task exists.
    """
    tasks = load_tasks(path)
    for index, task in enumerate(tasks):
        if task["id"] == task_id:
            del tasks[index]
            save_tasks(tasks, path)
            return task
    return None


def format_task(task):
    """Format a task as ``<id>\\t<status>\\t<title>``."""
    return "{}\t{}\t{}".format(task["id"], task["status"], task["title"])


def build_parser():
    parser = argparse.ArgumentParser(
        prog="tasktracker",
        description="A small task tracker CLI.",
    )
    subparsers = parser.add_subparsers(dest="command", metavar="<command>")
    subparsers.required = True

    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("title", help="Title of the task to add")

    subparsers.add_parser("list", help="List all tasks")

    done_parser = subparsers.add_parser("done", help="Mark a task as done")
    done_parser.add_argument("id", type=int, help="Id of the task to mark done")

    remove_parser = subparsers.add_parser("remove", help="Remove a task")
    remove_parser.add_argument("id", type=int, help="Id of the task to remove")

    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "add":
        task = add_task(args.title)
        print("Added task {}".format(task["id"]))
    elif args.command == "list":
        for task in list_tasks():
            print(format_task(task))
    elif args.command == "done":
        task = mark_done(args.id)
        if task is None:
            print("No task with id {}".format(args.id), file=sys.stderr)
            return 1
        print("Done task {}".format(task["id"]))
    elif args.command == "remove":
        task = remove_task(args.id)
        if task is None:
            print("No task with id {}".format(args.id), file=sys.stderr)
            return 1
        print("Removed task {}".format(task["id"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())

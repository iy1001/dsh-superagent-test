"""Tests for tasktracker.py."""

import json
import os
import tempfile
import unittest

import tasktracker


class TaskTrackerTest(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.path = os.path.join(self.tmpdir.name, "tasks.json")

    def tearDown(self):
        self.tmpdir.cleanup()

    def test_add_creates_task(self):
        task = tasktracker.add_task("Write report", path=self.path)

        self.assertEqual(task["id"], 1)
        self.assertEqual(task["title"], "Write report")
        self.assertEqual(task["status"], "open")
        self.assertIn("created", task)
        # A valid ISO 8601 round-trip timestamp.
        from datetime import datetime

        datetime.fromisoformat(task["created"])

        with open(self.path, encoding="utf-8") as handle:
            stored = json.load(handle)
        self.assertEqual(len(stored), 1)
        self.assertEqual(stored[0]["title"], "Write report")

    def test_add_assigns_incrementing_ids(self):
        first = tasktracker.add_task("One", path=self.path)
        second = tasktracker.add_task("Two", path=self.path)

        self.assertEqual(first["id"], 1)
        self.assertEqual(second["id"], 2)

    def test_list_returns_tasks_in_order(self):
        tasktracker.add_task("First", path=self.path)
        tasktracker.add_task("Second", path=self.path)

        tasks = tasktracker.list_tasks(path=self.path)

        self.assertEqual([task["title"] for task in tasks], ["First", "Second"])

    def test_list_empty_when_missing_file(self):
        self.assertEqual(tasktracker.list_tasks(path=self.path), [])

    def test_done_marks_task_complete(self):
        task = tasktracker.add_task("Finish me", path=self.path)

        updated = tasktracker.mark_done(task["id"], path=self.path)

        self.assertIsNotNone(updated)
        self.assertEqual(updated["status"], "done")
        tasks = tasktracker.list_tasks(path=self.path)
        self.assertEqual(tasks[0]["status"], "done")

    def test_done_unknown_id_returns_none(self):
        self.assertIsNone(tasktracker.mark_done(99, path=self.path))

    def test_format_task(self):
        task = {"id": 3, "title": "Hi", "status": "open", "created": "x"}
        self.assertEqual(tasktracker.format_task(task), "3\topen\tHi")


if __name__ == "__main__":
    unittest.main()

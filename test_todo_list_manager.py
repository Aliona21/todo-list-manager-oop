import unittest
import datetime
from task import Task
from todo_list_manager import TodoListManager
import os

class TestTodoListManager(unittest.TestCase):
    def setUp(self):
        self.manager = TodoListManager()
        self.task1 = Task("Buy groceries", False, 1, datetime.date(2025, 12, 25))
        self.task2 = Task("Write report", True, 2, datetime.date(2025, 12, 26))
        self.task3 = Task("Call John", False, 3, None)
        self.task4 = Task("Pay bills", False, None, datetime.date(2025, 10, 30))
        self.task5 = Task("Write a very long report", True, 1, datetime.date(2025, 11, 15))

    def test_add_task(self):
        self.manager.add_task("Buy groceries", 1, datetime.date(2025, 12, 25))
        self.assertEqual(len(self.manager.tasks), 1)
        self.assertEqual(self.manager.tasks[0], self.task1)

        with self.assertRaises(TypeError):
            self.manager.add_task(123)
        with self.assertRaises(ValueError):
            self.manager.add_task("")
        with self.assertRaises(TypeError):
            self.manager.add_task("Task", "invalid")
        with self.assertRaises(ValueError):
            self.manager.add_task("Task", 4)
        with self.assertRaises(TypeError):
            self.manager.add_task("Task", 1, "invalid")

    def test_list_tasks(self):
        self.manager.add_task("Buy groceries", 1, datetime.date(2025, 12, 25))
        self.manager.add_task("Write report", True, 2, datetime.date(2025, 12, 26))
        expected_output = "To-Do List:\n1. [ ] Buy groceries | Priority: High | Deadline: 2025-12-25\n2. [X] Write report | Priority: Medium | Deadline: 2025-12-26\n"
        self.assertEqual(self.manager.list_tasks(), expected_output)
        self.manager.tasks = []
        self.assertEqual(self.manager.list_tasks(), "No tasks in the to-do list.")

    def test_mark_task_as_done(self):
        self.manager.tasks.extend([self.task1, self.task2])
        self.manager.mark_task_as_done(1)
        self.assertTrue(self.manager.tasks[0].is_done)
        self.assertTrue(self.manager.tasks[1].is_done)

        with self.assertRaises(TypeError):
            self.manager.mark_task_as_done("invalid")
        with self.assertRaises(IndexError):
            self.manager.mark_task_as_done(3)
        with self.assertRaises(IndexError):
            self.manager.mark_task_as_done(0)

    def test_delete_task(self):
        self.manager.tasks.extend([self.task1, self.task2, self.task3])
        self.manager.delete_task(2)
        self.assertEqual(len(self.manager.tasks), 2)
        self.assertEqual(self.manager.tasks[0], self.task1)
        self.assertEqual(self.manager.tasks[1], self.task3)

        with self.assertRaises(TypeError):
            self.manager.delete_task("invalid")
        with self.assertRaises(IndexError):
            self.manager.delete_task(3)
        with self.assertRaises(IndexError):
            self.manager.delete_task(0)

    def test_save_and_load_tasks(self):
        self.manager.tasks = [self.task1, self.task2, self.task3, self.task4, self.task5]
        self.manager.save_to_file("test_todo_list.csv")

        new_manager = TodoListManager()
        new_manager.load_from_file("test_todo_list.csv")
        self.assertEqual(new_manager.tasks, [self.task1, self.task2, self.task3, self.task4, self.task5])

        # test that file not found does not raise error
        new_manager.load_from_file("nonexistent_file.csv")

        with self.assertRaises(TypeError):
            self.manager.save_to_file(123)
        with self.assertRaises(TypeError):
            self.manager.load_from_file(123)
        if os.path.exists("test_todo_list.csv"):
            os.remove("test_todo_list.csv")
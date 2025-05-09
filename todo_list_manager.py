#This module defines the TodoListManager class.

import datetime
from typing import List, Optional
from task import Task  # Import the Task class from task.py
import abc

# Define an interface for saving tasks
class TaskSaver(abc.ABC):
    @abc.abstractmethod
    def save(self, tasks: List[Task], filename: str) -> None:
        pass

# Implement concrete strategies for saving tasks
class TextTaskSaver(TaskSaver):
    def save(self, tasks: List[Task], filename: str) -> None:
        """Saves tasks to a plain text file."""
        if not isinstance(filename, str):
            raise TypeError("Filename must be a string.")
        try:
            with open(filename, "w") as f:
                for task in tasks:
                    f.write(f"{'X' if task.is_done else 'False'},{task.description},{task.priority if task.priority is not None else 'None'},{task.deadline.strftime('%Y-%m-%d') if task.deadline else 'None'}\n")
        except Exception as e:
            raise Exception(f"Error saving to file: {e}")
class CSVSaver(TaskSaver):
    def save(self, tasks: List[Task], filename: str) -> None:
        """Saves tasks to a CSV file."""
        import csv
        if not isinstance(filename, str):
            raise TypeError("Filename must be a string.")
        try:
            with open(filename, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["is_done", "description", "priority", "deadline"])  # header
                for task in tasks:
                    writer.writerow([
                        'X' if task.is_done else 'False',
                        task.description,
                        task.priority if task.priority is not None else 'None',
                        task.deadline.strftime('%Y-%m-%d') if task.deadline else 'None'
                    ])
        except Exception as e:
            raise Exception(f"Error saving to CSV file: {e}")

class TodoListManager:
    """
    Manages a collection of tasks.  Implements the Strategy Pattern.
    """
    def __init__(self, task_saver: TaskSaver = None):  # Strategy is injected here.
        """
        Initializes the TodoListManager.
        """
        self.tasks: List[Task] = []
        self.task_saver = task_saver or TextTaskSaver() # Default strategy

    def add_task(self, description: str, priority: Optional[int] = None, deadline: Optional[datetime.date] = None) -> None:
        """
        Adds a new task to the list.

        :param description: The description of the task.
        :param priority: The priority of the task (1-3, where 1 is highest).
        :param deadline: The deadline for the task.
        """
        if not isinstance(description, str):
            raise TypeError("Description must be a string.")
        if not description:
            raise ValueError("Description cannot be empty.")
        if priority is not None and not isinstance(priority, int):
            raise TypeError("Priority must be an integer or None.")
        if priority is not None and not 1 <= priority <= 3:
            raise ValueError("Priority must be between 1 and 3.")
        if deadline is not None and not isinstance(deadline, datetime.date):
            raise TypeError("Deadline must be a datetime.date object or None.")

        self.tasks.append(Task(description, priority=priority, deadline=deadline))

    def list_tasks(self) -> str:
        """
        Lists all tasks in the to-do list.

        :return: A string representation of the tasks.
        """
        if not self.tasks:
            return "No tasks in the to-do list."
        task_list_string = "To-Do List:\n"
        for index, task in enumerate(self.tasks):
            task_list_string += f"{index + 1}. {task}\n"
        return task_list_string

    def mark_task_as_done(self, index: int) -> None:
        """
        Marks a task as done.

        :param index: The index of the task to mark as done.
        """
        if not isinstance(index, int):
            raise TypeError("Index must be an integer.")
        if not 1 <= index <= len(self.tasks):
            raise IndexError("Invalid task index.")
        self.tasks[index - 1].mark_as_done()

    def delete_task(self, index: int) -> None:
        """
        Deletes a task from the list.

        :param index: The index of the task to delete.
        """
        if not isinstance(index, int):
            raise TypeError("Index must be an integer.")
        if not 1 <= index <= len(self.tasks):
            raise IndexError("Invalid task index.")
        del self.tasks[index - 1]

    def save_to_file(self, filename: str) -> None:
        """
        Saves the to-do list to a file.  Uses the injected strategy.

        :param filename: The name of the file to save to.
        """
        self.task_saver.save(self.tasks, filename)

    def load_from_file(self, filename: str = "todo_list.txt") -> None:
        """
        Loads the to-do list from a file.  Assumes CSV format.

        :param filename: The name of the file to load from.
        """
        if not isinstance(filename, str):
            raise TypeError("Filename must be a string.")
        if not filename.endswith(".csv"):
            filename = filename.replace(".txt", ".csv")
        self.tasks = []
        try:
            with open(filename, "r") as f:
                reader = f.readlines()
                if reader:
                    header = reader[0].strip().split(",")
                    if header == ["is_done", "description", "priority", "deadline"]:
                        for line in reader[1:]:
                            parts = line.strip().split(",")
                            if len(parts) == 4:
                                is_done = parts[0] == "X"
                                description = parts[1]
                                priority = int(parts[2]) if parts[2] != "None" else None
                                deadline_str = parts[3]
                                deadline = datetime.datetime.strptime(deadline_str,
                                                                     '%Y-%m-%d').date() if deadline_str != "None" and deadline_str != "None" else None
                                self.tasks.append(
                                    Task(description, is_done, priority, deadline))
                            else:
                                print(f"Skipping invalid line: {line.strip()}")
                    else:
                         for line in reader:
                            parts = line.strip().split(",")
                            if len(parts) == 4:
                                is_done = parts[0] == "X"
                                description = parts[1]
                                priority = int(parts[2]) if parts[2] != "None" else None
                                deadline_str = parts[3]
                                deadline = datetime.datetime.strptime(deadline_str,
                                                                     '%Y-%m-%d').date() if deadline_str != "None" and deadline_str != "None" else None
                                self.tasks.append(
                                    Task(description, is_done, priority, deadline))
                            else:
                                print(f"Skipping invalid line: {line.strip()}")
        except FileNotFoundError:
            pass
        except Exception as e:
            raise Exception(f"Error loading from file: {e}")
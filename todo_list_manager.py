#This module defines the TodoListManager class.

import datetime
from typing import List, Optional
from task import Task  # Import the Task class from task.py


class TodoListManager:
    """
    Manages a collection of tasks.
    """

    def __init__(self):
        """
        Initializes the TodoListManager.
        """
        self.tasks: List[Task] = []

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

    def save_to_file(self, filename: str = "todo_list.csv") -> None:
        """
        Saves the to-do list to a file.  Uses CSV format.

        :param filename: The name of the file to save to.
        """
        if not isinstance(filename, str):
            raise TypeError("Filename must be a string.")
        if not filename.endswith(".csv"):
            filename += ".csv"
        try:
            with open(filename, "w") as f:
                for task in self.tasks:
                    f.write(f"{'X' if task.is_done else 'False'},{task.description},{task.priority if task.priority is not None else 'None'},{task.deadline.strftime('%Y-%m-%d') if task.deadline else 'None'}\n")
        except Exception as e:
            raise Exception(f"Error saving to file: {e}")

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
                for line in f:
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
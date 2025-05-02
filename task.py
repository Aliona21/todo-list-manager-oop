import os

class Task:
    def __init__(self, description, is_done=False):
        if not isinstance(description, str):
            raise TypeError("Description must be a string.")
        if not isinstance(is_done, bool):
            raise TypeError("is_done must be a boolean.")
        self.description = description
        self.is_done = is_done

    def mark_as_done(self):
        self.is_done = True

    def __str__(self):
        return f"[{'X' if self.is_done else ' '}] {self.description}"

    def __eq__(self, other):
        if not isinstance(other, Task):
            return False
        return self.description == other.description and self.is_done == other.is_done

class TodoListManager:
    def __init__(self):
        self.tasks = []

    def add_task(self, description):
        if not isinstance(description, str):
            raise TypeError("Description must be a string.")
        if not description:
            raise ValueError("Description cannot be empty.")
        self.tasks.append(Task(description))

    def list_tasks(self):
        if not self.tasks:
            return "No tasks"
        task_list_string = "To-Do List:\n"
        for index, task in enumerate(self.tasks):
            task_list_string += f"{index + 1}. {task}\n"
        return task_list_string

    def mark_task_as_done(self, index):
        if not isinstance(index, int):
            raise TypeError("Index must be an integer.")
        if not 1 <= index <= len(self.tasks):
            raise IndexError("Invalid task index.")
        self.tasks[index - 1].mark_as_done()

    def delete_task(self, index):
        if not isinstance(index, int):
            raise TypeError("Index must be an integer.")
        if not 1 <= index <= len(self.tasks):
            raise IndexError("Invalid task index.")
        del self.tasks[index - 1]

    def save_to_file(self, filename="todo_list.txt"):
        if not isinstance(filename, str):
            raise TypeError("Filename must be a string.")
        try:
            with open(filename, "w") as f:
                for task in self.tasks:
                    f.write(f"{'X' if task.is_done else ' '} {task.description}\n")
        except Exception as e:
            raise Exception(f"Error saving to file: {e}")

    def load_from_file(self, filename="todo_list.txt"):
        if not isinstance(filename, str):
            raise TypeError("Filename must be a string.")
        self.tasks = []
        try:
            with open(filename, "r") as f:
                for line in f:
                    parts = line.strip().split(" ", 1)
                    if len(parts) == 2:
                        is_done = parts[0] == "X"
                        description = parts[1]
                        self.tasks.append(Task(description, is_done))
                    else:
                        print(f"Skipping invalid line: {line.strip()}")
        except FileNotFoundError:
            pass
        except Exception as e:
            raise Exception(f"Error loading from file: {e}")
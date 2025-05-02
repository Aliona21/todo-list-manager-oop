import os
import tkinter as tk
from tkinter import messagebox, simpledialog, scrolledtext

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

class TodoListApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List Manager")
        self.manager = TodoListManager()
        self.filename = "todo_list.txt"

        try:
            self.manager.load_from_file(self.filename)
        except Exception as e:
            messagebox.showerror("Error", f"Error loading from file: {e}")

        self.create_widgets()

    def create_widgets(self):
        self.task_list_label = tk.Label(self.root, text="To-Do List:")
        self.task_list_label.pack(pady=5)

        self.task_list_text = scrolledtext.ScrolledText(self.root, width=50, height=15)
        self.task_list_text.pack(pady=10)
        self.task_list_text.config(state=tk.DISABLED)

        self.add_task_button = tk.Button(self.root, text="Add Task", command=self.add_task)
        self.add_task_button.pack(pady=5)

        self.mark_done_button = tk.Button(self.root, text="Mark as Done", command=self.mark_task_as_done)
        self.mark_done_button.pack(pady=5)

        self.delete_task_button = tk.Button(self.root, text="Delete Task", command=self.delete_task)
        self.delete_task_button.pack(pady=5)

        self.save_button = tk.Button(self.root, text="Save to File", command=self.save_to_file)
        self.save_button.pack(pady=5)

        self.load_button = tk.Button(self.root, text="Load from File", command=self.load_from_file)
        self.load_button.pack(pady=5)

        self.exit_button = tk.Button(self.root, text="Exit", command=self.exit_app)
        self.exit_button.pack(pady=10)

        self.update_task_list()

    def add_task(self):
        description = simpledialog.askstring("Add Task", "Enter task description:")
        if description:
            try:
                self.manager.add_task(description)
                self.update_task_list()
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def mark_task_as_done(self):
        try:
            task_list_string = self.manager.list_tasks()
            if "No tasks" in task_list_string:
                messagebox.showinfo("Info", task_list_string)
                return

            index = simpledialog.askinteger("Mark as Done", "Enter the index of the task to mark as done:")
            if index is not None:
                self.manager.mark_task_as_done(index)
                self.update_task_list()
        except (TypeError, ValueError):
            messagebox.showerror("Error", "Invalid input. Please enter a number.")
        except IndexError:
            messagebox.showerror("Error", "Invalid task index.")

    def delete_task(self):
        try:
            task_list_string = self.manager.list_tasks()
            if "No tasks" in task_list_string:
                messagebox.showinfo("Info", task_list_string)
                return
            index = simpledialog.askinteger("Delete Task", "Enter the index of the task to delete:")
            if index is not None:
                self.manager.delete_task(index)
                self.update_task_list()
        except (TypeError, ValueError):
            messagebox.showerror("Error", "Invalid input. Please enter a number.")
        except IndexError:
            messagebox.showerror("Error", "Invalid task index.")

    def save_to_file(self):
        filename = simpledialog.askstring("Save to File", "Enter filename:")
        if filename:
            try:
                self.manager.save_to_file(filename)
                messagebox.showinfo("Success", "To-do list saved successfully.")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def load_from_file(self):
        filename = simpledialog.askstring("Load from File", "Enter filename:")
        if filename:
            try:
                self.manager.load_from_file(filename)
                self.update_task_list()
                messagebox.showinfo("Success", "To-do list loaded successfully.")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def update_task_list(self):
        self.task_list_text.config(state=tk.NORMAL)
        self.task_list_text.delete("1.0", tk.END)
        task_list_string = self.manager.list_tasks()
        if task_list_string:
            self.task_list_text.insert(tk.END, task_list_string)
        self.task_list_text.config(state=tk.DISABLED)

    def exit_app(self):
        self.root.destroy()



if __name__ == "__main__":
    root = tk.Tk()
    app = TodoListApp(root)
    root.mainloop()
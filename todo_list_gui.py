import tkinter as tk
from tkinter import messagebox, simpledialog, scrolledtext
from todo_list_manager import TodoListManager

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
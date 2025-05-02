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

import datetime
from typing import Optional

class Task:
    def __init__(self, description: str, is_done: bool = False, priority: Optional[int] = None, deadline: Optional[datetime.date] = None):
        if not isinstance(description, str):
            raise TypeError("Description must be a string.")
        if not isinstance(is_done, bool):
            raise TypeError("is_done must be a boolean.")
        if priority is not None and not isinstance(priority, int):
            raise TypeError("Priority must be an integer or None.")
        if priority is not None and not 1 <= priority <= 3:
            raise ValueError("Priority must be between 1 and 3.")
        if deadline is not None and not isinstance(deadline, datetime.date):
            raise TypeError("Deadline must be a datetime.date object or None.")

        self.description = description
        self.is_done = is_done
        self.priority = priority
        self.deadline = deadline

    def mark_as_done(self) -> None:
        self.is_done = True

    def __str__(self) -> str:
        priority_str = "High" if self.priority == 1 else "Medium" if self.priority == 2 else "Low" if self.priority == 3 else "None"
        deadline_str = self.deadline.strftime("%Y-%m-%d") if self.deadline else "None"
        return f"[{'X' if self.is_done else ' '}] {self.description} | Priority: {priority_str} | Deadline: {deadline_str}"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Task):
            return False
        return (self.description == other.description and
                self.is_done == other.is_done and
                self.priority == other.priority and
                self.deadline == other.deadline)
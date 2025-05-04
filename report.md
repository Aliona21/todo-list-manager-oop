#   To-Do List Manager - Coursework Report

##   Introduction

This report describes the design and implementation of a To-Do List Manager application developed as part of an Object-Oriented Programming (OOP) coursework. The application allows users to manage their tasks, including adding, listing, marking as done, deleting, saving to, and loading from a file. The application is implemented in Python and utilizes the principles of OOP. A command-line interface (and optionally a graphical user interface) is provided for user interaction.

### How to Run

1.  Ensure you have Python 3.6 or later installed.
2.  Clone this repository to your local machine:
    ```bash
    git clone <repository_url>
    cd <repository_name>
    ```
3.  Run the program:
    ```bash
    python todo_list_gui.py
    ```

### How to Use

When you run `todo_list_gui.py`, a window will appear with the following elements:

* **To-Do List:** A text area displaying the list of tasks.
* **Add Task:** A button to add a new task.  A dialog box will appear to enter the description, priority, and deadline.
* **Mark as Done:** A button to mark a task as done. A dialog box will appear to enter the index of the task.
* **Delete Task:** A button to delete a task.
* **Save to File:** A button to save the to-do list to a file.  A dialog box will appear to enter the filename.  The file will be saved in CSV format.
* **Load from File:** A button to load a to-do list from a file.  A dialog box will appear to enter the filename.  The program expects the file to be in CSV format.
* **Exit:** A button to exit the application.

##   Body / Analysis

###   OOP Pillars

The application demonstrates the following OOP principles:

* **Encapsulation:** The `Task` class encapsulates the data (description, is\_done, priority, deadline) and behavior (mark\_as\_done) related to a single task.
* **Abstraction:** The `TodoListManager` class provides a simplified interface for managing the collection of tasks, hiding the underlying complexity of managing the task list.
* **Aggregation:** The `TodoListManager` class aggregates `Task` objects. It holds a list of `Task` instances.
* **Polymorphism:** The `__str__` method in the `Task` class provides a string representation of the `Task` object, and can be used to represent the object in different ways.

###   Design Pattern

The application implements the Strategy design pattern.

* The `TaskSaver` interface defines a strategy for saving tasks.
* The `TextTaskSaver` and `CSVSaver` classes implement concrete strategies for saving tasks to a text file and a CSV file, respectively.
* The `TodoListManager` class uses a `TaskSaver` object to save tasks, allowing the saving strategy to be selected at runtime.
* The default strategy is `TextTaskSaver`.

The Strategy pattern is suitable here because it allows the application to support different ways of saving task data without modifying the core `TodoListManager` class. For example, if we wanted to add a database saving strategy in the future, we could create a `DatabaseTaskSaver` class and inject it into the `TodoListManager`.

###   Object Aggregation

The `TodoListManager` class uses object aggregation. It maintains a list of `Task` objects as an attribute. This demonstrates aggregation because the `TodoListManager` *has a* list of `Task` objects. The `Task` objects are not destroyed when the `TodoListManager` is destroyed.

###   Reading from/Writing to File

The application supports saving and loading tasks to/from a file. The `TodoListManager` class uses a `TaskSaver` strategy to save the data. The default strategy saves the data in a comma-separated format in a .txt file.

###   Code Structure

The application is structured into the following modules:

* `task.py`: Defines the `Task` class.
* `todo_list_manager.py`: Defines the `TodoListManager` class and the `TaskSaver` interface and its implementations.
* `todo_list_gui.py`: Defines the `TodoListApp` class, which provides a GUI for the to-do list manager.
* `test_todo_list_manager.py`: Contains unit tests for the `TodoListManager` class.

###   Error Handling and Validation

The code includes error handling and validation for various scenarios:

* Type checking for method parameters (e.g., ensuring description is a string, index is an integer).
* Value validation (e.g., ensuring priority is within the valid range, description is not empty).
* File handling exceptions (e.g., `FileNotFoundError`, general `Exception` during file operations).

##   Results

The application provides the following functionality:

* **Adding tasks:** Users can add tasks with a description, priority, and deadline.
* **Listing tasks:** Users can view all tasks with their details.
* **Marking tasks as done:** Users can mark tasks as completed.
* **Deleting tasks:** Users can delete tasks from the list.
* **Saving tasks:** Users can save tasks to a file (default: todo\_list.txt in CSV format).
* **Loading tasks:** Users can load tasks from a file.
* **User-friendly interface:** The GUI provides a more intuitive way to interact with the application.
* **Error handling:** The application handles invalid input and file operation errors.
* **Unit tests:** Includes unit tests to ensure the core functionality works as expected.

##   Conclusions

This project demonstrates the application of OOP principles to develop a practical To-Do List Manager application. The use of encapsulation, abstraction, aggregation, and the Strategy pattern results in a modular, flexible, and maintainable design. The application provides a user-friendly interface and robust error handling. The inclusion of unit tests ensures the reliability of the core functionality.

Future extensions of this application could include:

* Implementing more sophisticated task management features, such as recurring tasks, categories, and tags.
* Adding support for different data storage formats (e.g., JSON, databases).
* Implementing a web-based interface.
* Adding user authentication and collaboration features.
from tkinter import Tk, Label, Entry, Button, Listbox, END, StringVar, OptionMenu
import os # To check if a file exists

class TodoListGUI:
    def __init__(self, window):
        self.window = window
        self.window.title("Todo List")

        # --- Task Input Section ---
        self.label_task = Label(window, text="Task:")
        self.label_task.pack(pady=5) # Add some padding

        self.entry_task = Entry(window, width=50) # Make entry wider
        self.entry_task.pack(pady=2)

        # --- Priority Selection ---
        self.label_priority = Label(window, text="Priority:")
        self.label_priority.pack(pady=2)

        self.priority_options = ["High", "Medium", "Low"]
        self.priority_var = StringVar(window)
        self.priority_var.set(self.priority_options[1]) # Default to Medium
        self.option_priority = OptionMenu(window, self.priority_var, *self.priority_options)
        self.option_priority.pack(pady=2)

        # --- Action Buttons ---
        self.button_add = Button(window, text="Add Task", command=self.add_task)
        self.button_add.pack(pady=5)

        self.button_edit = Button(window, text="Edit Selected Task", command=self.edit_task)
        self.button_edit.pack(pady=2)

        # We'll make "Complete Task" toggle between done/undone
        self.button_complete = Button(window, text="Toggle Complete/Incomplete", command=self.toggle_complete_task)
        self.button_complete.pack(pady=2)

        self.button_clear_all = Button(window, text="Clear All Tasks", command=self.clear_all_tasks)
        self.button_clear_all.pack(pady=2)

        self.button_save = Button(window, text="Save Tasks", command=self.save_tasks)
        self.button_save.pack(pady=2)

        self.button_load = Button(window, text="Load Tasks", command=self.load_tasks)
        self.button_load.pack(pady=2)

        # --- Task Listbox ---
        self.task_list = Listbox(window, height=15, width=60) # Make listbox taller and wider
        self.task_list.pack(pady=10)

        # Internal state for editing
        self.editing_index = None # Stores the index of the task being edited

        # File for saving/loading tasks
        self.task_file = "todo_tasks.txt"

        # Load tasks automatically on startup
        self.load_tasks()

    def add_task(self):
        task_text = self.entry_task.get().strip() # .strip() removes leading/trailing whitespace
        priority = self.priority_var.get()

        if task_text:
            formatted_task = f"[{priority}] {task_text}"
            if self.editing_index is not None:
                # If we are in editing mode, update the existing task
                self.task_list.delete(self.editing_index)
                self.task_list.insert(self.editing_index, formatted_task)
                self.editing_index = None # Reset editing mode
                self.button_add.config(text="Add Task") # Change button text back
            else:
                # Otherwise, add a new task
                self.task_list.insert(END, formatted_task)

            self.entry_task.delete(0, END) # Clear the entry field
            self.priority_var.set(self.priority_options[1]) # Reset priority to Medium
        else:
            # Optionally show a message if the task is empty
            print("Task cannot be empty!")

    def edit_task(self):
        selected_index = self.task_list.curselection()
        if selected_index:
            # Get the actual index (curselection returns a tuple of indices)
            index = selected_index[0]
            task_to_edit = self.task_list.get(index)

            # Extract priority and actual task text
            # Assuming format: "[Priority] Task Text"
            if task_to_edit.startswith("[High] "):
                self.priority_var.set("High")
                clean_task = task_to_edit[7:] # remove "[High] "
            elif task_to_edit.startswith("[Medium] "):
                self.priority_var.set("Medium")
                clean_task = task_to_edit[9:] # remove "[Medium] "
            elif task_to_edit.startswith("[Low] "):
                self.priority_var.set("Low")
                clean_task = task_to_edit[6:] # remove "[Low] "
            elif task_to_edit.startswith("[DONE] "): # Handle completed tasks
                # If a task was [DONE], we'll assume its original priority was Medium for editing purposes
                # Or you could parse it further if priority was inside the DONE tag: [DONE][High] Task
                # For simplicity, let's remove [DONE] and then try to parse priority or set to Medium
                clean_task_with_priority = task_to_edit[7:] # remove "[DONE] "
                if clean_task_with_priority.startswith("[High] "):
                    self.priority_var.set("High")
                    clean_task = clean_task_with_priority[7:]
                elif clean_task_with_priority.startswith("[Medium] "):
                    self.priority_var.set("Medium")
                    clean_task = clean_task_with_priority[9:]
                elif clean_task_with_priority.startswith("[Low] "):
                    self.priority_var.set("Low")
                    clean_task = clean_task_with_priority[6:]
                else: # Fallback if no clear priority found after [DONE]
                    self.priority_var.set("Medium")
                    clean_task = clean_task_with_priority
            else: # Fallback for old tasks without priority or unexpected format
                self.priority_var.set("Medium")
                clean_task = task_to_edit


            self.entry_task.delete(0, END)
            self.entry_task.insert(0, clean_task)

            # Store the index so add_task knows to update instead of add
            self.editing_index = index
            self.button_add.config(text="Update Task") # Change button text

    def toggle_complete_task(self):
        selected_index = self.task_list.curselection()
        if selected_index:
            index = selected_index[0]
            current_task = self.task_list.get(index)

            if current_task.startswith("[DONE] "):
                # If it's already done, mark as incomplete
                new_task = current_task[7:] # Remove "[DONE] "
            else:
                # If it's not done, mark as complete
                new_task = f"[DONE] {current_task}"

            self.task_list.delete(index)
            self.task_list.insert(index, new_task)
            # You might want to automatically deselect or re-select here
            self.task_list.selection_set(index) # Re-select the modified item

    def clear_all_tasks(self):
        # A simple confirmation might be good here for a real app
        self.task_list.delete(0, END)

    def save_tasks(self):
        tasks = self.task_list.get(0, END)
        try:
            with open(self.task_file, "w") as f:
                for task in tasks:
                    f.write(task + "\n")
            print(f"Tasks saved to {self.task_file}")
        except IOError as e:
            print(f"Error saving tasks: {e}")

    def load_tasks(self):
        if os.path.exists(self.task_file):
            self.task_list.delete(0, END) # Clear current list before loading
            try:
                with open(self.task_file, "r") as f:
                    for line in f:
                        task = line.strip() # Remove newline characters
                        if task: # Only add non-empty lines
                            self.task_list.insert(END, task)
                print(f"Tasks loaded from {self.task_file}")
            except IOError as e:
                print(f"Error loading tasks: {e}")
        else:
            print(f"No task file found: {self.task_file}. Starting with empty list.")

def main():
    window = Tk()
    todo_list_gui = TodoListGUI(window)
    window.mainloop()

if __name__ == "__main__":
    main()
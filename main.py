from tkinter import Tk, Label, Entry, Button, Listbox, END

class TodoListGUI:
    def __init__(self, window):
        self.window = window
        self.window.title("Todo List")

        self.label_task = Label(window, text="Task:")
        self.label_task.pack()

        self.entry_task = Entry(window)
        self.entry_task.pack()

        self.button_add = Button(window, text="Add Task", command=self.add_task)
        self.button_add.pack()

        self.button_complete = Button(window, text="Complete Task", command=self.complete_task)
        self.button_complete.pack()

        self.task_list = Listbox(window)
        self.task_list.pack()

    def add_task(self):
        task = self.entry_task.get()
        if task:
            self.task_list.insert(END, task)
            self.entry_task.delete(0, END)

    def complete_task(self):
        selected_index = self.task_list.curselection()
        if selected_index:
            self.task_list.delete(selected_index)

def main():
    window = Tk()
    todo_list_gui = TodoListGUI(window)
    window.mainloop()

if __name__ == "__main__":
    main()

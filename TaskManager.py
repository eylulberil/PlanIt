import tkinter as tk
from tkinter import messagebox
import json
from tkinter import PhotoImage


class TaskManager:

    def __init__(self, root):
        self.root = root
        self.root.title("PlanIt!")

        self.tasks = {}
        self.deleted_tasks = {}
        self.completed_tasks = {}

        self.plan_it_label = tk.Label(root, text="PlanIt!", bg="#4a6896", fg="#061942",
                                      font=("Bradley Hand ITC", 50, "bold"))
        self.task_label = tk.Label(root, text="Planned Task", bg="#4a6896", fg="#061942",
                                   font=("Bradley Hand ITC", 20, "bold"))
        self.deleted_tasks_label = tk.Label(root, text="Removed Tasks", bg="#4a6896", fg="#061942",
                                            font=("Bradley Hand ITC", 20, "bold"))
        self.completed_tasks_label = tk.Label(root, text="Completed Tasks", bg="#4a6896", fg="#061942",
                                              font=("Bradley Hand ITC", 20, "bold"))
        self.task_entry = tk.Entry(root, width=30)
        self.add_button = tk.Button(root, text="Add", command=self.add_task, bg="#69affa", fg="#1c2e1e",
                                    font=("Bradley Hand ITC", 10, "bold"))
        self.remove_button = tk.Button(root, text="Remove", command=self.remove_task, bg="#69affa", fg="#1c2e1e",
                                       font=("Bradley Hand ITC", 10, "bold"))
        self.undo_button = tk.Button(root, text="Add Back", command=self.undo_removed_task, bg="#69affa", fg="#1c2e1e",
                                     font=("Bradley Hand ITC", 10, "bold"))
        self.complete_button = tk.Button(root, text="Complete", command=self.complete_task_with_event,
                                         bg="#69affa", fg="#1c2e1e", font=("Bradley Hand ITC", 10, "bold"))
        self.task_listbox = tk.Listbox(root, selectmode=tk.MULTIPLE, width=60, height=30, bg="#93adc4")
        self.deleted_tasks_listbox = tk.Listbox(root, selectmode=tk.MULTIPLE, width=60, height=30, bg="#93adc4")
        self.completed_tasks_listbox = tk.Listbox(root, width=60, height=30, bg="#93adc4")

        self.plan_it_label.grid(row=0, column=2, padx=0, columnspan=6, pady=0, sticky="S")
        self.task_label.grid(row=1, column=0, padx=0, pady=0)
        self.deleted_tasks_label.grid(row=3, column=4, padx=0, pady=0)
        self.completed_tasks_label.grid(row=3, column=5, padx=0, pady=0)
        self.task_entry.grid(row=2, column=0, padx=0, pady=0)
        self.add_button.grid(row=3, column=0, padx=0, pady=20)
        self.remove_button.grid(row=6, column=0, padx=0, pady=0)
        self.undo_button.grid(row=6, column=4, pady=20, sticky="S")
        self.complete_button.grid(row=6, column=5, padx=0, pady=0)
        self.task_listbox.grid(row=4, column=0, columnspan=1, padx=100, pady=0)
        self.deleted_tasks_listbox.grid(row=4, column=4, padx=20, pady=0)
        self.completed_tasks_listbox.grid(row=4, column=5, padx=0, pady=0)

        self.task_entry.bind('<Return>', lambda event=None: self.add_task())
        self.task_listbox.bind('<Return>', self.remove_task_with_event)
        self.task_listbox.bind('<space>', self.complete_task_with_event)

        self.tasks_file = "../JSON FILES/tasks.json"
        self.deleted_tasks_file = "../JSON FILES/deleted_tasks.json"
        self.completed_tasks_file = "../JSON FILES/completed_tasks.json"

        self.load_json_files()

    def add_task(self):
        task = self.task_entry.get()

        if not task:
            messagebox.showwarning("Empty Task", "Please enter a task before adding.")
            return

        if task not in self.tasks and task not in self.completed_tasks:
            self.tasks[task] = True
            self.task_listbox.insert(tk.END, task)
            self.task_entry.delete(0, tk.END)
            self.print_tasks()
        elif task not in self.tasks and task in self.completed_tasks:
            answer = messagebox.askquestion("Are you sure?",
                                            f'{task} is completed. Are you sure you want to add it again?')
            if answer == 'yes':
                self.tasks[task] = True
                self.task_listbox.insert(tk.END, task)
                self.task_entry.delete(0, tk.END)
                self.print_tasks()
            else:
                self.task_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Are you distracted?", f"{task} is already in your Planned Tasks list!")

        self.save_json_files()

    def remove_task(self):
        selected_indices = list(self.task_listbox.curselection())
        selected_tasks = [self.task_listbox.get(index) for index in selected_indices]

        for selected_task in selected_tasks:
            del self.tasks[selected_task]
            self.deleted_tasks[selected_task] = True

        for index in reversed(selected_indices):
            self.task_listbox.delete(index)

        self.print_tasks()

        self.update_deleted_tasks_display()

        self.save_json_files()

    def complete_task(self):
        selected_indices = list(self.task_listbox.curselection())
        selected_tasks = [self.task_listbox.get(index) for index in selected_indices]

        if not selected_tasks:
            messagebox.showinfo("Info", "Please select a task to complete.")
            return

        confirmation = messagebox.askyesno("Complete Task", f"Do you want to complete the selected task(s)?")

        if confirmation:
            completed_tasks_text = ""
            for selected_task in selected_tasks:
                if selected_task in self.tasks:
                    self.completed_tasks[selected_task] = True
                    self.tasks.pop(selected_task)
                    completed_tasks_text += f"{selected_task}\n"

            for index in reversed(selected_indices):
                self.task_listbox.delete(index)

            self.print_tasks()
            self.update_completed_tasks_display()
            self.save_json_files()

            if completed_tasks_text:
                messagebox.showinfo("Completed Task", f"Completed Task:\n{completed_tasks_text}")

    def undo_removed_task(self):

        selected_indices = list(self.deleted_tasks_listbox.curselection())
        selected_tasks = [self.deleted_tasks_listbox.get(index) for index in selected_indices]

        for selected_task in selected_tasks:
            del self.deleted_tasks[selected_task]
            self.tasks[selected_task] = True
        for index in reversed(selected_indices):
            self.deleted_tasks_listbox.delete(index)
        for task in selected_tasks:
            self.task_listbox.insert(tk.END, task)

        self.print_tasks()

        self.update_deleted_tasks_display()

        self.save_json_files()

    def remove_task_with_event(self, event=None):
        self.remove_task()

    def complete_task_with_event(self, event=None):
        self.complete_task()

    def update_task_listbox(self):
        self.task_listbox.delete(0, tk.END)

        for task in self.tasks.keys():
            self.task_listbox.insert(tk.END, task)

    def update_deleted_tasks_display(self):
        self.deleted_tasks_listbox.delete(0, tk.END)

        for deleted_task in self.deleted_tasks.keys():
            self.deleted_tasks_listbox.insert(tk.END, deleted_task)

    def update_completed_tasks_display(self):
        self.completed_tasks_listbox.delete(0, tk.END)

        for task in self.completed_tasks.keys():
            self.completed_tasks_listbox.insert(tk.END, task)

    def load_json_files(self):
        try:
            with open(self.tasks_file, "r") as file:
                self.tasks = json.load(file)
        except FileNotFoundError:
            self.tasks = {}

        try:
            with open(self.deleted_tasks_file, "r") as file:
                self.deleted_tasks = json.load(file)
        except FileNotFoundError:
            self.deleted_tasks = {}

        try:
            with open(self.completed_tasks_file, "r") as file:
                self.completed_tasks = json.load(file)
        except FileNotFoundError:
            self.completed_tasks = {}

        self.update_task_listbox()
        self.update_deleted_tasks_display()
        self.update_completed_tasks_display()

    def save_json_files(self):
        with open(self.tasks_file, "w") as file:
            json.dump(self.tasks, file, indent=2)

        with open(self.deleted_tasks_file, "w") as file:
            json.dump(self.deleted_tasks, file, indent=2)

        with open(self.completed_tasks_file, "w") as file:
            json.dump(self.completed_tasks, file, indent=2)

    def print_tasks(self):
        print("Planned Tasks:")
        for task, status in self.tasks.items():
            if status:
                print(f"{task}")

        print("\nRemoved Tasks:")
        for deleted_task in self.deleted_tasks.keys():
            print(deleted_task)

        print("\nCompleted Tasks:")
        for completed_task in self.completed_tasks.keys():
            print(completed_task)

        self.update_deleted_tasks_display()


def adjust_screen(window):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    window.geometry(f"{screen_width}x{screen_height}+0+0")


def add_photo():
    img = PhotoImage(file="../Images/photo7.png")
    label_photo = tk.Label(root, image=img, bg="#4a6896")
    label_photo.image = img
    label_photo.grid(row=0, column=6)


if __name__ == "__main__":
    root = tk.Tk()
    adjust_screen(root)
    root.configure(bg="#4a6896")
    add_photo()
    app = TaskManager(root)
    root.mainloop()

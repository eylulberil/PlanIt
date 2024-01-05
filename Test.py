"""import tkinter as tk
from tkinter import messagebox


class TaskManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Görev Yöneticisi")

        # Sözlükler
        self.tasks = {}
        self.deleted_tasks = {}
        self.completed_tasks = {}

        # Arayüz bileşenleri oluşturulması
        self.task_label = tk.Label(root, text="Görev:")
        self.task_entry = tk.Entry(root, width=30)
        self.add_button = tk.Button(root, text="Ekle", command=self.add_task)
        self.remove_button = tk.Button(root, text="Çıkar", command=self.remove_task)
        self.task_listbox = tk.Listbox(root, selectmode=tk.MULTIPLE)
        self.deleted_tasks_label = tk.Label(root, text="Çıkarılan Görevler:")
        self.deleted_tasks_listbox = tk.Listbox(root, selectmode=tk.MULTIPLE)
        self.completed_tasks_label = tk.Label(root, text="Tamamlanan Görevler:")
        self.completed_tasks_listbox = tk.Listbox(root)
        self.deleted_tasks_label.grid(row=2, column=0, columnspan=2, padx=10, pady=5)
        self.deleted_tasks_listbox.grid(row=3, column=0, columnspan=2, padx=10, pady=5)

        self.undo_button = tk.Button(root, text="Geri Al", command=self.undo_removed_task)
        self.undo_button.grid(row=2, column=2, padx=10, pady=10)

                              self.deleted_tasks_var = tk.StringVar()
                        self.deleted_tasks_var.set("")  # Boş bir başlangıç değeri
        self.deleted_tasks_display = tk.Label(root, textvariable=self.deleted_tasks_var)

        !GEREKESİZ KOD PARÇASI DENEME SÜRECİNDE YAZILDI!

        # Arayüz elemanlarını düzenlenmesi
        self.task_label.grid(row=0, column=0, padx=10, pady=10)
        self.task_entry.grid(row=0, column=1, padx=10, pady=10)
        self.add_button.grid(row=0, column=2, padx=10, pady=10)
        self.remove_button.grid(row=1, column=2, padx=10, pady=10)
        self.task_listbox.grid(row=1, column=0, columnspan=2, padx=10, pady=10)
        self.deleted_tasks_label.grid(row=2, column=0, columnspan=2, padx=10, pady=5)
        self.deleted_tasks_display.grid(row=3, column=0, columnspan=2, padx=10, pady=5)
        self.completed_tasks_label.grid(row=4, column=0, columnspan=2, padx=10, pady=5)
        self.completed_tasks_listbox.grid(row=5, column=0, columnspan=2, padx=10, pady=5)

        # Klavyeden bir tuşa basıldığında fonksiyon çağırılıyor
        self.task_entry.bind('<Return>', lambda event=None: self.add_task())
        self.task_listbox.bind('<Return>', self.remove_task_with_event)
        self.task_listbox.bind('<space>', self.complete_task_with_event)

    def add_task(self):
        task = self.task_entry.get()

        if task:
            if task not in self.tasks and task not in self.completed_tasks:
                self.tasks[task] = True
                self.task_listbox.insert(tk.END, task)
                self.task_entry.delete(0, tk.END)
                self.print_tasks()
            elif task not in self.tasks and task in self.completed_tasks:
                answer = messagebox.askquestion("Uyarı", f"{task} tamamlandı. Tekrar eklemek istediğinizden emin "
                                                         f"misiniz?!")
                if answer == 'yes':
                    self.tasks[task] = True
                    self.task_listbox.insert(tk.END, task)
                    self.task_entry.delete(0, tk.END)
                    self.print_tasks()
                else:
                    self.task_entry.delete(0, tk.END)
            else:
                messagebox.showwarning("Uyarı", f"{task} zaten Planlanan Görevler listenizde bulunuyor!")

    def remove_task(self):
        selected_tasks = [self.task_listbox.get(index) for index in selected_indices]

        for selected_task in selected_tasks:
            del self.tasks[selected_task]
            self.deleted_tasks[selected_task] = True

        for index in reversed(selected_indices):
            self.task_listbox.delete(index)

        self.print_tasks()

        self.update_deleted_tasks_display()

    def remove_task_with_event(self, event=None):
        # Hem çıkar butonuna tıklandığında hem de task_listboxtan eleman seçilip Enter'a basıldığında burası çalışıyor
        self.remove_task()

    def complete_task(self):
        selected_indices = list(self.task_listbox.curselection())
        selected_tasks = [self.task_listbox.get(index) for index in selected_indices]

        for selected_task in selected_tasks:
            if selected_task in self.tasks:
                self.completed_tasks[selected_task] = True
                self.tasks.pop(selected_task)

        for index in reversed(selected_indices):
            self.task_listbox.delete(index)

        self.print_tasks()

        self.update_completed_tasks_display()

    def complete_task_with_event(self, event=None):
        self.complete_task()

    def update_deleted_tasks_display(self):
        self.deleted_tasks_listbox.delete(0, tk.END)

        # Iterate over deleted tasks and add them to the listbox
        for deleted_task in self.deleted_tasks.keys():
            self.deleted_tasks_listbox.insert(tk.END, deleted_task)

    def update_completed_tasks_display(self):
        self.completed_tasks_listbox.delete(0, tk.END)  # Önce mevcut içeriği temizle

        completed_tasks_text = "\n".join(self.completed_tasks.keys())
        for task in self.completed_tasks.keys():
            self.completed_tasks_listbox.insert(tk.END, task)
        messagebox.showinfo("Tamamlanan Görevler", completed_tasks_text)

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

    def print_tasks(self):
        print("Planlanan Görevler:")
        for task, status in self.tasks.items():
            if status:
                print(f"{task}")

        print("\nÇıkarılan Görevler:")
        for deleted_task in self.deleted_tasks.keys():
            print(deleted_task)

        print("\nTamamlanan Görevler:")
        for completed_task in self.completed_tasks.keys():
            print(completed_task)

        self.update_deleted_tasks_display()


def adjust_screen(window):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    root.geometry(f"{screen_width}x{screen_height}+0+0")


if __name__ == "__main__":
    root = tk.Tk()
    adjust_screen(root)
    app = TaskManager(root)
    root.mainloop()"""

"""import tkinter as tk
from tkinter import messagebox
import json
from tkinter import PhotoImage


class TaskManager:

    def __init__(self, root):
        self.root = root
        self.root.title("Görev Yöneticisi")

        self.tasks = {}
        self.deleted_tasks = {}
        self.completed_tasks = {}

        self.plan_it_label = tk.Label(root, text="PlanIt", bg="#3a476e", fg="#518c3b",
                                      font=("Bradley Hand ITC", 50, "bold"))
        self.task_label = tk.Label(root, text="Planlanan Görev", bg="#3a476e", fg="#518c3b",
                                   font=("Bradley Hand ITC", 20, "bold"))
        self.deleted_tasks_label = tk.Label(root, text="Çıkarılan Görevler", bg="#3a476e", fg="#518c3b",
                                            font=("Bradley Hand ITC", 20, "bold"))
        self.completed_tasks_label = tk.Label(root, text="Tamamlanan Görevler", bg="#3a476e", fg="#518c3b",
                                              font=("Bradley Hand ITC", 20, "bold"))
        self.task_entry = tk.Entry(root, width=30, font=("Bradley Hand ITC", 10))
        self.add_button = tk.Button(root, text="Ekle", command=self.add_task, bg="#69affa",
                                    font=("Bradley Hand ITC", 10, "bold"))
        self.remove_button = tk.Button(root, text="Çıkar", command=self.remove_task, bg="#69affa",
                                       font=("Bradley Hand ITC", 10, "bold"))
        self.undo_button = tk.Button(root, text="Geri Al", command=self.undo_removed_task, bg="#69affa",
                                     font=("Bradley Hand ITC", 10, "bold"))
        self.task_listbox = tk.Listbox(root, selectmode=tk.MULTIPLE, width=60, height=30, bg="#6ec24f")
        self.deleted_tasks_listbox = tk.Listbox(root, selectmode=tk.MULTIPLE, width=60, height=30, bg="#6ec24f")
        self.completed_tasks_listbox = tk.Listbox(root, width=60, height=30, bg="#6ec24f")

        self.plan_it_label.grid(row=0, column=2, padx=0, columnspan=6, pady=0, sticky="S")
        self.task_entry.grid(row=2, column=0, padx=0, pady=0)
        self.add_button.grid(row=3, column=0, padx=0, pady=20)
        self.remove_button.grid(row=6, column=0, padx=0, pady=0)
        self.task_label.grid(row=1, column=0, padx=0, pady=0)
        self.deleted_tasks_label.grid(row=3, column=4, padx=0, pady=0)
        self.task_listbox.grid(row=4, column=0, columnspan=1, padx=100, pady=0)
        self.deleted_tasks_listbox.grid(row=4, column=4, padx=20, pady=0)
        self.completed_tasks_label.grid(row=3, column=5, padx=0, pady=0)
        self.completed_tasks_listbox.grid(row=4, column=5, padx=0, pady=0)
        self.undo_button.grid(row=6, column=4, pady=20, sticky="S")

        self.task_entry.bind('<Return>', lambda event=None: self.add_task())
        self.task_listbox.bind('<Return>', self.remove_task_with_event)
        self.task_listbox.bind('<space>', self.complete_task_with_event)

        self.tasks_file = "tasks.json"
        self.deleted_tasks_file = "deleted_tasks.json"
        self.completed_tasks_file = "completed_tasks.json"

        self.load_json_files()

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

    def add_task(self):
        task = self.task_entry.get()

        if task:
            if task not in self.tasks and task not in self.completed_tasks:
                self.tasks[task] = True
                self.task_listbox.insert(tk.END, task)
                self.task_entry.delete(0, tk.END)

                self.print_tasks()
            elif task not in self.tasks and task in self.completed_tasks:
                answer = messagebox.askquestion("Uyarı", f"{task} tamamlandı. Tekrar eklemek istediğinizden emin "
                                                         f"misiniz?!")
                if answer == 'yes':
                    self.tasks[task] = True
                    self.task_listbox.insert(tk.END, task)
                    self.task_entry.delete(0, tk.END)

                    self.print_tasks()
                else:
                    self.task_entry.delete(0, tk.END)
            else:
                messagebox.showwarning("Uyarı", f"{task} zaten Planlanan Görevler listenizde bulunuyor!")
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

    def remove_task_with_event(self, event=None):
        self.remove_task()

    def complete_task(self):
        selected_indices = list(self.task_listbox.curselection())
        selected_tasks = [self.task_listbox.get(index) for index in selected_indices]

        for selected_task in selected_tasks:
            if selected_task in self.tasks:
                self.completed_tasks[selected_task] = True
                self.tasks.pop(selected_task)

        for index in reversed(selected_indices):
            self.task_listbox.delete(index)

        self.print_tasks()
        self.update_completed_tasks_display()

        self.save_json_files()

    def complete_task_with_event(self, event=None):
        self.complete_task()

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

    def print_tasks(self):
        print("Planlanan Görevler:")
        for task, status in self.tasks.items():
            if status:
                print(f"{task}")

        print("\nÇıkarılan Görevler:")
        for deleted_task in self.deleted_tasks.keys():
            print(deleted_task)

        print("\nTamamlanan Görevler:")
        for completed_task in self.completed_tasks.keys():
            print(completed_task)

        self.update_deleted_tasks_display()


def adjust_screen(window):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    window.geometry(f"{screen_width}x{screen_height}+0+0")


def add_photo():
    img = PhotoImage(file="Images/photo7.png")
    label_photo = tk.Label(root, image=img, bg="#3a476e")
    label_photo.image = img  
    label_photo.grid(row=0, column=6)


if __name__ == "__main__":
    root = tk.Tk()
    adjust_screen(root)
    root.configure(bg="#3a476e")
    add_photo()
    app = TaskManager(root)
    root.mainloop()
"""
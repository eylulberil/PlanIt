import tkinter as tk
from TaskManager import TaskManager


def login_control(event=None):
    username = username_entry.get()
    password = password_entry.get()

    if username == "xxx" and password == "1308":
        task_manager_window(window)
    else:
        result_label.config(text="Incorrect Login!", bg="red", fg="black", font=("Bradley Hand ITC", 15, "bold"))
        username_label.config(bg="red")
        password_label.config(bg="red")
        window.config(bg="red")


def task_manager_window(login_window):
    login_window.destroy()
    main_window = tk.Tk()
    main_window.configure(bg="#4a6896")
    main_window.title("Task Manager")
    adjust_screen(main_window)
    img = tk.PhotoImage(file="../Images/photo7.png")

    label_photo = tk.Label(main_window, image=img, bg="#4a6896")
    label_photo.image = img
    label_photo.grid(row=0, column=6)
    TaskManager(main_window)
    main_window.mainloop()


def switch_to_task_manager(login_window):
    window.destroy()
    task_manager_window(login_window)


def adjust_screen(root):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.geometry(f"{screen_width}x{screen_height}+0+0")


window = tk.Tk()
window.title("Login Page")
window.geometry("400x250")
window.config(bg="#4a6896")

username_label = tk.Label(window, text="Username:", bg="#4a6896", fg="#061942", font=("Bradley Hand ITC", 15, "bold"))
username_label.pack(side="top", padx=10, pady=5)

password_label = tk.Label(window, text="Password:", bg="#4a6896", fg="#061942", font=("Bradley Hand ITC", 15, "bold"))
password_label.pack(side="top", padx=10, pady=5)

result_label = tk.Label(window, text="", bg="#4a6896")
result_label.pack(side="top", padx=10, pady=5)

username_entry = tk.Entry(window)
username_entry.pack(side="top", padx=10, pady=5)

password_entry = tk.Entry(window, show="*")
password_entry.pack(side="top", padx=10, pady=5)

login_button = tk.Button(window, text="Login", command=login_control, fg="#061942", bg="#69affa",
                         font=("Bradley Hand ITC", 10, "bold"))

login_button.pack(side="top", padx=10, pady=10)

window.bind('<Return>', login_control)


window.mainloop()

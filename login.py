from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import sqlite3
import os


# Login Window
def login_window():
    def open_register():
        login_root.destroy()
        register_window()

    def check_login():
        username = username_entry.get()
        password = password_entry.get()

        conn = sqlite3.connect('music-player.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Users WHERE Username=? AND Password=?", (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            user_id = user[0]  # users tablosunun UserID kolonundan ID alır
            os.environ['USER_ID'] = str(user_id)  # oturum ID'sini ayarlar
            messagebox.showinfo("Success", "Login successful!")
            login_root.destroy()
            open_music_player()
        else:
            messagebox.showerror("Error", "Invalid username or password.")

    login_root = Tk()
    login_root.title("Login | Sab's Music Player")
    login_root.geometry("400x300+{}+{}".format(
        (login_root.winfo_screenwidth() - 400) // 2, (login_root.winfo_screenheight() - 300) // 2
    ))
    login_root.resizable(False, False)
    login_root.iconbitmap("images/icon.ico")

    # Header with logo
    logo = Image.open("images/logo.png")
    logo = logo.resize((400, 90))
    logo = ImageTk.PhotoImage(logo)

    logo_label = Label(login_root, image=logo, bg="white")
    logo_label.image = logo
    logo_label.place(x=0, y=0)

    # Username
    Label(login_root, text="Username:").pack(pady=(110, 5))
    username_entry = Entry(login_root, width=30)
    username_entry.pack()

    # Password
    Label(login_root, text="Password:").pack(pady=5)
    password_entry = Entry(login_root, width=30, show="*")
    password_entry.pack()

    # Login Button
    Button(login_root, text="Login", width=10, command=check_login).pack(pady=10)

    # Register Link
    Button(login_root, text="Register from Here", fg="blue", bd=0, command=open_register).pack()

    login_root.mainloop()


# Register Window
def register_window():
    def go_back():
        register_root.destroy()
        login_window()

    def register_user():
        username = reg_username_entry.get()
        password = reg_password_entry.get()
        confirm_password = reg_confirm_password_entry.get()

        if not username or not password or not confirm_password:
            messagebox.showerror("Error", "All fields are required.")
            return

        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match!")
            return

        conn = sqlite3.connect('music-player.db')
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO Users (Username, Password) VALUES (?, ?)", (username, password))
            conn.commit()
            messagebox.showinfo("Success", "Registration successful!")
            register_root.destroy()
            login_window()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username already exists.")
        finally:
            conn.close()

    register_root = Tk()
    register_root.title("Register | Sab's Music Player")
    register_root.geometry("400x350+{}+{}".format(
        (register_root.winfo_screenwidth() - 400) // 2, (register_root.winfo_screenheight() - 350) // 2
    ))
    register_root.resizable(False, False)
    register_root.iconbitmap("images/icon.ico")

    logo = Image.open("images/logo.png")
    logo = logo.resize((400, 90))
    logo = ImageTk.PhotoImage(logo)

    logo_label = Label(register_root, image=logo, bg="white")
    logo_label.image = logo
    logo_label.place(x=0, y=0)

    Label(register_root, text="Username:").pack(pady=(110, 5))
    reg_username_entry = Entry(register_root, width=30)
    reg_username_entry.pack()

    Label(register_root, text="Password:").pack(pady=5)
    reg_password_entry = Entry(register_root, width=30, show="*")
    reg_password_entry.pack()

    Label(register_root, text="Confirm Password:").pack(pady=5)
    reg_confirm_password_entry = Entry(register_root, width=30, show="*")
    reg_confirm_password_entry.pack()

    Button(register_root, text="Register", command=register_user).pack(pady=10)
    Button(register_root, text="Go Back", fg="red", bd=0, command=go_back).pack()

    register_root.mainloop()


def open_music_player():
    os.system("python main.py")


if __name__ == "__main__":
    login_window()

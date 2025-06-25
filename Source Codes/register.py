import tkinter as tk
from tkinter import messagebox
import mysql.connector

def register_user():
    name = name_var.get()
    email = email_var.get()
    password = pass_var.get()
    confirm = confirm_pass_var.get()
    role = "admin"

    if name == "" or email == "" or password == "" or confirm == "":
        messagebox.showerror("Error", "All fields are required.")
        return
    
    if password != confirm:
        messagebox.showerror("Error", "Passwords do not match.")
        return
    
    try:
        con = mysql.connector.connect(
            host="localhost",
            user="root",
            password="sanjana1432",
            database="library_db"
        )
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE email=%s", (email,))
        existing = cur.fetchone()
        if existing:
            messagebox.showerror("Error", "Email already registered.")
        else:
            cur.execute("INSERT INTO users (name, email, password, role) VALUES (%s, %s, %s, %s)", 
                        (name, email, password, role))
            con.commit()
            messagebox.showinfo("Success", "Registration successful.")
            con.close()
            root.destroy()
            import login_page  
    except Exception as e:
        messagebox.showerror("Database Error", str(e))

def clear_fields():
    name_var.set("")
    email_var.set("")
    pass_var.set("")
    confirm_pass_var.set("")

def back_to_login():
    root.destroy()
    import login_page  

# ---------- GUI ----------
root = tk.Tk()
root.title("Admin Registration")
root.geometry("400x400")
root.resizable(False, False)

# Variables
name_var = tk.StringVar()
email_var = tk.StringVar()
pass_var = tk.StringVar()
confirm_pass_var = tk.StringVar()

# Title
tk.Label(root, text="Admin Registration", font=("Arial", 20, "bold")).pack(pady=10)

# Form Frame
frame = tk.Frame(root)
frame.pack(pady=20)

tk.Label(frame, text="Name:", font=("Arial", 12)).grid(row=0, column=0, sticky="w", padx=5, pady=5)
tk.Entry(frame, textvariable=name_var, width=30).grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame, text="Email:", font=("Arial", 12)).grid(row=1, column=0, sticky="w", padx=5, pady=5)
tk.Entry(frame, textvariable=email_var, width=30).grid(row=1, column=1, padx=5, pady=5)

tk.Label(frame, text="Password:", font=("Arial", 12)).grid(row=2, column=0, sticky="w", padx=5, pady=5)
tk.Entry(frame, textvariable=pass_var, show="*", width=30).grid(row=2, column=1, padx=5, pady=5)

tk.Label(frame, text="Confirm Password:", font=("Arial", 12)).grid(row=3, column=0, sticky="w", padx=5, pady=5)
tk.Entry(frame, textvariable=confirm_pass_var, show="*", width=30).grid(row=3, column=1, padx=5, pady=5)

# Buttons
tk.Button(root, text="Register", command=register_user, bg="green", fg="white", font=("Arial", 12), width=20).pack(pady=10)
tk.Button(root, text="Clear", command=clear_fields, bg="gray", fg="white", font=("Arial", 10), width=20).pack()
tk.Button(root, text="Back to Login", command=back_to_login, bg="#0078D7", fg="white", font=("Arial", 10), width=20).pack(pady=10)

root.mainloop()

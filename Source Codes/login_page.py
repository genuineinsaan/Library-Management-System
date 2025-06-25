import tkinter as tk
from tkinter import messagebox
import mysql.connector

def login_user():
    email = email_var.get()
    password = pass_var.get()

    if not email or not password:
        messagebox.showerror("Error", "All fields are required")
        return

    try:
        con = mysql.connector.connect(
            host="localhost",
            user="root",
            password="sanjana1432",
            database="library_db"  # Make sure this is your DB name
        )
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE email=%s AND password=%s", (email, password))
        row = cur.fetchone()
        con.close()

        if row:
            role = row[4]
            messagebox.showinfo("Success", f"Welcome {row[1]}!\nRole: {role.capitalize()}")
            root.destroy()
            if role == 'admin':
                import dashboard  # Redirect to admin dashboard
            else:
                import student_dashboard  # Redirect to student dashboard
        else:
            messagebox.showerror("Error", "Invalid email or password")

    except Exception as e:
        messagebox.showerror("Database Error", str(e))

def register():
    root.destroy()
    import register.py_page  # Redirect to register page

# ------------- GUI Setup -------------
root = tk.Tk()
root.title("Library Management Login")
root.geometry("400x350")
root.configure(bg="white")
root.resizable(False, False)

email_var = tk.StringVar()
pass_var = tk.StringVar()

tk.Label(root, text="Library Login", font=("Arial", 20, "bold"), bg="white", fg="black").pack(pady=20)

frame = tk.Frame(root, bg="white")
frame.pack(pady=10)

tk.Label(frame, text="Email:", font=("Arial", 12), bg="white").grid(row=0, column=0, sticky="e", padx=10, pady=10)
tk.Entry(frame, textvariable=email_var, width=30, bd=2, relief="groove").grid(row=0, column=1, padx=10, pady=10)

tk.Label(frame, text="Password:", font=("Arial", 12), bg="white").grid(row=1, column=0, sticky="e", padx=10, pady=10)
tk.Entry(frame, textvariable=pass_var, show="*", width=30, bd=2, relief="groove").grid(row=1, column=1, padx=10, pady=10)

tk.Button(root, text="Login", command=login_user, bg="#0078D7", fg="white",
          font=("Arial", 12, "bold"), width=20, pady=5).pack(pady=20)

tk.Button(root, text="Register", command=register, bg="#28a745", fg="white",
          font=("Arial", 12, "bold"), width=20, pady=5).pack()

root.mainloop()

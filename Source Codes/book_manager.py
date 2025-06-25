import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
import subprocess

# ---------- Database Functions ----------
def fetch_books():
    for row in book_table.get_children():
        book_table.delete(row)
    try:
        con = mysql.connector.connect(
            host="localhost",
            user="root",
            password="sanjana1432",
            database="library_db"
        )
        cur = con.cursor()
        cur.execute("SELECT * FROM books")
        rows = cur.fetchall()
        for row in rows:
            book_table.insert('', 'end', values=row)
        con.close()
    except Exception as e:
        messagebox.showerror("Error", str(e))

def add_book():
    if title_var.get() == "" or quantity_var.get() == "":
        messagebox.showerror("Error", "Title and Quantity are required")
        return
    try:
        con = mysql.connector.connect(
            host="localhost",
            user="root",
            password="sanjana1432",
            database="library_db"
        )
        cur = con.cursor()
        cur.execute("INSERT INTO books (title, author, category, quantity, shelf_no) VALUES (%s, %s, %s, %s, %s)",
                    (title_var.get(), author_var.get(), category_var.get(), quantity_var.get(), shelf_var.get()))
        con.commit()
        con.close()
        fetch_books()
        clear_form()
        messagebox.showinfo("Success", "Book added successfully")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def delete_book():
    selected = book_table.focus()
    if not selected:
        messagebox.showwarning("Select Book", "Please select a book to delete")
        return
    values = book_table.item(selected, 'values')
    book_id = values[0]
    confirm = messagebox.askyesno("Delete", "Are you sure you want to delete this book?")
    if confirm:
        try:
            con = mysql.connector.connect(
                host="localhost",
                user="root",
                password="sanjana1432",
                database="library_db"
            )
            cur = con.cursor()
            cur.execute("DELETE FROM books WHERE id=%s", (book_id,))
            con.commit()
            con.close()
            fetch_books()
            clear_form()
            messagebox.showinfo("Deleted", "Book deleted successfully")
        except Exception as e:
            messagebox.showerror("Error", str(e))

def clear_form():
    title_var.set("")
    author_var.set("")
    category_var.set("")
    quantity_var.set("")
    shelf_var.set("")

def go_home():
    root.destroy()
    subprocess.Popen(["python", "dashboard.py"])

# ---------- GUI ----------
root = tk.Tk()
root.title("Book Manager - Library")
root.geometry("950x500")
root.resizable(False, False)  # Disable maximize/minimize

# Variables
title_var = tk.StringVar()
author_var = tk.StringVar()
category_var = tk.StringVar()
quantity_var = tk.StringVar()
shelf_var = tk.StringVar()

# Form Frame
form_frame = tk.LabelFrame(root, text="Add New Book", padx=10, pady=10)
form_frame.place(x=20, y=20, width=400, height=330)

label_opts = {"anchor": "w", "padx": 5, "pady": 5}
entry_opts = {"width": 36}

# Form Fields
tk.Label(form_frame, text="Title", anchor="w").grid(row=0, column=0, sticky="w", padx=5, pady=5)
tk.Entry(form_frame, textvariable=title_var, width=36).grid(row=0, column=1)

tk.Label(form_frame, text="Author", anchor="w").grid(row=1, column=0, sticky="w", padx=5, pady=5)
tk.Entry(form_frame, textvariable=author_var, width=36).grid(row=1, column=1)

tk.Label(form_frame, text="Category", anchor="w").grid(row=2, column=0, sticky="w", padx=5, pady=5)
tk.Entry(form_frame, textvariable=category_var, width=36).grid(row=2, column=1)

tk.Label(form_frame, text="Quantity", anchor="w").grid(row=3, column=0, sticky="w", padx=5, pady=5)
tk.Entry(form_frame, textvariable=quantity_var, width=36).grid(row=3, column=1)

tk.Label(form_frame, text="Shelf No.", anchor="w").grid(row=4, column=0, sticky="w", padx=5, pady=5)
tk.Entry(form_frame, textvariable=shelf_var, width=36).grid(row=4, column=1)

# Button frame inside form
button_frame = tk.Frame(form_frame)
button_frame.grid(row=5, columnspan=2, pady=10)

tk.Button(button_frame, text="Clear", command=clear_form, bg="#6c757d", fg="white", width=12).pack(side="left", padx=10)
tk.Button(button_frame, text="Add Book", command=add_book, bg="#28a745", fg="white", width=12).pack(side="left", padx=10)

# Table Frame
table_frame = tk.LabelFrame(root, text="Book Records", padx=10, pady=10)
table_frame.place(x=430, y=20, width=500, height=450)

cols = ("ID", "Title", "Author", "Category", "Quantity", "Shelf No.")
book_table = ttk.Treeview(table_frame, columns=cols, show="headings")

for col in cols:
    book_table.heading(col, text=col)
    book_table.column(col, width=80)

book_table.pack(fill="both", expand=True)

# Bottom Button Frame
bottom_btn_frame = tk.Frame(root)
bottom_btn_frame.place(x=130, y=370)

tk.Button(bottom_btn_frame, text="Delete Selected Book", command=delete_book, bg="#dc3545", fg="white", font=("Arial", 12), width=25).pack(pady=5)
tk.Button(bottom_btn_frame, text="\U0001F3E0 Home", command=go_home, bg="#fd7e14", fg="white", font=("Arial", 11), width=25).pack()

# Load Data
fetch_books()

root.mainloop()

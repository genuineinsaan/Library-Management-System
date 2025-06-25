import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from datetime import date

# ---------- Database Operations ----------
def load_transactions():
    for row in trans_table.get_children():
        trans_table.delete(row)
    try:
        con = mysql.connector.connect(host="localhost", user="root", password="sanjana1432", database="library_db")
        cur = con.cursor()
        cur.execute("""
            SELECT t.id, b.title, m.name, t.issue_date, t.return_date
            FROM transactions t
            JOIN books b ON t.book_id = b.id
            JOIN members m ON t.member_id = m.id
            ORDER BY t.id DESC
        """)
        rows = cur.fetchall()
        for row in rows:
            trans_table.insert('', 'end', values=row)
        con.close()
    except Exception as e:
        messagebox.showerror("Database Error", str(e))

def issue_book():
    if not book_id_var.get() or not member_id_var.get():
        messagebox.showerror("Missing Info", "Please provide Book ID and Member ID")
        return
    try:
        con = mysql.connector.connect(host="localhost", user="root", password="sanjana1432", database="library_db")
        cur = con.cursor()
        cur.execute("SELECT * FROM books WHERE id=%s AND availability='Yes'", (book_id_var.get(),))
        book = cur.fetchone()
        if not book:
            messagebox.showwarning("Unavailable", "Book not available or does not exist")
            return

        cur.execute("INSERT INTO transactions (book_id, member_id, issue_date) VALUES (%s, %s, %s)",
                    (book_id_var.get(), member_id_var.get(), date.today()))
        cur.execute("UPDATE books SET availability='No' WHERE id=%s", (book_id_var.get(),))

        con.commit()
        con.close()
        load_transactions()
        clear_fields()
        messagebox.showinfo("Success", "Book issued successfully")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def return_book():
    selected = trans_table.focus()
    if not selected:
        messagebox.showwarning("Select Record", "Please select a transaction to return")
        return

    trans_id = trans_table.item(selected, 'values')[0]
    book_title = trans_table.item(selected, 'values')[1]
    return_date = trans_table.item(selected, 'values')[4]

    if return_date:
        messagebox.showinfo("Already Returned", f"Book '{book_title}' is already returned")
        return

    try:
        con = mysql.connector.connect(host="localhost", user="root", password="sanjana1432", database="library_db")
        cur = con.cursor()

        cur.execute("UPDATE transactions SET return_date=%s WHERE id=%s", (date.today(), trans_id))
        cur.execute("SELECT book_id FROM transactions WHERE id=%s", (trans_id,))
        book_id = cur.fetchone()[0]
        cur.execute("UPDATE books SET availability='Yes' WHERE id=%s", (book_id,))

        con.commit()
        con.close()
        load_transactions()
        messagebox.showinfo("Returned", f"Book '{book_title}' returned successfully")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def clear_fields():
    book_id_var.set("")
    member_id_var.set("")

def go_home():
    root.destroy()
    import dashboard

# ---------- GUI ----------
root = tk.Tk()
root.title("Issue / Return Books")
root.geometry("950x550")
root.configure(bg="white")

book_id_var = tk.StringVar()
member_id_var = tk.StringVar()

# Header
tk.Label(root, text="Issue / Return Books", font=("Arial", 20, "bold"), bg="#004d4d", fg="white", pady=10).pack(fill="x")

# Form Frame
form_frame = tk.LabelFrame(root, text="Issue Book", font=("Arial", 12, "bold"), padx=10, pady=10, bg="white")
form_frame.place(x=30, y=70, width=400, height=200)

# Form Fields
tk.Label(form_frame, text="Book ID:", font=("Arial", 12), bg="white").grid(row=0, column=0, sticky="w", pady=5)
tk.Entry(form_frame, textvariable=book_id_var, font=("Arial", 12), width=25).grid(row=0, column=1)

tk.Label(form_frame, text="Member ID:", font=("Arial", 12), bg="white").grid(row=1, column=0, sticky="w", pady=5)
tk.Entry(form_frame, textvariable=member_id_var, font=("Arial", 12), width=25).grid(row=1, column=1)

# Form Buttons
tk.Button(form_frame, text="Issue Book", command=issue_book, bg="#0066cc", fg="white", font=("Arial", 12)).grid(row=2, column=1, pady=10, sticky="e")
tk.Button(form_frame, text="Clear", command=clear_fields, bg="gray", fg="white", font=("Arial", 12)).grid(row=2, column=0, pady=10)

# Return Button
tk.Button(root, text="✔ Mark as Returned", command=return_book, bg="#009933", fg="white", font=("Arial", 13)).place(x=130, y=300)

# Home Button
tk.Button(root, text="🏠 Home", command=go_home, bg="#333333", fg="white", font=("Arial", 12)).place(x=30, y=300)

# Table Frame
table_frame = tk.LabelFrame(root, text="All Transactions", font=("Arial", 12, "bold"), padx=10, pady=10, bg="white")
table_frame.place(x=460, y=70, width=460, height=430)

cols = ("ID", "Book Title", "Member", "Issue Date", "Return Date")
trans_table = ttk.Treeview(table_frame, columns=cols, show="headings")

for col in cols:
    trans_table.heading(col, text=col)
    trans_table.column(col, width=90)

trans_table.pack(fill="both", expand=True)

# Load Data
load_transactions()

root.mainloop()

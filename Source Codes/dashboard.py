import tkinter as tk
from tkinter import messagebox
import mysql.connector
import importlib

def get_summary_counts():
    """Fetch total books, members, issued books, and books returned today from MySQL."""
    try:
        con = mysql.connector.connect(
            host="localhost",
            user="root",
            password="sanjana1432",
            database="library_db"
        )
        cur = con.cursor()

        cur.execute("SELECT COUNT(*) FROM books")
        total_books = cur.fetchone()[0]

        cur.execute("SELECT COUNT(*) FROM members")
        total_members = cur.fetchone()[0]

        cur.execute("SELECT COUNT(*) FROM transactions WHERE return_date IS NULL")
        books_issued = cur.fetchone()[0]

        cur.execute("SELECT COUNT(*) FROM transactions WHERE return_date = CURDATE()")
        returned_today = cur.fetchone()[0]

        con.close()

        lbl_books.config(text=f"Total Books\n{total_books}")
        lbl_members.config(text=f"Total Members\n{total_members}")
        lbl_issued.config(text=f"Issued Books\n{books_issued}")
        lbl_returned.config(text=f"Returned Today\n{returned_today}")

    except Exception as e:
        messagebox.showerror("Database Error", str(e))


def open_books():
    """Open Book Manager page."""
    root.destroy()
    import book_manager


def open_members():
    """Open Member Manager page."""
    root.destroy()
    import member_manager


def open_transactions():
    """Open Transactions Manager page."""
    root.destroy()
    import transaction_manager

def open_search_book():
    """Open Search Books page."""
    root.destroy()
    import search_books

# ---------- GUI ----------
root = tk.Tk()
root.title("Library Dashboard")
root.geometry("800x500")
root.resizable(False, False)

tk.Label(root, text="Library Management System", font=("Arial", 22, "bold"),
          bg="#006666", fg="white", pady=10).pack(fill="x")

# Summary cards
frame = tk.Frame(root, bg="#e0f7f7")
frame.pack(pady=20)

lbl_books = tk.Label(frame, text="Total Books\n0", font=("Arial", 16, "bold"),
                     bg="white", width=20, height=5, relief="groove")
lbl_books.grid(row=0, column=0, padx=10)

lbl_members = tk.Label(frame, text="Total Members\n0", font=("Arial", 16, "bold"),
                       bg="white", width=20, height=5, relief="groove")
lbl_members.grid(row=0, column=1, padx=10)

lbl_issued = tk.Label(frame, text="Issued Books\n0", font=("Arial", 16, "bold"),
                      bg="white", width=20, height=5, relief="groove")
lbl_issued.grid(row=1, column=0, padx=10, pady=10)

lbl_returned = tk.Label(frame, text="Returned Today\n0", font=("Arial", 16, "bold"),
                        bg="white", width=20, height=5, relief="groove")
lbl_returned.grid(row=1, column=1, padx=10, pady=10)

# Navigation Buttons
nav_frame = tk.Frame(root)
nav_frame.pack(pady=10)

tk.Button(nav_frame, text="📘 Manage Books", command=open_books,
          width=20, font=("Arial", 12), bg="#009999", fg="white").grid(row=0, column=0, padx=20)

tk.Button(nav_frame, text="👥 Manage Members", command=open_members,
          width=20, font=("Arial", 12), bg="#0066cc", fg="white").grid(row=0, column=1, padx=20)

tk.Button(nav_frame, text="🔁 Manage Transactions", command=open_transactions,
          width=20, font=("Arial", 12), bg="#ff9900", fg="white").grid(row=0, column=2, padx=20)

# Loading summary data
get_summary_counts()

root.mainloop()

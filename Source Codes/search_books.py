import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import mysql.connector
import csv

def search_books():
    for row in result_table.get_children():
        result_table.delete(row)
    query = search_var.get()
    try:
        con = mysql.connector.connect(host="localhost", user="root", password="sanjana1432", database="library_db")
        cur = con.cursor()
        cur.execute("SELECT * FROM books WHERE title LIKE %s OR author LIKE %s", (f"%{query}%", f"%{query}%"))
        rows = cur.fetchall()
        for row in rows:
            result_table.insert('', 'end', values=row)
        con.close()
    except Exception as e:
        messagebox.showerror("Error", str(e))

def export_books():
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV File", "*.csv")])
    if not file_path:
        return
    try:
        con = mysql.connector.connect(host="localhost", user="root", password="sanjana1432", database="library_db")
        cur = con.cursor()
        cur.execute("SELECT * FROM books")
        rows = cur.fetchall()
        con.close()

        with open(file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Title", "Author", "Genre", "Availability"])
            for row in rows:
                writer.writerow(row)

        messagebox.showinfo("Exported", "Books exported successfully.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# ---------- GUI ----------
root = tk.Tk()
root.title("Search Books / Export")
root.geometry("850x500")
root.resizable(False, False)

search_var = tk.StringVar()

tk.Label(root, text="Search Book (Title / Author):", font=("Arial", 12)).grid(row=0, column=0, padx=20, pady=20, sticky='w')
tk.Entry(root, textvariable=search_var, width=40).grid(row=0, column=1, pady=20, sticky='w')
tk.Button(root, text="Search", command=search_books, bg="#0078D7", fg="#ffffff").grid(row=0, column=2, padx=10, pady=20)
tk.Button(root, text="Export All Books to CSV", command=export_books, bg="#28a745", fg="#ffffff").grid(row=0, column=3, padx=10, pady=20)

# Table
cols = ("ID", "Title", "Author", "Genre", "Availability")
result_table = ttk.Treeview(root, columns=cols, show="headings")
for col in cols:
    result_table.heading(col, text=col)
    result_table.column(col, width=150)

result_table.grid(row=1, column=0, columnspan=4, padx=20, pady=20, sticky='nsew')

root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(1, weight=1)

root.mainloop()

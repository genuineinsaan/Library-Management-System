import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from datetime import date

# ---------- Database Functions ----------
def fetch_members():
    for row in member_table.get_children():
        member_table.delete(row)
    try:
        con = mysql.connector.connect(host="localhost", user="root", password="sanjana1432", database="library_db")
        cur = con.cursor()
        cur.execute("SELECT * FROM members")
        rows = cur.fetchall()
        for row in rows:
            member_table.insert('', 'end', values=row)
        con.close()
    except Exception as e:
        messagebox.showerror("Error", str(e))

def add_member():
    if name_var.get() == "" or email_var.get() == "":
        messagebox.showerror("Error", "Name and Email are required")
        return
    try:
        con = mysql.connector.connect(host="localhost", user="root", password="sanjana1432", database="library_db")
        cur = con.cursor()
        cur.execute("INSERT INTO members (name, email, phone, address, join_date) VALUES (%s, %s, %s, %s, %s)", 
                    (name_var.get(), email_var.get(), phone_var.get(), address_text.get("1.0", "end-1c"), date.today()))
        con.commit()
        con.close()
        fetch_members()
        clear_form()
        messagebox.showinfo("Success", "Member added successfully")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def delete_member():
    selected = member_table.focus()
    if not selected:
        messagebox.showwarning("Select Member", "Please select a member to delete")
        return
    member_id = member_table.item(selected, 'values')[0]
    confirm = messagebox.askyesno("Delete", "Are you sure you want to delete this member?")
    if confirm:
        try:
            con = mysql.connector.connect(host="localhost", user="root", password="sanjana1432", database="library_db")
            cur = con.cursor()
            cur.execute("DELETE FROM members WHERE id=%s", (member_id,))
            con.commit()
            con.close()
            fetch_members()
            clear_form()
            messagebox.showinfo("Deleted", "Member deleted successfully")
        except Exception as e:
            messagebox.showerror("Error", str(e))

def clear_form():
    name_var.set("")
    email_var.set("")
    phone_var.set("")
    address_text.delete("1.0", "end")

def go_home():
    root.destroy()
    import dashboard

# ---------- GUI ----------
root = tk.Tk()
root.title("Library Member Manager")
root.geometry("950x600")
root.resizable(False, False)

# Variables
name_var = tk.StringVar()
email_var = tk.StringVar()
phone_var = tk.StringVar()

# Form Frame
form_frame = tk.LabelFrame(root, text="Register New Member", font=("Arial", 14, "bold"), padx=20, pady=20, bg="#f2fbff")
form_frame.place(x=20, y=20, width=440, height=500)

label_opts = {'font': ('Arial', 12), 'bg': "#f2fbff"}

tk.Label(form_frame, text="Name", **label_opts).grid(row=0, column=0, sticky="w", pady=10)
tk.Entry(form_frame, textvariable=name_var, font=('Arial', 12), width=25).grid(row=0, column=1, pady=10)

tk.Label(form_frame, text="Email", **label_opts).grid(row=1, column=0, sticky="w", pady=10)
tk.Entry(form_frame, textvariable=email_var, font=('Arial', 12), width=25).grid(row=1, column=1, pady=10)

tk.Label(form_frame, text="Phone", **label_opts).grid(row=2, column=0, sticky="w", pady=10)
tk.Entry(form_frame, textvariable=phone_var, font=('Arial', 12), width=25).grid(row=2, column=1, pady=10)

tk.Label(form_frame, text="Address", **label_opts).grid(row=3, column=0, sticky="nw", pady=10)
address_text = tk.Text(form_frame, font=('Arial', 12), width=22, height=4)
address_text.grid(row=3, column=1, pady=10)

# Buttons below form
btn_frame = tk.Frame(form_frame, bg="#f2fbff")
btn_frame.grid(row=4, column=0, columnspan=2, pady=20)

tk.Button(btn_frame, text="Add Member", command=add_member, bg="#009688", fg="white",
          font=("Arial", 12, "bold"), width=15).grid(row=0, column=0, padx=10)

tk.Button(btn_frame, text="Clear", command=clear_form, bg="#607d8b", fg="white",
          font=("Arial", 12, "bold"), width=15).grid(row=0, column=1, padx=10)

# Table Frame
table_frame = tk.LabelFrame(root, text="Member Records", font=("Arial", 14, "bold"), padx=10, pady=10, bg="#f2fbff")
table_frame.place(x=480, y=20, width=450, height=500)

cols = ("ID", "Name", "Email", "Phone", "Address", "Join Date")
member_table = ttk.Treeview(table_frame, columns=cols, show="headings")

for col in cols:
    member_table.heading(col, text=col)
    member_table.column(col, width=100 if col == "ID" else 120)

member_table.pack(fill="both", expand=True)

# Bottom Buttons
bottom_frame = tk.Frame(root)
bottom_frame.place(x=250, y=530)

tk.Button(bottom_frame, text="Delete Selected Member", command=delete_member, bg="#e53935", fg="white",
          font=("Arial", 12, "bold"), width=22).grid(row=0, column=0, padx=20)

tk.Button(bottom_frame, text="Home", command=go_home, bg="#3f51b5", fg="white",
          font=("Arial", 12, "bold"), width=22).grid(row=0, column=1, padx=20)

# Load members
fetch_members()
root.mainloop()

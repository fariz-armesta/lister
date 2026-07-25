import tkinter as tk
from tkinter import ttk, messagebox
from db import Database

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Lister")
        self.geometry("720x720")

        self.db = Database()

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        tk.Label(self, text="Lister for making list!").grid(row=0, column=0, columnspan=2)

        tk.Label(self, text="Link: ").grid(row=2, column=0)
        tk.Label(self, text="Desc: ").grid(row=5, column=0)

        self.link = tk.Entry(self)
        self.link.grid(row=2, column=1)

        self.link_name = tk.Entry(self)
        self.link_name.grid(row=5, column=1)

        tk.Button(self, text="Input", width = 25, command=self.on_input).grid(row=7, column=0, columnspan=2)

        column = ("id", "title", "descriptions", "time")
        self.tree = ttk.Treeview(self, columns=column, show="headings", height=12)

        self.tree.heading("id", text="ID")
        self.tree.heading("title", text="Link")
        self.tree.heading("descriptions", text="Description")
        self.tree.heading("time", text="Date")

        self.tree.column("id", width=30, anchor="center")
        self.tree.column("title", width=200)
        self.tree.column("descriptions", width=150)
        self.tree.column("time", width=100)

        self.tree.grid(row=10, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)  

        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview) 
        scrollbar.grid(row=10, column=2, sticky="ns")
        self.tree.configure(yscrollcommand=scrollbar.set)   

        tk.Button(self, text="Delete All", width = 25, command=self.on_delete_all).grid(row=13, column=0, columnspan=2)

        tk.Button(self, text="Copy Link", command=self.on_copy_link).grid(row=15, column=0, columnspan=2, pady=5)

        self.refresh_list()

        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def refresh_list(self):
        for item in self.tree.get_children():           
            self.tree.delete(item)                       
        for row in self.db.get_all_items():
            self.tree.insert("", tk.END, values=(row["id"], row["title"], row["descriptions"], row["time"]))
            # CHANGED: was `self

    def on_delete_all(self):
        confirm_msg = messagebox.askyesno(
            "Delete All",
            "Are you sure you want to delete all items?"
        )
        if not confirm_msg:
            return
        self.db.delete_all_items()
        self.refresh_list()

    def on_copy_link(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Nothing selected", "Select an item first")
            return

        item_values = self.tree.item(selected[0])["values"]
        link = item_values[1]

        self.clipboard_clear()
        self.clipboard_append(link)

    def on_input(self):
        link = self.link.get().strip()
        desc = self.link_name.get().strip() 

        if not link or not desc:
            messagebox.showerror("Error", "Please fill in both fields")
            return

        self.db.add_item(link, desc)
        self.link.delete(0, tk.END)
        self.link_name.delete(0, tk.END)
        self.refresh_list()

    def on_close(self):
        self.db.close()
        self.destroy()
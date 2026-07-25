import tkinter as tk
from tkinter import messagebox
from db import Database

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Lister")
        self.geometry("400x400")

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

        tk.Button(self, text="View All", width = 25, command=self.print_all).grid(row=9, column=0, columnspan=2)

        self.listbox = tk.Listbox(self, width=50, height=10)
        self.listbox.grid(row=11, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)

        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.listbox.yview)
        self.scrollbar.grid(row=11, column=2, sticky="ns")

        self.listbox.config(yscrollcommand=self.scrollbar.set)

        tk.Button(self, text="Delete All", width = 25, command=self.on_delete_all).grid(row=13, column=0, columnspan=2)

        self.refresh_list()

        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def refresh_list(self):
        self.listbox.delete(0, tk.END)
        for row in self.db.get_all_items():
            display_text = f"[{row['id']}] {row['title']} — {row['descriptions']} ({row['time']})"
            self.listbox.insert(tk.END, display_text)

    def on_delete_all(self):
        confirm_msg = messagebox.askyesno(
            "Delete All",
            "Are you sure you want to delete all items?"
        )
        if not confirm_msg:
            return
        self.db.delete_all_items()
        self.refresh_list()

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

    def print_all(self):
        print(self.db.get_all_items())

    def on_close(self):
        self.db.close()
        self.destroy()
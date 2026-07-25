import tkinter as tk
from tkinter import ttk, messagebox
from db import Database
import ctypes
import os
import winsound

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        FONT_PATH = os.path.join(os.path.dirname(__file__), "fonts", "ArchivoBlack-Regular.ttf")
        self.load_font(FONT_PATH)
        self.title("Lister")
        self.configure(bg="#1e1e1e")
        width, height = 720, 720
        self.center_window(width, height)

        self.db = Database()

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        title_font = ("Archivo Black", 14)
        label_font = ("Archivo Black", 10)
        button_font = ("Archivo Black", 10)

        tk.Label(self, text="Lister the List Maker", bg="#f3921d", fg="#212c30", font=title_font).grid(row=0, column=0, columnspan=3, sticky="ew", pady=(0, 15))


        self.link = tk.Entry(self, bg="#2d2d2d", fg="white", insertbackground="white", width=70)
        self.link.grid(row=2, column=1)

        self.link_name = tk.Entry(self, bg="#2d2d2d", fg="white", insertbackground="white", width=70)
        self.link_name.grid(row=5, column=1)

        tk.Label(self, text="LINK: ", bg="#1e1e1e", fg="#2bf0cf", font=label_font).grid(row=2, column=0, sticky="e", padx=(0, 5))
        self.link.grid(row=2, column=1, sticky="w")

        tk.Label(self, text="DESC: ", bg="#1e1e1e", fg="#2bf0cf", font=label_font).grid(row=5, column=0, sticky="e", padx=(0, 5))
        self.link_name.grid(row=5, column=1, sticky="w")

        tk.Button(self, text="INPUT", width=25, command=self.on_input, bg="#3a3a3a", fg="#2bf0cf", font=button_font).grid(row=7, column=0, columnspan=2)
        self.bind("<Return>", lambda event: self.on_input())

        style = ttk.Style()
        style.theme_use("clam") 

        style.configure("Treeview",
            background="#2d2d2d",
            foreground="#2bf0cf",
            fieldbackground="#2d2d2d",
            bordercolor="#2d2d2d",
            lightcolor="#2d2d2d",
            darkcolor="#2d2d2d",
            rowheight=25,
            font=("Segoe UI", 10)
        )

        style.configure("Treeview.Heading",
            background="#3a3a3a",
            foreground="#d55a1e",
            bordercolor="#3a3a3a",
            lightcolor="#3a3a3a",
            darkcolor="#3a3a3a",
            font=("Segoe UI", 10, "bold")
        )

        style.map("Treeview",
            background=[("selected", "#4a6984")],
            foreground=[("selected", "white")]
        )

        style.layout("Treeview", [("Treeview.treearea", {"sticky": "nswe"})])

        column = ("id", "title", "descriptions", "time")
        self.tree = ttk.Treeview(self, columns=column, show="headings", height=15)

        self.tree.heading("id", text="ID")
        self.tree.heading("title", text="LINK")
        self.tree.heading("descriptions", text="DESCRIPTION")
        self.tree.heading("time", text="DATE")

        self.tree.column("id", width=30, anchor="center")
        self.tree.column("title", width=200)
        self.tree.column("descriptions", width=150)
        self.tree.column("time", width=100)

        self.tree.grid(row=10, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)  

        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview) 
        scrollbar.grid(row=10, column=2, sticky="ns")
        self.tree.configure(yscrollcommand=scrollbar.set)   

        delete_button_frame = tk.Frame(self, bg="#1e1e1e")
        delete_button_frame.grid(row=13, column=0, columnspan=2, pady=5)

        tk.Button(delete_button_frame, text="Delete Selected", command=self.delete_selected, bg="#3a3a3a", fg="#d55a1e", font=button_font).pack(side="left", padx=5)
        tk.Button(delete_button_frame, text="Delete All", command=self.on_delete_all, bg="#3a3a3a", fg="#d55a1e", font=button_font).pack(side="left", padx=5)
    
        tk.Button(self, text="COPY LINK", command=self.on_copy_link, bg="#3a3a3a", fg="#2bf0cf", font=button_font).grid(row=15, column=0, columnspan=2, pady=5)

        self.refresh_list()

        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def center_window(self, width, height):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.geometry(f"{width}x{height}+{x}+{y}")

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

    def delete_selected(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Nothing selected", "Select an item to delete first")
            return

        confirm_message = messagebox.askyesno(
            "Delete Item",
            "Delete this item permenantly?"
        )
        if not confirm_message:
            return

        item_values = self.tree.item(selected[0])["values"]
        item_id = item_values[0]

        self.db.delete_item(item_id)
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

        sfx_path = os.path.join(os.path.dirname(__file__), "sfx", "input.wav")
        winsound.PlaySound(sfx_path, winsound.SND_FILENAME | winsound.SND_ASYNC)

    def load_font(self, path):
        FR_PRIVATE = 0x10
        path = os.path.abspath(path)
        ctypes.windll.gdi32.AddFontResourceExW(path, FR_PRIVATE, 0)

    def on_close(self):
        sfx_path = os.path.join(os.path.dirname(__file__), "sfx", "close.wav")
        winsound.PlaySound(sfx_path, winsound.SND_FILENAME | winsound.SND_ASYNC)
        self.db.close()
        self.after(500, self.destroy)
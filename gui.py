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
        self.icon_image = tk.PhotoImage(file=os.path.join(os.path.dirname(__file__), "icons", "icon.gif"))
        icon_path = os.path.join(os.path.dirname(__file__), "icons", "icon.ico")
        self.iconbitmap(icon_path)
        self.iconphoto(True, self.icon_image)
        self.load_font(FONT_PATH)
        self.title("Lister")
        self.configure(bg="#1e1e1e")
        width, height = 720, 720
        self.center_window(width, height)

        self.db = Database()
        self.editing_id = None

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

        input_button_frame = tk.Frame(self, bg="#1e1e1e")
        input_button_frame.grid(row=7, column=0, columnspan=2, pady=5)

        self.input_button = tk.Button(input_button_frame, text="INPUT", width=25, command=self.on_input, bg="#3a3a3a", fg="#2bf0cf", font=button_font)
        self.input_button.pack(side="left", padx=5)

        tk.Button(input_button_frame, text="CANCEL", command=self.cancel_edit, bg="#3a3a3a", fg="#2bf0cf", font=button_font).pack(side="left", padx=5)
        self.bind("<Return>", lambda event: self.on_input())
        

        search_frame = tk.Frame(self, bg="#1e1e1e")
        search_frame.grid(row=8, column=0, columnspan=2, pady=(10, 5))

        tk.Label(search_frame, text="Search: ", bg="#1e1e1e", fg="#2bf0cf", font=label_font).pack(side="left")

        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", self.on_search)  

        self.search_entry = tk.Entry(search_frame, textvariable=self.search_var, bg="#2d2d2d", fg="white", insertbackground="white", width=40)
        self.search_entry.pack(side="left", padx=5)

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
        self.tree.bind("<Double-1>", self.on_row_select_for_edit)

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

        tk.Label(self, text="Note: Double click to update a record", bg="#1e1e1e", fg="#f3921d", font=label_font).grid(row=16, column=0, columnspan=2, pady=5)

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
            
    def on_delete_all(self):
        confirm_msg = messagebox.askyesno(
            "Delete All",
            "Are you sure you want to delete all items?"
        )
        if not confirm_msg:
            return
        self.db.delete_all_items()

        sfx_path = os.path.join(os.path.dirname(__file__), "sfx", "delete.wav")
        winsound.PlaySound(sfx_path, winsound.SND_FILENAME | winsound.SND_ASYNC)

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
        sfx_path = os.path.join(os.path.dirname(__file__), "sfx", "delete.wav")
        winsound.PlaySound(sfx_path, winsound.SND_FILENAME | winsound.SND_ASYNC)

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

        if self.editing_id is not None:
            self.db.update_item(self.editing_id, link, desc)
            self.editing_id = None
            self.input_button.config(text="Input")
        else:
            self.db.add_item(link, desc)
            sfx_path = os.path.join(os.path.dirname(__file__), "sfx", "input.wav")
            winsound.PlaySound(sfx_path, winsound.SND_FILENAME | winsound.SND_ASYNC)

        self.link.delete(0, tk.END)
        self.link_name.delete(0, tk.END)
        self.refresh_list()

    def load_font(self, path):
        FR_PRIVATE = 0x10
        path = os.path.abspath(path)
        ctypes.windll.gdi32.AddFontResourceExW(path, FR_PRIVATE, 0)

    def on_search(self, *args):
        query = self.search_var.get().strip().lower()

        for item in self.tree.get_children():
            self.tree.delete(item)

        if query:
            rows = self.db.search_items(query)
        else:
            rows = self.db.get_all_items()

        for row in rows:
            self.tree.insert("", tk.END, values=(row["id"], row["title"], row["descriptions"], row["time"]))

    def on_row_select_for_edit(self, event):
        selected = self.tree.selection()
        if not selected:
            return

        item_values = self.tree.item(selected[0])["values"]
        item_id, title, descriptions = item_values[0], item_values[1], item_values[2]

        self.link.delete(0, tk.END)
        self.link.insert(0, title)

        self.link_name.delete(0, tk.END)
        self.link_name.insert(0, descriptions)

        self.editing_id = item_id
        self.input_button.config(text="Update")

    def cancel_edit(self):
        self.editing_id = None
        self.link.delete(0, tk.END)
        self.link_name.delete(0, tk.END)
        self.input_button.config(text="Input")

    def on_close(self):
        sfx_path = os.path.join(os.path.dirname(__file__), "sfx", "close.wav")
        winsound.PlaySound(sfx_path, winsound.SND_FILENAME | winsound.SND_ASYNC)
        self.db.close()
        self.after(500, self.destroy)
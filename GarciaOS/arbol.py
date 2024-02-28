import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

class FileManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestor de Archivos")
        self.root.geometry("800x600")

        self.tree = ttk.Treeview(self.root)
        self.tree.pack(expand=True, fill="both", padx=10, pady=10)

        self.tree["columns"] = ("type", "size")
        self.tree.column("#0", width=250, minwidth=150)
        self.tree.column("type", width=100, anchor="center", stretch=tk.NO)
        self.tree.column("size", width=100, anchor="center", stretch=tk.NO)

        self.tree.heading("#0", text="Nombre", anchor=tk.W)
        self.tree.heading("type", text="Tipo", anchor=tk.W)
        self.tree.heading("size", text="Tamaño", anchor=tk.W)

        self.populate_tree()

    def populate_tree(self, path="."):
        self.tree.delete(*self.tree.get_children())  # Limpiar el árbol antes de repoblarlo
        try:
            for item in os.listdir(path):
                fullpath = os.path.join(path, item)
                if os.path.isdir(fullpath):
                    item_type = "Carpeta"
                    size = ""
                else:
                    item_type = "Archivo"
                    size = os.path.getsize(fullpath)
                self.tree.insert("", "end", text=item, values=(item_type, size))
        except Exception as e:
            messagebox.showerror("Error", str(e))

def main():
    root = tk.Tk()
    app = FileManager(root)
    root.mainloop()

if __name__ == "__main__":
    main()

import tkinter as tk
import json
import os

class ListItem(tk.Frame):
    def __init__(self, name: str, root: tk.Widget, rmv, save_callback=None):
        super().__init__(root, bg="#2b2b2b", padx=12, pady=10)

        self.name = name
        self.rmv = rmv
        self.save_callback = save_callback
        self.isediting = False

        # Row 1
        self.row1 = tk.Frame(self, bg="#2b2b2b")
        self.row1.pack(side="top", fill="x", pady=(0, 8))
        self.label = tk.Label(self.row1, text=self.name, bg="#2b2b2b", fg="#e0e0e0", font=("Segoe UI", 11), wraplength=250, justify="left")
        self.label.pack(side="left", fill="x", expand=True)

        self.buttons = tk.Frame(self.row1, bg="#2b2b2b")
        self.buttons.pack(side="right", padx=(10, 0))
        self.toggle_btn = tk.Button(
                    self.buttons,
                    text="✎",
                    command=self.clear,
                    background="#afe24a",
                    activebackground="#90bd35",
                    fg="black",
                    font=("Segoe UI", 10, "bold"),
                    relief="flat",
                    padx=8,
                    pady=4,
                    cursor="hand2"
                )

        self.toggle_btn.pack(side="left", padx=(0, 6))

        self.btn = tk.Button(
            self.buttons,
            text="✕",
            command=self.remove,
            background="#e74c3c",
            activebackground="#c0392b",
            fg="white",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            padx=8,
            pady=4,
            cursor="hand2"
        )
        self.btn.pack(side="right")
        

        # Row 2

        self.row2 = tk.Frame(self, bg="#2b2b2b")
        
        self.entry = tk.Entry(self.row2, bg="#3a3a3a", fg="#e0e0e0", font=("Segoe UI", 10), insertbackground="#4a90e2", relief="flat", bd=0)
        self.entry.pack(side="left", fill="x", expand=True, padx=(0, 6))

        self.confirm = tk.Button(
            self.row2,
            text="✓",
            command=self.edit,
            background="#27ae60",
            activebackground="#229954",
            fg="white",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            padx=8,
            pady=4,
            cursor="hand2"
        )
        self.confirm.pack(side="right")

        self.isediting = False
        
        
    def remove(self):
        self.rmv(self)
        
    def edit(self):
        if(self.entry.get().strip() == ""):
            return
        self.name = self.entry.get()
        self.label.config(text=self.entry.get())
        self.clear()
        if self.save_callback:
            self.save_callback()

    def clear(self):
        self.entry.delete(0, tk.END)
        self._toggle()

    def _toggle(self):
        if(self.isediting):
            self.row2.pack_forget()
            self.toggle_btn.config(text="✎")
        else:
            self.row2.pack(fill="x", pady=(10, 0))
            self.toggle_btn.config(text="▲")
        self.isediting = not self.isediting

class ToDo(tk.Frame):
    def __init__(self, root: tk.Widget):
        super().__init__(root, bg="#1a1a1a")
        self.lst = []
        self.save_file = "todos.json"
        self.isClearing = False
        # Title
        title = tk.Label(self, text="My To-Do List", bg="#1a1a1a", fg="#4a90e2", font=("Segoe UI", 18, "bold"), pady=20)
        title.pack()
        
        # Input frame
        self.frame = tk.Frame(self, bg="#1a1a1a")
        self.entry = tk.Entry(self.frame, bg="#3a3a3a", fg="#e0e0e0", font=("Segoe UI", 11), insertbackground="#4a90e2", relief="flat", bd=0)
        self.confirm = tk.Button(
            self.frame,
            text="+ Add",
            command=self.additem,
            background="#664ae2",
            activebackground="#5235bd",
            fg="white",
            font=("Segoe UI", 11, "bold"),
            relief="flat",
            padx=16,
            pady=8,
            cursor="hand2"
        )
        self.pack(fill="both", expand=True)
        self.frame.pack(fill="x", padx=15, pady=(0, 20))
        self.entry.pack(side="left", fill="both", expand=True, padx=(0, 10))
        self.confirm.pack(side="right")
        
        # Bottom frame (anchored to bottom)
        bottom_frame = tk.Frame(self, bg="#1a1a1a")
        bottom_frame.pack(side="bottom", fill="x", padx=15, pady=(10, 15))

        # Confirmation popup (hidden initially, appears above button)
        self.clear_frame = tk.Frame(bottom_frame, bg="#2b2b2b")
        desc = tk.Label(self.clear_frame, text="Are you sure you want to clear all items?", 
                        bg="#2b2b2b", fg="#e0e0e0", font=("Segoe UI", 11), pady=12)
        desc.pack()

        # Buttons frame
        button_frame = tk.Frame(self.clear_frame, bg="#2b2b2b")
        button_frame.pack(pady=(0, 12))

        confirm_btn = tk.Button(button_frame, text="Confirm", command=self.confirmClear,
                                background="#e74c3c", fg="white", font=("Segoe UI", 9, "bold"),
                                relief="flat", padx=12, pady=6, cursor="hand2")
        confirm_btn.pack(side="left", padx=5)

        cancel_btn = tk.Button(button_frame, text="Cancel", command=self.cancelClear,
                            background="#4a90e2", fg="white", font=("Segoe UI", 9, "bold"),
                            relief="flat", padx=12, pady=6, cursor="hand2")
        cancel_btn.pack(side="left", padx=5)
        
        # Keep it hidden initially
        self.clear_frame.pack_forget()

        # Clear All button (smaller, at bottom)
        self.clear_btn = tk.Button(
            bottom_frame,
            text="Clear All",
            command=self.tryClear,
            background="#880e00",
            activebackground="#c0392b",
            fg="white",
            font=("Segoe UI", 9, "bold"),
            relief="flat",
            padx=12,
            pady=5,
            cursor="hand2"
        )
        self.clear_btn.pack(side="bottom", fill="x")

        
        # Load saved items
        self.load_from_json()
    
    def save_to_json(self):
        """Save the list to a JSON file."""
        items = [item.name for item in self.lst]
        try:
            with open(self.save_file, 'w') as f:
                json.dump(items, f, indent=2)
        except Exception as e:
            print(f"Error saving to JSON: {e}")
    
    def load_from_json(self):
        """Load the list from a JSON file."""
        if os.path.exists(self.save_file):
            try:
                with open(self.save_file, 'r') as f:
                    items = json.load(f)
                    for item in items:
                        self.insert(item)
            except Exception as e:
                print(f"Error loading from JSON: {e}")
    
    def insert(self, name: str):
        item = ListItem(name, self, self.remove, self.save_to_json)
        item.pack(fill="x", padx=10, pady=(0, 8))
        self.lst.append(item)
    
    def remove(self, item: ListItem):
        if item in self.lst:
            self.lst.remove(item)
            item.destroy()
            self.save_to_json()
    
    def additem(self):
        if(self.entry.get().strip() == ""):
            return
        self.insert(self.entry.get())
        self.entry.delete(0, tk.END)
        self.save_to_json()

    def tryClear(self):
        # Show the confirmation popup
        if(self.isClearing):
            self.cancelClear()
            return
        self.isClearing = True
        self.clear_frame.pack(side="top", fill="x", pady=(10, 0))
        
    def cancelClear(self):
        # Hide the confirmation popup
        self.isClearing = False
        self.clear_frame.pack_forget()

    def confirmClear(self):
        # Clear items and hide popup
        self.isClearing = False
        self.clearAll()
        self.clear_frame.pack_forget()

    def clearAll(self):
        for item in list(self.lst):
            self.lst.remove(item)
            item.destroy()
        self.save_to_json()

def main():
    root = tk.Tk()
    root.title("To-Do List")
    root.geometry("450x750")
    root.configure(bg='#1a1a1a')
    root.resizable(True, True)
    lst = ToDo(root)
    
    # Save on window close
    def on_closing():
        lst.save_to_json()
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()

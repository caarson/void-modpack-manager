# Void Modpack Manager - Main Entry Point
import tkinter as tk
from mod_manager import ModManager
from ui import UIManager

def main():
    root = tk.Tk()
    manager = ModManager()
    ui = UIManager(root, manager)
    ui.setup_ui()
    root.mainloop()

if __name__ == "__main__":
    main()

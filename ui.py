# Void Modpack Manager - GUI Module

import tkinter as tk
from tkinter import filedialog, messagebox
from mod_manager import ModManager

class UIManager:
    def __init__(self, root, manager):
        self.root = root
        self.manager = manager
        
        # UI elements
        self.mod_list_frame = None
        self.upload_button = None
        self.apply_button = None
        self.config_minecraft_dir_button = None
        
    def setup_ui(self):
        """Setup the main GUI window."""
        self.root.title("Void Modpack Manager")
        self.root.geometry("600x400")
        
        # Main frame for controls
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Top control panel
        top_frame = tk.Frame(main_frame)
        top_frame.pack(fill=tk.X)
        
        self.upload_button = tk.Button(top_frame, text="Upload .jar", command=self.handle_upload)
        self.upload_button.pack(side=tk.LEFT)
        
        self.apply_button = tk.Button(top_frame, text="Apply Mods", command=self.handle_apply_mods)
        self.apply_button.pack(side=tk.RIGHT)
        
        # Minecraft directory config
        if self.manager.minecraft_dir is None:
            self.config_minecraft_dir_button = tk.Button(
                top_frame,
                text="Configure Minecraft Directory",
                command=self.configure_minecraft_dir
            )
            self.config_minecraft_dir_button.pack(side=tk.LEFT, padx=5)
        
        # Mod list sections - split into left and right
        mod_list_container = tk.Frame(main_frame)
        mod_list_container.pack(fill=tk.BOTH, expand=True)
        
        # Left side: all mods 
        self.mod_list_frame_left = tk.Frame(mod_list_container)
        self.mod_list_frame_left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Right side: active mods (highlighted)
        self.mod_list_frame_right = tk.Frame(mod_list_container)
        self.mod_list_frame_right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Load mods from Minecraft directory
        self.manager.load_mods_list()
        self.refresh_mod_lists()
    
    def refresh_mod_list(self):
        """Update the mod list UI."""
        for widget in self.mod_list_frame.winfo_children():
            widget.destroy()
            
        for i, mod in enumerate(self.manager.mods):
            frame = tk.Frame(self.mod_list_frame)
            frame.pack(fill=tk.X, pady=2)
            
            # Checkbox to enable/disable
            var = tk.BooleanVar(value=mod["enabled"])
            checkbox = tk.Checkbutton(frame, text=mod["name"], variable=var, command=lambda v=var, m=mod: self.update_mod_enabled(m["name"], v.get()))
            checkbox.pack(side=tk.LEFT)
            
            # Label for mod name
            label = tk.Label(frame, text=mod["name"])
            label.pack(side=tk.RIGHT)
    
    def handle_upload(self):
        """Handle custom .jar file upload."""
        file_path = filedialog.askopenfilename(
            title="Select .jar file",
            filetypes=[("Jar Files", "*.jar")]
        )
        
        if file_path:
            try:
                self.manager.add_custom_mod(file_path)
                self.refresh_mod_list()
            except FileNotFoundError as e:
                messagebox.showerror("Error", str(e))
    
    def handle_apply_mods(self):
        """Apply mods to Minecraft directory."""
        # Check if Minecraft dir is configured
        if self.manager.minecraft_dir is None:
            messagebox.showerror("Error", "Minecraft directory not configured")
            return
            
        try:
            self.manager.sync_mods_to_minecraft()
            messagebox.showinfo("Success", "Mods applied successfully")
        except ValueError as e:
            messagebox.showerror("Error", str(e))
    
    def configure_minecraft_dir(self):
        """Configure Minecraft installation directory manually."""
        dir_path = filedialog.askdirectory(
            title="Select Minecraft Directory"
        )
        
        if dir_path:
            self.manager.minecraft_dir = dir_path
            # Refresh UI to remove config button
            self.config_minecraft_dir_button.destroy()
            messagebox.showinfo("Success", "Minecraft directory configured")

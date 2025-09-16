# Void Modpack Manager - Core Logic Module

import os
import platform
from pathlib import Path

class ModManager:
    def __init__(self):
        self.mods = []
        self.minecraft_dir = None
        self.detect_minecraft_directory()
    
    def detect_minecraft_directory(self):
        """Automatically detect Minecraft installation directory."""
        system = platform.system()
        
        if system == "Windows":
            # Specific Windows 11 paths for Minecraft installations:
            possible_dirs = [
                os.path.expanduser("~/.minecraft"),  # Java Edition default
                os.path.expanduser("~/AppData/Roaming/.minecraft"),  # Java Edition user profile path
                os.path.expanduser("~/Minecraft"),  # common alternative
                "C:\\Program Files (x86)\\Minecraft Launcher",  # Launcher install path
                "C:\\Program Files\\Minecraft Launcher"  # Launcher install path
            ]
        elif system == "Darwin":  # macOS
            possible_dirs = [
                os.path.expanduser("~/Library/Application Support/minecraft"),
                os.path.expanduser("~/minecraft")
            ]
        else:  # Linux
            possible_dirs = [
                os.path.expanduser("~/.minecraft"),
                os.path.expanduser("~/minecraft")
            ]
        
        for path in possible_dirs:
            if os.path.exists(path):
                self.minecraft_dir = Path(path)
                return
        
        # If not found, set to None so user can configure manually
        self.minecraft_dir = None
    
    def get_minecraft_mods_directory(self):
        """Get the mods directory within Minecraft installation."""
        if self.minecraft_dir is None:
            raise ValueError("Minecraft directory not configured")
        
        mods_path = self.minecraft_dir / "mods"
        return mods_path
    
    def load_mods_list(self):
        """Load existing mods from Minecraft mods folder."""
        mods_path = self.get_minecraft_mods_directory()
        if not mods_path.exists():
            mods_path.mkdir(parents=True)
            
        # Simple list of .jar files in the directory
        jar_files = [f for f in mods_path.iterdir() if f.name.endswith(".jar")]
        
        # Create mod objects with name and enable state
        self.mods = [{ "name": str(f), "enabled": True } for f in jar_files]
    
    def add_custom_mod(self, file_path):
        """Add a custom .jar file to mods list."""
        if not os.path.exists(file_path):
            raise FileNotFoundError("File does not exist")
        
        # Add mod entry
        self.mods.append({ 
            "name": file_path,
            "enabled": True
        })
    
    def sync_mods_to_minecraft(self):
        """Sync enabled mods to Minecraft mods folder."""
        if self.minecraft_dir is None:
            raise ValueError("Minecraft directory not configured")
        
        mods_path = self.get_minecraft_mods_directory()
        
        # Clear current mods folder
        for f in mods_path.iterdir():
            if f.name.endswith(".jar"):
                f.unlink()
                
        # Copy enabled mods to the folder
        for mod in self.mods:
            if mod["enabled"]:
                import shutil
                src = Path(mod["name"])
                dst = mods_path / src.name
                shutil.copy2(src, dst)
                
    def set_mod_enabled(self, name, enable):
        """Set a specific mod's enabled state."""
        for mod in self.mods:
            if mod["name"] == name:
                mod["enabled"] = enable
                break

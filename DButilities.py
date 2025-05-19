import json
import os

class DButilities:
    def __init__(self):
        # File paths for different databases
        self.db_paths = {
            "Users": "DBes\\Users.json",
            "Businesses": "DBes\\businnesses.json",
            "Comments": "DBes\\Comments.json"
        }

    def get_path(self, name):
        """Return the file path for the specified database."""
        return self.db_paths.get(name)

    def get_data(self, name):
        """Retrieve data from the specified database (JSON file)."""
        path = self.get_path(name)
        if not path or not os.path.exists(path):
            print(f"Error: {name} database path not found.")
            return {}

        try:
            with open(path, 'r') as file:
                data = json.load(file)
            return data
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"Error reading {name} data: {e}")
            return {}

    def update_data(self, name, data):
        """Update the specified database with new data."""
        path = self.get_path(name)
        if not path:
            print(f"Error: Invalid database name {name}.")
            return
        
        try:
            with open(path, 'w') as file:
                json.dump(data, file, indent=4)
        except IOError as e:
            print(f"Error writing {name} data: {e}")

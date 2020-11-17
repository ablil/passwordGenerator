import json
import os
from typing import Dict, List

class Loader:

    def __init__(self, filename):
        self.filename = filename
        

    def validate_file(self):
        if not os.path.exists(self.filename):
            print(f"File {self.filename} NOT Found !!!")
            exit(1)

        if not os.path.isfile(self.filename):
            print(f"{self.filename} is NOT a file")
            exit(1)

    def json_import(self):
        """Import password from json file"""
        self.validate_file()
        
        with open(self.filename, 'r+') as f:
            data = json.load(f)

        return data['passwords']


    def json_export(self, passwords_list: List[Dict]):
        data = {
            "passwords": passwords_list
        }

        with open(self.filename, 'w+') as f:
            json.dump(data, f, indent=2)

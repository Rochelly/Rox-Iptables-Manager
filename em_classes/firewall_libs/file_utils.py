import os
import datetime
import re
class File_Utils:

    def __init__(self,dir_base) -> None:
        self.last_checked_file=dir_base+"last_checked.txt"
        self.dir_base=dir_base
        self.last_checked_date=datetime.datetime.fromisoformat('2000-01-01 00:00:00')

    
    def get_key_in_file(self, file_name, key):
        with open(file_name) as file:
            value = ''
            for line in file:
                if line.startswith(f'{key}='):
                    value = line.strip().split('=')[1]
                    break
        return value
    
              

    def get_changed_files(self):
        if os.path.exists(self.last_checked_file):
            with open(self.last_checked_file, 'r') as f:
                last_checked_date = datetime.datetime.fromisoformat(f.read().strip())
        
        files = os.listdir(self.dir_base)
        modified_files = []

        for file in files:
            file_path = os.path.join(self.dir_base, file)
            modification_time = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))
            if modification_time > last_checked_date and os.path.splitext(file)[-1] == '.fw':
                modified_files.append(file)

        with open(self.last_checked_file, 'w') as f:
            f.write(datetime.datetime.now().isoformat())

        return modified_files

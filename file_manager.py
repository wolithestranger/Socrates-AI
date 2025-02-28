import json
import os 
from datetime import datetime



class FileManager:
    def __init__(self, base_dir = './'):

        self.base_dir = base_dir
        self.allowed_extensions = ['.py','.txt', '.pdf', 'json', '.md']
        self.allowed_paths = ['.', 'src','resources', 'data','documents']
        
    def get_file_path(self, filename):
        for path in self.allowed_paths:
            file_path = os.path.join(self.base_dir, path, filename)
            if os.path.isfile(file_path):
                return file_path
        return None
    
    def read_file(self, filename, start_line = None, end_line=None):

        file_path = self.get_file_path(filename)
        
        if file_path is not None:
            try:
                # Try opening the file with UTF-8 encoding
                with open(file_path, 'r', encoding='utf-8') as file:
                    lines = file.readlines()
                    total_lines=len(lines)

                    #apply line range if specified
                    if start_line and end_line:
                        start_line =  max(0,start_line-1)# converts to 0-based index
                        end_line = min(total_lines, end_line)
                        lines = lines[start_line:end_line]
                    
                    #convert to a single string
                    content= ''.join(lines)
                    return content


                    #return file.read()
            except UnicodeDecodeError:
                print(f"UTF-8 decoding failed for {filename}. Trying alternative encoding...")
                try:
                    with open(file_path, 'r', encoding='latin-1') as file:
                        lines = file.read()
                        if start_line and end_line:
                            start_line = max(0, start_line -1)
                            end_line = min(len(lines), end_line)
                            lines = lines[start_line:end_line]
                        content = ''.join(lines)
                        return content
                except Exception as e:
                    print(f"Error reading {filename} with alternative encoding: {e}")
                    return None
            except PermissionError:
                print(f"Permission denied to access {filename}")
                return None
            except Exception as e:
                print(f"An error occurred while reading {filename}: {e}")
                return None
        else:
            print(f"File {filename} not found in allowed directories.")
            return None  

    
    def get_code_context(self, filename, line_start =None, line_end=None):
        code = self.read_code_file (filename)
        if code is None:
            return None
        
        if line_start and line_end:
            lines = code.splitlines()
            selected_lines = lines[line_start-1: line_end]
            return '\n'.join(selected_lines)
        else:
            return code
        
    def create_code_summary(self, filname):
        code = self.read_code_files(filname)
        if code is None:
            return "Unable to summarize. Code file not found."
        
        summary = f"# {filname}\n\n"
        summary += "### Code Preview:\n"
        lines = code.splitlines()
        if len(lines) > 10:
            summary += "\n".join(lines[:10]) + "\n..."
        else:
            summary += "\n".join(lines)

        return summary
    
    def save_code_changes(self, filename, content):
        file_path = self.get_file_path(filename)
        if file_path:
            try:
                with open(file_path, 'w') as file:
                    file.write(content)
                return True
            except Exception as e:
                print(f"Error saving changes to {filename}: {e}")
        return False
        


    # def check_file_extension(self, filename):
    #     return os.path.splitext(filename)[1] in self.allowed_extensions

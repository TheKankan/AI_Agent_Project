import os
from config import MAX_CHARS

def get_file_content(working_directory, file_path):
    
    print(f'result for "{file_path}" file:')
    abs_working_directory = os.path.abspath(working_directory)
    full_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not os.path.isfile(full_path):
        return(f'Error: File not found or is not a regular file: "{file_path}"')

    if not str(full_path).startswith(str(abs_working_directory)):
        return(f'Error: Cannot read "{file_path}" as it is outside the permitted working directory')

    try:
        with open(full_path, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            if len(file_content_string) >= MAX_CHARS:
                file_content_string += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
            return file_content_string
    except Exception as e:
        return f'Error reading file "{file_path}": {e}'


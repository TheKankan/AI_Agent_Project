import os

def write_file(working_directory, file_path, content):
    abs_working_directory = os.path.abspath(working_directory)
    full_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not str(full_path).startswith(str(abs_working_directory)):
        return(f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory')

    if not os.path.exists(full_path):
        try:
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
        except Exception as e:
            return f"Error: creating directory: {e}"
    if os.path.exists(full_path) and os.path.isdir(full_path):
        return f'Error: "{file_path}" is a directory, not a file'
    try:
        with open(full_path, "w") as f:
            f.write(content)
        return (
            f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        )
    except Exception as e:
        return f"Error: writing to file: {e}"
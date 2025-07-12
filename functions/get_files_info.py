import os

def get_files_info(working_directory, directory=None):

    
    abs_working_directory = os.path.abspath(working_directory)
    full_path = abs_working_directory

    if directory:
        print(f'result for "{directory}" directory:')
        full_path = os.path.abspath(os.path.join(working_directory, directory))
    else:
        print(f'result for "{working_directory}" directory:')

    if not os.path.isdir(full_path):
        return(f'Error: "{directory}" is not a directory')

    if not str(full_path).startswith(str(abs_working_directory)):
        return(f'Error: Cannot list "{directory}" as it is outside the permitted working directory')

    file_list = os.listdir(full_path)
    file_new_list = []

    for file in file_list:
        file_path = os.path.join(full_path, file)
        file_text = (f"- {file}: file_size={os.path.getsize(file_path)} bytes, is_dir={os.path.isdir(file_path)}")
        file_new_list.append(file_text)
    return "\n".join(file_new_list) 
import os
import subprocess

def run_python_file(working_directory, file_path, args=[]):
    abs_working_directory = os.path.abspath(working_directory)
    full_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not str(full_path).startswith(str(abs_working_directory)):
        return(f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory')

    if not os.path.exists(full_path):
        return(f'Error: File "{file_path}" not found.')

    if not file_path.endswith(".py"):
        return(f'Error: "{file_path}" is not a Python file.')

    cmd = ["python", full_path] + args
    try:
        cmd_output = subprocess.run(cmd, cwd=working_directory,capture_output=True, timeout=30, text=True)
    except Exception as e:
        return f"Error: executing Python file: {e}"

    cmd_str = ""

    if (not cmd_output.stdout == "") or (not cmd_output.stderr == ""):
        cmd_str = f"STDOUT: {cmd_output.stdout}\nSTDERR: {cmd_output.stderr}"
    else:
        return "No output produced."
    
    if cmd_output.returncode != 0:
        cmd_str += f"\nProcess exited with code {cmd_output.returncode}"
    return cmd_str


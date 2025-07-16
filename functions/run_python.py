import os
import subprocess
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="runs a python script in the specified directory, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the script to run, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.STRING,
                description="the arguments to be used in the script",
            ),
        },
    ),
)


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


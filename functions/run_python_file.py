import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path:str, args=[]):
    abs_working_dir = os.path.abspath(working_directory)
    target_file = os.path.abspath(os.path.join(working_directory, file_path))
   
    # return file_path.endswith("py")
    if not file_path.endswith("py"):
        return f'Error: "{file_path}" is not a Python file.'

    if not target_file.startswith(abs_working_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.isfile(target_file):
        return f'Error: File "{file_path}" not found.'
    
    try: 
        if args!= []: 
            result = subprocess.run(["python",target_file," ".join(args)], timeout=30.0)
        else:
            result = subprocess.run(["python",target_file], timeout=30.0)
        
        if result.returncode != 0:
            return f"STDOUT: {result.stdout} and STDERR: {result.stderr} Process exited with code {result.returncode}"
        
        if not result.stdout:
            return f"STDOUT: No output produced and STDERR: {result.stderr} "
        
        return f"STDOUT: {result.stdout} and STDERR: {result.stderr} \n\nresult: {result.stdout}"
    except Exception as e:
        return f"Error: executing Python file: {e}"


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a specific python file given that the file_path privided in the parameter is a python file. It uses subprocess.run() inside and it will return STDOUT, STDERR and if there is a non zero return code it will also give the return code.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The relative file path to the file, relative to the working directory. It must be provided",
            ),
            "args": types.Schema(
                type= types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING
                ),
                description="Arguments in order to get a specific file with arguments. Example: python main.py '2+3' the last '2+3' will be passed as an argument as ['2+3']",
            )
        },
    ),
)

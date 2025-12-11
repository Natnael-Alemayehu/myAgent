import os
from google.genai import types

def write_file(working_directory, file_path, content):
    absolute_working_dir = os.path.abspath(working_directory)
    target_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not target_file_path.startswith(absolute_working_dir):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    try:
        with open(target_file_path, "w") as f:
            if f.write(content):
                return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: error writing to file. {e}"

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="This function will write to a file being passed a file_path to write to and content to write as the parameter. If the file doesn't exist it will create the file. if text was in the file it will be overwritten with the new content.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The relative file path to the file, relative to the working directory. It must be provided",
            ),
            "content": types.Schema(
                type= types.Type.STRING,
                description="The content that will be written in the file."
            )
        },
    ),
)

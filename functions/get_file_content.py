import os
from config import MAX_CHARS
from google.genai import types

def get_file_content(working_directory, file_path):
    absolute_working_dir = os.path.abspath(working_directory)
    target_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not target_file_path.startswith(absolute_working_dir):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if os.path.isfile(target_file_path):
        f'Error: File not found or is not a regular file: "{file_path}"'

    try:
        with open(target_file_path, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            return f"{file_content_string} ...File {file_path} truncated at 10000 characters"

    except Exception as e:
        return f"Error: {e}"
    
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Lists the contents of a file in the specified directory. If the file is too large it will end with this message '...File with file_name and  truncated at 10000 characters'",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The relative file path to the file, relative to the working directory. It must be provided",
            ),
        },
    ),
)
import os
from config import MAX_CHARS

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
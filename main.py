import os
import argparse
import prompts
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.write_file import schema_write_file
from functions.run_python_file import schema_run_python_file

def main():
    parser = argparse.ArgumentParser(
        prog="myAgent",
        description="This is my cli agent that uses gemini 2.5 flash",
        epilog="For more help please contact se.natnael.alemayehu@gmail.com"
    )
    parser.add_argument("user_prompt", type=str, help="user prompt to be sent to Gemini AI")
    parser.add_argument("--verbose", action="store_true", help="prints debug information of the cli" )
    args = parser.parse_args()

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    
    if not api_key:
        raise RuntimeError("API key not found")
    client = genai.Client(api_key=api_key)


    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    available_functions = types.Tool(
        function_declarations=[schema_get_files_info, schema_get_file_content, schema_write_file, schema_run_python_file]
    )
    
    response = client.models.generate_content(
        model='gemini-2.5-flash', 
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=prompts.system_prompt)
    )

    if not response.usage_metadata:
        raise RuntimeError("Gemini API response appears to be malformed")
    
    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}") 

    print("Response:")
    # print(response.text)

    for function_call in response.function_calls:
        print(f"Calling function: {function_call.name}({function_call.args})")


if __name__ == "__main__":
    main()

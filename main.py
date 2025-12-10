import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
import functions


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

    response = client.models.generate_content(
        model='gemini-2.5-flash', contents=messages
    )
    if not response.usage_metadata:
        raise RuntimeError("Gemini API response appears to be malformed")
    
    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}") 

    print("Response:")
    print(response.text)

    print(os.path.join("calculator", "."))
    

if __name__ == "__main__":
    main()

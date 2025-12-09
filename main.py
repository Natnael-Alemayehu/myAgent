import os
import argparse
from dotenv import load_dotenv
from google import genai




def main():
    parser = argparse.ArgumentParser(
        prog="myAgent",
        description="This is my cli agent that uses gemini 2.5 flash",
        epilog="For more help please contact se.natnael.alemayehu@gmail.com"
    )
    parser.add_argument("user_prompt", type=str, help="user prompt to be sent to Gemini AI")
    args = parser.parse_args()
    
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    
    if not api_key:
        raise RuntimeError("API key not found")
    client = genai.Client(api_key=api_key)


    response = client.models.generate_content(
        model='gemini-2.5-flash', contents=args.prompt
    )
    if not response.usage_metadata:
        raise RuntimeError("Gemini API response appears to be malformed")
        
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}") 
    print("Response:")
    print(response.text)



if __name__ == "__main__":
    main()

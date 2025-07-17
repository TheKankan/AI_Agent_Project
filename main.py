import os
from dotenv import load_dotenv
from google import genai
import sys
from google.genai import types
from prompts import system_prompt
from call_function import available_functions, call_function


#main
def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    if len(sys.argv) < 2:
        print("AI Code Assistant")
        print('\nUsage: python main.py "your prompt here" [--verbose]')
        print('Example: python main.py "How do I fix the calculator?"')
        sys.exit(1)

    user_prompt = sys.argv[1]

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    verbose = False

    if len(sys.argv) > 2:
        if sys.argv[2] == "--verbose":
            verbose = True
    
    try:
        for i in range(20): #limiting functions calls to 20 to prevent infinite loop
            response = generate_content(client,messages,verbose)
            if response is not None:
                print(response)
                break
        else:
            print("Reached max iterations (20) without a final response.")
    except Exception as e:
        print(f"An error occurred: {e}")
    
    




def generate_content(client,messages, verbose):
    response = client.models.generate_content(
        model="gemini-2.0-flash-001", 
        contents=messages,
        config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt),
    )
    for candidate in response.candidates:
        messages.append(candidate.content)

    if verbose: #if the verbose flag has been written by the user
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    if not response.function_calls: #if no function is called
        return(response.text)

    function_responses = [] #when the AI calls a function
    for function_call_part in response.function_calls:
        function_call_result = call_function(function_call_part, verbose)
        if not function_call_result.parts or not function_call_result.parts[0].function_response.response:
            raise Exception("empty function call result")
        if verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")
        function_responses.append(function_call_result.parts[0])

    for f_response in function_responses:
        messages.append(types.Content(role="tool", parts=[f_response]))
    
    if not function_responses:
        raise Exception("no function responses generated, exiting.")
    
    return None # Return None if a function was called and another iteration is needed

if __name__ == "__main__":
    main()
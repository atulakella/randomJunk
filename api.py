import google.generativeai as genai

def configure_genai():
    genai.configure(api_key='AIzaSyD5HvoyjOQMIBNJRrFK3O4sxDap--BVU_Q')

def generate_gemini_response(prompt):
    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt)
        return response.text.replace('*', '') if response.text else "No response available."
    except Exception as e:
        return f"Error: {str(e)}"
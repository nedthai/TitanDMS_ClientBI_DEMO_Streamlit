import os
import google.generativeai as genai
from dotenv import load_dotenv
from src.prompts import SQL_GENERATION_PROMPT, INTERPRETATION_PROMPT

load_dotenv()

def _get_api_keys():
    """Returns a list of available API keys from environment."""
    keys = [os.getenv("GEMINI_API_KEY"), os.getenv("GEMINI_API_KEY_2")]
    return [k for k in keys if k]

def get_best_model():
    """Find the best available model for the active API key."""
    try:
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        preferred = [
            'models/gemini-2.5-flash',
            'models/gemini-2.5-pro',
            'models/gemini-2.0-flash',
            'models/gemini-1.5-pro',
            'models/gemini-flash-latest',
        ]
        
        for p in preferred:
            if p in available_models:
                return genai.GenerativeModel(p)
        
        if available_models:
            return genai.GenerativeModel(available_models[0])
            
        raise Exception("No generative models found.")
    except Exception:
        return genai.GenerativeModel("gemini-1.5-flash")

def _generate_with_fallback(prompt: str) -> str:
    """Attempts to generate content, rotating keys if a quota error occurs.
    This correctly catches 429 errors from generate_content and pivots keys.
    """
    keys = _get_api_keys()
    if not keys:
        raise Exception("No Gemini API keys found in environment.")
        
    last_error = None
    for i, key in enumerate(keys):
        try:
            genai.configure(api_key=key)
            model = get_best_model() # Fetch model for this specific key
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            last_error = e
            if "429" in str(e) or "quota" in str(e).lower():
                print(f"API Key {i+1} hit quota or rate limit. Trying next key if available...")
                continue # Key is exhausted, try next one
            raise e # Other error (e.g. invalid key format), stop here
            
    if last_error:
        raise Exception(f"All configured API keys have exceeded their quota. Last error: {last_error}")

def generate_sql(user_question: str, data_dictionary: str) -> str:
    """Generate a SQL query with transparent key rotation."""
    prompt = SQL_GENERATION_PROMPT.format(
        data_dictionary=data_dictionary,
        user_question=user_question
    )
    result = _generate_with_fallback(prompt)
    return result.replace("```sql", "").replace("```", "").strip()

def interpret_results(user_question: str, data_results: str,
                      user_chart_preference: str = "Not specified") -> str:
    """Interpret results with transparent key rotation."""
    prompt = INTERPRETATION_PROMPT.format(
        data_results=data_results,
        user_question=user_question,
        user_chart_preference=user_chart_preference,
    )
    return _generate_with_fallback(prompt)

import os
from google import genai
from dotenv import load_dotenv
from src.prompts import SQL_GENERATION_PROMPT, INTERPRETATION_PROMPT

load_dotenv()

def _get_api_keys():
    """Returns a list of available API keys from environment."""
    keys = [os.getenv("GEMINI_API_KEY"), os.getenv("GEMINI_API_KEY_2"), os.getenv("GEMINI_API_KEY_3")]
    return [k for k in keys if k]

def _get_preferred_models():
    """Returns a prioritized list of models to try."""
    return [
        'gemini-2.5-pro',
        'gemini-2.5-flash',
        'gemini-2.0-flash',
        'gemini-3.1-pro-preview',
        'gemini-3.1-flash-lite-preview',
        'gemini-3-pro-preview',
        'gemini-3-flash-preview',
        'gemini-1.5-pro',
        'gemini-flash-latest',
        'gemini-flash-lite-latest',
        'gemini-1.5-flash',
    ]

def _generate_with_fallback(prompt: str) -> str:
    """Attempts to generate content with a multi-layered fallback strategy.
    1. It tries the best model across all keys first.
    2. If all keys fail for the best model, it moves to the next model in preference list.
    """
    keys = _get_api_keys()
    if not keys:
        raise Exception("No Gemini API keys found in environment.")
        
    preferred_models = _get_preferred_models()
    clients = [{"key_index": i+1, "client": genai.Client(api_key=key), "supported": None} for i, key in enumerate(keys)]
    
    last_error = None
    
    # Tiered approach: Try each model across ALL keys before moving to a lower model
    for model_name in preferred_models:
        for item in clients:
            idx = item["key_index"]
            client = item["client"]
            
            # Lazy-load supported models for this client once
            if item["supported"] is None:
                try:
                    item["supported"] = [m.name.replace("models/", "") for m in client.models.list()]
                except Exception:
                    item["supported"] = []

            # Skip if this specific model name is not in the key's available list
            if model_name not in item["supported"]:
                continue
                
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt
                )
                return response.text
            except Exception as e:
                last_error = e
                err_msg = str(e).lower()
                if "429" in err_msg or "quota" in err_msg or "limit" in err_msg:
                    # Rate limited on this key for this model, try next key OR next model
                    print(f"API Key {idx} hit limit for {model_name}. Pivoting...")
                    continue 
                # For non-429 errors (e.g. safety, invalid request), we might want to stop early or just skip key
                continue

    if last_error:
        raise Exception(f"All configured API keys and models have failed or exceeded quota. Last error: {last_error}")
    raise Exception("No suitable models found or all keys failed.")

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

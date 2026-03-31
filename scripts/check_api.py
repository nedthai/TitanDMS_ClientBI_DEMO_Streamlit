import os
import sys
from google import genai
from dotenv import load_dotenv

# Find the .env file in the parent directory relative to this script
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path)

def check_keys():
    keys = [
        os.getenv("GEMINI_API_KEY"),
        os.getenv("GEMINI_API_KEY_2"),
        os.getenv("GEMINI_API_KEY_3")
    ]
    
    # Filter out empty keys
    keys = [k for k in keys if k]
    
    if not keys:
        print("❌ No API keys found in .env")
        return

    print("="*60)
    print("💎 GEMINI API HEALTH & QUOTA DIAGNOSTIC")
    print("="*60)
    print(f"Checking {len(keys)} configured keys...\n")
    
    for i, key in enumerate(keys):
        label = f"Key {i+1} ({key[:8]}...{key[-4:]})"
        print(f"👉 TESTING {label}:")
        
        try:
            client = genai.Client(api_key=key)
            
            # 1. Fetch available model names
            try:
                available_models = list(client.models.list())
                # Filter for generative-looking names
                gen_models = [m.name for m in available_models if 'gemini' in m.name.lower()]
                
                if not gen_models:
                    print(f"    ⚠️ No 'gemini' models found for this key.")
                    continue
                
                print(f"    📊 Found {len(gen_models)} Gemini models.")
                
                # 2. Check each model for rate limit
                for mod_name in gen_models:
                    clean_name = mod_name.replace("models/", "")
                    short_name = clean_name.ljust(25)
                    
                    try:
                        # Simple generation attempt
                        client.models.generate_content(
                            model=clean_name,
                            contents="Hi"
                        )
                        print(f"       ✅ {short_name}: ACTIVE (Within Quota)")
                    except Exception as mod_e:
                        err_str = str(mod_e).lower()
                        if "429" in err_str or "quota" in err_str or "limit" in err_str:
                            print(f"       ❌ {short_name}: RATE LIMITED (Reached Limit)")
                        elif "404" in err_str or "not found" in err_str:
                            # Some models listed might not actually be generative (e.g. preview)
                            # or might not exist in the region/version being used.
                            print(f"       ❓ {short_name}: NOT FOUND (Disabled/Hidden)")
                        else:
                            print(f"       ⚠️ {short_name}: ERROR ({type(mod_e).__name__})")
                            
            except Exception as list_e:
                print(f"    ❌ Failed to list models for this key: {list_e}")

        except Exception as e:
            print(f"    ❌ CRITICAL ERROR initializing key: {e}")
        
        print("-" * 60)

    # Clean up test attr script
    test_script = os.path.join(os.path.dirname(__file__), 'test_attr.py')
    if os.path.exists(test_script):
        os.remove(test_script)

if __name__ == "__main__":
    check_keys()

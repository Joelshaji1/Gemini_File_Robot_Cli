"""
Gemini File Robot
A CLI tool to organize files using Google's Gemini AI.
"""
import os
import shutil
import json
from openai import OpenAI
from dotenv import load_dotenv

# --- SETUP ---
load_dotenv("APIKEY.env")
OPENROUTER_KEY = os.getenv("OPENROUTER_API_KEY") or os.getenv("GEMINI_API_KEY") # Fallback for now

if not OPENROUTER_KEY:
    print("❌ API Key Missing! Check your APIKEY.env file.")
    input("Press Enter to exit...")
    exit()

client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=OPENROUTER_KEY,
)

# --- THE BRAIN ---
def ask_gemini(user_input):
    system_prompt = f"""
    You are a file system robot. Convert the user's request into a JSON command.
    
    Format:
    {{
      "action": "collect_files" or "list_files",
      "file_type": "pdf",
      "search_path": "C:\\\\Users",
      "dest": "C:\\\\Collected_PDFs"
    }}

    Rules:
    - If user says "Desktop", use "C:\\\\Users\\\\{os.getlogin()}\\\\Desktop"
    - If user says "C drive", use "C:\\\\"
    - If no destination specified, use "C:\\\\Users\\\\{os.getlogin()}\\\\Desktop\\\\Collected_Files"
    """
    
    response = client.chat.completions.create(
      model="google/gemini-2.0-flash-001", # OpenRouter model ID
      messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_input},
      ]
    )
    
    # Strip any markdown the AI might add
    clean_text = response.choices[0].message.content.strip().replace("```json", "").replace("```", "")
    return json.loads(clean_text)

# --- THE HANDS ---
def run_robot(instructions):
    action = instructions.get("action")
    ext = instructions.get("file_type") or "*"
    root = instructions.get("search_path")
    dest = instructions.get("dest")

    if action == "collect_files":
        if not dest:
            dest = os.path.join(r"C:\Users", os.getlogin(), "Desktop", "Collected_Files")
            print(f"⚠️ No destination specified. Defaulting to: {dest}")

        print(f"🔍 Searching for .{ext} files in {root}...")
        if not os.path.exists(dest):
            os.makedirs(dest)

        count = 0
        for base, _, files in os.walk(root):
            for f in files:
                if f.lower().endswith(f".{ext}"):
                    try:
                        shutil.copy2(os.path.join(base, f), dest)
                        count += 1
                    except:
                        continue # Skip locked system files
        
        print(f"✅ Mission Accomplished! Found {count} files and put them in {dest}")
    
    elif action == "list_files":
        print(f"[SEARCH] Listing .{ext} files in {root}...")
        count = 0
        for base, _, files in os.walk(root):
            for f in files:
                if ext == "*" or f.lower().endswith(f".{ext}"):
                    print(f"- {f}  (in {base})")
                    count += 1
        print(f"[DONE] Found {count} files.")

# --- CLI LOOP ---
if __name__ == "__main__":
    print("🤖 Gemini Robot is Online.")
    while True:
        cmd = input("\nCommand the Robot (or 'exit'): ")
        if cmd.lower() == 'exit': break
        try:
            plan = ask_gemini(cmd)
            run_robot(plan)
        except Exception as e:
            print(f"⚠️ Robot Error: {e}")
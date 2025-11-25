import os
import time
import pyperclip
import logging
from openai import OpenAI

# Path to the logical data model file
MODEL_FILE = "./database_model.txt"

def load_logical_model() -> str:
    """Read the database logical model description from file."""
    try:
        with open(MODEL_FILE, "r", encoding="utf-8") as f:
            return f.read().strip()
    except Exception as e:
        logging.error(f"❌ Could not read model file: {e}")
        return "Database model not found."

def build_prompt_prefix() -> str:
    """Build the full prompt prefix with logical model text."""
    logical_model = load_logical_model()
    return (
        "Write an SQL code based on the user's prompt below using the following Logical Data Model. "
        "Write all SQL clauses, keywords, and operators in small caps. "
        "Respond only with SQL code — no explanations, comments, or markdown.\n\n"
        f"Logical Data Model:\n{logical_model}\n\nUser prompt:\n"
    )

# later in your code, before API call:
PROMPT_PREFIX = build_prompt_prefix()
print(PROMPT_PREFIX)

CHECK_INTERVAL = 1.0  # seconds between clipboard checks
LOG_FILE = os.path.expanduser("./chatgpt_clipboard_sql_log.log")

# ========== LOGGING SETUP ==========

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
)

# ========== CHATGPT CLIENT ==========
api_key = "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";

if not api_key:
    raise ValueError("❌ OPENAI_API_KEY not set")

client = OpenAI(api_key=api_key)

# ========== MAIN LOOP ==========
def main():
    logging.info("🚀 Clipboard watcher started.")
    previous_text = ""

    while True:
        try:
            current_text = pyperclip.paste().strip()
            # Ignore empty or repeated clipboard content
            if not current_text or current_text == previous_text:
                time.sleep(CHECK_INTERVAL)
                continue
            
            # Prevent recursion — skip if it's likely already SQL
            if current_text.lower().startswith(("select", "insert", "update", "delete", "drop")):
                previous_text = current_text
                continue

            print(previous_text);
            logging.info(f"📋 New clipboard text detected ({len(current_text)} chars).")

            messages = [
                {"role": "system", "content": "You are a SQL expert. Respond only with SQL code — no text or commentary."},
                {"role": "user", "content": PROMPT_PREFIX + current_text},
            ]

            # Send to ChatGPT API
            response = client.chat.completions.create(
                model="gpt-5", #model="gpt-4o-mini"
                messages=messages,
            )
            print(response);
            sql_result = response.choices[0].message.content.strip()

            #print(sql_result);

            # Copy SQL result back to clipboard
            pyperclip.copy(sql_result)
            logging.info("✅ SQL copied to clipboard successfully.")

            previous_text = sql_result  # prevent re-triggering

        except Exception as e:
            print(e);
            logging.error(f"❌ Error: {e}")
            time.sleep(3)


if __name__ == "__main__":
    main()

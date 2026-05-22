import ast
import os
import shutil
import subprocess
import time
from pathlib import Path

from google import genai

TARGET_FILE = Path("app/target_code.py")
BACKUP_FILE = Path("app/target_code.py.bak")

PROMPT = """
You are a senior Python engineer.

Improve this code carefully.

STRICT RULES:
- NEVER rename function calculate
- NEVER change calculate arguments
- NEVER change functionality
- Improve readability
- Add type hints
- Add validation if safe
- Add comments/docstrings if useful
- Return ONLY valid Python code
- NO markdown
"""


def get_client():
    api_key = os.environ.get("GEMINI_API_KEY")

    if not api_key:
        raise RuntimeError("GEMINI_API_KEY missing")

    return genai.Client(api_key=api_key)


def backup():
    shutil.copy(TARGET_FILE, BACKUP_FILE)


def restore():
    if BACKUP_FILE.exists():
        shutil.copy(BACKUP_FILE, TARGET_FILE)


def validate_python(code):
    ast.parse(code)


def run(cmd):
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
    )

    print(result.stdout)
    print(result.stderr)

    return result.returncode == 0


def validate_pipeline():
    checks = [
        ["ruff", "check", "."],
        ["black", "."],
        ["pytest"],
    ]

    for cmd in checks:
        if not run(cmd):
            return False

    return True


def improve(code):
    client = get_client()

    prompt = f"{PROMPT}\n\nCODE:\n{code}"

    retries = 3

    for attempt in range(retries):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
            )

            if not response.text:
                raise RuntimeError("Empty Gemini response")

            return response.text.strip()

        except Exception as exc:
            print(exc)

            if attempt == retries - 1:
                raise

            time.sleep(5)


def main():
    original = TARGET_FILE.read_text()

    backup()

    try:
        improved = improve(original)

        if improved == original:
            print("No changes generated")
            return

        validate_python(improved)

        TARGET_FILE.write_text(improved)

        if validate_pipeline():
            print("Validation successful")
        else:
            print("Validation failed")
            restore()

    except Exception as exc:
        print(exc)
        restore()
        raise


if __name__ == "__main__":
    main()

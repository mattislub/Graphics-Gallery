import os
import shutil
import time
import openai
from dotenv import load_dotenv
from tqdm import tqdm

# טען משתני סביבה
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

NEXT_PROJECT_PATH = "./graphics-next/src/app"  # יעד ברירת מחדל

def backup_project(project_path):
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    backup_path = f"{project_path}-backup-{timestamp}"
    shutil.copytree(project_path, backup_path)
    print(f"[✔] גיבוי נוצר: {backup_path}")

def analyze_project_structure(project_path):
    summary = []
    skip_dirs = ['venv', '__pycache__', 'node_modules', '.next', 'migrations', 'build', 'staticfiles']
    for root, dirs, files in os.walk(project_path):
        dirs[:] = [d for d in dirs if d not in skip_dirs]  # סינון תיקיות
        for file in files:
            if file.endswith(('.py', '.html', '.css', '.js', '.json')):
                full_path = os.path.join(root, file)
                summary.append(full_path)
            if len(summary) >= 200:
                return summary
    return summary

def ask_gpt_for_conversion_plan(file_list):
    joined = "\n".join(file_list)
    prompt = f"""
אני עובד על המרת פרויקט מפייתון ל־Next.js.
הנה רשימת קבצים בפרויקט:

{joined}

על סמך הסיומות והמבנה, הצע לי מה נכון להמיר ל־JSX, ל־API, או ל־public/styles, כדי להשתמש בזה ב־Next.js מודרני עם App Router ו־Tailwind.
"""
    res = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    return res.choices[0].message.content

def convert_file_to_nextjs(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    prompt = f"""המר את הקובץ הבא כך שיתאים ל־Next.js:
{filepath}

התוכן:
-----
{content}
-----"""

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )
    return response.choices[0].message.content

def run_conversion(file_list, project_path, nextjs_path):
    total = len(file_list)
    for idx, path in enumerate(file_list, start=1):
        filename = os.path.basename(path)
        filename = filename.replace(".html", ".tsx").replace(".py", ".ts")
        save_path = os.path.join(nextjs_path, filename)

        if os.path.exists(save_path):
            print(f"[⏭] {idx}/{total} דילוג — כבר קיים: {save_path}")
            continue

        print(f"\n📄 [{idx}/{total}] ממיר: {path}")
        try:
            converted = convert_file_to_nextjs(path)
            with open(save_path, 'w', encoding='utf-8') as f:
                f.write(converted)
            print(f"[✔] {idx}/{total} נשמר אל: {save_path}")
        except Exception as e:
            print(f"[✖] {idx}/{total} שגיאה בקובץ {path}: {e}")

if __name__ == "__main__":
    print("📁 נתיב לפרויקט פייתון (ברירת מחדל: ./): ")
    path = input().strip() or "."
    if not os.path.exists(path):
        print("⚠ הנתיב לא קיים.")
        exit(1)

    backup_project(path)
    files = analyze_project_structure(path)
    print(f"\n🔍 נמצאו {len(files)} קבצים רלוונטיים לסריקה.")
    suggestion = ask_gpt_for_conversion_plan(files)
    print("\n🧠 GPT מציע את התוכנית הבאה:\n")
    print(suggestion)
    
    print("\n❓ האם להמיר את כל הקבצים כעת? [y/n]: ")
    confirm = input().strip().lower()
    if confirm == "y":
        run_conversion(files, path, NEXT_PROJECT_PATH)
    else:
        print("🚫 ההמרה בוטלה.")

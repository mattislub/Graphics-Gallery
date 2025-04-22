import os
import shutil
import time
import openai
from dotenv import load_dotenv
from tqdm import tqdm

# טוען את מפתח ה-API מתוך קובץ .env
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# יצירת גיבוי לפרויקט הקיים
def backup_project(project_path):
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    backup_path = f"{project_path}-backup-{timestamp}"
    shutil.copytree(project_path, backup_path)
    print(f"[✔] גיבוי נוצר: {backup_path}")

# שליחת קובץ ל-OpenAI להמרה
def convert_file_to_nextjs(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    prompt = f"""המר את הקובץ הבא מ־Python או HTML לקבצים עבור פרויקט Next.js (כולל JSX או API או static במידת הצורך). 
שמור על שמות משתנים הגיוניים ואל תשתמש בקוד מיותר.
-----
{content}
-----"""

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )
    return response.choices[0].message.content

# מעבר על הקבצים בפרויקט
def run_conversion(project_path):
    for root, _, files in os.walk(project_path):
        for file in tqdm(files, desc="🔍 סריקת קבצים"):
            if file.endswith((".py", ".html")):
                full_path = os.path.join(root, file)
                print(f"\n📄 קובץ: {full_path}")
                choice = input("1=לקובץ חדש, 2=לדרוס, 3=דלג >> ")
                if choice == "3":
                    continue
                try:
                    new_code = convert_file_to_nextjs(full_path)
                    if choice == "1":
                        new_path = full_path + ".converted"
                    else:
                        new_path = full_path
                    with open(new_path, 'w', encoding='utf-8') as f:
                        f.write(new_code)
                    print(f"[✔] המרה נשמרה ב־: {new_path}")
                except Exception as e:
                    print(f"[✖] שגיאה בהמרה: {e}")

# התחלה
if __name__ == "__main__":
    path = input("📁 נתיב לתיקיית הפרויקט להמרה: ").strip()
    if not os.path.exists(path):
        print("⚠ הנתיב לא קיים.")
        exit(1)
    backup_project(path)
    run_conversion(path)

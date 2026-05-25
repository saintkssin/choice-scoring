import os
import json
import time
from google import genai
from config import GEMINI_API_KEY

client = genai.Client(api_key=GEMINI_API_KEY)

os.makedirs("output/scores", exist_ok=True)

with open("script.json") as f:
    script = json.load(f)

def score_call(call_id, transcript):
    print(f"Скорингую: {call_id}")

    prompt = f"""
Ти — експерт з оцінки якості продажів.

Ось еталонний скрипт по блоках:
{json.dumps(script, ensure_ascii=False, indent=2)}

Ось транскрипт дзвінка:
{transcript}

Завдання:
1. Для кожного блоку скрипту постав оцінку від 0 до 10
2. Вкажи конкретну цитату з розмови яка підтверджує оцінку
3. Якщо блок пропущений — оцінка 0, причина "не згадано"
4. Підсумковий скор = середнє по всіх блоках

Відповідай ТІЛЬКИ у форматі JSON без markdown та без зайвого тексту:
{{
  "call_id": "{call_id}",
  "total_score": 74,
  "blocks": [
    {{"id": 1, "name": "Аналіз клієнта та підготовка", "score": 8, "comment": "...", "quote": "..."}},
    {{"id": 2, "name": "Встановлення контакту", "score": 7, "comment": "...", "quote": "..."}},
    {{"id": 3, "name": "Виявлення потреби", "score": 6, "comment": "...", "quote": "..."}},
    {{"id": 4, "name": "Презентація та експертність", "score": 5, "comment": "...", "quote": "..."}},
    {{"id": 5, "name": "Робота із запереченнями", "score": 4, "comment": "...", "quote": "..."}},
    {{"id": 6, "name": "Закриття", "score": 3, "comment": "...", "quote": "..."}}
  ]
}}
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        text = response.text.strip()
        text = text.replace("```json", "").replace("```", "").strip()
        result = json.loads(text)

        with open(f"output/scores/{call_id}.json", "w") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        print(f"Збережено: output/scores/{call_id}.json")
        return result

    except Exception as e:
        print(f"Помилка для {call_id}: {e}")
        time.sleep(10)
        return None

if __name__ == "__main__":
    transcript_dir = "data/transcripts"

    for filename in sorted(os.listdir(transcript_dir)):
        if filename.endswith(".txt"):
            call_id = filename.replace(".txt", "")

            if os.path.exists(f"output/scores/{call_id}.json"):
                print(f"Вже є: {call_id}, пропускаю")
                continue

            with open(f"{transcript_dir}/{filename}") as f:
                transcript = f.read()

            score_call(call_id, transcript)
            time.sleep(3)

    print("Скоринг завершено!")
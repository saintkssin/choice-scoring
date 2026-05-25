import os
import time
from google import genai
from google.genai import types
from config import GEMINI_API_KEY

client = genai.Client(api_key=GEMINI_API_KEY)

os.makedirs("data/transcripts", exist_ok=True)

def transcribe_audio(audio_path, call_id):
    print(f"Транскрибую: {call_id}")
    
    with open(audio_path, "rb") as f:
        audio_data = f.read()
    
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[
                types.Part.from_bytes(data=audio_data, mime_type="audio/wav"),
                "Транскрибуй цей аудіо дзвінок. Розділи репліки на [МЕНЕДЖЕР] та [КЛІЄНТ]. Мова українська або російська."
            ]
        )
        
        transcript = response.text
        
        if not transcript:
            print(f"Порожня відповідь для {call_id}, пропускаю")
            return None
            
        with open(f"data/transcripts/{call_id}.txt", "w") as f:
            f.write(transcript)
        
        print(f"Збережено: data/transcripts/{call_id}.txt")
        return transcript
        
    except Exception as e:
        print(f"Помилка для {call_id}: {e}")
        time.sleep(10)
        return None

if __name__ == "__main__":
    audio_dir = "data/audio"
    files = sorted(os.listdir(audio_dir))[:15]
    
    for filename in files:
        if filename.endswith(".mp3") or filename.endswith(".wav"):
            call_id = filename.replace(".mp3", "").replace(".wav", "")
            
            # Пропускаємо вже готові
            if os.path.exists(f"data/transcripts/{call_id}.txt"):
                print(f"Вже є: {call_id}, пропускаю")
                continue
            
            audio_path = f"{audio_dir}/{filename}"
            transcribe_audio(audio_path, call_id)
            time.sleep(3)
    
    print("Всі транскрипти готові!")
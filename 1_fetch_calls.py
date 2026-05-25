import requests
import csv
import os
from config import RINGOSTAT_API_KEY, DATE_FROM, DATE_TO, MIN_DURATION, MANAGERS

os.makedirs("data/audio", exist_ok=True)

def fetch_calls():
    print("Завантажую список дзвінків...")

    response = requests.get(
        "https://api.ringostat.net/calls/list",
        headers={
            "Content-Type": "application/json",
            "Auth-key": RINGOSTAT_API_KEY
        },
        params={
            "limit": 15,
            "export_type": "json",
            "from": DATE_FROM,
            "to": DATE_TO,
            "fields": "calldate,caller,dst,disposition,billsec,recording",
            "filters": f"billsec>{MIN_DURATION},disposition=ANSWERED"
        }
    )

    print("Відповідь:", response.status_code, response.text[:200])

    calls = response.json()
    print(f"Знайдено дзвінків: {len(calls)}")

    if MANAGERS:
        calls = [c for c in calls if any(m in c.get("caller", "") for m in MANAGERS)]
        print(f"Після фільтру по менеджерах: {len(calls)}")

    if not calls:
        print("Немає дзвінків після фільтрації!")
        return []

    with open("data/calls.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=calls[0].keys())
        writer.writeheader()
        writer.writerows(calls)

    for call in calls:
        if call.get("recording"):
            print(f"Скачую аудіо: {call['recording']}")
            audio = requests.get(call["recording"], headers={"Auth-key": RINGOSTAT_API_KEY})
            call_id = call.get("calldate", "unknown").replace(" ", "_").replace(":", "-")
            with open(f"data/audio/{call_id}.mp3", "wb") as f:
                f.write(audio.content)

    print("Готово! Файли збережені в data/")
    return calls

if __name__ == "__main__":
    fetch_calls()
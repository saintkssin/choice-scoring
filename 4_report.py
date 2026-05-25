import os
import json
import csv

os.makedirs("output", exist_ok=True)

def get_manager_name(call_id):
    try:
        with open("data/calls.csv") as f:
            for row in csv.DictReader(f):
                date = row.get("calldate", "").replace(" ", "_").replace(":", "-")
                if date == call_id:
                    caller = row.get("caller", "")
                    # Витягуємо ім'я з "choiceqrcom_Sporysh"
                    if "_" in caller:
                        return caller.split("_")[-1].strip().strip('"').strip(">")
    except:
        pass
    return "Невідомо"

def build_report():
    scores_dir = "output/scores"
    rows = []

    for filename in sorted(os.listdir(scores_dir)):
        if filename.endswith(".json"):
            with open(f"{scores_dir}/{filename}") as f:
                score = json.load(f)

            call_id = filename.replace(".json", "")
            manager = get_manager_name(call_id)

            row = {
                "Дзвінок": call_id,
                "Менеджер": manager,
                "Загальний скор": score["total_score"],
            }

            for block in score["blocks"]:
                row[block["name"]] = block["score"]

            rows.append(row)

    with open("output/report.csv", "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    print("Звіт збережено: output/report.csv")

    with open("output/report_detailed.txt", "w", encoding="utf-8") as f:
        for filename in sorted(os.listdir(scores_dir)):
            if filename.endswith(".json"):
                with open(f"{scores_dir}/{filename}") as sf:
                    score = json.load(sf)

                call_id = filename.replace(".json", "")
                manager = get_manager_name(call_id)

                f.write(f"\n{'='*60}\n")
                f.write(f"Дзвінок: {call_id}\n")
                f.write(f"Менеджер: {manager}\n")
                f.write(f"Загальний скор: {score['total_score']}/10\n")
                f.write(f"{'='*60}\n")

                for block in score["blocks"]:
                    f.write(f"\n[{block['name']}] — {block['score']}/10\n")
                    f.write(f"Коментар: {block['comment']}\n")
                    f.write(f"Цитата: {block['quote']}\n")

    print("Детальний звіт: output/report_detailed.txt")

if __name__ == "__main__":
    build_report()
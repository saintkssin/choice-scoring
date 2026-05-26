import subprocess
import sys

def run(script):
    print(f"\n{'='*40}")
    print(f"Запускаю: {script}")
    print(f"{'='*40}")
    result = subprocess.run([sys.executable, script])
    if result.returncode != 0:
        print(f"Помилка в {script}!")
        sys.exit(1)

if __name__ == "__main__":
    run("1_fetch_calls.py")
    run("2_transcribe.py")
    run("3_score.py")
    run("4_report.py")
    print("\n✅ Pipeline завершено! Дивись output/report.csv")
from datetime import datetime, timedelta

# Автоматично останні 14 днів
DATE_TO = datetime.now().strftime("%Y-%m-%d 23:59:59")
DATE_FROM = (datetime.now() - timedelta(days=14)).strftime("%Y-%m-%d 00:00:00")

RINGOSTAT_API_KEY = "NjV7IhCV8MRQ2nuHrA0XXyDFC3e8vkQp"
GEMINI_API_KEY = "AIzaSyB03eJo0s2FF0piDHXAGva66mXEUQMAado"
MIN_DURATION = 60
MANAGERS = ["Sporysh", "bondarchuk", "Horobets", "karpiuk"]
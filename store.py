import json
from datetime import datetime

def save_data(name, user_id, url, result):
    current_time = datetime.now()
    timestamp = current_time.strftime("%d-%m-%Y | %I:%M:%S %p")
    new_data = {
        timestamp: {
            "name": name,
            "user_id": user_id,
            "url": url,
            "result": result
        }
    }

    try:
        with open('store.json', 'r') as file:
            existing_data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        existing_data = {}

    existing_data.update(new_data)
    with open('store.json', 'w') as file:
        json.dump(existing_data, file, indent=2)

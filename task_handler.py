import json
import os
from datetime import datetime


DATA_FILE = "task.json"
def load_tasks():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)
    
def save_tasks(tasks):
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(tasks, file, indent=4, ensure_ascii=False)

def add_task(title, content):
    now = datetime.now()
    tasks = load_tasks()
    index =1
    if len(tasks):
        index = tasks[len(tasks)-1]["id"]
        index = index+1
    tasks.append({ "id": index, "title": title, "content": content, "date": now.strftime("%d.%m.%Y %H:%M:%S")})
    save_tasks(tasks)
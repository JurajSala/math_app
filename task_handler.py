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
    tasks.append({ "id": index, "title": title, "content": content, "date": now.strftime("%d.%m.%Y %H:%M:%S"), "solutions_count": 0})
    save_tasks(tasks)

def get_task(task_id):
    tasks = load_tasks()
    for task in tasks:
        if( task["id"] == int(task_id) ):
          return task
    return None

def get_tasks_exclude_task(task_id):
    tasks = load_tasks()
    result_tasks = [item for item in tasks if item["id"] != int(task_id)]
    return result_tasks

def update_task(task_id, title, content, date, solutions_count):
    tasks = load_tasks()
    for task in tasks:
        if( task["id"] == int(task_id) ):
            print("Podminka splnena")
            task["title"] = title
            task["content"] = content
            task["date"] = date
            task["solutions_count"] = solutions_count
            save_tasks(tasks)
            print("Úloha id:{} s titulem: {} upravena".format(task_id, title))
            return True
    return False
           
def delete_task(task_id):
    tasks = load_tasks()
    for task in tasks:
        if( task["id"] == int(task_id) ):
            tasks.remove(task)
            save_tasks(tasks)
            return True
    return False
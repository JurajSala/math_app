import json
import os
from datetime import datetime


DATA_FILE = "data.json"
def load_posts():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)
    
def get_posts_for(task_id):
    allPosts = load_posts()
    result =[]
    for post in allPosts:
        value =str(post["task_id"])
        
        if task_id == value:
            result.append(post)
    return result

def save_posts(posts):
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(posts, file, indent=4, ensure_ascii=False)

def add_post(title, content, task_id):
    now = datetime.now()
    posts = load_posts()
    index =1
    if len(posts):
        index = posts[len(posts)-1]["id"]
        index = index+1
    posts.append({ "id": index, "task_id": task_id, "title": title, "content": content, "date": now.strftime("%d.%m.%Y %H:%M:%S")})
    save_posts(posts)
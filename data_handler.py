import json
import os
from datetime import datetime


DATA_FILE = "data.json"
def load_posts():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)

def save_posts(posts):
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(posts, file, indent=4, ensure_ascii=False)

def add_post(title, content):
    now = datetime.now()
    posts = load_posts()
    index =1
    if len(posts):
        index = posts[len(posts)-1]["id"]
        index = index+1
    posts.append({ "id": index, "title": title, "content": content, "date": now.strftime("%d.%m.%Y %H:%M:%S")})
    save_posts(posts)
import json
import os
from datetime import datetime
from flask import jsonify
from task_handler import get_task, update_task


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

def get_post(post_id):
    allPosts = load_posts()
    for post in allPosts:
        if( post["id"] == post_id ):
          return post
    
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
    task = get_task(task_id)
    newCount = task["solutions_count"] + 1
    update_task(task["id"], task["title"], task["content"], task["date"], newCount)
    return get_posts_for(task_id)

def delete_post(post_id):
    item = get_post(int(post_id))
    posts= load_posts()
    new_posts = [item for item in posts if item["id"] != int(post_id)]
    if len(new_posts) == len(posts):
        return jsonify({"message": "ID nenalezeno", "success": False}), 404
    save_posts(new_posts)
    task = get_task(item["task_id"])
    if task:
      newCount = task["solutions_count"] - 1
      update_task(task["id"], task["title"], task["content"], task["date"], newCount)
      print("Mazání řešení: " +item["title"] +" --> proběhlo úspěšně!!")
    else:
        print("Odstranění se nezdařilo nebo došlo k nějaké chybě!!")
    return new_posts

def delete_all_posts_with(task_id):
    posts = get_posts_for(task_id)
    for post in posts:
      delete_post(post["id"])
      print("Deleting all solutions for the task with id = {} was successful".format(task_id))
      return True
    return False

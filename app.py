from flask import Flask, render_template, request, redirect, url_for
import requests

from data_handler import get_posts_for, add_post
from task_handler import load_tasks,add_task

app = Flask(__name__)


@app.route('/')
def index():
    tasks = load_tasks()
    tasks.reverse()
    return render_template('tasks.html', tasks=tasks)

@app.route('/process_add_ask', methods=['POST'])
def process_add_ask():
    task_id = request.form.get('task_id')
    task_title = request.form.get('task_title')
    task_content = request.form.get('task_content')
    solutions = get_posts_for(task_id)
    print(solutions)
    return render_template('index.html', data=
                           {
                               "task":{
                                   "title":task_title,
                                   "content":task_content
                               },
                               "data": solutions,
                               "id": task_id
                           })

@app.route('/addSolution', methods=['POST'])
def addPost():
    task_id = request.form.get('task_id')
    title = request.form.get('title')
    content = request.form.get('content')
    if title and content:
        add_post(title, content, task_id)
    return redirect(url_for('index'))

@app.route('/addTask', methods=['POST'])
def addTask():
    title = request.form.get('title')
    content = request.form.get('content')
    if title and content:
        add_task(title, content)
    return redirect(url_for('index'))

@app.route('/external')
def external_data():
    response = requests.get("https://jsonplaceholder.typicode.com/posts/1")
    data = response.json()
    return render_template('external.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)
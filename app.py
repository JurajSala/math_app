from flask import Flask, render_template, request, redirect, url_for
import requests

from data_handler import get_posts_for, add_post, delete_post, delete_all_posts_with
from task_handler import load_tasks, add_task, get_task, delete_task , update_task, get_tasks_exclude_task

from datetime import datetime


app = Flask(__name__)


@app.route('/')
def tasks():
    tasks = load_tasks()
    tasks.reverse()
    return render_template('tasks.html', data= {
                                                  "tasks": tasks 
                                                }
        )

@app.route('/process_add_solution_for_ask', methods=['POST'])
def process_add_solution_for_ask():
    task_id = request.form.get('task_id')
    task_title = request.form.get('task_title')
    task_content = request.form.get('task_content')
    task = { "title": task_title, "content": task_content }
    solutions = get_posts_for(task_id)
    print(solutions)
    return render_template('index.html', solutions=
                           {
                               "task":task,
                               "data": solutions,
                               "id": task_id
                           })

@app.route('/addSolution', methods=['POST'])
def addSolution():
    task_id = request.form.get('task_id')
    title = request.form.get('title')
    content = request.form.get('content')
    if title and content:
        solutions = add_post(title, content, task_id)
        task = get_task(task_id)
        return render_template('index.html', solutions=
                           {
                               "task": task,
                               "data": solutions,
                               "id": task_id
                           })
    
@app.route('/deleteSolution', methods=['POST'])
def deleteSolution():
    solution = request.form.get('solution_id')
    task_id = request.form.get('task_id')
    task = get_task(task_id)
    delete_post(solution)
    solutions = get_posts_for(task_id)
    return render_template('index.html', solutions=
                           {
                               "task": task,
                               "data": solutions,
                               "id": task_id
                           })

@app.route('/deleteTask', methods=['POST'])
def deleteTask():
    task_id= request.form.get('task_id')
    delete_task(task_id)
    tasks = load_tasks()
    delete_all_posts_with(task_id)
    return render_template('tasks.html', data= {
                                                  "tasks": tasks 
                                                })
    

@app.route('/addTask', methods=['POST'])
def addTask():
    title = request.form.get('title')
    content = request.form.get('content')
    if title and content:
        add_task(title, content)
    return redirect(url_for('tasks'))

@app.route('/startEditTask', methods=['POST'])
def startEditTask():
    task_id = request.form.get('task_id')
    task = get_task(task_id)
    tasks = get_tasks_exclude_task(task_id)
 
    return render_template('tasks.html', data=
                           {
                               "task":task,
                               "tasks":tasks
                           })

@app.route('/editTask/<int:task_id>', methods=['GET','POST'])
def editTask(task_id):
    task = get_task(task_id)
    title = request.form.get('title')
    content = request.form.get('content')
    now = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    count = task["solutions_count"]
    print("Před update_task")
    update_task(task_id,title,content,now,count)
    return redirect(url_for('tasks'))

@app.route('/external')
def external_data():
    response = requests.get("https://jsonplaceholder.typicode.com/posts/1")
    data = response.json()
    return render_template('external.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, render_template, request, redirect, url_for, send_file
import requests
import base64

from data_handler import get_posts_for, add_post, delete_post, delete_all_posts_with
from task_handler import load_tasks, add_task, get_task, delete_task , update_task, get_tasks_exclude_task

from datetime import datetime
import io
from classes.fractal import Fractal_Mandelbrot, KochSnowflake,SquareSnowflake,FractalJulia,LyapunovFractal,BarnsleyFern
from classes.group_generator import enumerate_finite_group

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


@app.route('/fractal')
def fractal_generator():
    fractal_type = request.args.get('type', 'koch')
    depth = int(request.args.get('depth', 4))
    size = int(request.args.get('size', 800))
    img = None

    if fractal_type == 'square':
        F = SquareSnowflake(size=size, depth=depth, line_width=2)
        img = F.to_image()
    elif fractal_type == 'mandelbrot':
        # Mandelbrot: můžeme povolit vlastní c nebo použít default
        max_iter = int(request.args.get('iter', 100))
        power = int(request.args.get('p', 2))
        mandel = Fractal_Mandelbrot(width=size, height=int(size*0.75), \
            max_iter=max_iter, power=power)
        img = mandel.to_image()
    elif fractal_type == 'julia':
        max_iter = int(request.args.get('iter', 100))
        power = float(request.args.get('p', 2))
        cre = float(request.args.get('cre', -0.7))
        cim = float(request.args.get('cim', 0.27015))
        julia = FractalJulia(width=size, height=int(size*0.75), max_iter=max_iter, power=power, c=complex(cre, cim))
        img = julia.to_image()
    elif fractal_type == 'lyapunov':
        iterations = int(request.args.get('iter', 100))
        pattern = request.args.get('pattern', 'AB')
        a_min = float(request.args.get('a_min', 2.5))
        a_max = float(request.args.get('a_max', 4.0))
        b_min = float(request.args.get('b_min', 2.5))
        b_max = float(request.args.get('b_max', 4.0))
        L = LyapunovFractal(width=size, height=int(size*0.75),
                            iterations=iterations,
                            pattern=pattern,
                            a_range=(a_min, a_max),
                            b_range=(b_min, b_max))
        img = L.to_image()
    elif fractal_type == 'barnsley':
        img = BarnsleyFern(width=size, height=int(size*0.75), iterations=int(request.args.get('iter',100000))).to_image()
    else:
        F = KochSnowflake(size=size, depth=depth, line_width=2)
        img = F.to_image()

    buf = io.BytesIO()
    img.save(buf, 'PNG')
    buf.seek(0)
    img_b64 = base64.b64encode(buf.read()).decode('ascii')
    return render_template('fractal.html', depth=depth, size=size,
                           fractal=fractal_type, img_data=img_b64)

@app.route('/group', methods=['GET'])
def group_view():
    print(">>> group_view called with", request.args)
    # Parametry z formuláře: generators oddělené čárkou, relace oddělené středníkem
    gens = [g.strip() for g in request.args.get('generators','').split(',') if g.strip()]
    rels = [r.strip() for r in request.args.get('relations','').split(';')   if r.strip()]

    # Vytvoříme prezentaci grupy a vygenerujeme prvky a tabulku násobení
    try:
        elements, table = enumerate_finite_group(
            generators=gens,
            relators=rels,
            max_cosets=5000
        )
        print(">>> enumerate_finite_group returned", elements)
    except Exception as e:
        import traceback; traceback.print_exc()
        error = str(e)
        elements, table = [], {}
        # tady můžeš předat chybu do šablony
        return render_template('group.html',
                               error=str(error),
                               generators=gens,
                               relations=rels,
                               elements=None,
                               table=None)

    # 3) Předáš výsledky do Jinja šablony
    return render_template('group.html',
                           generators=gens,
                           relations=rels,
                           elements=elements,
                           table=table)

if __name__ == '__main__':
    app.run(debug=True)
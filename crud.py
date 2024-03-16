from datetime import datetime
from flask import Flask, json, render_template, request
import requests

# Create a Flask application instance
app = Flask(__name__)

@app.route('/', methods=['GET'])
def show_index():
    # return render_template('index.html')
   response = requests.get('http://host.docker.internal:8080/tasks')
   return response.json()

# Deleting tasks
@app.route('/delete')
def render_delete():
 return render_template('delete.html')

# Deleting tasks
@app.route('/deletetask', methods=['POST'])
@app.route('/deletetask/<id_del>')
def delete_tasks():
    id_del = request.form["id_del"]
    response = requests.delete(f'http://host.docker.internal:8080/tasks/{id_del}')
    if response.status_code == 200:
        return 'Task Deleted Successfully'
    else:
        return 'Error: Failed to delete  data from the API'

# searching tasks
@app.route('/tasks', methods=['GET'])
@app.route('/tasks/<task_id>')
def search_tasks():
    task_id = request.args.get('task_id')   
    if not task_id:
        # response = requests.get('http://localhost:8080/tasks')
       response = requests.get('http://host.docker.internal:8080/tasks')
    else:
        response = requests.get(f'http://host.docker.internal:8080/tasks/{task_id}')
    if response.status_code == 200:
        search_tasks= response.json()
        if task_id:
           search_tasks = [search_tasks]
        return render_template('findall.html', search_tasks=search_tasks)
    else:
        return 'Error: Failed to fetch data from the API'

#creating tasks
@app.route('/create')
def render_create():
 return render_template('create.html', search_tasks=[search_tasks])

@app.route('/createtask', methods=['POST'])
def create_task():
    dt = datetime.strptime(request.form["startTime"], "%Y-%m-%dT%H:%M")
    microseconds = "{:03d}".format(dt.microsecond // 1000)

    # Format the datetime object 
    formatted_str = dt.strftime("%Y-%m-%d %H:%M:%S") + f".{microseconds}Z"
    task_data = {
        "name": request.form["name"],
        "id": request.form["id"],
        "assignee": request.form["assignee"],
        "project": request.form["project"],
        "startTime": formatted_str
    }

    headers = {"Content-Type": "application/json; charset=utf-8"}

    response = requests.post('http://host.docker.internal:8080/tasks', json=json.loads(json.dumps(task_data)),headers=headers)

    if response.status_code == 201:
        return '<h1>Task created successfully</h1> <a href="/">Go to Home</a></div>'
    else:
        return '<h1>Error: Failed to create task</h1> <div class="footer"><a href="/">Go to Home</a></div>'
    
#Assignee tasks
@app.route('/assignee')
def render_assignee():
 return render_template('assignee.html', search_tasks=[search_tasks])

#searching top 10 assignee
@app.route('/assigneetask', methods=['GET'])
@app.route('/assigneetask/<assignee_id>')
def search_assignee():
    assignee_id = request.args.get('assignee_id')
    response = requests.get(f'http://host.docker.internal:8080/tasks/assignee/{assignee_id}')
    print(response)
    if response.status_code == 200:
        search_tasks= response.json()
        return render_template('assignee.html', search_tasks=search_tasks)
    else:
        return 'Error: Failed to fetch data from the API'


# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)

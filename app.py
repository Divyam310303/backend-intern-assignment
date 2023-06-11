from flask import Flask, render_template, request, jsonify,url_for
import os, re, datetime
from models import Task
import database as db


app = Flask(__name__)

# create the database and table. Insert 10 test tasks into db
# Do this only once to avoid inserting the test task into 
# the db multiple times
if not os.path.isfile('tasks.db'):
    db.connect()

# route for landing page
# check out the template folder for the index.html file
# check out the static folder for css and js files
@app.route("/")
def index():
    return render_template("index.html")

def isValid(email):
    regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
    if re.fullmatch(regex, email):
      return True
    else:
      return False


@app.route("/request", methods=['POST'])
def postRequest():
    req_data = request.get_json()
    email = req_data['email']
    if not isValid(email):
        return jsonify({
            'status': '422',
            'res': 'failure',
            'error': 'Invalid email format. Please enter a valid email address'
        })
    title = req_data['title']
    bks = [b.serialize() for b in db.view()]
    for b in bks:
        if b['title'] == title:
            return jsonify({
                # 'error': '',
                'res': f'Error ⛔❌! Task with title {title} is already in library!',
                'status': '404'
            })

    bk = Task(db.getNewId(), True, title, datetime.datetime.now())
    print('new task: ', bk.serialize())
    db.insert(bk)
    new_bks = [b.serialize() for b in db.view()]
    print('Tasks in lib: ', new_bks)
    
    return jsonify({
                # 'error': '',
                'res': bk.serialize(),
                'status': '200',
                'msg': 'Success creating a new task|👍😀'
            })


@app.route('/request', methods=['GET'])
def getRequest():
    content_type = request.headers.get('Content-Type')
    bks = [b.serialize() for b in db.view()]
    if (content_type == 'application/json'):
        json = request.json
        for b in bks:
            if b['id'] == int(json['id']):
                return jsonify({
                    # 'error': '',
                    'res': b,
                    'status': '200',
                    'msg': 'Success getting all tasks in library!👍😀'
                })
        return jsonify({
            'error': f"Error ⛔❌! Task with id '{json['id']}' not found!",
            'res': '',
            'status': '404'
        })
    else:
        return jsonify({
                    # 'error': '',
                    'res': bks,
                    'status': '200',
                    'msg': 'Success getting all tasks in library!👍😀',
                    'no_of_tasks': len(bks)
                })


@app.route('/request/<id>', methods=['GET'])
def getRequestId(id):
    req_args = request.view_args
    # print('req_args: ', req_args)
    bks = [b.serialize() for b in db.view()]
    if req_args:
        for b in bks:
            if b['id'] == int(req_args['id']):
                return jsonify({
                    # 'error': '',
                    'res': b,
                    'status': '200',
                    'msg': 'Success getting task by ID!👍😀'
                })
        return jsonify({
            'error': f"Error ⛔❌! Task with id '{req_args['id']}' was not found!",
            'res': '',
            'status': '404'
        })
    else:
        return jsonify({
                    # 'error': '',
                    'res': bks,
                    'status': '200',
                    'msg': 'Success getting task by ID!👍😀',
                    'no_of_tasks': len(bks)
                })

@app.route("/request", methods=['PUT'])
def putRequest():
    req_data = request.get_json()
    status = req_data['status']
    title = req_data['title']
    description = req_data['description']
    the_id = req_data['id']
    bks = [b.serialize() for b in db.view()]
    for b in bks:
        if b['id'] == the_id:
            bk = Task(
                the_id, 
                status,
                description, 
                title, 
                datetime.datetime.now()
            )
            print('new task: ', bk.serialize())
            db.update(bk)
            new_bks = [b.serialize() for b in db.view()]
            print('tasks in lib: ', new_bks)
            return jsonify({
                # 'error': '',
                'res': bk.serialize(),
                'status': '200',
                'msg': f'Success updating the Task titled {title}!👍😀'
            })        
    return jsonify({
                # 'error': '',
                'res': f'Error ⛔❌! Failed to update Task with title: {title}!',
                'status': '404'
            })
    
    


@app.route('/request/<id>', methods=['DELETE'])
def deleteRequest(id):
    req_args = request.view_args
    print('req_args: ', req_args)
    bks = [b.serialize() for b in db.view()]
    if req_args:
        for b in bks:
            if b['id'] == int(req_args['id']):
                db.delete(b['id'])
                updated_bks = [b.serialize() for b in db.view()]
                print('updated_bks: ', updated_bks)
                return jsonify({
                    'res': updated_bks,
                    'status': '200',
                    'msg': 'Success deleting task by ID!👍😀',
                    'no_of_tasks': len(updated_bks)
                })
    else:
        return jsonify({
            'error': f"Error ⛔❌! No task ID sent!",
            'res': '',
            'status': '404'
        })

if __name__ == '__main__':
    app.run()
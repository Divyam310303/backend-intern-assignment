import sqlite3, random, datetime
from models import Task


def getNewId():
    return random.getrandbits(28)


tasks = [
    # {
    #     'status': True,
    #     'title': 'Don Quixote',
    #     'description': 'don'
    #     'timestamp': datetime.datetime.now()
    # },
    {
        'status': True,
        'title': 'A Tale of Two Cities',
        'description' : 'Tale',
        'duedate': datetime.datetime.now()
    },
]    

def connect():
    conn = sqlite3.connect('tasks.db')
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS books (id INTEGER PRIMARY KEY, status BOOLEAN, title TEXT, description TEXT, timestamp TEXT)")
    conn.commit()
    conn.close()
    for i in tasks:
        bk = Task(getNewId(), i['status'], i['title'], i['description'], i['duedate'])
        insert(bk)

def insert(task):
    conn = sqlite3.connect('tasks.db')
    cur = conn.cursor()
    cur.execute("INSERT INTO tasks VALUES (?,?,?,?,?)", (
        self.id,
        self.title,
        self.description,
        self.deudate,
        self.status
    ))
    conn.commit()
    conn.close()

def view():
    conn = sqlite3.connect('tasks.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM tasks")
    rows = cur.fetchall()
    books = []
    for i in rows:
        task = Task(i[0], True if i[1] == 1 else False, i[2], i[3], i[4])
        tasks.append(task)
    conn.close()
    return tasks

def update(task):
    conn = sqlite3.connect('tasks.db')
    cur = conn.cursor()
    cur.execute("UPDATE tasks SET status=?,duedate=?, title=?, description=? WHERE id=?", (self.id,
        self.title,
        self.description,
        self.deudate,
        self.status))
    conn.commit()
    conn.close()

def delete(theId):
    conn = sqlite3.connect('tasks.db')
    cur = conn.cursor()
    cur.execute("DELETE FROM tasks WHERE id=?", (theId,))
    conn.commit()
    conn.close()

def deleteAll():
    conn = sqlite3.connect('tasks.db')
    cur = conn.cursor()
    cur.execute("DELETE FROM tasks")
    conn.commit()
    conn.close()
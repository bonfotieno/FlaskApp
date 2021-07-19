# a simple flask app that lets you can input your daily tasks, save them to a database, update and also delete
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'  # forward slashes is for specifying a relative path
db = SQLAlchemy(app)


# to create the data base do:
#  from flasktutorials import db
#  db.create_all()
#  exit()


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):  # returns a string
        return '<Task %r>' % self.id


@app.route('/', methods=['POST', 'GET'])
def index():  # Define a function for that route
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)

        # pushing to the database
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'there was an issue adding your task'
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()  # query the database by date created, returns all the values
        return render_template(
            "index.html", tasks=tasks)


@app.route('/delete/<int:ID>')
def delete(ID):
    task_to_delete = Todo.query.get_or_404(ID)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return "There was an error deleting that task"


@app.route('/update/<int:id>', methods=['GET','POST'])
def update(id):
    task = Todo.query.get_or_404(id)
    if request.method == 'POST':
        task.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/')  # returns as to the home page
        except:
            return 'There was an issue updating your task'

    else:
        return render_template('update.html', task=task)


if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

#setting up config for db and using sqlite with test.db as db name
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db' 
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_create = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return "Task %r" % self.id


@app.route("/", methods=["POST", "GET"])
def home():
    """
    Displays the content and listen for adding 
    new list to db if user added anything
    """
    if request.method == "POST":
        task_content = request.form["content"]
        new_task = Todo(content=task_content)
        
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect("/")
        except:
            return "Failed"
            
    else:
        tasks = Todo.query.order_by(Todo.date_create).all()
        return render_template("index.html", tasks=tasks)


@app.route("/delete/<int:id>")
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    """
    Delete the list from db 
    """
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect("/")
    except:
        return "sorry no such id"


@app.route("/update/<int:id>", methods=["POST", "GET"])
def update(id):
    task = Todo.query.get_or_404(id)

    """
    Updates the list to database 
    """
    if request.method == "POST":
        task.content = request.form["content"]

        try:
            db.session.commit()
            return redirect("/")
        except:
            return "There was an issue updating your task"

    else:
        return render_template("update.html", task=task)


if __name__ == "__main__":
    app.run(debug=True)
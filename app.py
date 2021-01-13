from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    created = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return '<Task %r>' % self.id

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            content = request.form["content"]

            task = Todo(content=content)
            db.session.add(task)
            db.session.commit()

            return redirect("/")
        except:
            return "Something went wrong."
    else:
        tasks = Todo.query.order_by(Todo.created).all()
        return render_template("index.html", tasks=tasks)

@app.route("/delete/<int:id>")
def delete(id):
    try:
        task = Todo.query.get_or_404(id)
        db.session.delete(task)
        db.session.commit()

        return redirect("/")
    except:
        return "Something went wrong"

@app.route("/update/<int:id>", methods = ["GET", "POST"])
def update(id):
    task = Todo.query.get_or_404(id)
    if request.method == "POST":
        try:
            task.content = request.form["content"]
            db.session.commit()

            return redirect("/")
        except:
            return "Something went wrong"
    else:
        return render_template("update.html", task=task)

if __name__ == "__main__":
    app.run(debug=True)
#!/

from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///test.db"
db = SQLAlchemy(app)

class Todo(db.Model):
	# set up columns
	id = db.Column(db.Integer, primary_key=True)
	content = db.Column(db.String(200), nullable=False)
	date_created = db.Column(db.DateTime, default=datetime.utcnow())

	def __repr__(self):
		return "<Task %r>" % self.id

@app.route("/", methods=["POST", "GET"])
def index():
	if request.method == "POST":
		# Grab the task and put it in the DB
		task_content = request.form["content"]
		new_task = Todo(content=task_content)
		try:
			db.session.add(new_task)
			db.session.commit()
			return redirect("/")
		except:
			return "There was an issue adding your task!"
	else:
		# Show all the tasks
		tasks = Todo.query.order_by(Todo.date_created).all()
		return render_template("index.html", tasks=tasks)

@app.route("/delete/<int:id>")
def delete(id):
	task_to_delete = Todo.query.get_or_404(id)
	try:
		db.session.delete(task_to_delete)
		db.session.commit()
		return redirect("/")
	except:
		return "Couldn't delete this task from the DB!"

@app.route("/update/<int:id>", methods=["GET", "POST"])
def update(id):
	task = Todo.query.get_or_404(id)
	if request.method == "POST":
		task.content = request.form['content']
		try:
			db.session.commit()
			return redirect("/")
		except:
			return "Couldn't update this task in the DB!"
	else:
		return render_template("update.html", task=task)
	return "..."

if __name__ == "__main__":
	app.run(debug=True)
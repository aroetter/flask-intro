#!/

from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import routes

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

@app.route(routes.TODO_APP_BASEURL, methods=["POST", "GET"])
def index():
	if request.method == "POST":
		# Grab the task and put it in the DB
		task_content = request.form["content"]
		new_task = Todo(content=task_content)
		try:
			db.session.add(new_task)
			db.session.commit()
			return redirect(routes.TODO_APP_BASEURL)
		except Exception as ex:
			return "There was an issue adding your task!" + repr(ex)
	else:
		# Show all the tasks
		tasks = Todo.query.order_by(Todo.date_created).all()
		return render_template("index.html", tasks=tasks, base_url=routes.TODO_APP_BASEURL)

@app.route(routes.TODO_APP_BASEURL + "/delete/<int:id>")
def delete(id):
	task_to_delete = Todo.query.get_or_404(id)
	try:
		db.session.delete(task_to_delete)
		db.session.commit()
		return redirect(routes.TODO_APP_BASEURL)
	except Exception as ex:
		return "Couldn't delete this task from the DB!" + repr(ex)

@app.route(routes.TODO_APP_BASEURL + "/update/<int:id>", methods=["GET", "POST"])
def update(id):
	task = Todo.query.get_or_404(id)
	if request.method == "POST":
		task.content = request.form['content']
		try:
			db.session.commit()
			return redirect(routes.TODO_APP_BASEURL)
		except Exception as ex:
			return "Couldn't update this task in the DB!" + repr(ex)
	else:
		return render_template("update.html", task=task, base_url=routes.TODO_APP_BASEURL)
	return "..."

if __name__ == "__main__":
	app.run(debug=True)
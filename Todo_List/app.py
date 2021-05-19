
from re import template
from flask import Flask, url_for, redirect, render_template, request  # Import Flask class
from flask_sqlalchemy import SQLAlchemy  # Import SQLAlchemy class
from flask_wtf import FlaskForm  # to create a new form (class)
# we need these fields to create new form
from wtforms import StringField, SubmitField

# create Flask object. We make our 'app object' but it needs to know what model we are running
app = Flask(__name__)

# Set the connection string to connect to the database, name of DB in GCP
# app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:root@34.105.152.18:3306/myflaskdb"  # ==>>> this one is for stand alone DB

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///data.db"
app.config["SECRET_KEY"] = "jksdhk"

# this is our db object which is going to be an object of the SQLALchemy class and all we need to pass is the app variable
db = SQLAlchemy(app)

'''below we make our table
    1. we have a class called Todos, that is going to be the name of our table 
    2. it will inherit db.model
'''


class Todos(db.Model):  # this is our model that has our tasks and if they are complete
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(50), nullable=False)
    complete = db.Column(db.Boolean, default=False)


''' To create a new form to allow users to enter Todos:
    1. we need to import
            1. from flask_wtf import FlaskForm
            2. from wtforms import StringField, SubmitField
    2. This will be added to 'add.html' '''


class TodoForm(FlaskForm):  # inherits FlaskForm
    # in this form we will have a filed called "Task" stored in variable task
    task = StringField("Task")
    # we need another variable to store the value "Add Todo" which is a Submit Button
    submit = SubmitField("Add Todo")


# we need to create our routes


@app.route('/')  # we want the index
def index():  # this route is for the INDEX page so we call the function 'INDEX'. It will show a list of Todos and everything that has been completed
    all_todos = Todos.query.all()
    todos_string = ""
    '''once we have created the 'index.html' we do not need the for loop below. We need to import a 'RENDER TEMPLATE' to use it'''
    # for todo in all_todos:
    #     todos_string += "<br>" + "<br>" + str(todo.id) + \
    #         " " + todo.task + " " + str(todo.complete)
    # return "This is a TODO list " + todos_string
    '''we return a render template, we render 'index.html' and we pass 'all to_dos' '''
    return render_template('index.html', all_todos=all_todos)    # we are passing all the todos that come from query in line 52


''' 2.1 Create routes that ADDS a new Todo with the value 'New Todo' every time
@app.route("/add")
def add():  # adds a new entry in the database
    # we create a new todo (new_todo1) from the 'Todos' table (line 22). All it needs is a TASK because line 24 (complete) is default to False and the ID is automatically generated
    # whatever we type in here it will appear as 'new todo' in the web page
    new_todo = Todos(task='New Todo')
    db.session.add(new_todo)  # need to add the new_todo1 to the DB
    db.session.commit()  # need to save (commit) the new_todo in the DB
    return new_todo.task  # it is the same as "Added a new ToDO item"
'''
# For task 2.5:


@app.route("/add", methods=["GET", "POST"])
def add():
    form = TodoForm()  # we make an instance of our form called TodoForm()
    if form.validate_on_submit():  # if the form is valid on submit we will add the new todo
        # this will get the value entered in the form by the user
        new_todo = Todos(task=form.task.data)
        db.session.add(new_todo)  # need to add the new_todo1 to the DB
        db.session.commit()  # need to save (commit) the new_todo in the DB
        # if the form is valid it will redirect you to the home page. You need to call the function index in here that shows all_todos
        return redirect(url_for("index"))
    # we render the template 'add.html' and we pass the form as form
    return render_template("add.html", form=form)


# we had add a new variable to the complete page called @todo_id' so we can find it by ID
@app.route("/complete/<int:todo_id>")
def complete(todo_id):
    # we need to GET the entry in the DB so we need to do 'query' in the TODOS DB. We have to pass the todo ID no to find it
    todo = Todos.query.get(todo_id)
    # now this 'todo' variable in line 49 holds the ID for the todo in the ()
    todo.complete = True
    db.session.commit()
    # return "Completed Todo"
    ''' To make it a better experience instead of telling us it has completed the todo, we will redirect to the index page '''
    return redirect(url_for("index"))

# to get "/complete/<int:todo_id>" with URL_FOR:
#   url_for("complete", todo_id = 6 ) ## this will be the same as /complete/6


# This route below just does the opposite to the complete one
@app.route("/incomplete/<int:todo_id>")
def incomplete(todo_id):
    todo = Todos.query.get(todo_id)
    todo.complete = False
    db.session.commit()
    # return "Incompleted Todo"  see line 99
    return redirect(url_for("index"))

# This route below will delete items by giving it a todo ID


@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    todo = Todos.query.get(todo_id)  # we need to get the id number for the DB
    db.session.delete(todo)
    db.session.commit()  # once we have deleted the todo, we want to go back to the index. For this in line 1 we import 'URL_FOR & REDIRECT and we use it here
    return redirect(url_for("index"))  # this takes us back to index page


# to use the update page we need another route
@app.route("/update/<int:todo_id>", methods=["GET", "POST"])
def update(todo_id):  # we have to pass the variable(todo_id)
    form = TodoForm()
    # first time user goes to the update page we need to be able to tell them what todo they are updating. We get this from the DB
    todo_to_be_updated = Todos.query.get(todo_id)
    if form.validate_on_submit():  # user sends some data, what to do with it? we want to UPDATE the DB, not to add a new one
        # if the form is valid, change the column to the new value entered and we assign it to the DB with commit
        todo_to_be_updated.task = form.task.data
        db.session.commit()
        # when user enters update name, it will redirect them to home page to see their new todo
        return redirect(url_for("index"))
    elif request.method == "GET":  # they have made a get request, they have not entered or submitted anything yet
        # if they do not press submit (elif request.method=="GET":), show them in the column (form.task.data) what the column already says (todo_to_be_updated.task)
        form.task.data = todo_to_be_updated.task
    # we return a render template and we are going to render 'update.html' & we pass the form into that template
    return render_template("update.html", form=form)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')


from flask import Flask, render_template, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Todo(db.Model):
    
    sno = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(200),nullable = False)
    desc = db.Column(db.String(500),nullable = False)
    date_created = db.Column(db.DateTime, default=datetime.now())

def __repr__(self):
    return f"{self.sno} - {self.title}"



@app.route('/')
def index():
    return render_template("index.html")

# insert data 

@app.route("/insert", methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()

    return " "

@app.route("/show", methods=['GET', 'POST'])
def show():
    allTodo = Todo.query.all()
  

    if request.method == 'POST':
        output = ''
        output +='<div class="container my shownotes" id="shownotes">'
        for i in allTodo:
            output +=" "+ f'''
        
                <div class="card  my-3" style="width: 18rem;"  id ='{i.sno}'>
                    <div class="card-body">
                            <h5 class="card-title" id = "title">{i.title}</h5>
                            <p class="card-text" id = "desc">{i.desc}</p>
                            <p class="card-text">{i.date_created}</p>
                            <a href="/update/{i.sno}" class="btn btn-warning btn-lg active edit-btn" role="button" aria-pressed="true">Edit</a>
                             <a href="#" class="btn btn-danger btn-lg active delete-btn" data-id ={i.sno} role="button" aria-pressed="true">Delete</a>
                           
                    </div>    
                    </div>
                 
 '''
    output +=' </div>'
    count = len(allTodo)
    return jsonify({'output': output , 'count' : count})

@app.route('/delete', methods=['DELETE'])
def delete():
   
    if request.method == 'DELETE':
        sno = request.form['id']
        todo = Todo.query.filter_by(sno=sno).first()
        db.session.delete(todo)
        db.session.commit()
    
    allTodo = Todo.query.all()
    count = len(allTodo)

    return f"{count}"



@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/")
        
    todo = Todo.query.filter_by(sno=sno).first()
    return render_template('update.html', todo=todo)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')


if __name__ == "__main__":
   app.run(debug=True)
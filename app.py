from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import os
import json



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Block(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    body = db.Column(db.Text, nullable=False)


@app.route('/')
def home():
    return render_template("home.html")


@app.route('/blogs')
def blogs():
    return render_template('blogs.html')


@app.route('/calculator', methods=["GET", "POST"])
def calculator():
    if request.method == "GET":
        return render_template("calculator.html")
    else:
        num1 = request.form.get("num1")
        num2 = request.form.get("num2")
        action = request.form.get("action")
        num1, num2 = int(num1), int(num2)
        match action:
            case "add":
                natija = num1 + num2
            case "subtract":
                natija = num1 - num2
            case "mul":
                natija = num1 * num2
            case "div":
                if num2 == 0:
                    natija = " Cannot be divided by 0 ❌"
                else:
                    natija = num1 / num2
            case "pow":
                natija = num1 ** num2
        return render_template("calculator.html", natija=natija)


@app.route("/block/<pk>")
def blog_detail(pk):
    result = Block.query.get(int(pk))
    if result:
        return render_template("bloc.html", id=result.id, title=result.title, body=result.body)
    else:
        return "Block not found",


@app.route("/temp/<pk>")
def temp(pk):
    result = Block.query.get(int(pk))
    if result:
        return render_template("temp.html", id=result.id, title=result.title, body=result.body)
    else:
        return "Block not found",


@app.route('/create', methods=["GET", "POST"])
def new_block():
    if request.method == "GET":
        return render_template("new_bloc.html")
    else:
        res = Block(title=request.form.get("title"), body=request.form.get("body"))
        if res:
            db.session.add(res)
            db.session.commit()
            message = "Block added"
        else:
            message = "Block not added"
        return render_template("new_bloc.html", message=message)


@app.route('/delete', methods=["GET", "POST"])
def delete_block():
    if request.method == "GET":
        return render_template("delete.html")
    else:
        id = request.form.get("id")
        if id:
            block = Block.query.get(id)
            if block:
                db.session.delete(block)
                db.session.commit()
                message = f"Block with id {id} deleted"
            else:
                message = f"Block with id {id} not found"
        else:
            message = "Please provide an id"
        return render_template("delete.html", message=message)


@app.route('/blok_list')
def blok_list():
    blocks = Block.query.all()
    return render_template("blok_list.html", blocks=blocks)


@app.route('/update_block', methods=["GET", "POST"])
def update_block():
    if request.method == "GET":
        blocks = Block.query.all()
        return render_template("update_block.html", blocks=blocks)
    else:
        id = request.form.get("id")
        title = request.form.get("title")
        body = request.form.get("body")

        block = Block.query.get(id)
        if block:
            block.title = title
            block.body = body
            db.session.commit()
            message = f"Block with id {id} updated"
        else:
            message = f"Block with id {id} not found"

        return render_template("update_block.html", blocks=Block.query.all(), message=message)


@app.route('/title_update/<id>', methods=['GET', 'POST'])
def title_update(id):
    block = Block.query.get(int(id))
    if request.method == "GET":
        if block:
            return render_template("title_update.html", id=id, current_title=block.title)
        else:
            return "Block not found"
    else:
        new_title = request.form.get("title")
        if block:
            block.title = new_title
            db.session.commit()
            message = f"Title of block {id} updated"
        else:
            message = f"Block with id {id} not found"
        return render_template("title_update.html", id=id, current_title=new_title, message=message)


@app.route('/body_update/<id>', methods=['GET', 'POST'])
def body_update(id):
    block = Block.query.get(int(id))
    if request.method == "GET":
        if block:
            return render_template("body_update.html", id=id, current_body=block.body)
        else:
            return "Block not found"
    else:
        new_body = request.form.get("body")
        if block:
            block.body = new_body
            db.session.commit()
            message = f"Body of block {id} updated"
        else:
            message = f"Block with id {id} not found"
        return render_template("body_update.html", id=id, current_body=new_body, message=message)


if __name__ == '__main__':
    app.run(debug=True)








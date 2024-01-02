from flask import render_template, request, redirect
from MainPackage import app, login
import os
import utils
from MainPackage.admin import *
from flask_login import login_user



@app.route("/")
def home():
    users = [{
        "name": "Nguyen Van A",
        "email": "a@gamil.com"
    }, {
        "name": "Tran Thi B",
        "email": "b@gamil.com"
    }, {
        "name": "Vo Van C",
        "email": "c@gamil.com"
    }]

    kw = request.args.get("keyword")

    if kw:
        # users = [u for u in users if u['name'].find(kw) >= 0] biểu thức viết gọn
        kq = []

        for u in users:
            if u['name'].lower().find(kw.lower()) >= 0:
                kq.append(u)

        users = kq


    return render_template('index.html', users = users)

# @app.route("/id")
# def id():
#     return render_template('index.html')
#
# #path params
# @app.route("/hello/<int:name>")
# def hello(name):
#     return render_template('index.html', message = "XIN CHAO %s!!" % name)
#
# #get params
# @app.route("/hello")
# def hello2():
#     fn = request.args.get('first_name', 'A')
#     ln = request.args.get('last_name', 'B')
#     return render_template('index.html', message = "XIN CHAO %s %s!!" % (fn, ln))
#
# @app.route("/login", methods = ['post'])
# def login():
#     username = request.form['username']
#     password = request.form['password']
#
#     if username == "admin" and password == "123":
#         return 'successful'
#
#     return 'failed'
#
# @app.route("/upload", methods = ['post'])
# def upload():
#     f = request.files['avatar']
#
#     f.save(os.path.join(app.root_path, 'static/uploads/', f.filename))
#
#     return 'DONE.'

@app.route("/admin-login", methods = ['post'])
def admin_login():
    username = request.form.get('username')
    password = request.form.get('password')

    user = utils.check_login(username=username, password=password)
    if user:
        login_user(user=user)

    return redirect('/admin')

@login.user_loader
def load_user(user_id):
    return utils.get_user_by_id(user_id=user_id)

if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, request, redirect, render_template, session,jsonify
import os
from second import app2
from flask_jwt_extended import JWTManager
from db import db

app = Flask(__name__)  # 建立Application 實例
app.config["JSON_AS_ASCII"] = False
app.secret_key = "I'm secert key"
app.register_blueprint(app2)
app.config["JWT_SECRET_KEY"] = "supersecret"

jwt = JWTManager(app)


@jwt.expired_token_loader #過時token
def my_expired_token_callback(callback1,callback2):
    return redirect('/')

@jwt.invalid_token_loader #token被更改過
def my_invalid_token_callback(callback):
    return redirect('/')

@jwt.unauthorized_loader #沒付上token
def unauthorized_loader(callbak):
    return redirect('/')



# 建立路徑 / 對應的處理函式
@app.route("/index")
def index():
    # print("請求方法", request.method)
    # print("通訊協定", request.scheme)
    # print("主機名稱", request.host)
    # print("路徑", request.path)
    # print("網址", request.url)
    # print("語言", request.accept_languages)
    # return {"status": "ok", "text": "你好"}
    # return render_template("index", name="婉茹")
    return render_template("index")


# 表單使用post方法，前端輸入的值不會顯示在路由的querry string上，它會另外存放在body內，但GET方法會顯示在querry string上


@app.route("/page")
def page():
    return "get to another page."


@app.route("/calculate", methods=["POST"])
def calculate():
    # number = int(request.args.get("number", 0))
    number = int(request.form["number"])
    total = 0
    for i in range(number + 1):
        total += i
    return render_template("result.html", total=total)


@app.route("/show")
def show():
    name = request.args.get("name", "")
    return f"歡迎光臨，{name}"


# /hello?name=pam
@app.route("/hello")
def hello():
    name = request.args.get("name", "")
    session["user"] = name
    return f"你好，{name}"


@app.route("/talk")
def talk():
    return f"哈囉，又見到你了 {session['user']}"


@app.route("/getsum")
def getsum():
    maxNum = request.args.get("max", None)
    if maxNum is not None:
        sumNum = 0
        for i in range(int(maxNum) + 1):
            sumNum += i
        return f"{sumNum}"
    return "沒有數字"


@app.route("/user/<name>")
def user(name):
    return f"你好, {name.capitalize()}"


# 啟動伺服器
app.run(host="0.0.0.0", port=2000)

db.cnx.close() #資料庫連線終止
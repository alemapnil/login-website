from flask import Blueprint, render_template, request, session, redirect, jsonify
from flask_jwt_extended import create_access_token
from flask_jwt_extended import set_access_cookies, unset_jwt_cookies
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from db import db

app2 = Blueprint("abc", __name__)


@app2.route("/")
def home():
    return render_template("/ply/home.html")


@app2.route("/signup", methods=["POST"]) #register
def signup():
    name, username, password = (
        request.form["name"].strip(),
        request.form["username"].strip(),
        request.form["password"].strip(),
    )
    if len(name) == 0 or len(username) == 0 or len(password) == 0:
        return redirect(f"/error?message=註冊的值不可為空")
    ans = db.signup(name, username, password)
    if ans["ok"] is True:  # username is registered
        return redirect("/")
    else:
        return redirect(f"/error?message={username} 已經被註冊")


@app2.route("/signin", methods=["POST"]) #login
def signin():
    login_account, login_password = (
        request.form["login_account"].strip(),
        request.form["login_password"].strip(),
    )
    if len(login_account) == 0 or len(login_password) == 0:
        return redirect("/error?message=請輸入帳號、密碼")
    else:
        ans = db.signin(login_account, login_password) #印出帳號所屬姓名
        if ans["ok"] is False:
            return redirect(f"/error?message={ans['msg']}")
        else:
            session['name'] = ans['msg'] #set session 使用者姓名
            abcToken = create_access_token(identity={"login_account": login_account})  # type is string
            resp = redirect("/member")
            set_access_cookies(resp, abcToken) #set JWT cookies
            print(resp,'登入了',abcToken)
            
            return resp


@app2.route("/signout") #logout
@jwt_required(locations=["cookies"])  # locations=["cookies"]指定該去哪裡找JWT
def signout():
    # if "user" in session:
    #     session.pop("user")
    resp = redirect("/")
    unset_jwt_cookies(resp)
    del session['name']
    return resp


@app2.route("/member")
@jwt_required(locations=["cookies"])
def member():
    # if "user" in session:
    #     return render_template("/ply/member.html")
    user = get_jwt_identity()
    print('JWT >>',user)
    return render_template("/ply/member.html", member=session['name'])


@app2.route("/error")
def error():
    message = request.args.get("message", "")
    if len(message) > 0:  # querry string 有錯誤訊息
        return render_template("/ply/error.html", message=message)
    return redirect("/")


# JWT
@app2.route("/api/members")
@jwt_required(locations=["cookies"])
def search_member():
    user = get_jwt_identity()
    print(user)
    username = request.args.get("username", "")
    ans = db.search_member(username)
    return jsonify(ans)


# JWT
@app2.route("/api/member", methods=["POST"])
@jwt_required(locations=["cookies"])
def change_member():
    user = get_jwt_identity()
    print("用戶是", user)
    # changeName = request.form["name"].strip()
    changeName=request.get_json()['name']
    print('改名',changeName)
    if len(changeName) == 0:
        return jsonify({"msg": 'blank is not allowed'})
    else:
        ans = db.change_member(changeName, user["login_account"])
        print(ans)
        if ans['ok']:
            session['name'] = changeName
        return jsonify(ans)

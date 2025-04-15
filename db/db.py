import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path='w.env')

cnx = mysql.connector.connect(
    host = os.getenv('DB_HOST'), user = os.getenv('DB_USERNAME'), password = os.getenv('DB_PASSWORD'), 
    database = "website_db"
)

def signup(para1, para2, para3):
    mycursor = cnx.cursor()
    sql = "select *from member where username=%s"
    mycursor.execute(sql, (para2,))
    results = mycursor.fetchall()
    if len(results) == 0:  # 帳號沒註冊過
        sql = "insert into member (name, username, password) values(%s,%s,%s)"
        mycursor.execute(sql, (para1, para2, para3))
        cnx.commit()
        if mycursor.rowcount == 1:
            print(mycursor.rowcount, cnx,'in DB')
            return {"ok": True, "msg": f"{para2} is registered."}
    return {"ok": False, "msg": f"{para2} exists."}


def signin(para1, para2):  #登入後印出帳號所屬姓名
    mycursor = cnx.cursor()
    sql = "select * from member where username =%s and password=%s"
    mycursor.execute(sql, (para1, para2))
    results = mycursor.fetchall()
    if len(results) == 0: #找不到資料
        return {"ok": False, "msg": "帳號或密碼輸入錯誤"}
    return {"ok": True, "msg": results[0][1]}


def search_member(para):
    mycursor = cnx.cursor()
    sql = "select *from member where username =%s"
    mycursor.execute(sql, (para,))
    results = mycursor.fetchall()
    if len(results) == 0:
        return {"data": None}
    row = results[0]
    return {"data": {"id": row[0], "name": row[1], "username": row[2]}}


def change_member(para1, para2):
    mycursor = cnx.cursor()
    sql = "update member set name=%s where username=%s"
    mycursor.execute(sql, (para1, para2))
    cnx.commit()
    print(para1, para2,'In DB')
    if mycursor.rowcount == 1:
        return {"ok": True}
    else:
        return {"ok": False}

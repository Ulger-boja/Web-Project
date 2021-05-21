import mysql.connector
from flask import Flask, request,Response
from backend.utilities.generateAuthToken import generate

app = Flask(__name__)

dbContext = mysql.connector.connect(
    host="db-mysql-ams3-87275-do-user-9252818-0.b.db.ondigitalocean.com",
    port="25060",
    user="doadmin",
    password="xsyy941cq8224eaj",
    database='defaultdb',
)
cursor = dbContext.cursor()

@app.route('/provideToken', methods=["POST"])
def provideToken():
    token = generate()
    userId = request.args.get('userId')
    command = ("UPDATE author SET token = '"+token+"' WHERE user_id = '"+userId+"';")
    cursor.execute(command)
    dbContext.commit()
    return token

@app.route('/provideRole', methods=["GET"])
def provideRole():   
    token = request.args.get('token')
    getAuthorQuery = ("SELECT user_id FROM author WHERE token = '"+token+"'")
    cursor.execute(getAuthorQuery)
    userId = str(cursor.fetchone()[0])
    getRoleQuery = ("select role from login inner join author a on login.ID = a.user_id where ID = '"+userId+"'")
    cursor.execute(getRoleQuery)
    role = str(cursor.fetchone()[0])
    return role

@app.route('/provideUser', methods=["GET"])
def provideUser():
    token = request.args.get('token')
    getAuthorQuery = ("SELECT user_id FROM author WHERE token = '"+token+"'")
    cursor.execute(getAuthorQuery)
    userId = str(cursor.fetchone()[0])
    getUserQuery = ("select * from login inner join author a on login.ID = a.user_id where ID = '"+userId+"'")
    cursor.execute(getUserQuery)
    user = str(cursor.fetchone())
    return user
    

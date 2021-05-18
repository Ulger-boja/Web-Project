import sys
sys.path.append(
    r'C:\Users\UlgerBoja\AppData\Local\Programs\Python\Python39\Lib\site-packages')

from flask import Flask, request, jsonify
import requests
import mysql.connector
from datetime import datetime

app = Flask(__name__)

mydb = mysql.connector.connect(
    host="localhost",
    port="3307",
    user="root",
    password="Ulysses321",
    database='project'
)
mycursor = mydb.cursor()


@app.route('/')
def main():

    return 'Wellcome to fish\'s API'


@app.route('/Create_Post', methods=["GET", "POST"])
def Create_Post(mydb, mycursor):

    if request.method == "POST":
    
        headLine = request.form['headLine']
        description = request.form['description']
        image_url = request.form['image_url']
        author = request.form['author']
        dita = datetime.today().strftime('%Y-%m-%d')

        sql = ("INSERT INTO posts (headLine,description,image_url,author,dita) VALUES ('" +
               headLine+"','"+description+"','"+image_url+"','"+author+"','"+dita+"');")

        mycursor.execute(sql)
        mydb.commit()

    return 'ok'


@app.route('/delete_post', methods=["GET", "POST"])
def delete_post():

    if request.method == "POST":

        postID = request.form['postID']

        sql = ("DELETE * FROM posts WHERE postID = '"+postID+"';")
        mycursor.execute(sql)
        mydb.commit()

    return 'ok'


@app.route('/edit_post')
def edit_post():

    if request.method == "POST":
    
        postID = request.form['postID']
        headLine = request.form['headLine']
        description = request.form['description']
        image_url = request.form['image_url']
        author = request.form['author']
        dita = datetime.today().strftime('%Y-%m-%d')

        sql = ("UPDATE posts WHERE SET headLine = '"+headLine+"',description = '"+description+"',image_url = '"+image_url+"',author = '"+author+"',dita = '"+dita+"' WHERE postID = '"+postID+"';")
        mycursor.execute(sql)
        mydb.commit()

    return 'ok'


@app.route('/user_create')
def user_create():

    if request.method == "POST":
    
        username = request.form['username']
        password = request.form['password']

        sql = ("INSERT INTO login (username,password,roli) VALUES ('"+username+"','"+password+"', 'user')")
        mycursor.execute(sql)
        mydb.commit()

    return 'ok'


@app.route('/user_validate')
def user_validate():

    return 'not ok'


@app.route('/get_posts_by_user_id')
def get_posts_by_user_id():

    return 'not ok'


@app.route('/reccomended_post')
def reccomended_post():

    return 'not ok'

@app.route('/show_all_posts')
def show_all_posts():

    mycursor.execute("SELECT * FROM posts")

    myresult = mycursor.fetchall()

    for x in myresult:
      return jsonify(x)

if __name__ == '__main__':
    app.run(debug=True)

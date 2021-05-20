import sys



import mysql.connector
from flask import Flask, request,Blueprint
import json
import os
from  utilities.upload import AzureBlobFileUploader as uploader
app = Flask(__name__)

#path = os.getcwd()

#TODO:Find why this still return home dir
#Note run upload.py seperately then comment the path finding part
with open('data.txt', 'r') as file:
    data = file.read().replace('\n', '')
print(data, 'data')
#upload = uploader
#TODO:Find why it only works if the path is hardwritten
path = '/media/elidor/CC98A71E98A70654/Ubuntu/Web-Project/backend/buffer'
print(path)
#path = path.replace('api', 'buffer')

###
###################################################################         #################
app.config["imageUpload"] = path#     #####################
###################################################################         #################
                                                                                ###
mydb = mysql.connector.connect(
    host="db-mysql-ams3-87275-do-user-9252818-0.b.db.ondigitalocean.com",
    port="25060",
    user="doadmin",
    password="xsyy941cq8224eaj",
    database='defaultdb',
)
mycursor = mydb.cursor()

@app.route('/')
def main():
    
    return 'Welcome to fish\'s API'


@app.route('/Create_Post', methods=["GET", "POST"])
def Create_Post():

    if request.method == "POST":

        headLine = request.form['headLine']
        description = request.form['description']
        author = str(request.form['author'])


        if request.files:
            image = request.files["image"]
            print(image)
            print(path)
            image.save(os.path.join(
                path, image.filename))
        sql = ("INSERT INTO posts (headLine,description,author) VALUES ('" +
               headLine + "','" + description + "','" + author + "');")
        mycursor.execute(sql)
        mydb.commit()


    return '200'


@app.route('/delete_post', methods=["GET", "POST"])
def delete_post():

    if request.method == "POST":

        postID = request.form['post_id']

        sql = ("DELETE FROM posts WHERE post_id = '"+postID+"';")
        mycursor.execute(sql)
        mydb.commit()

    return 'ok'


@app.route('/edit_post', methods=["GET", "POST"])
def edit_post():

    if request.method == "POST":

        postID = request.form['post_id']
        headLine = request.form['headLine']
        description = request.form['description']
        author = request.form['author']

        sql = ("UPDATE posts WHERE SET headLine = '"+headLine+"',description = '"+description +
               ",author = '"+author+"' WHERE post_id = '"+postID+"';")
        mycursor.execute(sql)
        mydb.commit()

        if request.files:
            image = request.files["image"]
            print(image)
            image.save(os.path.join(
                app.config["imageUpload"], image.filename))

    return 'ok'


@app.route('/user_create', methods=["GET", "POST"])
def user_create():

    if request.method == "POST":

        username = request.form['username']
        password = request.form['password']

        sql = ("INSERT INTO login (username,password,roli) VALUES ('" +
               username+"','"+password+"', 'user')")
        mycursor.execute(sql)
        mydb.commit()

    return 'ok'


@app.route('/get_posts_by_user_id', methods=["GET", "POST"])
def get_posts_by_user_id():

    if request.method == "POST":
    
        userid = request.form['user_id']
        postID = request.form['post_id']

        sql = ("INSERT INTO reccomendations (user_id,post_id) VALUES ('"+userid+"','"+postID+"')")
        mycursor.execute(sql)
        mydb.commit()

    return 'ok'

class create_dict(dict):

    def __init__(self):
        self = dict()

    def add(self, key, value):
        self[key] = value


@app.route('/get_posts', methods=["GET", "POST"])
def get_posts():

    mydict = create_dict()
    select_post = """SELECT * FROM posts"""
    cursor = mydb.cursor()
    cursor.execute(select_post)
    result = cursor.fetchall()

    for row in result:
        mydict.add(row[0], ({"author": row[1], "description": row[2],
                   "image_url": row[3], "headLine": row[4], "dita": row[4]}))

    res = json.dumps(mydict, indent=2, sort_keys=True)

    return res

@app.route('/get_post_by_id', methods=["GET", "POST"])
def get_post_by_id():

    if request.method == "POST":

        postID = request.form['post_id']

        mydict = create_dict()
        select_post = ("SELECT * FROM posts WHERE post_id = '"+postID+"'")
        cursor = mydb.cursor()
        cursor.execute(select_post)
        result = cursor.fetchall()

        for row in result:
            mydict.add(row[0], ({"author": row[1], "description": row[2],
                       "image_url": row[3], "headLine": row[4], "dita": row[4]}))

        res = json.dumps(mydict, indent=2, sort_keys=True)

        return res

@app.route('/reccomended_post', methods=["GET", "POST"])
def reccomended_post():

    mydict = create_dict()
    select_post = """SELECT * FROM reccomendations"""
    cursor = mydb.cursor()
    cursor.execute(select_post)
    result = cursor.fetchall()

    for row in result:
        mydict.add(row[0], ({"author": row[1], "description": row[2],
                   "image_url": row[3], "headLine": row[4], "dita": row[4]}))

    res = json.dumps(mydict, indent=2, sort_keys=True)

    return res




if __name__ == '__main__':
    app.run(debug=True)

from werkzeug.utils import secure_filename
import boto3
import sys


import mysql.connector
from flask import Flask, request, Blueprint
import json
import os
from utilities.upload import AzureBlobFileUploader as uploader
app = Flask(__name__)


mydb = mysql.connector.connect(
    host="db-mysql-ams3-87275-do-user-9252818-0.b.db.ondigitalocean.com",
    port="25060",
    user="doadmin",
    password="xsyy941cq8224eaj",
    database='defaultdb',
)
mycursor = mydb.cursor()

upload = uploader


session = boto3.session.Session()
client = session.client('s3',
                        region_name='nyc3',
                        endpoint_url='https://fra1.digitaloceanspaces.com',
                        aws_access_key_id='NS24MAUHRGZ56BDTJRSF',
                        aws_secret_access_key='Z6oz3oxKV47F91gEUoZNorpowqZ9gvLelsPKsfiTAXs')


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
            bucket = 'web-project'
            image = request.files["image"]
            filename = secure_filename(image.filename)
            filename = filename + upload.get_random_string(10)
            content_type = 'image/jpg'
            client.put_object(Body=image,
                              Bucket=bucket,
                              Key=filename,
                              ContentType=content_type,
                              ACL='public-read')

        url = 'https://web-project.fra1.digitaloceanspaces.com/'+filename
        sql = ("INSERT INTO posts (headLine,description,author, image_url) VALUES ('" +
               headLine + "','" + description + "','" + author + "','"+url+"');")
        mycursor.execute(sql)
        mydb.commit()

    return '200'


@app.route('/delete_post', methods=["DELETE"])
def delete_post():

    if request.method == "DELETE":

        postID = request.form['post_id']

        sql = ("DELETE FROM posts WHERE post_id = '"+postID+"';")
        mycursor.execute(sql)
        mydb.commit()

    return '200'


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

    return '200'


@app.route('/user_create', methods=["GET", "POST"])
def user_create():

    if request.method == "POST":

        username = request.form['username']
        password = request.form['password']

        sql = ("INSERT INTO login (username,password,roli) VALUES ('" +
               username+"','"+password+"', 'user')")
        mycursor.execute(sql)
        mydb.commit()

    return '200'


@app.route('/get_posts_by_user_id', methods=["GET", "POST"])
def get_posts_by_user_id():

    if request.method == "POST":

        userid = request.form['user_id']
        postID = request.form['post_id']

        sql = ("INSERT INTO reccomendations (user_id,post_id) VALUES ('" +
               userid+"','"+postID+"')")
        mycursor.execute(sql)
        mydb.commit()

    return '200'


class create_dict(dict):

    def __init__(self):
        self = dict()

    def add(self, key, value):
        self[key] = value


@app.route('/get_posts', methods=["GET"])
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


@app.route('/get_post_by_id', methods=["GET"])
def get_post_by_id():

    if request.method == "GET":

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


@app.route('/reccomended_post', methods=["GET"])
def reccomended_post():

    postID = request.form['post_id']
    mydict = create_dict()
    select_post = """SELECT * FROM reccomendations LEFT JOIN post_id on posts.post_id = reccomendations.post_id """
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

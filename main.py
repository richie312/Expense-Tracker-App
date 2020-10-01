import flask
from flask import Flask, request, json,render_template,redirect,url_for,jsonify,json
from dotenv import load_dotenv
import mysql
import mysql.connector
import os
import sys
import pandas as pd
from datetime import datetime

""" decrypt the database details"""
main_dir = os.getcwd()
os.listdir(os.path.join(main_dir,'auth'))
from decrypt import *

db_auth = {'dbname.txt':'key_dbname.txt',
           'db_pass.txt':'key_db_pass.txt',
           'host.txt':'key_host.txt',
           'dbuser.txt':'key_dbuser.txt'}
filename = {}
for i in db_auth.keys():
    with open(r'auth/' +i, 'r') as readfile:
        filename['{}'.format(i.split('.')[0])]= json.load(readfile)

file_key = {}
for i in db_auth.keys():
    with open(r'auth/' +db_auth[i], 'r') as readfile:
        file_key['{}'.format(db_auth[i].split('.')[0])]= json.load(readfile)

db_auth = {}
for i in filename.keys():
    db_auth[i] = decrypt(eval(filename[i]),eval(file_key['key_'+i])).decode("utf-8")

app = Flask(__name__)
app.config['DEBUG'] = True

# load the environement variables

load_dotenv('.env')

""" read the list of users"""
@app.route("/")        
def homepage():
    with open(r'workout_type.txt','r') as readfile:
        workout_type = readfile.readlines()
    
    return render_template("user_form.html", workout_type = workout_type)





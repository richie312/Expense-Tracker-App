import mysql
import mysql.connector
import os
import sys
from decrypt import *
import json

""" decrypt the database details"""

def db_connection_string():
    main_dir = os.getcwd()
    os.listdir(os.path.join(main_dir,'auth'))
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

    connection = mysql.connector.connect(host=db_auth['host'], 
                                            user=db_auth['dbuser'],
                                            port=3306,
                                            passwd=db_auth['db_pass'], 
                                            db='Expense')
    return connection
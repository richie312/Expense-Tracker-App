import flask
from flask import Flask, request, json,render_template,redirect,url_for,jsonify,json
from dotenv import load_dotenv
import mysql
import mysql.connector
import os
import sys
import pandas as pd
import config.meta as meta
from datetime import datetime
from database import db_connection_string

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

# set the root and data folder
root_folder = os.getcwd()
data_folder = os.path.join(root_folder,'data')
# set workbook variables
filename = 'monthly_exp.xlsx'
list_sheet_names = meta.run_config['sheetname']
cost_based_items = ['veg','chicken','Grocery','Miscellaneous','credit','Tea','Tea Mom','Amla and giloy']
quantity_based_items = ['rum','cig','netflix','amazon','onedrive','internet','Juice','ParkFee']

""" read the list of users"""
@app.route("/")        
def homepage():
    # Initiate the database connection
    conn = db_connection_string()
    df = pd.read_csv(os.path.join(data_folder,'actual_cost_v1.csv'))
    commodity_list = df['Commodity'].values.tolist()
    cursor = conn.cursor()
    query = "Select * from Expense.current_total_expense_v1 order by batchid desc"
    cursor.execute(query)
    val = cursor.fetchone()
    last_cash_withdrawn = int(val[3])
    #cursor.close()
    #conn.close()
    return render_template("user_form.html", 
                            item_list = commodity_list,
                            last_cash_withdrawn = last_cash_withdrawn)

@app.route("/expense_data",methods=['GET'])
def expense_data():
    expense_df = pd.read_csv(os.path.join(data_folder,'expense.csv'))
    columns = ['Commodity','Cost','ColorCode','Unit of Measurement']
    item_data = expense_df.columns.values.tolist()
    col_data = expense_df.iloc[:1,].values.tolist()
    cost_data = expense_df.iloc[:len(expense_df),].values.tolist()[1:]
    temp_df = pd.DataFrame(columns = columns)
    temp_df['Commodity'] = item_data
    temp_df['Cost'] = cost_data[0]
    temp_df['ColorCode'] = col_data[0]
    temp_df['Unit of Measurement'] = ['Bottle','Units','INR','INR','Bottle','INR','INR','INR','INR']
    data = temp_df.iloc[:len(temp_df),].values.tolist()
    collection = [dict(zip(columns,data[i])) for i in range(len(data))]
    data = {"data": collection}
    return jsonify(data)

@app.route("/current_expense_data",methods=['GET'])
def current_expense_data():
    conn = db_connection_string()
    cursor = conn.cursor()
    latest_batchid_query = "Select max(batchid) from Expense.current_total_expense_v1"
    cursor.execute(latest_batchid_query)
    latest_batchid = cursor.fetchall()
    latest_batchid = latest_batchid[0][0]
    query = "select * from Expense.current_total_expense_v1 where batchid = {}".format(latest_batchid)
    cursor.execute(query)
    data = cursor.fetchall()
    real_time_data = list(data[0])
    
    current_expense_df = pd.read_csv(os.path.join(data_folder,'current_total_expense_v1.csv'))
    column_list = current_expense_df.columns.values.tolist()
    collection = dict(zip(column_list,real_time_data[:4]))
    val = {"data": [collection]}
    return jsonify(val)

@app.route("/addDetails",methods=['POST'])
def addDetails():
    # Initiate the database connection
    conn = db_connection_string()
    cursor = conn.cursor()
    data = request.form
    if data["cash"] ==  '':
        pass
    else:
        latest_batchid_query = "Select max(batchid) from Expense.current_total_expense_v1"
        cursor.execute(latest_batchid_query)
        latest_batchid = cursor.fetchall()
        latest_batchid = latest_batchid[0][0]

        query = "SET SQL_SAFE_UPDATES = 0;"
        cursor.execute(query)
        cash_query = """update Expense.current_total_expense_v1 set Cash_Withdrawn = Cash_Withdrawn  + {},updated = %s where batchid = {}""".format(int(data["cash"]),latest_batchid)
        cursor.execute(cash_query,(datetime.now().strftime('%Y-%m-%d %H:%M:%S'),))
        conn.commit()
    if (data["cost"] == "") and (data["quantity"] == ""):
        handler = 'empty'
    elif (data["cost"] != "") and (data["quantity"] != "") and (data["item_type"] in cost_based_items):
        handler = "Database Updated"
        latest_batchid_query = "Select max(batchid) from Expense.actual_cost_v1"
        cursor.execute(latest_batchid_query)
        latest_batchid = cursor.fetchall()
        latest_batchid = latest_batchid[0][0]

        query = "SET SQL_SAFE_UPDATES = 0;"
        cursor.execute(query)
        cash_query = """update Expense.actual_cost_v1 set Quantity = {}, Cumulative_Quantity = Cumulative_Quantity + {}, Cost = Cost + {},updated = %s where batchid = {} and Commodity = %s""".format(int(data["quantity"]),int(data["quantity"]),int(data["cost"]),latest_batchid)
        cursor.execute(cash_query,(datetime.now().strftime('%Y-%m-%d %H:%M:%S'),data['item_type'],))
        conn.commit()
        update_total_cost_query = "update Expense.actual_cost_v1 set Total = Cumulative_Quantity * Cost, updated = %s where batchid = {} and Commodity = %s".format(latest_batchid)
        cursor.execute(update_total_cost_query,(datetime.now().strftime('%Y-%m-%d %H:%M:%S'),data['item_type'],))
        conn.commit()
        sum_query = "Select sum(Total) from Expense.actual_cost_v1 where batchid = {}".format(latest_batchid)
        cursor.execute(sum_query)
        total = cursor.fetchone()
        total = int(total[0])
        update_total_column = """update Expense.actual_cost_v1 set GrandTotal = {}, updated = %s where batchid = {}""".format(total,latest_batchid)
        cursor.execute(update_total_column,(datetime.now().strftime('%Y-%m-%d %H:%M:%S'),))
        conn.commit()

    elif (data["cost"] != "") and (data["quantity"] != "") and (data["item_type"] in quantity_based_items):
        handler = "Database Updated"
        latest_batchid_query = "Select max(batchid) from Expense.actual_cost_v1"
        cursor.execute(latest_batchid_query)
        latest_batchid = cursor.fetchall()
        latest_batchid = latest_batchid[0][0]

        query = "SET SQL_SAFE_UPDATES = 0;"
        cursor.execute(query)
        cash_query = """update Expense.actual_cost_v1 set Quantity = {}, Cumulative_Quantity = Cumulative_Quantity + {}, Cost = {},Total = Cumulative_Quantity * {},updated = %s where batchid = {} and Commodity = %s""".format(int(data["quantity"]),int(data["quantity"]),int(data["cost"]),int(data["cost"]),latest_batchid)
        cursor.execute(cash_query,(datetime.now().strftime('%Y-%m-%d %H:%M:%S'),data['item_type'],))
        conn.commit()
        sum_query = "Select sum(Total) from Expense.actual_cost_v1 where batchid = {}".format(latest_batchid)
        cursor.execute(sum_query)
        total = cursor.fetchone()
        total = int(total[0])
        update_total_column = """update Expense.actual_cost_v1 set GrandTotal = {}, updated = %s where batchid = {}""".format(total,latest_batchid)
        cursor.execute(update_total_column,(datetime.now().strftime('%Y-%m-%d %H:%M:%S'),))
        conn.commit()
    else:
        handler = "Nothing to Submit"
    return render_template('user_form_response.html')

if __name__ == '__main__':
    app.run(host = '0.0.0.0',debug=True,port=5003)



import os
from dotenv import load_dotenv
import mysql
import mysql.connector
import pandas as pd
import config.meta as meta
import logging
from database import db_connection_string
from datetime import datetime
from helper_functions import generate_dataframe,DataObject, rules_check

# Initailise the logger
logger = logging.getLogger()
logging.basicConfig(level= logging.INFO)


# set the root and data folder
root_folder = os.getcwd()
data_folder = os.path.join(root_folder,'data')
# set workbook variables
filename = 'monthly_exp.xlsx'
list_sheet_names = meta.run_config['sheetname']


# Generate Dataframe
for sheet in list_sheet_names:
   data = generate_dataframe(filename,sheet)
   data.to_csv(os.path.join(data_folder,'{}.csv'.format(sheet)),index = False)

# Data Insertion
# Instantiate database connection
logger.info("{}: Connecting to database...".format(datetime.now()))
conn = db_connection_string()

for sheet in list_sheet_names:
    logger.info("{}: Data insertion for table {} is in progress...".format(datetime.now(),sheet))
    datapath = os.path.join(data_folder,sheet+'.csv')
    df = DataObject(datapath)
    data = df.get_data()
    eval(meta.run_config[sheet])
    logger.info("{}: Data insertion for table {} is completed.".format(datetime.now(),sheet))
   
# Rules Check for expense growth rate
logger.info("{}: Checking rules for relevant commodities...".format(datetime.now()))
result = rules_check(conn)
expense_gr_df = pd.DataFrame(result,columns = list(result.keys()))
expense_gr_df.to_csv(os.path.join(data_folder,'expense.csv'),index = False)
print(expense_gr_df)
logger.info("{}: All the rules has been applied and ready for expense growth rate data insertion.".format(datetime.now()))

# Expense Growth Rate Data Insertion
logger.info("{}: Data Insertion for expense growth rate is completed.".format(datetime.now()))



logger.info("Updating the cumulative quantity for each item in actual_cost_v1 table.")
cursor = conn.cursor()
latest_batchid_query = "Select max(batchid) from Expense.actual_cost_v1"
cursor.execute(latest_batchid_query)
latest_batchid = cursor.fetchall()
latest_batchid = latest_batchid[0][0]
latest_df = "select * from Expense.actual_cost_v1 where batchid = {}".format(latest_batchid)
cursor.execute(latest_df)
latest_updated_df = cursor.fetchall()
quantity = [latest_updated_df[i][1] for i in range(len(latest_updated_df))]
Commodity = [latest_updated_df[i][0] for i in range(len(latest_updated_df))]

for quant in range(len(quantity)):
    print(quantity[quant])
    query = "SET SQL_SAFE_UPDATES = 0"
    cursor.execute(query)
    cursor.execute("update Expense.actual_cost_v1 set Cumulative_Quantity = {} where batchid = {} and Commodity = %s".format(quantity[quant],latest_batchid),(Commodity[quant],))
    conn.commit()

logger.info("Updated.")
# Connection Closure
logger.info("{}: Database connection closure.".format(datetime.now()))
conn.close()
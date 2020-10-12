#/home/ubuntu/envs/expense/bin/python3
import os
from dotenv import load_dotenv
import mysql
import argparse
import mysql.connector
import pandas as pd
import config.meta as meta
import logging
from database import db_connection_string
from datetime import datetime
from helper_functions import generate_dataframe,DataObject, rules_check

# Initailise the logger
logger = logging.getLogger()
logging.basicConfig(filename='cron_man.log', encoding='utf-8', level= logging.INFO)


# set the root and data folder
root_folder = os.getcwd()
data_folder = os.path.join(root_folder,'data')
# set workbook variables
filename = 'monthly_exp.xlsx'
list_sheet_names = meta.run_config['sheetname']

# Generate command line args for generating dataframe from base template
my_parser = argparse.ArgumentParser()
my_parser.add_argument('--generate_dataframe',
                        help = 'True or False in order to create dataset from template.csv',
                        default = False,
                        required = False)

# print default values of the command line argument

args = my_parser.parse_args()
generate_dataframe = bool(args.generate_dataframe)
logger.info('The arg value for generate_dataframe is {}'.format(generate_dataframe))


# Data Insertion
# Instantiate database connection
logger.info("{}: Connecting to database...".format(datetime.now()))
conn = db_connection_string()

# Rules Check for expense growth rate
logger.info("{}: Checking rules for relevant commodities...".format(datetime.now()))
result = rules_check(conn)
expense_gr_df = pd.DataFrame(result,columns = list(result.keys()))
expense_gr_df.to_csv(os.path.join(data_folder,'expense.csv'),index = False)
print(expense_gr_df)
logger.info("{}: All the rules has been applied and ready for expense growth rate data insertion.".format(datetime.now()))

# data insertion
for sheet in list_sheet_names:
    print(sheet)
    if sheet == 'actual_cost_v1':
        print('Actual table is populated on real time basis.')
    elif sheet == 'planned_estimated_cost_v1':
        print('This table is updated on the last day of the month.')
    elif sheet == 'current_total_expense_base':
        print('This table is updated on the last day of the month.')    
    else:
        logger.info("{}: Data insertion for table {} is in progress...".format(datetime.now(),sheet))
        datapath = os.path.join(data_folder,sheet+'.csv')
        df = DataObject(datapath)
        eval(meta.run_config[sheet])
        logger.info("{}: Data insertion for table {} is completed.".format(datetime.now(),sheet))
   

logger.info("All Database Updated.")
with open(r'logs.txt','a+') as outfile:
    outfile.write("{}: All database updated \n".format(datetime.now()))

with open(r'month_last_date.json','r') as readfile:
    month_lastdate_map = json.load(readfile)

day_of_month = datetime.now().day
month = datetime.now().month

if day_of_month == month_lastdate_map[str(month)]:
    logger.info("Generating and Inserting the base templates in the database.") 
    list_base_templates = []
    list_base_templates.extend(list_sheet_names)
    list_base_templates.append('current_total_expense_base')
    list_base_templates.append('planned_estimated_cost_v1')
    list_base_templates = list_base_templates[-2:]
    for sheet in list_base_templates:
        logger.info('generating base template for {}'.format(sheet))
        data = generate_dataframe(filename,sheet)
        data.to_csv(os.path.join(data_folder,'{}.csv'.format(sheet)),index = False)
    # Inserting in the the database
        logger.info("{}: Data insertion for table {} is in progress...".format(datetime.now(),sheet))
        datapath = os.path.join(data_folder,sheet+'.csv')
        df = DataObject(datapath)
        eval(meta.run_config[sheet])
        logger.info("{}: Data insertion for table {} is completed.".format(datetime.now(),sheet))

# Connection Closure
logger.info("{}: Database connection closure.".format(datetime.now()))
conn.close()
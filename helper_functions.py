import os
from dotenv import load_dotenv
import mysql
import mysql.connector
import pandas as pd
from datetime import datetime, timedelta
import logging

logger = logging.getLogger()
logging.basicConfig(level= logging.INFO)

def generate_dataframe(filename,sheet):
    root_folder = os.getcwd()
    data_folder = os.path.join(root_folder,'data')
    xls = pd.ExcelFile(os.path.join(data_folder,filename))
    df1 = pd.read_excel(xls, sheet)
    return df1


class DataObject(object):
    # Constructor
    def __init__(self,datapath):
        super().__init__()
        self.data = pd.read_csv(datapath)

    def get_data(self):
        return self.data

    def display_columns(self):
        return self.data.columns.values.tolist()

    def current_total_expense_insertion(self,conn,sheet,row):
        cursor = conn.cursor()
        validation_query = """Select max(batchid) from Expense.{table_name}""".format(table_name = sheet)
        cursor.execute(validation_query)
        max_batchid = cursor.fetchone()
        max_batch_id = max_batchid[0]
        # Check whether the max batchid is of today or nor?
        if int(datetime.now().strftime('%Y%m%d')) == max_batch_id:
            logger.info("{}:Expense.{table_name} has been updated today. Aborting".format(datetime.now(),table_name = sheet))
        else:
            logger.info("{}:Inserting data for Expense.{table_name} ... ".format(datetime.now(),table_name = sheet))
            values = self.data.iloc[:row+1,].values.tolist()[0]
            values.append(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            query = """INSERT INTO Expense.{table_name} (Earlier, Now, Days_Left, Cash_Withdrawn, updated) values {vals}""".format(table_name = sheet,vals= tuple(values))
            cursor.execute(query)
            print(query)
            conn.commit()
        cursor.close()
        

    def actual_cost_insertion(self,conn,sheet,row):
        cursor = conn.cursor()
        validation_query = """Select max(batchid) from Expense.{table_name}""".format(table_name = sheet)
        cursor.execute(validation_query)
        max_batchid = cursor.fetchone()
        max_batch_id = max_batchid[0]
        # Check whether the max batchid is of today or nor?
        if int(datetime.now().strftime('%Y%m%d')) == max_batch_id:
            logger.info("{}:Expense.{table_name} has been updated today. Aborting".format(datetime.now(),table_name = sheet))
        else:
            logger.info("{}:Inserting data for Expense.{table_name} ... ".format(datetime.now(),table_name = sheet))
            values = self.data.iloc[:row,].values.tolist()
            for val in values:
                val.append(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                val.append(int(datetime.now().strftime('%Y%m%d')))
                query = """INSERT INTO Expense.{table_name} (Commodity, Quantity, Cost, Total, GrandTotal, updated, batchid) values {vals}""".format(table_name = sheet,vals= tuple(val))
                cursor.execute(query)  
                conn.commit()
                print(query)
        cursor.close()
    
    def planned_estimated_cost_insertion(self,conn,sheet,row):
        cursor = conn.cursor()
        validation_query = """Select max(batchid) from Expense.{table_name}""".format(table_name = sheet)
        cursor.execute(validation_query)
        max_batchid = cursor.fetchone()
        max_batch_id = max_batchid[0]
        # Check whether the max batchid is of today or nor?
        if int(datetime.now().strftime('%Y%m%d')) == max_batch_id:
            logger.info("{}:Expense.{table_name} has been updated today. Aborting".format(datetime.now(),table_name = sheet))
        else:
            logger.info("{}:Inserting data for Expense.{table_name} ... ".format(datetime.now(),table_name = sheet))
            values = self.data.iloc[:row,].values.tolist()
            for val in values:
                val.append(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                val.append(int(datetime.now().strftime('%Y%m%d')))
                query = """INSERT INTO Expense.{table_name} (Commodity, Quantity, Cost, Total, GrandTotal, updated, batchid) values {vals}""".format(table_name = sheet,vals= tuple(val))
                cursor.execute(query)  
                conn.commit()
                print(query)
        cursor.close()

    def expense_growth_rate_insertion(self,conn,sheet,row):
        cursor = conn.cursor()
        validation_query = """Select max(batchid) from Expense.{table_name}"""
        cursor.execute(validation_query)
        max_batchid = cursor.fetchone()
        max_batch_id = max_batchid[0]
        # Check whether the max batchid is of today or nor?
        if int(datetime.now().strftime('%Y%m%d')) == max_batch_id:
            logger.info("{}:Expense.{table_name} has been updated today. Aborting".format(datetime.now(),table_name = sheet))
        else:
            logger.info("{}:Inserting data for Expense.{table_name} ... ".format(datetime.now(),table_name = sheet))
            values = self.data.iloc[:row+1,].values.tolist()[0]
            values.append(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            query = """INSERT INTO Expense.{table_name} (Earlier, Now, Days_Left, Cash_Withdrawn, updated) values {vals}""".format(table_name = sheet,vals= tuple(values))
            cursor.execute(query)    
            conn.commit()
            print(query)
        cursor.close()


def rules_check(conn):
    cursor = conn.cursor()
    items = ['rum','cig', 'Tea', 'Tea Mom', 'Juice', 'chicken', 'veg', 'Grocery', 'Miscellaneous']
    planned_quantity = []
    estimated_price = []
    estimated_total_cost = []
    for item in items:
        query = """Select Quantity,Cost,Total from Expense.planned_estimated_cost_v1 where Commodity = %s"""
        cursor.execute(query,(item,))
        val = cursor.fetchall()
        planned_quantity.append(val[0][0])
        estimated_price.append(val[0][1])
        estimated_total_cost.append(val[0][2])

    #collect information from actual
    query = """Select max(batchid) from Expense.actual_cost_v1"""
    cursor.execute(query)
    max_batchid = cursor.fetchone()
    max_batch_id = max_batchid[0]        
    actual_quantity = []
    actual_price = []
    actual_total_cost = []
    for item in items:
        query = """Select Quantity,Cost,Total from Expense.actual_cost_v1 where Commodity = %s and batchid = {batchid}""".format(batchid = max_batch_id)
        cursor.execute(query,(item,))
        val = cursor.fetchall()
        actual_quantity.append(val[0][0])
        actual_price.append(val[0][1])
        actual_total_cost.append(val[0][2])
    cursor.close() 
    # make a new dataframe
    new_df = pd.DataFrame(columns=['items','planned_quantity','estimated_price',
                                    'estimated_total_cost','actual_quantity','actual_price','actual_total_cost'])
    columns=['items','planned_quantity','estimated_price',
                                    'estimated_total_cost','actual_quantity','actual_price','actual_total_cost']
    for col in columns:
        new_df[col] = eval(col) 
    # logic for each commodity
    # Rum Per week 2 bottles check
    result = {}
    day_of_month = datetime.now().day
    week_number = (day_of_month - 1) // 7 + 1
    if new_df['actual_quantity'][new_df['items'] == 'rum'].values[0] == week_number * new_df['actual_quantity'][new_df['items'] == 'rum'].values[0]:
        Color='#FFA500'
        Quantity=new_df['actual_quantity'][new_df['items'] == 'rum'].values[0]

    elif new_df['actual_quantity'][new_df['items'] == 'rum'].values[0]< (week_number * 2):
        Color = '#008000'
        Quantity = new_df['planned_quantity'][new_df['items'] == 'rum'].values[0]- new_df['actual_quantity'][new_df['items'] == 'rum'].values[0]

    elif new_df['actual_quantity'][new_df['items'] == 'rum'].values[0] > (week_number * 2):
        Color = '#FF0000'
        Quantity = new_df['actual_quantity'][new_df['items'] == 'rum'].values[0] - new_df['planned_quantity'][new_df['items'] == 'rum'].values[0]
    result['rum'] = {'Color':Color,'Quantity': Quantity}
    
    # Cig per day 5 check
    day_of_month = datetime.now().day
    
    if new_df['actual_quantity'][new_df['items'] == 'cig'].values[0] == day_of_month * new_df['planned_quantity'][new_df['items'] == 'cig'].values[0]:
        Color='#FFA500'
        Quantity=new_df['actual_quantity'][new_df['items'] == 'cig'].values[0]

    elif new_df['actual_quantity'][new_df['items'] == 'cig'].values[0] < (new_df['planned_quantity'][new_df['items'] == 'cig'].values[0]):
        Color = '#008000'
        Quantity = (new_df['planned_quantity'][new_df['items'] == 'cig'].values[0]) - new_df['actual_quantity'][new_df['items'] == 'cig'].values[0]*day_of_month

    elif new_df['actual_quantity'][new_df['items'] == 'cig'].values[0]  > (new_df['planned_quantity'][new_df['items'] == 'cig'].values[0]):
        Color = '#FF0000'
        Quantity = new_df['actual_quantity'][new_df['items'] == 'cig'].values[0]*day_of_month - (new_df['planned_quantity'][new_df['items'] == 'cig'].values[0])
    result['cig'] = {'Color':Color,'Quantity': Quantity}

    # Personal Tea Consumption is less than equal Rs 1400

    if new_df['actual_total_cost'][new_df['items'] == 'Tea'].values[0] == 1400:
        Color='#FFA500'
        Quantity=new_df['actual_total_cost'][new_df['items'] == 'Tea'].values[0]

    elif new_df['actual_total_cost'][new_df['items'] == 'Tea'].values[0] < 1400:
        Color = '#008000'
        Quantity = new_df['estimated_total_cost'][new_df['items'] == 'Tea'].values[0] - new_df['actual_total_cost'][new_df['items'] == 'Tea'].values[0]

    elif new_df['actual_total_cost'][new_df['items'] == 'Tea'].values[0]  > 1400:
        Color = '#FF0000'
        Quantity = new_df['actual_total_cost'][new_df['items'] == 'Tea'].values[0] - new_df['estimated_total_cost'][new_df['items'] == 'Tea'].values[0]
    result['Tea'] = {'Color':Color,'Quantity': Quantity}

    # Expense on Tea for mother less than equal Rs 1400

    if new_df['actual_total_cost'][new_df['items'] == 'Tea Mom'].values[0] == 1400:
        Color='#FFA500'
        Quantity=new_df['actual_total_cost'][new_df['items'] == 'Tea Mom'].values[0]

    elif new_df['actual_total_cost'][new_df['items'] == 'Tea Mom'].values[0] < 1400:
        Color = '#008000'
        Quantity = new_df['estimated_total_cost'][new_df['items'] == 'Tea Mom'].values[0] - new_df['actual_total_cost'][new_df['items'] == 'Tea Mom'].values[0]

    elif new_df['actual_total_cost'][new_df['items'] == 'Tea Mom'].values[0]  > 1400:
        Color = '#FF0000'
        Quantity = new_df['actual_total_cost'][new_df['items'] == 'Tea Mom'].values[0] - new_df['estimated_total_cost'][new_df['items'] == 'Tea Mom'].values[0]
    result['Tea Mom'] = {'Color':Color,'Quantity': Quantity}

    # Juice Bottle Consumtion Check; must be less than 3 per week
    day_of_month = datetime.now().day
    week_number = (day_of_month - 1) // 7 + 1
    if new_df['actual_quantity'][new_df['items'] == 'Juice'].values[0] == week_number * new_df['planned_quantity'][new_df['items'] == 'Juice'].values[0]:
        Color='#FFA500'
        Quantity=new_df['actual_quantity'][new_df['items'] == 'Juice'].values[0]

    elif new_df['actual_quantity'][new_df['items'] == 'Juice'].values[0]< (new_df['planned_quantity'][new_df['items'] == 'Juice'].values[0]):
        Color = '#008000'
        Quantity = (new_df['planned_quantity'][new_df['items'] == 'Juice'].values[0])- new_df['actual_quantity'][new_df['items'] == 'Juice'].values[0]

    elif new_df['actual_quantity'][new_df['items'] == 'Juice'].values[0] > (new_df['planned_quantity'][new_df['items'] == 'Juice'].values[0]):
        Color = '#FF0000'
        Quantity = new_df['actual_quantity'][new_df['items'] == 'Juice'].values[0] - new_df['planned_quantity'][new_df['items'] == 'Juice'].values[0]
    result['Juice'] = {'Color':Color,'Quantity': Quantity}
    
    # Chicken Consumption is less than equal Rs 250 per week
    day_of_month = datetime.now().day
    week_number = (day_of_month - 1) // 7 + 1

    if new_df['actual_total_cost'][new_df['items'] == 'chicken'].values[0] == new_df['estimated_price'][new_df['items'] == 'chicken'].values[0] * week_number:
        Color='#FFA500'
        Quantity=new_df['actual_total_cost'][new_df['items'] == 'chicken'].values[0]

    elif new_df['actual_total_cost'][new_df['items'] == 'chicken'].values[0] < new_df['estimated_price'][new_df['items'] == 'chicken'].values[0] * week_number:
        Color = '#008000'
        Quantity = new_df['estimated_total_cost'][new_df['items'] == 'chicken'].values[0] - new_df['actual_total_cost'][new_df['items'] == 'chicken'].values[0]

    elif new_df['actual_total_cost'][new_df['items'] == 'chicken'].values[0]  > new_df['estimated_price'][new_df['items'] == 'chicken'].values[0] * week_number:
        Color = '#FF0000'
        Quantity = new_df['actual_total_cost'][new_df['items'] == 'chicken'].values[0] - new_df['estimated_total_cost'][new_df['items'] == 'chicken'].values[0]
    result['chicken'] = {'Color':Color,'Quantity': Quantity}


    # Vegetable consumptions must be less than 250 per week
    day_of_month = datetime.now().day
    week_number = (day_of_month - 1) // 7 + 1

    if new_df['actual_total_cost'][new_df['items'] == 'veg'].values[0] == 250 * week_number:
        Color='#FFA500'
        Quantity=new_df['actual_total_cost'][new_df['items'] == 'veg'].values[0]

    elif new_df['actual_total_cost'][new_df['items'] == 'veg'].values[0] < 250 * week_number:
        Color = '#008000'
        Quantity = new_df['estimated_total_cost'][new_df['items'] == 'veg'].values[0] - new_df['actual_total_cost'][new_df['items'] == 'veg'].values[0]

    elif new_df['actual_total_cost'][new_df['items'] == 'veg'].values[0]  > 250 * week_number:
        Color = '#FF0000'
        Quantity = new_df['actual_total_cost'][new_df['items'] == 'veg'].values[0] - new_df['estimated_total_cost'][new_df['items'] == 'veg'].values[0]
    result['veg'] = {'Color':Color,'Quantity': Quantity}


    # Gorcery consumption must be less than 750 per week
    day_of_month = datetime.now().day
    week_number = (day_of_month - 1) // 7 + 1

    if new_df['actual_total_cost'][new_df['items'] == 'Grocery'].values[0] == 750 * week_number:
        Color='#FFA500'
        Quantity=new_df['actual_total_cost'][new_df['items'] == 'Grocery'].values[0]

    elif new_df['actual_total_cost'][new_df['items'] == 'Grocery'].values[0] < 750 * week_number:
        Color = '#008000'
        Quantity = (750 * week_number) - new_df['actual_total_cost'][new_df['items'] == 'Grocery'].values[0]

    elif new_df['actual_total_cost'][new_df['items'] == 'Grocery'].values[0]  > 750 * week_number:
        Color = '#FF0000'
        Quantity = new_df['actual_total_cost'][new_df['items'] == 'Grocery'].values[0] - (750 * week_number)
    result['Grocery'] = {'Color':Color,'Quantity': Quantity}

    # Miscellaneous Expense must be less than 250 per week
    day_of_month = datetime.now().day
    week_number = (day_of_month - 1) // 7 + 1

    if new_df['actual_total_cost'][new_df['items'] == 'Miscellaneous'].values[0] == 250 * week_number:
        Color='#FFA500'
        Quantity=new_df['actual_total_cost'][new_df['items'] == 'Miscellaneous'].values[0]

    elif new_df['actual_total_cost'][new_df['items'] == 'Miscellaneous'].values[0] < 250 * week_number:
        Color = '#008000'
        Quantity = new_df['estimated_total_cost'][new_df['items'] == 'Miscellaneous'].values[0] - new_df['actual_total_cost'][new_df['items'] == 'Miscellaneous'].values[0]

    elif new_df['actual_total_cost'][new_df['items'] == 'Miscellaneous'].values[0]  > 250 * week_number:
        Color = '#FF0000'
        Quantity = new_df['actual_total_cost'][new_df['items'] == 'Miscellaneous'].values[0] - new_df['estimated_total_cost'][new_df['items'] == 'Miscellaneous'].values[0]
    result['Miscellaneous'] = {'Color':Color,'Quantity': Quantity}

    return result
run_config = {

'sheetname': ['current_total_expense_v1','actual_cost_v1','planned_estimated_cost_v1'],
'current_total_expense_v1':'df.current_total_expense_insertion(conn,sheet,len(data))',
'actual_cost_v1': 'df.actual_cost_insertion(conn,sheet,len(data))',
'planned_estimated_cost_v1': 'df.planned_estimated_cost_insertion(conn,sheet,len(data))'

}
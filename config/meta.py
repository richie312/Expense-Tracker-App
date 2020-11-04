run_config = {

'sheetname': ['current_total_expense_v1','actual_cost_v1','expense'],
'current_total_expense_v1':'df.current_total_expense_insertion(conn)',
'current_total_cash_base': 'df.current_total_cash_base_insertion(conn)',
'actual_cost_v1': 'df.actual_cost_insertion(conn)',
'expense': 'df.expense_growth_rate_update(conn)',
'planned_estimated_cost_v1':'df.planned_estimated_cost_insertion(conn,sheet,len(data))',
'current_total_expense_base': 'df.current_total_expense_base(conn,sheet,len(data))'
}
 SET SQL_SAFE_UPDATES = 0;
 --  delete from Expense.current_total_expense_v1 where batchid is NULL
-- Select * from Expense.current_total_expense_v1
-- Select max(batchid) from Expense.planned_estimated_cost_v1
-- Select * from Expense.planned_estimated_cost_v1 where batchid = 20201001
-- alter table Expense.current_total_expense_v1 add column batchid bigint;
-- rename table Expense.planned_estimated_cost to Expense.planned_estimated_cost_v1
-- Select * from Expense.actual_cost_v1 where batchid = max(batchid) 
-- alter table Expense.actual_cost_v1 add column updated datetime
-- alter table Expense.actual_cost_v1 add column Cumulative_Quantity bigint
-- update Expense.actual_cost_v1 set Cumulative_Quantity = 1 where batchid = 202010051305 and Commodity = 'Grocery'
 Select * from Expense.actual_cost_v1 where batchid = 202010060950
-- update Expense.current_total_expense_v1  set batchid = 20201001
 SET SQL_SAFE_UPDATES = 0;
 -- delete from Expense.current_total_expense_v1 where updated = '2020-10-01 19:05:35'
Select * from Expense.current_total_expense_v1
-- Select max(batchid) from Expense.planned_estimated_cost_v1
-- Select * from Expense.planned_estimated_cost_v1 where batchid = 20201001
-- alter table Expense.current_total_expense_v1 add column batchid bigint;
-- rename table Expense.planned_estimated_cost to Expense.planned_estimated_cost_v1
-- Select * from Expense.actual_cost_v1 where batchid = max(batchid) 
-- alter table Expense.actual_cost_v1 add column updated datetime
-- alter table Expense.actual_cost_v1 add column batchid bigint
-- Select * from Expense.current_total_expense_v1
-- update Expense.current_total_expense_v1  set batchid = 20201001
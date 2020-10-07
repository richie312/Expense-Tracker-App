SET SQL_SAFE_UPDATES = 0;
 --  delete from Expense.current_total_expense_v1 where batchid is NULL
-- Select max(batchid) from Expense.planned_estimated_cost_v1
-- Select * from Expense.planned_estimated_cost_v1 where batchid = 20201001
-- alter table Expense.current_total_expense_v1 add column batchid bigint;
-- rename table Expense.planned_estimated_cost to Expense.planned_estimated_cost_v1
-- Select * from Expense.actual_cost_v1 where batchid = max(batchid) 
-- alter table Expense.actual_cost_v1 add column updated datetime
-- alter table Expense.actual_cost_v1 add column Cumulative_Quantity bigint
-- update Expense.actual_cost_v1 set Cumulative_Quantity = 1 where batchid = 202010051305 and Commodity = 'Grocery'
update Expense.actual_cost_v1 set Total = 2000 where batchid= 202010061202 and Commodity = 'Cash Withdrawl'
-- select * from Expense.actual_cost_v1 where batchid= 202010061202
-- select * from Expense.current_total_expense_v1 where batchid = 202010061202
-- update Expense.actual_cost_v1 set Total = Cumulative_Quantity * Cost, updated = %s where batchid = 202010061202 and Commodity = %s
--  Select * from Expense.current_total_expense_v1

-- Update Expense.expense_growth_rate_v1 set ColorCode = '#008000', Cost_Quantity = 875,updated = '2020-10-06 15:19:34' where batchid = 202010061453 and Commodity = 'Miscellaneous'
-- update Expense.current_total_expense_v1 set Cash_Withdrawn = Cash_Withdrawn  + 100, updated = '2020-10-06 11:46:59' where batchid = 202010061146 
-- INSERT INTO Expense.expense_growth_rate_v1 (Commodity, ColorCode,Cost_Quantity,updated,batchid) values ('Miscellaneous', '#008000', '875', '2020-10-06 14:52:32',202010061453)

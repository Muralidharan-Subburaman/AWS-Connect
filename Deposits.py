def withdraw(account_id, amount): 
	if not account_id: 
		return "Error: invalid account ID" 
	account = db.query(account_id) 
		if not account: 
		return "Error: account not found" 
	if amount is None or amount <= 0:
		return "error invalid withdrwal"
	if account["balance"] < amount:
		return "error insufficient funds"
	account["balance"] -=amount
	db.update(account_id, account)
	
	return f"Success withdrew{amount}. Remaining balance {account['balance']}"
	
	
def deposit(account_id, amount): 
	if not account_id: 
		return "Error: invalid account ID" 
	account = db.query(account_id) 
		if not account: 
		return "Error: account not found" 
	if amount is None or amount <= 0:
		return "error invalid deposit"	
	account["balance"] +=amount
	db.update(account_id, account)
	
	return f"Success Deposited{amount}. Remaining balance {account['balance']}"
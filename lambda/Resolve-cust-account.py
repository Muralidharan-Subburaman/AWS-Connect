import os
import requests
from concurrent.futures import ThreadPoolExecutor

class APIclient():
	def __init__(self):
		self.url        =   os.environ["GRAPHQL_API_URL"]
        self.api_key    =   os.environ["GRAPHQL_API_KEY"]
        self.headers = {
        "x-api-key": self.api_key,
        "content-type": "application/json"
        }
        
    def post(self, query, variables=None):
        response = requests.post(
            self.url,
            json={'query': query, 'variables': variables},
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()['data']


def query_customer_accounts(session_id, customer_id):
    client = APIclient()

    query = """
    query GetCustomerAccounts($cid: String!) {
        accountRelations(customerId: $cid) {
            accounts {
                accountNumber
                accountType
                relationshipIndicator
            }
        }
    }
    """

    variables = {
        "cid": customer_id
    }

    return client.post(query, variables=variables)
    
    
def query_debit_cards(session_id, customer_id):
    client = APIclient()
    query = """
    query GetDebitCards($cid: String!) {
        debitCards(customerId: $cid) {
            cards {
                cardNumber
                cardStatus
                cardType
            }
        }
    }
    """
    variables = {"cid": customer_id}
    return client.post(query, variables=variables)
    
def query_customer_address(session_id, customer_id):
    client = APIclient()
    query  = """
    query GetCustomerAddress($cid: String!) {
        customerAddress(customerId: $cid) {
            street
            city
            state
            zipCode
        }
    }
    """
    variables = {"cid": customer_id}
    return client.post(query, variables=variables)


def query_customer_loans(session_id, customer_id):
    client = APIclient()
    query  = """
    query GetCustomerLoans($cid: String!) {
        loanDetails(customerId: $cid) {
            loans {
                loanNumber
                loanType
                balance
                dueDate
            }
        }
    }
    """
    variables = {"cid": customer_id}
    return client.post(query, variables=variables)
    
    
def lambda_handler(event, context):
    
    # Step 1: Get customer info from the session
    session_data = get_session_data(event)
    customer_id = session_data["customerId"]
    session_id = event["sessionId"]

    # Step 2: Call two APIs at the same time (parallel)
    with ThreadPoolExecutor(max_workers=4) as executor:
        fetch_accounts = executor.submit(query_customer_accounts, session_id, customer_id)
        fetch_cards    = executor.submit(query_debit_cards, session_id, customer_id)
        fetch_address  = executor.submit(query_customer_address,   session_id, customer_id)
        fetch_loans    = executor.submit(query_customer_loans,     session_id, customer_id)


    accounts = fetch_accounts.result()["accountRelations"]["accounts"]
    cards    = fetch_cards.result()["debitCards"]["cards"]
    address  = fetch_address.result()["customerAddress"]
    loans    = fetch_loans.result()["loanDetails"]["loans"]
    
    # Step 3: Filter only primary accounts
    primary_accounts = [
        acc for acc in accounts 
        if acc.get("relationshipIndicator") == "P"
    ]

    # Step 4: Build result and store in session
    if primary_accounts:
        result = [{"accountDetails": primary_accounts, "debitCards": cards, "address" :address,"loans": loans}]
        save_to_session(event, account_found=True, result=result)
        state = READY_FOR_FULFILLMENT
    else:
        log_error("No primary accounts found")
        state = FAILED

    # Step 5: Return response back to Lex
    return build_response(event, state)
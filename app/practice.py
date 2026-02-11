transactions = [
  {"user_id":"u1","amount":100,"type":"credit"},
  {"user_id":"u1","amount":40,"type":"debit"},
  {"user_id":"u2","amount":999,"type":"credit"},
  {"user_id":"u1","amount":-5,"type":"credit"},      # ignore
  {"user_id":"u1","type":"credit"},                  # ignore
  {"user_id":"u1","amount":"10","type":"credit"},    # ignore
  {"user_id":"u1","amount":7,"type":"refund"}        # ignore
]

def compute_balance(transactions, user_id):
    balance = 0

    for transaction in transactions:
        #amount = transaction[0]["amount"]   # ❌ wrong
        #card_type = transaction[0]["type"]  # ❌ wrong
        amount = transaction.get("amount")
        card_type = transaction.get("type")
        """Why .get()? Because if the key is missing, it returns None instead of crashing. That helps with validation."""
        # validation checks go here

        if transaction.get("user_id") != user_id:
            continue

        """
        if not isinstance(amount, int):
        That already covers:
        None
        string
        float
        anything not int
        So you do not need amount is None separately.

        """
        if not isinstance(amount, int):
            continue
        
        """
        1.If amount is None → continue
        2.If not int → continue
        3.If amount < 0 → continue
        4.If type not in ("credit", "debit") → continue
        
        """
        # if amount < 0 and amount is None: ❌ wrong if amount is None, the comparison amount < 0 will already crash.
        if amount < 0:
            continue
        # Remove the unnecessary if amount >= 0:  already filtered amount < 0 above.
        if card_type != "credit" and card_type != "debit":
            continue
        if card_type == "credit":
            balance+=amount 

        elif card_type == "debit":
            balance-=amount
    print(balance)
    return  balance


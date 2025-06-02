
from datetime import datetime

class Transaction:
    def __init__(self, amount, transaction_type, narration):
        self.amount = amount
        self.transaction_type = transaction_type 
        self.narration = narration
        self.date_time = datetime.now()


class Account:
    def __init__(self, owner, min_balance, account_number):
        self.owner = owner
        self._account_number = account_number  
        self._transactions = [] 
        self._loan = 0
        self._frozen = False
        self._min_balance = min_balance
        self._closed = False

    def deposit(self, amount, narration="Deposit"):
        if self._closed:
            return "Account is closed."
        if self._frozen:
            return "Account is frozen."
        if amount <= 0:
            return "Deposit amount must be positive."
        self._transactions.append(Transaction(amount, "deposit", narration))
        return f"You have deposited {amount}. Your new balance is {self.get_balance()}."

    def withdraw(self, amount, narration="Withdrawal"):
        if self._closed:
            return "Account is closed."
        if self._frozen:
            return "Account is frozen."
        if amount <= 0:
            return "Withdrawal amount must be positive."
        if self.get_balance() - amount < self._min_balance:
            return f"Cannot withdraw: Minimum balance of {self._min_balance} required."
        if amount > self.get_balance():
            return "Insufficient funds."
        self._transactions.append(Transaction(-amount, "withdrawal", narration))
        return f"You have withdrawn {amount}. Your new balance is {self.get_balance()}."

    def transfer_funds(self, amount, target_account, narration="Transfer Out"):
        if self._closed:
            return "Account is closed."
        if self._frozen:
            return "Account is frozen."
        if target_account._closed:
            return "Target account is closed."
        if target_account._frozen:
            return "Target account is frozen."
        if amount <= 0:
            return "Transfer amount must be positive."
        if self.get_balance() - amount < self._min_balance:
            return f"Cannot transfer: Minimum balance of {self._min_balance} required."
        if amount > self.get_balance():
            return "Insufficient funds."
        self._transactions.append(Transaction(-amount, "transfer_out", narration))
        target_account._transactions.append(Transaction(amount, "transfer_in", f"From {self.owner}"))
        return (f"Transferred {amount} to {target_account.owner}. "
                f"New balance: {self.get_balance()}.")

    def get_balance(self):
        return sum(t.amount for t in self._transactions)

    def request_loan(self, amount):
        if self._closed:
            return "Account is closed."
        if self._frozen:
            return "Account is frozen."
        if amount <= 0:
            return "Loan amount must be positive."
        self._loan += amount
        self._transactions.append(Transaction(amount, "loan_granted", "Loan granted"))
        return (f"You have been granted a loan of {amount}. "
                f"New balance is {self.get_balance()}, Loan outstanding: {self._loan}.")

    def repay_loan(self, amount):
        if self._closed:
            return "Account is closed."
        if self._frozen:
            return "Account is frozen."
        if amount <= 0:
            return "Repayment amount must be positive."
        if amount > self.get_balance():
            return "Insufficient funds to repay loan."
        if self._loan == 0:
            return "No loan to repay."
        repay_amount = min(amount, self._loan)
        self._loan -= repay_amount
        self._transactions.append(Transaction(-repay_amount, "loan_repaid", "Loan repayment"))
        return (f"You have repaid {repay_amount} of your loan. "
                f"Loan outstanding: {self._loan}, Current balance: {self.get_balance()}.")

    def view_account_details(self):
        return (f"Account owner: {self.owner}\n"
                f"Account number: {self._account_number}\n"
                f"Balance: {self.get_balance()}\n"
                f"Remaining loan: {self._loan}")

    def change_account_owner(self, new_owner):
        if self._closed:
            return "Account is closed."
        self.owner = new_owner
        return f"Account owner has been changed to {self.owner}."

    def account_statement(self):
        print(f"Statement for {self.owner}:")
        for t in self._transactions:
            print(str(t))
        print(f"Current balance is {self.get_balance()}.")

    def interest_calculation(self):
        if self._closed:
            return "Account is closed."
        if self._frozen:
            return "Account is frozen."
        interest = self.get_balance() * 0.05
        self._transactions.append(Transaction(interest, "interest", "Interest credited"))
        return f"You have received interest of {interest}. New balance is {self.get_balance()}."

    def freeze_account(self):
        if self._closed:
            return "Account is closed."
        self._frozen = True
        return "Account has been frozen."

    def unfreeze_account(self):
        if self._closed:
            return "Account is closed."
        self._frozen = False
        return "Account has been unfrozen."

    def set_minimum_balance(self, amount):
        if amount < 0:
            return "Minimum balance cannot be negative."
        self._min_balance = amount
        return f"Minimum balance has been set to {self._min_balance}."

    def close_account(self):
        self._closed = True
        self._transactions.clear()
        self._frozen = False
        self._loan = 0
        return "Account has been closed, balance set to zero, and transactions cleared."

 

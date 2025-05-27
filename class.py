class Account:
    def __init__(self, owner, min_balance):
        self.owner = owner
        self.transactions = []  
        self.balance = 0
        self.loan = 0
        self.frozen = False
        self.min_balance = min_balance
        self.closed = False
        self.deposits_list = []
        self.withdrawals_list = []

    def deposit(self, amount):
        if self.closed:
            return "Account is closed."
        if self.frozen:
            return "Account is frozen."
        if amount <= 0:
            return "Deposit amount must be positive."
        self.transactions.append(("deposit", amount))
        self.balance += amount
        return f"You have deposited {amount} your new balance is {self.balance}."
    

    def withdraw(self, amount):
        if self.closed:
            return "Account is closed."
        if self.frozen:
            return "Account is frozen."
        if amount <= 0:
            return "Withdrawal amount must be positive."
        if self.balance - amount < self.min_balance:
            return f"Cannot withdraw: Minimum balance of {self.min_balance} required."
        if amount > self.balance:
            return "Insufficient funds."
        self.transactions.append(("withdrawal", amount))
        self.balance -= amount
        return f"you have wihdrawn {amount} your new balance is {self.balance}."

    def transfer_funds(self, amount, target_account):
        if self.closed:
            return "Account is closed."
        if self.frozen:
            return "Account is frozen."
        if target_account.closed:
            return "Target account is closed."
        if target_account.frozen:
            return "Target account is frozen."
        if amount <= 0:
            return "Transfer amount must be positive."
        if self.balance - amount < self.min_balance:
            return f"you cannot transfer that amount ,Minimum balance of {self.min_balance} required."
        if amount > self.balance:
            return "Insufficient balance."
        self.transactions.append(("transfer_out", amount))
        self.balance -= amount
        target_account.transactions.append(("transfer_in", amount))
        target_account.balance += amount
        return (f"Transferred {amount} to {target_account.owner}. "
                f"New balance: {self.balance}.")

    def get_balance(self):
        return self.balance

    def request_loan(self, amount):
        if self.closed:
            return "Account is closed."
        if self.frozen:
            return "Account is frozen."
        if amount <= 0:
            return "Loan amount must be positive."
        self.loan += amount
        self.balance += amount
        self.transactions.append(("loan_granted", amount))
        return f"you have been granted a loan of {amount}, your New balance is {self.balance}, with Loan outstanding: {self.loan}."

    def repay_loan(self, amount):
        if self.closed:
            return "Account is closed."
        if self.frozen:
            return "Account is frozen."
        if amount <= 0:
            return "Repayment amount must be positive."
        if amount > self.balance:
            return "Insufficient funds to repay loan."
        if self.loan == 0:
            return "No loan to repay."
        repay_amount = min(amount, self.loan)
        self.loan -= repay_amount
        self.balance -= repay_amount
        self.transactions.append(("loan_repaid", repay_amount))
        return f"you have repaid {repay_amount} of your loan, your Loan outstanding is{self.loan}, your current Balance is {self.balance}."

    def view_account_details(self):
        return f"Account owner {self.owner}\nBalance: {self.balance}\n Remaining loan: {self.loan}"

    def change_account_owner(self, new_owner):
        if self.closed:
            return "Account is closed."
        self.owner = new_owner
        return f"Account owner has been changed to {self.owner}."

    def account_statement(self):
        print(f"Statement for {self.owner}:")
        for t_type, amount in self.transactions:
            print(f"{t_type.capitalize()}: {amount}")
        print(f"your Current balance is {self.balance}")

    def interest_calculation(self):
        if self.closed:
            return "Account is closed."
        if self.frozen:
            return "Account is frozen."
        interest = self.balance * 0.05
        self.balance += interest
        self.transactions.append(("interest", interest))
        return f "you have got an interest of {interest} your new balance is {self.balance}."

    def freeze_account(self):
        if self.closed:
            return "Account is closed."
        self.frozen = True
        return "Account has been frozen."

    def unfreeze_account(self):
        if self.closed:
            return "Account is closed."
        self.frozen = False
        return "Account has been unfrozen."

    def set_minimum_balance(self, amount):
        if amount < 0:
            return "Minimum balance cannot be negative."
        self.min_balance = amount
        return f"Minimum balance has been set to {self.min_balance}."

    def close_account(self):
        self.closed = True
        self.balance = 0
        self.loan = 0
        self.transactions.clear()
        self.frozen = False
        return "Account has been closed your balance is set to zero and your transaction is cleared."


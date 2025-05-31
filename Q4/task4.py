from custom_errors import *

class BankAccount:
    """
    BankAccount class for representing and managing simple bank accounts.

    Class Attributes:
        next_account_number (int): The next account number to assign.
        banned_accounts (dict): Dictionary of banned account numbers.
        opening_bonus (float): Default opening bonus for all accounts.

    Instance Attributes:
        owner (str): The name of the account owner.
        balance (float): The current balance of the account.
        account_number (int): The unique account number.
        banned (bool): Whether this account is banned.
        ban_reason (str): The reason this account was banned.
        transaction_limit (float | None): The maximum allowed transaction amount.
    """

    next_account_number = 1045
    banned_accounts = {} # key: account_number, value: BankAccount object
    opening_bonus = 49.99

    def __init__(self, owner: str, initial_balance: int | float):
        """
        Initialize a BankAccount instance.

        Arguments:
            owner (str): Account owner's name.
            initial_balance (int | float): Starting balance (must be non-negative).

        Raises:
            CustomTypeError: If the owner is not a string or initial_balance is not a number.
            CustomValueError: If initial_balance is negative.
        """

        # Check that the owner is a string.
        if not isinstance(owner, str):
            raise CustomTypeError("Owner name must be a string.")

        # Check that the initial balance is a number (int or float).
        if not isinstance(initial_balance, (int, float)):
            raise CustomTypeError("Initial balance must be a number.")

        # Check that the initial balance is not negative.
        if initial_balance < 0:
            raise CustomValueError("Initial balance must be non-negative.")

        self.owner = owner

        # Set the balance, including the opening bonus.
        self.balance = float(initial_balance) + self.opening_bonus
        self.account_number = BankAccount.next_account_number
        self.banned = False
        self.ban_reason = ""

        # No transaction limit by default.
        self.transaction_limit = None

        # Increment the class-level account number counter.
        # BankAccount.next_account_number += 1
        self.set_next_account_number(BankAccount.next_account_number + 1)

        # Assert that the balance is at least the opening bonus.
        assert self.balance >= self.opening_bonus, (
            f"Initialization failed: expected balance >= {self.opening_bonus}, "
            f"got {self.balance}"
        )

    @classmethod
    def set_next_account_number(cls, next_account_number: int) -> None:
        """
        Reset the account number counter (for testing or administrative purposes).

        Arguments:
            next_account_number (int): The new starting account number.

        Raises:
            CustomTypeError: If next_account_number is not an integer.
            CustomValueError: If next_account_number is negative.
            CustomValueError: If next_account_number is smaller than 1045.
        """

        # Check that next_account_number is an integer.
        if not isinstance(next_account_number, int):
            raise CustomTypeError("Account number must be an integer.")

        # Check that next_account_number is non-negative.
        if next_account_number < 0:
            raise CustomValueError("Account number must be non-negative.")
        
        # Check that next_account_number is smaller than 1045
        if next_account_number < 1045:
            raise CustomValueError("Account number must be at least 1045.")

        # Set the class-level next account number.
        cls.next_account_number = next_account_number

        # Assert that the next account number is dictionary correctly.
        assert cls.next_account_number == next_account_number, (
            f"set_next_account_number failed: expected {next_account_number}, "
            f"got {cls.next_account_number}"
        )

    @classmethod
    def unban_all(cls) -> None:
        """
        Remove all account bans by clearing the dictionary of banned account numbers.
        """
        # for banned_account in BankAccount.banned_accounts:
        #     banned_account.banned = False

        # Unban all accounts by setting banned to False using for-loop
        for account in cls.banned_accounts.values():
            account.banned = False
            account.ban_reason = ""

        # Clear the banned_accounts dictionary.
        cls.banned_accounts.clear()

        # Assert that the banned_accounts dictionary is empty.
        assert len(cls.banned_accounts) == 0, (
            f"unban_all failed: expected banned_accounts to be empty, "
            f"got {cls.banned_accounts}"
        )

    def ban_account(self, reason: str) -> None:
        """
        Ban this account and block all transactions.

        Arguments:
            reason (str): The reason for banning the account.

        Raises:
            CustomTypeError: If reason is not a string.
        """

        # Check that the reason is a string.
        if not isinstance(reason, str):
            raise CustomTypeError("Ban reason must be a string.")

        # Mark the account as banned.
        self.banned = True

        # Store the ban reason.
        self.ban_reason = reason

        # Add the account number to the dictionary of banned accounts.
        BankAccount.banned_accounts[self.account_number] = self

        # Assert that the account is marked as banned
        assert self.banned, (
            f"ban_account failed: Expected: True, Received={self.banned} "
        )

        #Assert present in banned_accounts.
        assert self.account_number in BankAccount.banned_accounts, (
            f"account should be one of the banned accounts\n"
            f"current banned_accounts={BankAccount.banned_accounts}"
        )


    def is_banned(self) -> bool:
        """
        Check if the account is banned.

        Returns:
            bool: True if the account is banned, False otherwise.
        """

        # Return the banned status.
        return self.banned

    def deposit(self, amount: float | int) -> None:
        """
        Deposit funds into the account.

        Arguments:
            amount (float | int): The amount to deposit.

        Raises:
            CustomOperationError: If the account is banned.
            CustomTypeError: If amount is not a number.
            CustomValueError: If amount is negative.
            CustomLimitError: If amount exceeds the transaction limit.
        """

        # Prevent deposit if the account is banned.
        if self.is_banned():
            raise CustomOperationError("Operation not allowed: account is banned.")

        # Ensure the deposit amount is a number.
        if not isinstance(amount, (int, float)):
            raise CustomTypeError("Deposit amount must be a number.")

        # Ensure the deposit amount is non-negative.
        if amount < 0:
            raise CustomValueError("Deposit amount must be non-negative.")

        # If a transaction limit is set, check that the amount does not exceed it.
        if self.transaction_limit is not None:
            if amount > self.transaction_limit:
                raise CustomLimitError("Deposit exceeds transaction limit.")

        # Store the previous balance for assertion.
        previous_balance = self.balance

        # Add the deposit amount to the balance.
        self.balance += amount

        # Assert that the new balance is correct after deposit.
        assert self.balance == previous_balance + amount, (
            f"Deposit balance update failed: expected {previous_balance + amount}, "
            f"got {self.balance} (previous balance: {previous_balance}, deposit amount: {amount})"
        )

    def withdraw(self, amount: float | int) -> None:
        """
        Withdraw funds from the account.

        Arguments:
            amount (float | int): The amount to withdraw.

        Raises:
            CustomOperationError: If the account is banned.
            CustomTypeError: If amount is not a number.
            CustomValueError: If amount is negative or exceeds available balance.
            CustomLimitError: If amount exceeds the transaction limit.
        """

        # Prevent withdrawal if the account is banned.
        if self.is_banned():
            raise CustomOperationError("Operation not allowed: account is banned.")

        # Ensure the withdrawal amount is a number.
        if not isinstance(amount, (int, float)):
            raise CustomTypeError("Withdrawal amount must be a number.")

        # Ensure the withdrawal amount is non-negative.
        if amount < 0:
            raise CustomValueError("Withdrawal amount must be non-negative.")

        # If a transaction limit is set, check that the amount does not exceed it.
        if self.transaction_limit is not None:
            if amount > self.transaction_limit:
                raise CustomLimitError("Withdrawal exceeds transaction limit.")

        # Ensure there are sufficient funds for withdrawal.
        if amount > self.balance:
            raise CustomValueError("Insufficient funds for withdrawal.")

        # Store the previous balance for assertion.
        previous_balance = self.balance

        # Subtract the withdrawal amount from the balance.
        self.balance -= amount

        # Assert that the new balance is correct after withdrawal.
        assert self.balance == previous_balance - amount, (
            f"Withdrawal balance update failed: expected {previous_balance - amount}, "
            f"got {self.balance} (previous balance: {previous_balance}, withdrawal amount: {amount})"
        )

        # Assert that the balance is not negative after withdrawal.
        assert self.balance >= 0, (
            f"Negative balance after withdrawal: balance is {self.balance}, expected >= 0"
        )

    def transfer_to(self, target_account: "BankAccount", amount: float | int) -> None:
        """
        Transfer funds to another account.

        Arguments:
            target_account (BankAccount): The account to transfer funds to.
            amount (float | int): The amount to transfer.

        Raises:
            CustomTypeError: If target_account is not a BankAccount or amount is not a number.
            CustomOperationError: If either account is banned.
            CustomValueError: If amount is negative or exceeds available balance.
            CustomLimitError: If amount exceeds transaction limits.
        """

        # Check that the target account is a BankAccount instance.
        if not isinstance(target_account, BankAccount):
            raise CustomTypeError("Target must be a BankAccount instance.")

        # Prevent transfer if either account is banned.
        if self.is_banned() or target_account.is_banned():
            raise CustomOperationError("Operation not allowed: banned account(s).")

        # Ensure the transfer amount is a number.
        if not isinstance(amount, (int, float)):
            raise CustomTypeError("Transfer amount must be a number.")

        # Ensure the transfer amount is non-negative.
        if amount < 0:
            raise CustomValueError("Transfer amount must be non-negative.")

        # If a transaction limit is set, check that the amount does not exceed it for the sender.
        if self.transaction_limit is not None:
            if amount > self.transaction_limit:
                raise CustomLimitError("Transfer exceeds transaction limit.")

        # If a transaction limit is set for the recipient, check that the amount does not exceed it.
        if target_account.transaction_limit is not None:
            if amount > target_account.transaction_limit:
                raise CustomLimitError("Transfer exceeds target's transaction limit.")

        # Ensure there are sufficient funds for transfer.
        if amount > self.balance:
            raise CustomValueError("Insufficient funds for transfer.")

        # Store previous balances for assertion.
        previous_self_balance = self.balance
        previous_target_balance = target_account.balance

        # Subtract the transfer amount from the sender's balance.
        self.withdraw(amount)

        # Add the transfer amount to the recipient's balance.
        target_account.deposit(amount)

        # Assert that the sender's new balance is correct.
        assert self.balance == previous_self_balance - amount, (
            f"Sender balance incorrect: expected {previous_self_balance - amount}, "
            f"got {self.balance} (previous: {previous_self_balance}, transfer: {amount})"
        )

        # Assert that the recipient's new balance is correct.
        assert target_account.balance == previous_target_balance + amount, (
            f"Recipient balance incorrect: expected {previous_target_balance + amount}, "
            f"got {target_account.balance} (previous: {previous_target_balance}, transfer: {amount})"
        )

        # Assert that the sender's balance is not negative after transfer.
        assert self.balance >= 0, (
            f"Negative sender balance after transfer: balance is {self.balance}, expected >= 0"
        )

    def set_transaction_limit(self, limit: float | int | None) -> None:
        """
        Set a maximum allowed transaction amount for this account.

        Arguments:
            limit (float | int | None): The new transaction limit, or None to remove the limit.

        Raises:
            CustomTypeError: If limit is not a number or None.
            CustomValueError: If limit is negative.
        """

        # If a limit is specified, ensure it is a number.
        if limit is not None:
            if not isinstance(limit, (int, float)):
                raise CustomTypeError("Limit must be a number or None.")

        # If a limit is specified, ensure it is non-negative.
        if limit is not None:
            if limit < 0:
                raise CustomValueError("Limit must be non-negative or None.")

        # Set the transaction limit.
        self.transaction_limit = limit

        # Assert that the transaction limit is valid (None or >= 0).
        assert self.transaction_limit is None or self.transaction_limit >= 0, (
            f"Transaction limit invalid: got {self.transaction_limit}, expected None or >= 0"
        )

    def __str__(self):
        """
        Return a formatted summary of the account, including ban reason if banned.

        Returns:
            str: Summary string for the account.
        """

        # Format the balance with two decimal places and a dollar sign.
        formatted_balance = f"${self.balance:,.2f}"

        # Format the transaction limit or show "$N/A" if not set.
        if self.transaction_limit is not None:
            formatted_limit = f"${self.transaction_limit:,.2f}"
        else:
            formatted_limit = "$N/A"

        # Determine if the account is banned.
        banned_status = "Yes" if self.is_banned() else "No"

        # Start building the summary string with basic account info.
        summary = (
            f"{self.owner}'s account ({self.account_number}): "
            f"Balance={formatted_balance} | "
            f"Limit={formatted_limit} | "
            f"Banned={banned_status}"
        )

        # If the account is banned, append the ban reason to the summary.
        if self.is_banned():
            summary += f" | Ban Reason: {self.ban_reason}"

        # Return the complete summary string.
        return summary


if __name__ == '__main__':
    # Create two accounts for demonstration.
    alice = BankAccount("Alice", 100)
    bob = BankAccount("Bob", 50)
    alice.ban_account("fraud")
    bob.ban_account("murder")
    print(f'Alice: {alice}\nBob: {bob}\n')
    BankAccount.unban_all()
    # Uncomment the following lines to test deposit, withdrawal, and transfer functionality.

    # alice.deposit(50)
    # print(f'Alice: {alice}\nBob: {bob}\n')

    # alice.withdraw(20)
    # print(f'Alice: {alice}\nBob: {bob}\n')

    # alice.transfer_to(bob, 30)
    print(f'Alice: {alice}\nBob: {bob}\n')

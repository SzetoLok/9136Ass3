import unittest
from task4 import BankAccount
from custom_errors import *

class TestBankAccount(unittest.TestCase):

    def setUp(self):
        """
        Prepare fresh state for each test: reset account numbers and bans, and create a account.
        """

        # Reset account number for reproducibility
        BankAccount.set_next_account_number(1045)

        # Remove all bans before each test
        BankAccount.unban_all()

        # Create a BankAccount object
        self.account = BankAccount("TransferFrom", 100)
        self.target_account = BankAccount("TransferTo", 200)


    def test_valid_initialisation(self):
        """
        Test that BankAccount class and instance variables are correctly initialised.
        """

        # Set up expected values
        expected_owner = "TestOwner"
        expected_initial_balance = 100
        expected_opening_bonus = 49.99
        expected_account_number = 1045

        # Reset account numbering for predictable test
        BankAccount.set_next_account_number(expected_account_number)

        # Create a BankAccount instance
        account = BankAccount(expected_owner, expected_initial_balance)

        # --- Test class variables ---

        # opening_bonus
        assert hasattr(BankAccount, 'opening_bonus'), "BankAccount class is missing class variable: opening_bonus"
        self.assertEqual(BankAccount.opening_bonus, expected_opening_bonus,
            f"BankAccount.opening_bonus incorrect: expected {expected_opening_bonus}, got {BankAccount.opening_bonus}")

        # next_account_number
        assert hasattr(BankAccount, 'next_account_number'), "BankAccount class is missing class variable: next_account_number"
        expected_next_account_number = 1046
        self.assertEqual(BankAccount.next_account_number, expected_next_account_number,
            f"BankAccount.next_account_number incorrect: expected {expected_next_account_number}, got {BankAccount.next_account_number}")

        # banned_accounts
        assert hasattr(BankAccount, 'banned_accounts'), "BankAccount class is missing class variable: banned_accounts"
        expected_banned_accounts = {}
        self.assertEqual(BankAccount.banned_accounts, expected_banned_accounts,
            f"BankAccount.banned_accounts incorrect: expected {expected_banned_accounts}, got {BankAccount.banned_accounts}")

        # --- Test instance variables ---

        # owner
        assert hasattr(account, 'owner'), "BankAccount instance is missing variable: owner"
        self.assertEqual(account.owner, expected_owner,
            f"account.owner incorrect: expected {expected_owner}, got {account.owner}")

        # balance
        assert hasattr(account, 'balance'), "BankAccount instance is missing variable: balance"
        expected_balance = expected_initial_balance + expected_opening_bonus
        self.assertAlmostEqual(account.balance, expected_balance, places=2,
            msg=f"account.balance incorrect: expected {expected_balance}, got {account.balance}")

        # account_number
        assert hasattr(account, 'account_number'), "BankAccount instance is missing variable: account_number"
        expected_account_number = 1045
        self.assertEqual(account.account_number, expected_account_number,
            f"account.account_number incorrect: expected {expected_account_number}, got {account.account_number}")

        # banned
        assert hasattr(account, 'banned'), "BankAccount instance is missing variable: banned"
        expected_banned = False
        self.assertEqual(account.banned, expected_banned,
            f"account.banned incorrect: expected {expected_banned}, got {account.banned}")

        # ban_reason
        assert hasattr(account, 'ban_reason'), "BankAccount instance is missing variable: ban_reason"
        expected_ban_reason = ""
        self.assertEqual(account.ban_reason, expected_ban_reason,
            f"account.ban_reason incorrect: expected '{expected_ban_reason}', got '{account.ban_reason}'")

        # transaction_limit
        assert hasattr(account, 'transaction_limit'), "BankAccount instance is missing variable: transaction_limit"
        expected_transaction_limit = None
        self.assertEqual(account.transaction_limit, expected_transaction_limit,
            f"account.transaction_limit incorrect: expected {expected_transaction_limit}, got {account.transaction_limit}")


    def test_invalid_initialisation(self):
        """
        test_invalid_initialisation
        Test that BankAccount raises the correct custom errors for invalid initialisation.
        """

        # Test invalid owner type (should raise CustomTypeError)
        invalid_owner = 123
        valid_balance = 100

        with self.assertRaises(CustomTypeError, 
            msg = f"Expected CustomTypeError when owner is {invalid_owner!r} (type {type(invalid_owner)}). "
                   f"Either no error or the incorrect error was raised."):
            
            BankAccount(invalid_owner, valid_balance)

        # Test invalid balance type (should raise CustomTypeError)
        valid_owner = "TestOwner"
        invalid_balance = "one hundred"
        with self.assertRaises(CustomTypeError, 
            msg=f"Expected CustomTypeError when balance is {invalid_balance!r} (type {type(invalid_balance)}). "
                f"Either no error or the incorrect error was raised."):
            
            BankAccount(valid_owner, invalid_balance)

        # Test negative balance (should raise CustomValueError)
        negative_balance = -50
        with self.assertRaises(
                                CustomValueError, 
                                msg=f"Expected CustomValueError when balance is {negative_balance}. "
                                    f"Either no error or the incorrect error was raised."
                                ):
            
            BankAccount(valid_owner, negative_balance)


    def test_set_next_account_number_valid(self):
        """
        Test that set_next_account_number correctly updates the class variable when given a valid integer.
        """

        # Set up expected value
        expected_next_account_number = 2000

        # Call the method
        BankAccount.set_next_account_number(expected_next_account_number)

        # Assert the class variable is updated
        self.assertEqual
        (
            BankAccount.next_account_number,
            expected_next_account_number,
            f"set_next_account_number did not set the class variable correctly. "
            f"Expected {expected_next_account_number}, got {BankAccount.next_account_number}"
        )


    def test_set_next_account_number_invalid_type(self):
        """
        Test that set_next_account_number raises CustomTypeError when given a non-integer value.
        """

        # Try to set next_account_number to a string
        invalid_next_account_number = "not-an-int"

        with self.assertRaises(
                                CustomTypeError,
                                msg=(
                                    f"Expected CustomTypeError when next_account_number is {invalid_next_account_number!r}"
                                    f" (type {type(invalid_next_account_number)}. "
                                    f"Either no error or the incorrect error was raised."
                                )
                            ):
            
            BankAccount.set_next_account_number(invalid_next_account_number)


    def test_set_next_account_number_negative(self):
        """
        Test that set_next_account_number raises CustomValueError when given a negative integer.
        """

        # Try to set next_account_number to a negative value
        invalid_next_account_number = -5
        with self.assertRaises(
                                CustomValueError,
                                msg=(
                                    f"Expected CustomValueError when next_account_number is negative number,"
                                    f" got {invalid_next_account_number}. "
                                    f"Either no error or the incorrect error was raised."
                                )
                            ):
            BankAccount.set_next_account_number(invalid_next_account_number)


    def test_account_number_starts_at_1045(self):
        """Test that the first account created has the minimum account number (1045)."""

        """Reset class state before each test."""
        BankAccount.set_next_account_number(1045)
        BankAccount.unban_all()

        account = BankAccount("Alice", 100)
        self.assertEqual(account.account_number, 1045,
            f"Expected first account number to be 1045, got {account.account_number}")


    def test_account_number_increments_by_one(self):
        """Test that each new account increments the account number by 1."""

        """Reset class state before each test."""
        BankAccount.set_next_account_number(1045)
        BankAccount.unban_all()

        # Create three accounts and verify sequential numbering
        acc1 = BankAccount("Alice", 100)
        acc2 = BankAccount("Bob", 200)
        acc3 = BankAccount("Charlie", 300)
        
        self.assertEqual(acc1.account_number, 1045,
            f"Account 1: Expected 1045, got {acc1.account_number}")
        self.assertEqual(acc2.account_number, 1046,
            f"Account 2: Expected 1046, got {acc2.account_number}")
        self.assertEqual(acc3.account_number, 1047,
            f"Account 3: Expected 1047, got {acc3.account_number}")


    def test_set_next_account_number_resets_sequence(self):
        """Test that set_next_account_number correctly resets the sequence."""

        """Reset class state before each test."""
        BankAccount.set_next_account_number(1045)
        BankAccount.unban_all()

        # Set next account number to 2000
        BankAccount.set_next_account_number(2000)
        acc = BankAccount("David", 400)
        self.assertEqual(acc.account_number, 2000,
            f"Expected account number 2000 after reset, got {acc.account_number}")
        
        # Verify subsequent accounts increment from 2000
        next_acc = BankAccount("Eve", 500)
        self.assertEqual(next_acc.account_number, 2001,
            f"Expected account number 2001, got {next_acc.account_number}")
        

    def test_set_next_account_number_below_minimum(self):
        """
        Test that set_next_account_number raises CustomValueError when given a value less than 1045.
        """

        """Reset class state before each test."""
        BankAccount.set_next_account_number(1045)
        BankAccount.unban_all()

        # Try to set next_account_number to 1044 (below minimum allowed)
        invalid_next_account_number = 1044
        with self.assertRaises(
            CustomValueError,
            msg=(
                f"Expected CustomValueError when next_account_number is set to {invalid_next_account_number}. "
                f"Either no error or the incorrect error was raised."
            )
        ):
            BankAccount.set_next_account_number(invalid_next_account_number)


    def test_is_banned_for_new_account(self):
        """
        Test that is_banned() returns False for newly created accounts.
        """

        # Create fresh account
        account = BankAccount("TestUser", 100)
        
        # Verify initial banned status
        self.assertFalse(account.is_banned(),
            f"Expected is_banned()=False for new account, got {account.is_banned()}")


    def test_is_banned_after_banning(self):
        """
        Test that is_banned() returns True after account is banned.
        """

        # Ban account
        self.account.ban_account("Fraud detection")
        
        # Verify banned status
        self.assertTrue(self.account.is_banned(),
            f"Expected is_banned()=True after banning, got {self.account.is_banned()}")
        

    def test_is_banned_after_unbanning(self):
        """
        Test that is_banned() returns False after account is unbanned.
        """

        # Ban account
        self.account.ban_account("Fraud detection")
        # Unbanning all the banned accounts
        BankAccount.unban_all()

        # Verify banned status
        self.assertFalse(self.account.is_banned(),
            f"Expected is_banned()=False after banning, got {self.account.is_banned()}")
        

    def test_unban_all_clears_banned_accounts_set(self):
        """
        Test that unban_all() removes all account from banned_accounts.
        """
        # Ban an account
        self.account.ban_account("Reason1")

        # Verify account is in banned set
        self.assertIn(self.account.account_number, BankAccount.banned_accounts,
            f"Account1 ({self.account.account_number}) missing from banned_accounts")

        # Perform unban operation
        BankAccount.unban_all()

        # Verify banned_accounts is empty
        self.assertEqual(len(BankAccount.banned_accounts), 0,
            f"Expected empty banned_accounts after unban_all(), got {BankAccount.banned_accounts}")


    def test_unban_all_resets_account_status(self):
        """
        Test that unban_all() sets banned=False, clears ban_reason, and removes the account from banned_accounts.
        """
        # Ban an account
        self.account.ban_account("Test ban reason")

        # Check pre-unban status
        self.assertTrue(self.account.banned, f"Expected banned=True before unban, got {self.account.banned}")
        self.assertEqual(self.account.ban_reason, "Test ban reason", f"Expected ban_reason='Test ban reason' before unban, got '{self.account.ban_reason}'")
        self.assertIn(self.account.account_number, BankAccount.banned_accounts, 
                    f"Expected account number {self.account.account_number} in banned_accounts before unban, got {BankAccount.banned_accounts}")

        # Unban all accounts
        BankAccount.unban_all()

        # Check post-unban status
        self.assertFalse(self.account.banned, f"Expected banned=False after unban_all, got {self.account.banned}")
        self.assertEqual(self.account.ban_reason, "", f"Expected ban_reason='' after unban_all, got '{self.account.ban_reason}'")
        self.assertNotIn(self.account.account_number, BankAccount.banned_accounts, 
                        f"Expected account number {self.account.account_number} not in banned_accounts after unban_all, got {BankAccount.banned_accounts}")
    

    def test_deposit_positive(self):
        """
        Test that deposit correctly adds a valid amount to the balance.
        """

        # Set up
        deposit_amount = 50
        expected_balance = self.account.balance + deposit_amount

        # Perform deposit
        self.account.deposit(deposit_amount)

        # Assert new balance
        self.assertAlmostEqual(
            self.account.balance, 
            expected_balance, 
            places=2,
            msg=f"Deposit did not add correctly. Expected {expected_balance}, got {self.account.balance}"
        )


    def test_deposit_banned_account(self):
        """
        Test that deposit raises CustomOperationError if the account is banned.
        """
        # Ban the account
        self.account.ban_account("Testing")

        # Attempt deposit and expect CustomOperationError
        with self.assertRaises(
            CustomOperationError,
            msg="Expected CustomOperationError when depositing to banned account. Either no error or the incorrect error was raised."
        ):
            self.account.deposit(10)


    def test_deposit_invalid_type(self):
        """
        Test that deposit raises CustomTypeError if the amount is not a number.
        """

        # Attempt deposit with a string
        with self.assertRaises(
            CustomTypeError,
            msg="Expected CustomTypeError when deposit amount is not a number. Either no error or the incorrect error was raised."
        ):
            self.account.deposit("fifty")


    def test_deposit_negative_amount(self):
        """
        Test that deposit raises CustomValueError if the amount is negative.
        """

        # Attempt deposit with a negative value
        with self.assertRaises(
            CustomValueError,
            msg="Expected CustomValueError when deposit amount is negative. Either no error or the incorrect error was raised."
        ):
            self.account.deposit(-10)


    def test_deposit_zero(self):
        """
        Test that depositing zero does not change the balance.
        """

        # Get initial balance
        initial_balance = self.account.balance

        # Deposit zero
        self.account.deposit(0)

        # Assert balance remains the same
        self.assertAlmostEqual(
            self.account.balance, initial_balance, places=2,
            msg=f"Deposit of zero changed balance. Expected {initial_balance}, got {self.account.balance}"
        )


    def test_deposit_exceeds_transaction_limit(self):
        """
        test_deposit_exceeds_transaction_limit
        Test that deposit raises CustomLimitError if the amount exceeds the transaction limit.
        """
        # Set a transaction limit
        self.account.set_transaction_limit(20)

        # Attempt deposit exceeding the limit
        with self.assertRaises(
            CustomLimitError,
            msg="Expected CustomLimitError when deposit amount exceeds transaction limit. Either no error or the incorrect error was raised."
        ):
            self.account.deposit(21)


    def test_withdraw_positive(self):
        """
        Test that withdraw correctly deducts a valid amount from the balance.
        """

        # Set up
        withdraw_amount = 30
        expected_balance = self.account.balance - withdraw_amount

        # Perform withdrawal
        self.account.withdraw(withdraw_amount)

        # Assert new balance
        self.assertAlmostEqual(
            self.account.balance, expected_balance, places=2,
            msg=f"Withdraw did not deduct correctly. Expected {expected_balance}, got {self.account.balance}"
        )


    def test_withdraw_banned_account(self):
        """
        Test that withdraw raises CustomOperationError if the account is banned.
        """

        # Ban the account
        self.account.ban_account("Testing")

        # Attempt withdrawal and expect CustomOperationError
        with self.assertRaises(
            CustomOperationError,
            msg="Expected CustomOperationError when withdrawing from banned account. Either no error or the incorrect error was raised."
        ):
            self.account.withdraw(10)


    def test_withdraw_invalid_type(self):
        """
        Test that withdraw raises CustomTypeError if the amount is not a number.
        """

        # Attempt withdrawal with a string
        with self.assertRaises(
            CustomTypeError,
            msg="Expected CustomTypeError when withdraw amount is not a number. Either no error or the incorrect error was raised."
        ):
            self.account.withdraw("thirty")


    def test_withdraw_negative_amount(self):
        """
        Test that withdraw raises CustomValueError if the amount is negative.
        """

        # Attempt withdrawal with a negative value
        with self.assertRaises(
            CustomValueError,
            msg="Expected CustomValueError when withdraw amount is negative. Either no error or the incorrect error was raised."
        ):
            self.account.withdraw(-10)


    def test_withdraw_zero(self):
        """
        Test that withdrawing zero does not change the balance.
        """

        # Get initial balance
        initial_balance = self.account.balance

        # Withdraw zero
        self.account.withdraw(0)

        # Assert balance remains the same
        self.assertAlmostEqual(
            self.account.balance, initial_balance, places=2,
            msg=f"Withdrawal of zero changed balance. Expected {initial_balance}, got {self.account.balance}"
        )


    def test_withdraw_exceeds_transaction_limit(self):
        """
        Test that withdraw raises CustomLimitError if the amount exceeds the transaction limit.
        """

        # Set a transaction limit
        self.account.set_transaction_limit(20)

        # Attempt withdrawal exceeding the limit
        with self.assertRaises(
            CustomLimitError,
            msg="Expected CustomLimitError when withdraw amount exceeds transaction limit. Either no error or the incorrect error was raised."
        ):
            self.account.withdraw(21)


    def test_withdraw_insufficient_funds(self):
        """
        Test that withdraw raises CustomValueError if the amount exceeds the balance.
        """

        # Attempt withdrawal more than balance
        with self.assertRaises(
            CustomValueError,
            msg=f"Expected CustomValueError when withdraw amount exceeds balance ({self.account.balance}). Either no error or the incorrect error was raised."
        ):
            self.account.withdraw(self.account.balance + 1)


    def test_transfer_to_positive(self):
        """
        Test that transfer_to correctly transfers a valid amount between accounts.
        """

        # Set up
        transfer_amount = 50
        expected_sender_balance = self.account.balance - transfer_amount
        expected_recipient_balance = self.target_account.balance + transfer_amount

        # Perform transfer
        self.account.transfer_to(self.target_account, transfer_amount)

        # Assert balances
        self.assertAlmostEqual(
            self.account.balance, expected_sender_balance, places=2,
            msg=f"Sender balance incorrect after transfer. Expected {expected_sender_balance}, got {self.account.balance}"
        )

        self.assertAlmostEqual(
            self.target_account.balance, expected_recipient_balance, places=2,
            msg=f"Recipient balance incorrect after transfer. Expected {expected_recipient_balance}, got {self.target_account.balance}"
        )


    def test_transfer_to_banned_sender(self):
        """
        Test that transfer_to raises CustomOperationError if the sender is banned.
        """

        # Ban the sender account
        self.account.ban_account("Audit")

        # Attempt transfer and expect CustomOperationError
        with self.assertRaises(
            CustomOperationError,
            msg="Expected CustomOperationError when sender is banned. Either no error or the incorrect error was raised."
        ):
            self.account.transfer_to(self.target_account, 10)


    def test_transfer_to_banned_recipient(self):
        """
        Test that transfer_to raises CustomOperationError if the recipient is banned.
        """

        # Ban the recipient account
        self.target_account.ban_account("Audit")

        # Attempt transfer and expect CustomOperationError
        with self.assertRaises(
            CustomOperationError,
            msg="Expected CustomOperationError when recipient is banned. Either no error or the incorrect error was raised."
        ):
            self.account.transfer_to(self.target_account, 10)


    def test_transfer_to_invalid_target(self):
        """
        Test that transfer_to raises CustomTypeError if the target is not a BankAccount.
        """

        # Attempt transfer to an invalid target
        with self.assertRaises(
            CustomTypeError,
            msg="Expected CustomTypeError when target is not a BankAccount. Either no error or the incorrect error was raised."
        ):
            self.account.transfer_to("not-an-account", 10)


    def test_transfer_to_invalid_amount_type(self):
        """
        Test that transfer_to raises CustomTypeError if the amount is not a number.
        """

        # Attempt transfer with a string amount
        with self.assertRaises(
            CustomTypeError,
            msg="Expected CustomTypeError when transfer amount is not a number. Either no error or the incorrect error was raised."
        ):
            self.account.transfer_to(self.target_account, "ten")


    def test_transfer_to_negative_amount(self):
        """
        Test that transfer_to raises CustomValueError if the amount is negative.
        """

        # Attempt transfer with a negative amount
        with self.assertRaises(
            CustomValueError,
            msg="Expected CustomValueError when transfer amount is negative. Either no error or the incorrect error was raised."
        ):
            self.account.transfer_to(self.target_account, -10)


    def test_transfer_zero(self):
        """
        Test that transferring zero does not change either account's balance.
        """

        # Create target account
        target_account = BankAccount("TransferTarget", 50)

        # Get initial balances
        initial_sender_balance = self.account.balance
        initial_recipient_balance = target_account.balance

        # Transfer zero
        self.account.transfer_to(target_account, 0)

        # Assert balances remain the same
        self.assertAlmostEqual(
            self.account.balance, initial_sender_balance, places=2,
            msg=f"Sender balance changed after zero transfer. Expected {initial_sender_balance}, got {self.account.balance}"
        )
        self.assertAlmostEqual(
            target_account.balance, initial_recipient_balance, places=2,
            msg=f"Recipient balance changed after zero transfer. Expected {initial_recipient_balance}, got {target_account.balance}"
        )


    def test_transfer_to_exceeds_sender_limit(self):
        """
        Test that transfer_to raises CustomLimitError if the amount exceeds the sender's transaction limit.
        """

        # Set sender's transaction limit
        self.account.set_transaction_limit(20)

        # Attempt transfer exceeding the sender's limit
        with self.assertRaises(
            CustomLimitError,
            msg="Expected CustomLimitError when transfer amount exceeds sender's transaction limit. Either no error or the incorrect error was raised."
        ):
            self.account.transfer_to(self.target_account, 21)


    def test_transfer_to_exceeds_recipient_limit(self):
        """
        Test that transfer_to raises CustomLimitError if the amount exceeds the recipient's transaction limit.
        """

        # Set recipient's transaction limit
        self.target_account.set_transaction_limit(20)

        # Attempt transfer exceeding the recipient's limit
        with self.assertRaises(
            CustomLimitError,
            msg="Expected CustomLimitError when transfer amount exceeds recipient's transaction limit. Either no error or the incorrect error was raised."
        ):
            self.account.transfer_to(self.target_account, 21)


    def test_transfer_to_insufficient_funds(self):
        """
        Test that transfer_to raises CustomValueError if the amount exceeds the sender's balance.
        """

        # Attempt transfer more than available balance
        excessive_amount = self.account.balance + 1
        with self.assertRaises(
            CustomValueError,
            msg=f"Expected CustomValueError when transfer amount exceeds sender's balance ({self.account.balance}). Either no error or the incorrect error was raised."
        ):
            self.account.transfer_to(self.target_account, excessive_amount)


    def test_set_transaction_limit_positive(self):
        """
        Test that set_transaction_limit sets a valid positive limit.
        """

        limit = 200
        self.account.set_transaction_limit(limit)
        self.assertEqual(
            self.account.transaction_limit, limit,
            f"set_transaction_limit did not set the limit correctly. Expected {limit}, got {self.account.transaction_limit}"
        )


    def test_set_transaction_limit_remove(self):
        """
        Test that set_transaction_limit removes the limit when given None.
        """

        # Set a limit first
        self.account.set_transaction_limit(100)

        # Remove the limit
        self.account.set_transaction_limit(None)

        self.assertIsNone(
            self.account.transaction_limit,
            f"set_transaction_limit did not remove the limit. Expected None, got {self.account.transaction_limit}"
        )


    def test_set_transaction_limit_zero(self):
        """
        Test that set_transaction_limit accepts zero as a valid limit.
        """

        limit = 0
        self.account.set_transaction_limit(limit)
        self.assertEqual(
            self.account.transaction_limit, limit,
            f"set_transaction_limit did not set the limit to zero. Expected {limit}, got {self.account.transaction_limit}"
        )


    def test_set_transaction_limit_invalid_type(self):
        """
        Test that set_transaction_limit raises CustomTypeError when the limit is not a number or None.
        """

        invalid_limit = "not-a-number"
        with self.assertRaises(
            CustomTypeError,
            msg=(
                f"Expected CustomTypeError when transaction limit is set to {invalid_limit!r}. "
                f"Either no error or the incorrect error was raised."
            )
        ):
            self.account.set_transaction_limit(invalid_limit)


    def test_set_transaction_limit_negative(self):
        """
        Test that set_transaction_limit raises CustomValueError when the limit is negative.
        """

        invalid_limit = -10
        with self.assertRaises(
            CustomValueError,
            msg=(
                f"Expected CustomValueError when transaction limit is set to {invalid_limit}. "
                f"Either no error or the incorrect error was raised."
            )
        ):
            self.account.set_transaction_limit(invalid_limit)


    def test_str_unbanned_no_limit(self):
        """
        Test that __str__ produces correct output for an unbanned account with no transaction limit.
        """

        # Create an account with default state
        account = BankAccount("RE", 1000)
        expected_account_number = account.account_number
        expected_balance = 1000 + BankAccount.opening_bonus
        expected_string = (
            f"RE's account ({expected_account_number}): "
            f"Balance=${expected_balance:,.2f} | Limit=$N/A | Banned=No"
        )

        # Assert __str__ output
        self.assertEqual(
            str(account), expected_string,
            f"__str__ output incorrect for unbanned account with no limit.\nExpected: {expected_string}\nGot: {str(account)}"
        )

    def test_str_unbanned_with_limit(self):
        """
        Test that __str__ produces correct output for an unbanned account with a transaction limit.
        """

        # Create account and set transaction limit
        account = BankAccount("CC", 10**7)
        account.set_transaction_limit(10)
        expected_account_number = account.account_number
        expected_balance = 10**7 + BankAccount.opening_bonus
        expected_limit = 10

        expected_string = (
            f"CC's account ({expected_account_number}): "
            f"Balance=${expected_balance:,.2f} | Limit=${expected_limit:,.2f} | Banned=No"
        )

        self.assertEqual(
            str(account), expected_string,
            f"__str__ output incorrect for unbanned account with limit.\nExpected: {expected_string}\nGot: {str(account)}"
        )

    def test_str_banned_account(self):
        """
        Test that __str__ produces correct output for a banned account, including the ban reason.
        """

        # Create account, ban it, and set a ban reason
        account = BankAccount("Gary", 70.33)
        account.ban_account("Suspicious activity")
        expected_account_number = account.account_number
        expected_balance = 70.33 + BankAccount.opening_bonus
        expected_ban_reason = "Suspicious activity"

        expected_string = (
            f"Gary's account ({expected_account_number}): "
            f"Balance=${expected_balance:,.2f} | Limit=$N/A | Banned=Yes | Ban Reason: {expected_ban_reason}"
        )

        self.assertEqual(
            str(account), expected_string,
            f"__str__ output incorrect for banned account.\nExpected: {expected_string}\nGot: {str(account)}"
        )


if __name__ == "__main__":
    unittest.main()

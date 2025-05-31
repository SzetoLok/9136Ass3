from task4 import *
def test_unban_all_resets_account_status(self):
    """
    Test that unban_all() sets banned=False, clears ban_reason, and removes the account from banned_accounts.
    """
    # Create and ban an account
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
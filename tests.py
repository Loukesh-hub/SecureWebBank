import unittest
import os

from database import init_db, get_db_connection
from auth import register_user, login_user
from banking import deposit_money, withdraw_money, get_balance


class SecureWebBankTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        init_db()

    def setUp(self):
        conn = get_db_connection()

        conn.execute("""
            DELETE FROM fraud_alerts
        """)

        conn.execute("""
            DELETE FROM transactions
        """)

        conn.execute("""
            DELETE FROM accounts
        """)

        conn.execute("""
            DELETE FROM users
        """)

        conn.commit()
        conn.close()

        register_user(
            "Test User",
            "test@example.com",
            "password123"
        )

        success, user = login_user(
            "test@example.com",
            "password123"
        )

        self.user_id = user["id"]

    def test_registration_and_login(self):
        success, user = login_user(
            "test@example.com",
            "password123"
        )

        self.assertTrue(success)
        self.assertEqual(user["name"], "Test User")

    def test_deposit(self):
        initial_balance = get_balance(self.user_id)

        success, message = deposit_money(
            self.user_id,
            1000
        )

        self.assertTrue(success)
        self.assertEqual(
            get_balance(self.user_id),
            initial_balance + 1000
        )

    def test_withdrawal(self):
        initial_balance = get_balance(self.user_id)

        success, message = withdraw_money(
            self.user_id,
            500
        )

        self.assertTrue(success)
        self.assertEqual(
            get_balance(self.user_id),
            initial_balance - 500
        )

    def test_insufficient_balance(self):
        success, message = withdraw_money(
            self.user_id,
            1000000
        )

        self.assertFalse(success)
        self.assertIn("Insufficient", message)

    def test_invalid_deposit(self):
        success, message = deposit_money(
            self.user_id,
            -100
        )

        self.assertFalse(success)


if __name__ == "__main__":
    unittest.main(verbosity=2)
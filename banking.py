from database import get_db_connection


def get_user_account(user_id):
    conn = get_db_connection()

    try:
        account = conn.execute("""
            SELECT * FROM accounts
            WHERE user_id = ?
        """, (user_id,)).fetchone()

        return account

    finally:
        conn.close()


def deposit_money(user_id, amount):
    if amount <= 0:
        return False, "Deposit amount must be greater than zero."

    conn = get_db_connection()

    try:
        cursor = conn.cursor()

        account = cursor.execute("""
            SELECT * FROM accounts
            WHERE user_id = ?
        """, (user_id,)).fetchone()

        if not account:
            return False, "Bank account not found."

        cursor.execute("""
            UPDATE accounts
            SET balance = balance + ?
            WHERE user_id = ?
        """, (amount, user_id))

        cursor.execute("""
            INSERT INTO transactions
            (account_id, transaction_type, amount, description)
            VALUES (?, 'Deposit', ?, 'Money deposited')
        """, (account["id"], amount))

        conn.commit()
        return True, "Money deposited successfully."

    except Exception:
        conn.rollback()
        return False, "Deposit failed. Please try again."

    finally:
        conn.close()


def withdraw_money(user_id, amount):
    if amount <= 0:
        return False, "Withdrawal amount must be greater than zero."

    conn = get_db_connection()

    try:
        cursor = conn.cursor()

        account = cursor.execute("""
            SELECT * FROM accounts
            WHERE user_id = ?
        """, (user_id,)).fetchone()

        if not account:
            return False, "Bank account not found."

        if account["balance"] < amount:
            return False, "Insufficient balance."

        cursor.execute("""
            UPDATE accounts
            SET balance = balance - ?
            WHERE user_id = ?
        """, (amount, user_id))

        cursor.execute("""
            INSERT INTO transactions
            (account_id, transaction_type, amount, description)
            VALUES (?, 'Withdrawal', ?, 'Money withdrawn')
        """, (account["id"], amount))

        conn.commit()
        return True, "Money withdrawn successfully."

    except Exception:
        conn.rollback()
        return False, "Withdrawal failed. Please try again."

    finally:
        conn.close()


def get_balance(user_id):
    account = get_user_account(user_id)

    if not account:
        return 0

    return account["balance"]


def get_transactions(user_id):
    conn = get_db_connection()

    try:
        transactions = conn.execute("""
            SELECT
                transactions.id,
                transactions.transaction_type,
                transactions.amount,
                transactions.description,
                transactions.status,
                transactions.created_at
            FROM transactions
            JOIN accounts
                ON transactions.account_id = accounts.id
            WHERE accounts.user_id = ?
            ORDER BY transactions.created_at DESC
        """, (user_id,)).fetchall()

        return transactions

    finally:
        conn.close()
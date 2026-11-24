
from database import get_db_connection
from werkzeug.security import generate_password_hash, check_password_hash


# Register a new user
def register_user(name, email, password):

    name = name.strip()
    email = email.strip().lower()

    if not name or not email or not password:
        return False, "All fields are required."

    if len(password) < 8:
        return False, "Password must contain at least 8 characters."

    hashed_password = generate_password_hash(password)

    conn = get_db_connection()

    try:
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO users (name, email, password)
            VALUES (?, ?, ?)
        """, (name, email, hashed_password))

        user_id = cursor.lastrowid

        # Generate a demo bank account
        account_number = f"SWB{user_id:08d}"

        cursor.execute("""
            INSERT INTO accounts
            (user_id, account_number, account_type, balance)
            VALUES (?, ?, 'Savings', 5000.00)
        """, (user_id, account_number))

        conn.commit()

        return True, "Registration successful!"

    except Exception as error:
        conn.rollback()

        if "UNIQUE constraint failed" in str(error):
            return False, "This email is already registered."

        return False, "Registration failed. Please try again."

    finally:
        conn.close()


# Authenticate an existing user
def login_user(email, password):

    email = email.strip().lower()

    conn = get_db_connection()

    try:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM users WHERE email = ?
        """, (email,))

        user = cursor.fetchone()

        if user and check_password_hash(user["password"], password):
            return True, dict(user)

        return False, "Invalid email or password."

    finally:
        conn.close()

from flask import (
    Flask, render_template, request,
    redirect, url_for, session, flash
)
from database import init_db, get_db_connection
from auth import register_user, login_user
from banking import (
    get_balance,
    deposit_money,
    withdraw_money,
    get_transactions
)

import os

app = Flask(__name__)

app.secret_key = os.environ.get("SECRET_KEY")

if not app.secret_key:
    raise RuntimeError("SECRET_KEY environment variable is missing")

# Initialize database
with app.app_context():
    init_db()


# Home page
@app.route("/")
def home():
    if "user_id" in session:
        return redirect(url_for("dashboard"))

    return redirect(url_for("login"))


# Registration
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name", "")
        email = request.form.get("email", "")
        password = request.form.get("password", "")

        success, message = register_user(
            name, email, password
        )

        if success:
            flash(message, "success")
            return redirect(url_for("login"))

        flash(message, "error")

    return render_template("register.html")


# Login
@app.route("/login", methods=["GET", "POST"])
def login():
    if "user_id" in session:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        email = request.form.get("email", "")
        password = request.form.get("password", "")

        success, result = login_user(email, password)

        if success:
            session["user_id"] = result["id"]
            session["user_name"] = result["name"]

            flash("Login successful!", "success")
            return redirect(url_for("dashboard"))

        flash(result, "error")

    return render_template("login.html")


# Dashboard
@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))

    user_id = session["user_id"]

    balance = get_balance(user_id)

    conn = get_db_connection()

    try:
        account = conn.execute("""
            SELECT * FROM accounts
            WHERE user_id = ?
        """, (user_id,)).fetchone()
    finally:
        conn.close()

    transactions = get_transactions(user_id)

    return render_template(
        "dashboard.html",
        user_name=session["user_name"],
        balance=balance,
        account=account,
        transactions=transactions[:5]
    )


# Deposit money
@app.route("/deposit", methods=["GET", "POST"])
def deposit():
    if "user_id" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        try:
            amount = float(request.form.get("amount", 0))

            success, message = deposit_money(
                session["user_id"], amount
            )

            if success:
                flash(message, "success")
                return redirect(url_for("dashboard"))

            flash(message, "error")

        except ValueError:
            flash("Please enter a valid amount.", "error")

    return render_template("deposit.html")


# Withdraw money
@app.route("/withdraw", methods=["GET", "POST"])
def withdraw():
    if "user_id" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        try:
            amount = float(request.form.get("amount", 0))

            success, message = withdraw_money(
                session["user_id"], amount
            )

            if success:
                flash(message, "success")
                return redirect(url_for("dashboard"))

            flash(message, "error")

        except ValueError:
            flash("Please enter a valid amount.", "error")

    return render_template("withdraw.html")


# Transaction history
@app.route("/transactions")
def transactions():
    if "user_id" not in session:
        return redirect(url_for("login"))

    history = get_transactions(session["user_id"])

    return render_template(
        "transactions.html",
        transactions=history
    )


# Logout
@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=False)
from flask import Blueprint, render_template, flash
from utils.api_client import APIClient
from utils.filters import format_number

dashboard = Blueprint("dashboard", __name__)
api_client = APIClient()


@dashboard.route("/")
def home():
    try:

        bank_accounts = api_client.get("/bank_accounts/")

        # Obtener datos de expenses
        expenses_response = api_client.get("/expenses/this-month")
        total_expenses = sum(
            format_number(expense.get("total_cost", 0)) for expense in expenses_response
        )

        # Obtener datos de payments
        payments_response = api_client.get("/payments/this-month")
        total_payments = sum(
            format_number(payment.get("total_amount", 0))
            for payment in payments_response
        )

        return render_template(
            "dashboard.html",
            bank_accounts=bank_accounts,
            total_expenses=total_expenses,
            total_payments=total_payments,
        )

    except Exception as e:
        flash(str(e), "error")
        return render_template("dashboard.html", bank_accounts=[])

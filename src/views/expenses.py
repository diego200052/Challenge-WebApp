from flask import Blueprint, render_template, redirect, url_for
from utils.api_client import APIClient
from datetime import datetime
from utils.mappers import ExpenseStatusMapper
from flask import request, jsonify
import uuid
from utils.filters import format_number

expenses = Blueprint("expenses", __name__)
api_client = APIClient()


@expenses.route("/expenses")
def home():
    try:
        expenses = api_client.get("/expenses/")

        # Obtener datos de expenses
        expenses_response = api_client.get("/expenses/this-month")
        total_expenses = sum(
            format_number(expense.get("total_cost", 0)) for expense in expenses_response
        )

        for expense in expenses:
            expense["expense_date"] = datetime.fromisoformat(
                expense["expense_date"]
            ).strftime("%d/%m/%Y")
            expense["due_date"] = datetime.fromisoformat(expense["due_date"]).strftime(
                "%d/%m/%Y"
            )
            expense["status_class"] = ExpenseStatusMapper.get_status_class(
                expense["status"]
            )
            expense["status"] = ExpenseStatusMapper.get_status_text(expense["status"])

            # Verificar si tiene un payment_id y obtener el estado del pago
            if expense.get("payment_id"):
                try:
                    payment = api_client.get(f"/payments/{expense['payment_id']}")
                    expense["payment_status"] = payment["status"]
                except Exception:
                    expense["payment_status"] = 2
            else:
                expense["payment_status"] = None  # No tiene pago asociado

        return render_template(
            "expenses.html", expenses=expenses, total_expenses=total_expenses
        )
    except Exception:
        return render_template("expenses.html", expenses=[], total_expenses=0)


# Ruta para mostrar el formulario y procesar el envío
@expenses.route("/expenses-create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        # try:
        # Obtener datos del formulario
        expense_date = request.form.get("expense_date")  # Puede ser None si no se llena
        description = request.form["description"]
        due_date = request.form.get("due_date")  # Puede ser None si no se llena
        total_cost = float(request.form["total_cost"])
        recipient_account = request.form.get("recipient_account")
        status = int(request.form["status"])
        provider_id = request.form.get("provider_id")
        created_by = uuid.UUID(
            "8cb4cad4-ecf2-4a42-8c61-334fe9486df0"
        )  # Convertir a UUID

        # Crear payload para la API
        payload = {
            "expense_date": expense_date,
            "description": description,
            "due_date": due_date,
            "total_cost": total_cost,
            "recipient_account": recipient_account,
            "status": status,
            "provider_id": provider_id,
            "created_by": str(created_by),
        }

        # Llamar al API usando api_client
        response = api_client.post("/expenses/", json=payload)
        return redirect(url_for("expenses.home"))

    # except:
    #    return redirect(url_for("expenses.home"))

    try:
        return render_template("expenses_create.html")
    except Exception:
        return render_template("expenses_create.html")


@expenses.route("/expenses/<expense_id>/update-status", methods=["POST"])
def update_status(expense_id):
    try:
        # Obtener el nuevo estado de la solicitud
        data = request.get_json()
        new_status = data.get("status")

        # Llamar al API para actualizar el estado del gasto
        response = api_client.post(
            f"/expenses/{expense_id}/update-status", json={"status": new_status}
        )

        if response.status_code >= 200 and response.status_code <= 300:
            return home()

    except Exception:
        return home()


@expenses.route("/expenses/<expense_id>/approve", methods=["POST"])
def approve_expense(expense_id):
    try:
        response = api_client.post(f"/expenses/{expense_id}/approve")
        if type(response) != dict:
            return {"error": "Expense could not be approved due to an error."}, 400
        return {"message": "Expense approved successfully!"}, 200
    except Exception as e:
        return {"error": str(e)}, 500


@expenses.route("/expenses/<expense_id>/cancel", methods=["POST"])
def cancel_expense(expense_id):
    try:
        response = api_client.post(f"/expenses/{expense_id}/cancel")
        if type(response) != dict:
            return {"error": "Expense could not be approved due to an error."}, 400
        return {"message": "Expense canceled successfully!"}, 200
    except Exception as e:
        return {"error": str(e)}, 500


@expenses.route("/expenses/<expense_id>/generate-payment", methods=["POST"])
def generate_payment(expense_id):
    try:
        created_by = "8cb4cad4-ecf2-4a42-8c61-334fe9486df0"
        payload = {
            "expense_ids": [expense_id],
            "created_by": created_by,
        }
        response = api_client.post("/payments/generate", json=payload)
        if type(response) != dict and type(response) != list:
            return {"error": "No se pudo generar el pago."}, 400
        return jsonify(response), 200
    except Exception as e:
        return {"error": str(e)}, 500

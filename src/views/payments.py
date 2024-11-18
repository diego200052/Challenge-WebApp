from flask import Blueprint, render_template, redirect, url_for
from utils.api_client import APIClient
from datetime import datetime
from utils.mappers import PaymentStatusMapper
from flask import request
from utils.filters import format_number

payments = Blueprint("payments", __name__)
api_client = APIClient()


@payments.route("/payments")
def home():
    try:

        payments = api_client.get("/payments/")
        bank_accounts = api_client.get("/bank_accounts/")

        # Obtener datos de payments
        payments_response = api_client.get("/payments/this-month")
        total_payments = sum(
            format_number(payment.get("total_amount", 0))
            for payment in payments_response
        )

        for payment in payments:
            payment["payment_date"] = datetime.fromisoformat(
                payment["payment_date"]
            ).strftime("%d/%m/%Y")
            payment["status_class"] = PaymentStatusMapper.get_status_class(
                payment["status"]
            )
            payment["status"] = PaymentStatusMapper.get_status_text(payment["status"])

        return render_template(
            "payments.html",
            payments=payments,
            bank_accounts=bank_accounts,
            total_payments=total_payments,
        )
    except Exception:
        return render_template("payments.html", payments=[])


@payments.route("/payments/<payment_id>/approve", methods=["POST"])
def approve_payment(payment_id):
    # try:
    response = api_client.post(f"/payments/{payment_id}/approve")
    if type(response) != dict:
        return {"error": "Expense could not be approved due to an error."}, 400
    return {"message": "Pago aprobado correctamente"}, 200


# except Exception as e:
#    return {"error": str(e)}, 500


@payments.route("/payments/<payment_id>/cancel", methods=["POST"])
def cancel_payment(payment_id):
    try:
        response = api_client.post(f"/payments/{payment_id}/cancel")
        if type(response) != dict:
            return {"error": "Expense could not be canceled due to an error."}, 400
        return {"message": "Pago cancelado correctamente"}, 200
    except Exception as e:
        return {"error": str(e)}, 500


@payments.route("/payments/<payment_id>/execute", methods=["POST"])
def execute_payment(payment_id):
    try:
        executor_id = request.json.get("executor_id", None)
        if not executor_id:
            return {"error": "Executor ID is required"}, 400

        response = api_client.post(
            f"/payments/{payment_id}/execute", data={"executor_id": executor_id}
        )
        if type(response) != dict:
            return {"error": "No se pudo ejecutar el pago"}, 400
        return {"message": "Pago ejecutado correctamente"}, 200
    except Exception as e:
        return {"error": str(e)}, 500


@payments.route("/payments/<payment_id>/pay", methods=["POST"])
def pay_payment(payment_id):
    try:
        # Obtener el ID de la cuenta bancaria desde el formulario
        bank_account_id = request.form.get("bank_account_id")
        executor_id = "8cb4cad4-ecf2-4a42-8c61-334fe9486df0"  # Cambia este valor según tus pruebas

        if not bank_account_id:
            raise Exception("Bank account is required")

        # Obtener los detalles del pago desde el API
        payment_details = api_client.get(f"/payments/{payment_id}")

        # Validar que se obtuvo el total_amount
        if "total_amount" not in payment_details:
            raise Exception("Unable to retrieve payment details")

        # Obtener el monto del pago
        total_amount = payment_details["total_amount"]

        response = api_client.post(
            f"/bank_accounts/{bank_account_id}/deduct-balance?amount={float(total_amount)}"
        )

        # Validar la respuesta del API
        if type(response) != dict:
            return {"error": response.json()}, 400

        # Marcar el pago como ejecutado llamando a su respectivo endpoint
        execute_payload = {"bank_account_id": bank_account_id}
        execute_response = api_client.post(
            f"/payments/{payment_id}/execute?executor_id={executor_id}",
            json=execute_payload,
        )

        if type(execute_response) != dict:
            return {"error": execute_response.json()}, 400

        # Redirigir a la vista principal de pagos
        return redirect(url_for("payments.home"))

    except Exception as e:
        return {"error": str(e)}, 500

# Flask application for the Expense Tracker.
# This file connects the HTML/JavaScript frontend
# to the Python expense-management functions.
from flask import Flask, render_template, request, jsonify
from datetime import datetime
#Import the Decimal library for data verification
from decimal import Decimal, InvalidOperation
#Flask Application
app = Flask(__name__)
# Main list containing all expenses
expenses = []
# Accepted payment methods
payment_methods = ["credit", "debit", "cash", "other"]
# User information
user_name = ""
# User's total budget
total_budget = 0.0
#Home Route
@app.route("/")
def home():
    #Display the main HTML application.
    return render_template("index.html")
#Validation Functions
def expenses_for_json():
    result = []

    for expense in expenses:
        expense_copy = expense.copy()

        expense_copy["cost"] = float(
            expense_copy["cost"]
        )

        result.append(expense_copy)

    return result
def validate_expense_data(data):
    #Validate and clean expense data received from the frontend.
    # Validate description
    description = data.get("description", "").strip()
    if not description:
        raise ValueError("Description cannot be empty.")
    # Validate unit cost
    unit_cost = data.get("unit_cost")
    if unit_cost is None:
        raise ValueError("Cost is required.")
    unit_cost_text = str(unit_cost).strip()

    if "e" in unit_cost_text.lower():
        raise ValueError("Scientific notation is not allowed.")
    try:
        unit_cost = Decimal(unit_cost_text)
    except (InvalidOperation, ValueError, TypeError):
        raise ValueError("Cost must be a valid number.")
    if not unit_cost.is_finite():
        raise ValueError("Cost must be a finite number.")
    if unit_cost <= 0:
        raise ValueError("Cost must be greater than 0.")
    MAX_UNIT_COST = Decimal("1000000")
    if unit_cost > MAX_UNIT_COST:
        raise ValueError("Cost is too large.")
    # Validate category and date
    category = data.get("category", "").strip()
    if not category:
        raise ValueError("Category cannot be empty.")
    date = data.get("date", "").strip()
    if not date:
        raise ValueError("Date cannot be empty.")
    # Validate payment method
    payment = data.get("payment", "").strip().lower()
    if payment not in payment_methods:
        raise ValueError("Invalid payment method. Please enter credit, debit, cash, or other.")
    # Validate quantity
    MAX_QUANTITY = 100000
    try:
        amount = int(data.get("amount"))
    except (TypeError, ValueError):
        raise ValueError("Quantity must be a whole number.")
    if amount < 1:
        raise ValueError("Quantity must be at least 1.")
    if amount > MAX_QUANTITY:
        raise ValueError("Quantity is too large.")
    # Return cleaned data
    return {
        "description": description,
        "unit_cost": unit_cost,
        "category": category,
        "amount": amount,
        "date": date,
        "payment": payment
    }
#Expense Functions
def add_expense(data):
    #Create and add a new expense.
    validated = validate_expense_data(data)
    # Generate the next expense ID
    if expenses:
        expense_id = max(
            expense["id"] for expense in expenses
        ) + 1
    else:
        expense_id = 1
    # Calculate total cost
    total_cost = (
        validated["unit_cost"]
        * validated["amount"]
    )
    # Create expense dictionary
    expense = {
        "id": expense_id,
        "description": validated["description"],
        "cost": total_cost,
        "category": validated["category"],
        "amount": validated["amount"],
        "date": validated["date"],
        "payment": validated["payment"]
    }
    # Add expense to the main list
    expenses.append(expense)
    return expense
def search_by_id(expense_id):
    #Search for one expense by ID.
    for expense in expenses:
        if expense["id"] == expense_id:
            return expense
    return None
def search_by_date(date):
    #Search for all expenses on a specific date.
    return [
        expense
        for expense in expenses
        if expense["date"] == date
    ]
def edit_expense(expense_id, data):
    #Edit an existing expense.
    validated = validate_expense_data(data)
    for index, expense in enumerate(expenses):
        if expense["id"] == expense_id:
            total_cost = (
                validated["unit_cost"]
                * validated["amount"]
            )
            updated_expense = {
                "id": expense_id,
                "description": validated["description"],
                "cost": total_cost,
                "category": validated["category"],
                "amount": validated["amount"],
                "date": validated["date"],
                "payment": validated["payment"]
            }
            expenses[index] = updated_expense
            return updated_expense
    raise ValueError("Expense not found.")
def delete_expense(expense_id):
    #Delete an expense by ID.
    for expense in expenses:
        if expense["id"] == expense_id:
            expenses.remove(expense)
            return expense
    raise ValueError("Expense not found.")
#Sorting Functions
def sort_by_date():
    #Sort expenses from earliest date to latest date.
    expenses.sort(
        key=lambda expense: expense["date"]
    )
    return expenses
def sort_by_id():
    #Sort expenses by expense ID.
    expenses.sort(
        key=lambda expense: expense["id"]
    )
    return expenses
#Budget Functions
def calculate_total_spent():
    #Calculate total money spent.
    return sum(
        expense["cost"]
        for expense in expenses
    )
def get_budget_summary():
    #Calculate and return budget information.
    total_spent = calculate_total_spent()
    remaining_budget = (
        total_budget - total_spent
    )
    return {
        "total_budget": total_budget,
        "total_spent": total_spent,
        "remaining_budget": remaining_budget,
        "over_budget": remaining_budget < 0
    }
#API ROUTES
"""
START TRACKER
"""
@app.route("/api/start", methods=["POST"])
def start_tracker():
    global user_name
    global total_budget
    try:
        data = request.get_json()
        name = data.get("name", "").strip()
        budget = data.get("budget")
        if not name:
            return jsonify({
                "error": "Please enter your name."
            }), 400
        # Make sure a budget was actually supplied
        if budget is None:
            return jsonify({
                "error": "Please enter a budget."
            }), 400
        budget_text = str(budget).strip()
        # Do not allow scientific notation
        if "e" in budget_text.lower():
            return jsonify({
                "error": "Scientific notation is not allowed."
            }), 400
        try:
            budget = Decimal(budget_text)
        except (InvalidOperation, ValueError, TypeError):
            return jsonify({
                "error": "Please enter a valid budget."
            }), 400
        # Reject NaN and Infinity
        if not budget.is_finite():
            return jsonify({
                "error": "Budget must be a finite number."
            }), 400
        # Budget must be positive
        if budget <= 0:
            return jsonify({
                "error": "Budget must be greater than 0."
            }), 400
        # Prevent absurdly large budgets
        MAX_BUDGET = Decimal("1000000000")
        if budget > MAX_BUDGET:
            return jsonify({
                "error": "Budget is too large."
            }), 400
        user_name = name
        total_budget = budget
        return jsonify({
            "message": "Tracker started successfully.",
            "name": user_name,
            "budget": float(total_budget)
        })
    except Exception as error:
        return jsonify({
            "error": str(error)
        }), 500
"""
GET ALL EXPENSES
"""
@app.route("/api/expenses", methods=["GET"])
def get_expenses():
    return jsonify(expenses_for_json())
"""
ADD EXPENSE
"""
@app.route("/api/expenses", methods=["POST"])
def create_expense():
    try:
        data = request.get_json()
        expense = add_expense(data)
        response_expense = expense.copy()
        response_expense["cost"] = float(
            response_expense["cost"]
        )
        return jsonify(response_expense), 201
    except ValueError as error:
        return jsonify({
            "error": str(error)
        }), 400
"""
GET ONE EXPENSE
"""
@app.route("/api/expenses/<int:expense_id>",methods=["GET"])
def get_one_expense(expense_id):
    expense = search_by_id(expense_id)
    if expense is None:
        return jsonify({"error": "Expense not found."}), 404
    expense_copy = expense.copy()
    expense_copy["cost"] = float(expense_copy["cost"])
    return jsonify(expense_copy)
"""
SEARCH BY DATE
"""
@app.route("/api/expenses/date/<date>",methods=["GET"])
def get_expenses_by_date(date):
    # Validate date format
    try:
        datetime.strptime(
            date,
            "%Y-%m-%d"
        )
    except ValueError:
        return jsonify({
            "error": "Invalid date. Please use YYYY-MM-DD."
        }), 400
    results = search_by_date(date)
    response_results = []

    for expense in results:
        expense_copy = expense.copy()
        expense_copy["cost"] = float(
            expense_copy["cost"]
        )
        response_results.append(expense_copy)
    return jsonify(response_results)
"""
EDIT EXPENSE
"""
@app.route("/api/expenses/<int:expense_id>",methods=["PUT"])
def update_expense(expense_id):
    try:
        data = request.get_json()
        updated_expense = edit_expense(
            expense_id,
            data
        )
        response_expense = updated_expense.copy()
        response_expense["cost"] = float(response_expense["cost"])
        return jsonify(response_expense)
    except ValueError as error:
        return jsonify({
            "error": str(error)
        }), 400
"""
DELETE EXPENSE
"""
@app.route("/api/expenses/<int:expense_id>",methods=["DELETE"])
def remove_expense(expense_id):
    try:
        deleted_expense = delete_expense(expense_id)
        deleted_expense_copy = deleted_expense.copy()
        deleted_expense_copy["cost"] = float(deleted_expense_copy["cost"])
        return jsonify({"message": "Expense deleted successfully.",
            "expense": deleted_expense_copy
        })
    except ValueError as error:
        return jsonify({
            "error": str(error)
        }), 404
"""
SORT BY DATE
"""
@app.route("/api/expenses/sort/date", methods=["GET"])
def sort_expenses_by_date():
    sort_by_date()
    return jsonify(expenses_for_json())
"""
SORT BY ID
"""
@app.route("/api/expenses/sort/id", methods=["GET"])
def sort_expenses_by_id():
    sort_by_id()
    return jsonify(expenses_for_json())
"""
GET BUDGET SUMMARY
"""
@app.route("/api/budget",methods=["GET"])
def budget_summary():
    summary = get_budget_summary()
    return jsonify({"total_budget": float(summary["total_budget"]),
        "total_spent": float(summary["total_spent"]),
        "remaining_budget": float(summary["remaining_budget"]),
        "over_budget": summary["over_budget"]
    })
#Run Flask Application
if __name__ == "__main__":
    app.run(debug=True)
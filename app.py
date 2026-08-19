# Flask application for the Expense Tracker.
# This file connects the HTML/JavaScript frontend
# to the Python expense-management functions.
from flask import Flask, render_template, request, jsonify
from datetime import datetime
#Flask Application
app = Flask(__name__)
#Global Data
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
def validate_expense_data(data):
    #Validate and clean expense data received from the frontend.
    # Validate description
    description = data.get("description", "").strip()
    if not description:
        raise ValueError("Description cannot be empty.")
    # Validate unit cost
    unit_cost = data.get("unit_cost")
    try:
        unit_cost = float(unit_cost)
    except (TypeError, ValueError):
        raise ValueError("Cost must be a valid number.")
    if unit_cost <= 0:
        raise ValueError("Cost must be greater than 0.")
    # Validate category
    category = data.get("category", "").strip()
    if not category:
        raise ValueError("Category cannot be empty.")
    # Validate date
    date = data.get("date", "").strip()
    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        raise ValueError(
            "Invalid date. Please use YYYY-MM-DD."
        )
    # Validate payment method
    payment = data.get("payment", "").strip().lower()
    if payment not in payment_methods:
        raise ValueError(
            "Invalid payment method. "
            "Please enter credit, debit, cash, or other."
        )
    # Validate quantity
    try:
        amount = int(data.get("amount"))
    except (TypeError, ValueError):
        raise ValueError(
            "Quantity must be a whole number."
        )
    if amount < 1:
        raise ValueError(
            "Quantity must be at least 1."
        )
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
        try:
            budget = float(budget)
        except (TypeError, ValueError):
            return jsonify({
                "error": "Please enter a valid budget."
            }), 400
        if budget < 0:
            return jsonify({
                "error": "Budget cannot be negative."
            }), 400
        user_name = name
        total_budget = budget
        return jsonify({
            "message": "Tracker started successfully.",
            "name": user_name,
            "budget": total_budget
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
    return jsonify(expenses)
"""
ADD EXPENSE
"""
@app.route("/api/expenses", methods=["POST"])
def create_expense():
    try:
        data = request.get_json()
        expense = add_expense(data)
        return jsonify(expense), 201
    except ValueError as error:
        return jsonify({
            "error": str(error)
        }), 400
"""
GET ONE EXPENSE
"""
@app.route(
    "/api/expenses/<int:expense_id>",
    methods=["GET"]
)
def get_one_expense(expense_id):
    expense = search_by_id(expense_id)
    if expense is None:
        return jsonify({
            "error": "Expense not found."
        }), 404
    return jsonify(expense)
"""
SEARCH BY DATE
"""
@app.route(
    "/api/expenses/date/<date>",
    methods=["GET"]
)
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
    return jsonify(results)
"""
EDIT EXPENSE
"""
@app.route(
    "/api/expenses/<int:expense_id>",
    methods=["PUT"]
)
def update_expense(expense_id):
    try:
        data = request.get_json()
        updated_expense = edit_expense(
            expense_id,
            data
        )
        return jsonify(updated_expense)
    except ValueError as error:
        return jsonify({
            "error": str(error)
        }), 400
"""
DELETE EXPENSE
"""
@app.route(
    "/api/expenses/<int:expense_id>",
    methods=["DELETE"]
)
def remove_expense(expense_id):
    try:
        deleted_expense = delete_expense(
            expense_id
        )
        return jsonify({
            "message": "Expense deleted successfully.",
            "expense": deleted_expense
        })
    except ValueError as error:
        return jsonify({
            "error": str(error)
        }), 404
"""
SORT BY DATE
"""
@app.route(
    "/api/expenses/sort/date",
    methods=["GET"]
)
def sort_expenses_by_date():
    sorted_expenses = sort_by_date()
    return jsonify(sorted_expenses)
"""
SORT BY ID
"""
@app.route(
    "/api/expenses/sort/id",
    methods=["GET"]
)
def sort_expenses_by_id():
    sorted_expenses = sort_by_id()
    return jsonify(sorted_expenses)
"""
GET BUDGET SUMMARY
"""
@app.route(
    "/api/budget",
    methods=["GET"]
)
def budget_summary():
    return jsonify(
        get_budget_summary()
    )
#Run Flask Application
if __name__ == "__main__":
    app.run(debug=True)
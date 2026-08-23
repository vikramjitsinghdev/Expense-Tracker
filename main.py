# Using Flask to create a web application for the Expense Tracker
# and connect the HTML frontend to the Python backend.
# Importing Flask modules
from flask import Flask, render_template
# Importing datetime module to validate date input
from datetime import datetime
#Import the Decimal library for data verification
from decimal import Decimal, InvalidOperation
"""
Flask Application
"""
# Creates the Flask application
app = Flask(__name__)
# Routes the home page to the index.html file
@app.route("/")
def home():
    # Renders and returns the index.html file
    return render_template("index.html")
"""
Variable Declaration Section
"""
# Creation of the main list of expenses
expenses = []
# List of accepted payment methods
payment_methods = ["credit", "debit", "cash", "other"]
"""
Validation Functions
"""
# Validates all information provided for an expense
def validate_expense_data(data):
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
        raise ValueError(
            "Scientific notation is not allowed."
        )
    try:
        unit_cost = Decimal(unit_cost_text)
    except (InvalidOperation, ValueError, TypeError):
        raise ValueError(
            "Cost must be a valid number."
        )

    if not unit_cost.is_finite():
        raise ValueError(
            "Cost must be a finite number."
        )

    if unit_cost <= 0:
        raise ValueError(
            "Cost must be greater than 0."
        )

    MAX_UNIT_COST = Decimal("1000000")

    if unit_cost > MAX_UNIT_COST:
        raise ValueError(
            "Cost is too large."
        )
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
    MAX_QUANTITY = 100000
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

    if amount > MAX_QUANTITY:
        raise ValueError(
            "Quantity is too large."
        )
    # Return the cleaned and validated information
    return {
        "description": description,
        "unit_cost": unit_cost,
        "category": category,
        "amount": amount,
        "date": date,
        "payment": payment
    }
"""
Sorting Functions
"""
# Sort expenses by Expense ID/Number
def sort_by_id(expenses):
    expenses.sort(
        key=lambda expense: expense["id"]
    )
# Sort expenses by date
def sort_by_date(expenses):
    expenses.sort(
        key=lambda expense: expense["date"]
    )
"""
Search Functions
"""
# Search for an expense by Expense ID/Number
def search_by_id(expenses, expense_id):
    for expense in expenses:
        if expense["id"] == expense_id:
            return expense
    return None
# Search for expenses by date
def search_by_date(expenses, date):
    return [
        expense
        for expense in expenses
        if expense["date"] == date
    ]
"""
Expense Management Functions
"""
# Add a new expense
def add_expense(expenses, expense_id, data):
    # Validate the provided expense data
    validated = validate_expense_data(data)
    # Calculate total cost
    total_cost = (
        validated["unit_cost"]
        * validated["amount"]
    )
    # Create the expense dictionary
    expense = {
        "id": expense_id,
        "description": validated["description"],
        "cost": total_cost,
        "category": validated["category"],
        "amount": validated["amount"],
        "date": validated["date"],
        "payment": validated["payment"]
    }
    # Add the expense to the main expenses list
    expenses.append(expense)
    # Return the newly created expense
    return expense
# Delete an expense by ID/Number
def delete_expense(expenses, expense_id):
    for expense in expenses:
        if expense["id"] == expense_id:
            # Store the deleted expense
            deleted_expense = expense
            # Remove it from the list
            expenses.remove(expense)
            return deleted_expense

    raise ValueError("Expense not found.")
# Edit an existing expense by ID/Number
def edit_expense(expenses, expense_id, data):
    # Validate the new expense data
    validated = validate_expense_data(data)
    # Search for the expense
    for index, expense in enumerate(expenses):
        if expense["id"] == expense_id:
            # Calculate the new total cost
            total_cost = (
                validated["unit_cost"]
                * validated["amount"]
            )
            # Create the updated expense
            updated_expense = {
                "id": expense_id,
                "description": validated["description"],
                "cost": total_cost,
                "category": validated["category"],
                "amount": validated["amount"],
                "date": validated["date"],
                "payment": validated["payment"]
            }
            # Replace the old expense
            expenses[index] = updated_expense

            # Return both old and new information
            return updated_expense, expense["cost"]

    raise ValueError("Expense not found.")
"""
Calculation Functions
"""
# Calculate the total amount spent
def calculate_total_spent(expenses):
    return sum(
        expense["cost"]
        for expense in expenses
    )
# Calculate the budget information
def get_budget_summary(total_budget, expenses):
    total_spent = calculate_total_spent(expenses)
    remaining_budget = (
        total_budget - total_spent
    )
    return {
        "total_budget": total_budget,
        "total_spent": total_spent,
        "remaining_budget": remaining_budget,
        "over_budget": remaining_budget < 0
    }
"""
Display Function
"""
# Display all expenses in a formatted manner
# This is useful for testing the Python backend.
def display_expenses(expenses):
    if not expenses:
        print("There are no expenses to display.")
        return
    print("\nAll Expenses:")
    for expense in expenses:
        print(
            f"Expense {expense['id']}: "
            f"{expense['description']} - "
            f"${expense['cost']:.2f} in "
            f"{expense['category']} on "
            f"{expense['date']} via "
            f"{expense['payment']}\n"
        )
"""
Run Flask Application
"""
# Runs the Flask development server when this file
# is executed directly.
if __name__ == "__main__":
    app.run(debug=True)
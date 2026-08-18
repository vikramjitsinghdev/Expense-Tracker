# import datetime module to validate date input
from datetime import datetime
"""
Variable Declaration section
"""
# Creation of list of expenses
expenses = []
# Setting total spent to 0
total_spent = 0
# Accepting only valid payment methods
payment_methods = ["credit", "debit", "cash", "other"]
"""
Function Declaration Section
"""
# Sorting function to sort expenses by Expense ID/Number
def sort_by_id(expenses):
    expenses.sort(key=lambda expense: expense["id"])
# Sorting function to sort expenses by date
def sort_by_date(expenses):
    expenses.sort(key=lambda expense: expense["date"])
# Function to normalize expense IDs after deletion to ensure they remain sequential
def normalize_expense_ids(expenses):
    for index, expense in enumerate(expenses, start=1):
        expense["id"] = index
# Search function to search for expenses by Expense ID/Number
def search_by_id(expenses):
    while True:
        try:
            expense_id = int(input("Enter the expense number to search for: ").strip())
            break
        except ValueError:
            print("Please enter a valid expense number.")
    for expense in expenses:
        if expense["id"] == expense_id:
            print("\nExpense found:")
            print(f"Expense #{expense['id']}")
            print(f"Description: {expense['description']}")
            print(f"Cost: ${expense['cost']:.2f}")
            print(f"Category: {expense['category']}")
            print(f"Quantity: {expense['amount']}")
            print(f"Date: {expense['date']}")
            print(f"Payment: {expense['payment']}")
            return
    print("Expense not found.")
# Search function to search for expenses by date
def search_by_date(expenses):
    while True:
        date = input("Enter the date to search for (YYYY-MM-DD): ").strip()
        try:
            datetime.strptime(date, "%Y-%m-%d")
            break
        except ValueError:
            print("Invalid date. Please use YYYY-MM-DD.")
    found = False
    for expense in expenses:
        if expense["date"] == date:
            print("\nExpense found:")
            print(f"Expense #{expense['id']}")
            print(f"Description: {expense['description']}")
            print(f"Cost: ${expense['cost']:.2f}")
            print(f"Category: {expense['category']}")
            print(f"Quantity: {expense['amount']}")
            print(f"Date: {expense['date']}")
            print(f"Payment: {expense['payment']}")
            found = True
    if not found:
        print("No expenses found for that date.")
# Function to collect and validate expense details
def get_expense_details():
    # Validate expense description
    while True:
        description = input("What did you buy? ").strip()
        if description:
            break
        print("Description cannot be empty.")
    # Validate unit cost
    while True:
        try:
            unit_cost = float(input("How much did it cost per item? "))
            if unit_cost > 0:
                break
            print("Cost must be greater than 0.")
        except ValueError:
            print("Please enter a valid number.")
    # Validate category
    while True:
        category = input("What category? ").strip()
        if category:
            break
        print("Category cannot be empty.")
    # Validate date
    while True:
        date = input("What date? (YYYY-MM-DD) ").strip()
        try:
            datetime.strptime(date, "%Y-%m-%d")
            break
        except ValueError:
            print("Invalid date. Please use YYYY-MM-DD.")
    # Validate payment method
    while True:
        payment = input("How did you pay? ").strip().lower()
        if payment in payment_methods:
            break
        print("Invalid payment method." "Please enter credit, debit, cash, or other.")
    # Validate quantity
    while True:
        try:
            amount = int(input("How many items did you buy? ").strip())
            if amount >= 1:
                break
            print("Please enter an amount of at least 1.")
        except ValueError:
            print("Please enter a whole number.")
    # Calculate total cost
    total_cost = unit_cost * amount
    return (
        description,
        total_cost,
        category,
        amount,
        date,
        payment
    )
# Function to add a new expense
def add_expense(expenses, expense_id):
    print(f"\nExpense {expense_id}:")
    (
        description,
        total_cost,
        category,
        amount,
        date,
        payment
    ) = get_expense_details()
    expense = {
        "id": expense_id,
        "description": description,
        "cost": total_cost,
        "category": category,
        "amount": amount,
        "date": date,
        "payment": payment
    }
    expenses.append(expense)
    print(f"\nExpense recorded: {description} - "f"${total_cost:.2f} in {category} "f"on {date} via {payment}")
    return total_cost
# Function to delete an expense by ID/Number
def delete_expense(expenses):
    while True:
        try:
            expense_id = int(input("Enter the expense number to delete: ").strip())
            break
        except ValueError:
            print("Please enter a valid expense number.")
    for expense in expenses:
        if expense["id"] == expense_id:
            deleted_cost = expense["cost"]
            expenses.remove(expense)
            # Renumber remaining expenses
            normalize_expense_ids(expenses)
            print(f"Expense {expense_id} deleted successfully.")
            # Return deleted cost so total_spent can be updated
            return deleted_cost
    print("Expense not found.")
    return 0
# Function to edit an expense by ID/Number
def edit_expense(expenses):
    while True:
        try:
            expense_id = int(input("Enter the expense number to edit: ").strip())
            break
        except ValueError:
            print("Please enter a valid expense number.")
    for index, expense in enumerate(expenses):
        if expense["id"] == expense_id:
            print(f"\nEditing Expense {expense_id}")
            print("Enter the new information below.")
            # Store the old cost before replacing the expense
            old_cost = expense["cost"]
            (   description,
                total_cost,
                category,
                amount,
                date,
                payment
            ) = get_expense_details()
            # Create the replacement expense
            new_expense = {
                "id": expense_id,
                "description": description,
                "cost": total_cost,
                "category": category,
                "amount": amount,
                "date": date,
                "payment": payment
            }
            # Replace the old expense
            expenses[index] = new_expense
            print(f"Expense {expense_id} updated successfully.")
            # Return the difference in cost
            return total_cost - old_cost
    print("Expense not found.")
    return 0
# Function to print all expenses in a formatted manner
def display_expenses(expenses):
    if not expenses:
        print("There are no expenses to display.")
        return
    print("\nAll Expenses:")
    for expense in expenses:
        print(f"Expense {expense['id']}: "f"{expense['description']} - "f"${expense['cost']:.2f} in "f"{expense['category']} on "f"{expense['date']} via "f"{expense['payment']}\n")
# Function to display the current budget information
def display_budget(total_budget, total_spent):
    remaining_budget = total_budget - total_spent
    print(f"\nTotal spent: ${total_spent:.2f}")
    print(f"Remaining budget: ${remaining_budget:.2f}")
    if remaining_budget < 0:
        print(f"WARNING: You are "f"${abs(remaining_budget):.2f} over budget!")
"""
Main Program Section
"""
# Inputting user name and greeting
name = input("Enter your name: ")
print("Hello", name)
# User input for total budget with validation
while True:
    try:
        total_budget = float(
            input("Enter your total budget: ")
        )
        if total_budget >= 0:
            break
        print("Budget cannot be negative.")
    except ValueError:
        print("Please enter a valid number.")
# User input for number of initial expenses with validation
while True:
    try:
        number_of_expenses = int(input("How many expenses do you want to enter? "))
        if number_of_expenses >= 1:
            break
        print("Please enter at least one expense.")
    except ValueError:
        print("Please enter a whole number.")
# Loop to collect every initial expense
for i in range(1, number_of_expenses + 1):
    total_cost = add_expense(expenses, i)
    total_spent += total_cost
    display_budget(total_budget, total_spent)
while True:
    print("EXPENSE TRACKER")
    print("1. Add expense")
    print("2. View expenses")
    print("3. Search by expense number")
    print("4. Search by date")
    print("5. Sort by expense number")
    print("6. Sort by date")
    print("7. Edit expense")
    print("8. Delete expense")
    print("9. View budget")
    print("10. Exit")
    choice = input("Choose an option: ").strip()
    # Add a new expense
    if choice == "1":
        # Restore natural ID order before adding
        sort_by_id(expenses)
        new_id = len(expenses) + 1
        total_cost = add_expense(
            expenses,
            new_id
        )
        total_spent += total_cost
        display_budget(
            total_budget,
            total_spent
        )
    # Display all expenses
    elif choice == "2":
        display_expenses(expenses)
    # Search by expense number
    elif choice == "3":
        search_by_id(expenses)
    # Search by date
    elif choice == "4":
        search_by_date(expenses)
    # Sort expenses by ID
    elif choice == "5":
        sort_by_id(expenses)
        print("\nExpenses sorted by expense number.")
        display_expenses(expenses)
    # Sort expenses by date
    elif choice == "6":
        sort_by_date(expenses)
        print("\nExpenses sorted by date.")
        display_expenses(expenses)
    # Edit an expense
    elif choice == "7":
        # Restore natural ID order before editing
        sort_by_id(expenses)
        cost_difference = edit_expense(expenses)
        # Update total spent using the difference
        total_spent += cost_difference
        display_budget(
            total_budget,
            total_spent
        )
    # Delete an expense
    elif choice == "8":
        # Restore natural ID order before deleting
        sort_by_id(expenses)
        deleted_cost = delete_expense(expenses)
        # Update total spent
        total_spent -= deleted_cost
        display_budget(
            total_budget,
            total_spent
        )
    # Display budget information
    elif choice == "9":
        display_budget(
            total_budget,
            total_spent
        )
    # Exit program
    elif choice == "10":
        print("\nThank you for using the Expense Tracker!")
        break
    # Invalid menu choice
    else:
        print("Invalid option. Please choose a number from 1 to 10.")
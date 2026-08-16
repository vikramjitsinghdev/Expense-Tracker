#import datetime module to validate date input
from datetime import datetime
"""
Variable Declaration section
"""
#Creation of list of expenses
expenses = []
#setting total spent to 0
total_spent = 0
#Accepting only valid payment methods
payment_methods = ["credit", "debit", "cash", "other"]
"""
Function Declaration Section
"""
#sorting function to sort expenses by date
def sort_by_date(expenses):
    expenses.sort(key=lambda expense: expense["date"])
#search function to search for an expense by expense number
def search_by_id(expenses):
    while True:
        try:
            expense_id = int(input("Enter the expense number you want to search for: "))
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
#search function to search for expenses by date
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
"""
Main Program Section
"""
#inputting user name and greeting
name = input("Enter your name: ")
print("Hello", name)
#User input for total budget and number of expenses with validation
while True:
    try:
        total_budget = float(input("Enter your total budget: "))
        if total_budget >= 0:
            break
        print("Budget cannot be negative.")
    except ValueError:
        print("Please enter a valid number.")
#user input for number of expenses with validation
while True:
    try:
        number_of_expenses = int(input("How many expenses do you want to enter? "))
        if number_of_expenses >= 1:
            break
        print("Please enter at least one expense.")
    except ValueError:
        print("Please enter a whole number.")
#Loop to collect every expense details from the user
for i in range(1, number_of_expenses + 1):
    print(f"Expense {i}:")
    #Input validation for each expense description, unit cost,
    #category, date, payment method, and amount
    while True:
        description = input("What did you buy? ").strip()
        if description:
            break
        print("Description cannot be empty.")
    while True:
        try:
            unit_cost = float(input("How much did it cost per item? "))
            if unit_cost > 0:
                break
            print("Cost must be greater than 0.")
        except ValueError:
            print("Please enter a valid number.")
    while True:
        category = input("What category? ").strip()
        if category:
            break
        print("Category cannot be empty.")
    while True:
        date = input("What date? (YYYY-MM-DD) ").strip()
        try:
            datetime.strptime(date, "%Y-%m-%d")
            break
        except ValueError:
            print("Invalid date. Please use YYYY-MM-DD.")
    while True:
        payment = input("How did you pay? ").strip().lower()
        if payment in payment_methods:
            break
        else:
            print(
                "Invalid payment method. "
                "Please enter credit, debit, cash, or other."
            )
    while True:
        try:
            amount = int(input("How many items did you buy? "))
            if amount >= 1:
                break
            print("Please enter an amount of at least 1.")
        except ValueError:
            print("Please enter a whole number.")
    # Calculating total cost and updating total spent
    total_cost = unit_cost * amount
    total_spent += total_cost
    # printing expense details and remaining budget
    print(
        f"Expense recorded: {description} - "
        f"${total_cost:.2f} in {category} "
        f"on {date} via {payment}"
    )
    remaining_budget = total_budget - total_spent
    # validation to check if the user is over budget
    if remaining_budget < 0:
        print(
            f"WARNING: You are "
            f"${abs(remaining_budget):.2f} over budget!"
        )
    # outputting total spent and remaining budget
    print(f"Total spent: ${total_spent:.2f}")
    print(f"Remaining budget: ${remaining_budget:.2f}")
    # new dictionary to store each expense details instead of a list
    expense = {
        "id": i,
        "description": description,
        "cost": total_cost,
        "category": category,
        "amount": amount,
        "date": date,
        "payment": payment
    }
    expenses.append(expense)
# asking user if they want to print all expenses
print_expenses = input(
    "Do you want to print all expenses? (yes/no) "
).strip().lower()
if print_expenses == "yes":
    print("\nAll Expenses:")
    for exp in expenses:
        print(
            f"Expense {exp['id']}: "
            f"{exp['description']} - "
            f"${exp['cost']:.2f} in "
            f"{exp['category']} on "
            f"{exp['date']} via "
            f"{exp['payment']}\n"
        )
# asking user if they want to sort expenses by date
sort_expenses = input(
    "Do you want to sort expenses by date? (yes/no) "
).strip().lower()
if sort_expenses == "yes":
    sort_by_date(expenses)
# printing expenses again after sorting
print_expenses = input(
    "Do you want to print all expenses? (yes/no) "
).strip().lower()
if print_expenses == "yes":
    print("\nAll Expenses:")
    for exp in expenses:
        print(
            f"Expense {exp['id']}: "
            f"{exp['description']} - "
            f"${exp['cost']:.2f} in "
            f"{exp['category']} on "
            f"{exp['date']} via "
            f"{exp['payment']}\n"
        )
# asking user whether they want to search
search_expenses = input(
    "Do you want to search for an expense? (yes/no) "
).strip().lower()
if search_expenses == "yes":
    print("\nSearch Options:")
    print("1. Search by expense number")
    print("2. Search by date")
    while True:
        search_choice = input("Choose a search option (1/2): ").strip()
        if search_choice == "1":
            search_by_id(expenses)
            break
        elif search_choice == "2":
            search_by_date(expenses)
            break
        else:
            print("Please enter 1 or 2.")
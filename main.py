#import datetime module to validate date input
from datetime import datetime
#inputtting user name and greeting
name = input("Enter your name: ")
print("Hello", name)
#Creation of list of expenses
expenses = []
#setting total spent to 0
total_spent = 0
#Accepting only valid payment methods
payment_methods = ["credit", "debit", "cash", "other"]
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
    expense = []
    print(f"Expense {i}:")
    #Input validation for each expense description, unit cost, category, date, payment method, and amount
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
        date = input("What date? (YYYY-MM-DD) ")

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
            print("Invalid payment method. Please enter credit, debit, cash, or other.")
    while True:
        try:
            amount = int(input("How many items did you buy? "))
            if amount >= 1:
                break
            print("Please enter an amount of at least 1.")
        except ValueError:
            print("Please enter a whole number.")
    #Calculating total cost and updating total spent
    total_cost = unit_cost * amount
    total_spent += total_cost
    #printing expense details and remaining budget
    print(f"Expense recorded: {description} - ${total_cost:.2f} in {category} on {date} via {payment}")
    remaining_budget = total_budget - total_spent
    #validation to check if the user is over budget
    if remaining_budget < 0:
        print(f"WARNING: You are ${abs(remaining_budget):.2f} over budget!")
    #outputting total spent and remaining budget
    print(f"Total spent: ${total_spent:.2f}")
    print(f"Remaining budget: ${remaining_budget:.2f}")
    #adding expense details to the expenses list
    expense.append(i)
    expense.append(description)
    expense.append(total_cost)
    expense.append(category)
    expense.append(amount)
    expense.append(date)
    expense.append(payment)
    expenses.append(expense)
#asking user if they want to print all expenses and printing them if they do
print_expenses = input("Do you want to print all expenses? (yes/no) ").lower()
if print_expenses == "yes":
    print("\nAll Expenses:")
    for exp in expenses:
        print(f"Expense {exp[0]}: {exp[1]} - ${exp[2]} in {exp[3]} on {exp[5]} via {exp[6]}\n")
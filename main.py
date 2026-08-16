from datetime import datetime
name = input("Enter your name: ")
print("Hello", name)
expenses = []
total_spent = 0
payment_methods = ["credit", "debit", "cash", "other"]
total_budget = float(input("Enter your total budget: "))
number_of_expenses = int(input("How many expenses do you want to enter? "))
for i in range(1, number_of_expenses + 1):
    expense = []
    print(f"Expense {i}:")
    description = input("What did you buy? ")
    while True:
        try:
            cost = float(input("How much did it cost? "))
            if cost >= 0:
                break
            print("Cost cannot be negative.")
        except ValueError:
            print("Please enter a valid number.")
    category = input("What category? ")
    amount = int(input("How many items did you buy? "))
    while True:
        date = input("What date? (YYYY-MM-DD) ")

        try:
            datetime.strptime(date, "%Y-%m-%d")
            break
        except ValueError:
            print("Invalid date. Please use YYYY-MM-DD.")
    while True:
        payment = input("How did you pay? ").lower()

        if payment in payment_methods:
            break
        else:
            print("Invalid payment method. Please enter credit, debit, cash, or other.")
    while amount < 1:
        print("Please enter an amount of at least 1.")
        amount = int(input("How many items did you buy? "))
    cost *= amount
    total_spent += cost
    print(f"Expense recorded: {description} - ${cost} in {category} on {date} via {payment}")
    remaining_budget = total_budget - total_spent
    print(f"Total spent: ${total_spent}")
    print(f"Remaining budget: ${remaining_budget}\n")
    expense.append(i)
    expense.append(description)
    expense.append(cost)
    expense.append(category)
    expense.append(amount)
    expense.append(date)
    expense.append(payment)
    expenses.append(expense)
    print_expenses = input("Do you want to print all expenses? (yes/no) ").lower()
    if print_expenses == "yes":
        print("\nAll Expenses:")
        for exp in expenses:
            print(f"Expense {exp[0]}: {exp[1]} - ${exp[2]} in {exp[3]} on {exp[5]} via {exp[6]}\n")
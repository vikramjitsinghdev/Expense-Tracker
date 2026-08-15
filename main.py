name = input("Enter your name: ")
print("Hello", name)
total_spent = 0
total_budget = float(input("Enter your total budget: "))
number_of_expenses = int(input("How many expenses do you want to enter? "))
for i in range(1, number_of_expenses + 1):
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
    date = input("What date? (YYYY-MM-DD) ")
    payment = input("How did you pay? ")
    while amount < 1:
        print("Please enter an amount of at least 1.")
        amount = int(input("How many items did you buy? "))
    cost *= amount
    total_spent += cost
    print(f"Expense recorded: {description} - ${cost} in {category} on {date} via {payment}")
    remaining_budget = total_budget - total_spent
    print(f"Total spent: ${total_spent}")
    print(f"Remaining budget: ${remaining_budget}\n")
# Student Expense Analyzer
#
# Advanced topics used:
# 1. File Input/Output
#    The program saves and loads expense records from expenses.txt.
#
# 2. Recursion
#    The program uses recursion to calculate the total spending.
#
# Other topics used:
# Classes and Objects, functions, loops, conditionals, lists,
# dictionaries, string processing, and input validation.


class Expense:
    def __init__(self, date, category, amount, note):
        self.date = date
        self.category = category
        self.amount = amount
        self.note = note

    def to_file_line(self):
        return f"{self.date}|{self.category}|{self.amount}|{self.note}"

    def __str__(self):
        return f"{self.date} | {self.category} | ${self.amount:.2f} | {self.note}"


class ExpenseTracker:
    def __init__(self, filename="expenses.txt"):
        self.filename = filename
        self.expenses = []
        self.budget = 0

    def load_expenses(self):
        try:
            file = open(self.filename, "r")

            for line in file:
                line = line.strip()

                if line == "":
                    continue

                parts = line.split("|")

                if len(parts) == 4:
                    date = parts[0]
                    category = parts[1]

                    try:
                        amount = float(parts[2])
                    except ValueError:
                        continue

                    note = parts[3]

                    expense = Expense(date, category, amount, note)
                    self.expenses.append(expense)

            file.close()

        except FileNotFoundError:
            file = open(self.filename, "w")
            file.close()

    def save_expenses(self):
        file = open(self.filename, "w")

        for expense in self.expenses:
            file.write(expense.to_file_line() + "\n")

        file.close()

    def add_expense(self):
        print("\nAdd New Expense")

        while True:
            date = input("Enter date, for example 2026-05-19: ").strip()

            if len(date) == 10 and date[4] == "-" and date[7] == "-":
                break
            else:
                print("Please enter the date in YYYY-MM-DD format.")

        category = input(
            "Enter category, for example food, transport, study, rent, entertainment, other: "
        ).strip().lower()

        while True:
            amount_text = input("Enter amount: ").strip()

            try:
                amount = float(amount_text)

                if amount <= 0:
                    print("Amount must be greater than 0.")
                else:
                    break

            except ValueError:
                print("Please enter a valid number.")

        note = input("Enter a short note: ").strip()
        note = note.replace("|", "-")

        expense = Expense(date, category, amount, note)
        self.expenses.append(expense)
        self.save_expenses()

        print("Expense added successfully.")

    def view_expenses(self):
        print("\nAll Expense Records")

        if len(self.expenses) == 0:
            print("No expense records found.")
            return

        for i in range(len(self.expenses)):
            print(f"{i + 1}. {self.expenses[i]}")

    def calculate_total_recursive(self, index=0):
        if index == len(self.expenses):
            return 0

        return self.expenses[index].amount + self.calculate_total_recursive(index + 1)

    def show_total_spending(self):
        print("\nTotal Spending")

        total = self.calculate_total_recursive()
        print(f"Total spending: ${total:.2f}")

    def spending_by_category(self):
        summary = {}

        for expense in self.expenses:
            if expense.category not in summary:
                summary[expense.category] = 0

            summary[expense.category] += expense.amount

        return summary

    def show_category_summary(self):
        print("\nSpending by Category")

        if len(self.expenses) == 0:
            print("No expense records found.")
            return

        summary = self.spending_by_category()

        for category in summary:
            print(f"{category}: ${summary[category]:.2f}")

    def show_highest_category(self):
        print("\nHighest Spending Category")

        if len(self.expenses) == 0:
            print("No expense records found.")
            return

        summary = self.spending_by_category()

        highest_category = None
        highest_amount = 0

        for category in summary:
            if summary[category] > highest_amount:
                highest_amount = summary[category]
                highest_category = category

        print(f"You spent the most on {highest_category}: ${highest_amount:.2f}")

    def show_monthly_summary(self):
        print("\nMonthly Summary")

        if len(self.expenses) == 0:
            print("No expense records found.")
            return

        while True:
            month = input("Enter month, for example 2026-05: ").strip()

            if len(month) == 7 and month[4] == "-":
                break
            else:
                print("Please enter the month in YYYY-MM format.")

        summary = {}
        total = 0
        found = False

        for expense in self.expenses:
            if expense.date.startswith(month):
                found = True

                if expense.category not in summary:
                    summary[expense.category] = 0

                summary[expense.category] += expense.amount
                total += expense.amount

        if not found:
            print("No expense records found for this month.")
            return

        print(f"\nSummary for {month}")

        for category in summary:
            print(f"{category}: ${summary[category]:.2f}")

        print(f"Monthly total: ${total:.2f}")

    def set_budget(self):
        print("\nSet Budget")

        while True:
            budget_text = input("Enter your budget: ").strip()

            try:
                budget = float(budget_text)

                if budget <= 0:
                    print("Budget must be greater than 0.")
                else:
                    self.budget = budget
                    print(f"Budget set to ${self.budget:.2f}")
                    break

            except ValueError:
                print("Please enter a valid number.")

    def check_budget(self):
        print("\nBudget Check")

        if self.budget == 0:
            print("You have not set a budget yet.")
            return

        total = self.calculate_total_recursive()

        print(f"Budget: ${self.budget:.2f}")
        print(f"Total spending: ${total:.2f}")

        if total > self.budget:
            print("Warning: You are over your budget.")
        else:
            remaining = self.budget - total
            print(f"You are within your budget. Remaining: ${remaining:.2f}")

    def search_expenses(self):
        print("\nSearch Expenses")

        if len(self.expenses) == 0:
            print("No expense records found.")
            return

        keyword = input("Enter a category or keyword to search: ").strip().lower()

        found = False

        for i in range(len(self.expenses)):
            expense = self.expenses[i]

            if keyword in expense.category.lower() or keyword in expense.note.lower():
                print(f"{i + 1}. {expense}")
                found = True

        if not found:
            print("No matching expense records found.")

    def delete_expense(self):
        print("\nDelete Expense")

        if len(self.expenses) == 0:
            print("No expense records found.")
            return

        self.view_expenses()

        while True:
            choice = input("Enter the expense number to delete: ").strip()

            try:
                index = int(choice)

                if index < 1 or index > len(self.expenses):
                    print("Please enter a valid expense number.")
                else:
                    removed = self.expenses.pop(index - 1)
                    self.save_expenses()
                    print(f"Deleted: {removed}")
                    break

            except ValueError:
                print("Please enter a valid number.")


def show_menu():
    print("\nStudent Expense Analyzer")
    print("1. Add expense")
    print("2. View all expenses")
    print("3. Show total spending")
    print("4. Show spending by category")
    print("5. Show highest spending category")
    print("6. Show monthly summary")
    print("7. Set budget")
    print("8. Check budget")
    print("9. Search expenses")
    print("10. Delete expense")
    print("11. Exit")


def main():
    tracker = ExpenseTracker()
    tracker.load_expenses()

    while True:
        show_menu()

        choice = input("Choose an option: ").strip()

        if choice == "1":
            tracker.add_expense()

        elif choice == "2":
            tracker.view_expenses()

        elif choice == "3":
            tracker.show_total_spending()

        elif choice == "4":
            tracker.show_category_summary()

        elif choice == "5":
            tracker.show_highest_category()

        elif choice == "6":
            tracker.show_monthly_summary()

        elif choice == "7":
            tracker.set_budget()

        elif choice == "8":
            tracker.check_budget()

        elif choice == "9":
            tracker.search_expenses()

        elif choice == "10":
            tracker.delete_expense()

        elif choice == "11":
            print("Thank you for using Student Expense Analyzer.")
            break

        else:
            print("Invalid choice. Please choose a number from 1 to 11.")


if __name__ == "__main__":
    main()

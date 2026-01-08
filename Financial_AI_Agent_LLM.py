def analyze_budget(income, fixed_expenses, saving_goal):

    remaining = income - fixed_expenses

    messages = []

    if remaining <= 0:
        messages.append(" your expenses exceed your income")
        messages.append(" Action: reduce expenses or increase income.")
        return messages

    if saving_goal > income:
        messages.append("Your saving goal is unrealistic.")
        messages.append("you are tring to save more than you earn.")
        messages.append("Action: increase income or lower the goal")
        return messages


    if saving_goal > remaining:
        messages.append(" your saving goal is too high")
        messages.append("Action: lower the saving goal or cut expenses")
    else:
        ratio = round((saving_goal / income) * 100, 2)
        messages.append(" your saving goal is achievable.")
        messages.append(f"Recommended saving ratio: {ratio}%") 

    messages.append("Suggestions:")
    messages.append(" keep savings between 20% and 40% of income")
    messages.append(" Reduce non-essential spending if needed")
    messages.append(" Build an emergency fund (3-6) months")

    return messages
    



def read_float(prompt):
    while True:
        raw = input(prompt).strip().lower()
        if raw == "q":
            return None
        try:
            return float(raw)
        except ValueError:

            print("Please enter a valid number or type q to quit.")
        



def main():
    print("Personal Budget Assistant v2")

    while True:
        choice = input(" Press Enter to calculate, or type q to quit:").strip().lower()

        if choice == "q":

            print("Bye")
            break

        income = read_float("Monthly income:")
        if income is None:
            print("Bye.")
            break

        fixed = read_float("Fixed expenses:")
        if fixed is None:
            print("Bye.")
            break


        goal = read_float("Saving goal:")
        if goal is None:
            print("Bye.")
            break

        results = analyze_budget(income, fixed, goal)
        

        print("-------Result-------")
        for line in results:
            print(line)
        
        


if __name__ == "__main__":
    main()
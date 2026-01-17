# ------------------------------------------------
# Financial_AI_Agent_LLM.py
# A simple personal budget assistant that analyzes income, fixed expenses, and saving goals.
# It provides feedback and suggestions based on the user's financial inputs.
# Author: Zemou Huang
# Last Modified: 2026-1-11
# License: NAU Public Domain License
# This program is free software; you can redistribute it and/or modify it.
# There is NO WARRANTY, to the extent permitted by law.
# This program requires Python 3.6 or higher.
# Usage: Run the script and follow the prompts to input your financial data.
# ------------------------------------------------

#123

#main()
# ├─ read_float()   # 输入校验
# ├─ analyze_budget()  ←【这里是“大脑”】【该升级的地方】
# │    ├─ 计算 remaining
# │    ├─ 判断条件
# │    ├─ messages.append(...)
# │    └─ return messages
# └─ 把 messages：
#      ├─ print 给用户
#      └─ join 成 fact_text → 交给 LLM 总结
#    已追加询问系统 2026/1/17

import os
from zhipuai import ZhipuAI

client = ZhipuAI(api_key=os.getenv("ZHIPU_API_KEY"))

def generate_followup_questions(result):
    questions = []

    # 用户目标为 0：就引导他设目标
    if "zero_goal" in result["flags"]:
        questions.append("Do you want help setting a realistic monthly saving goal?")
        questions.append("Do you want a simple plan to start saving (e.g., $50/week)?")
        return questions

    # 收支为负：先问支出结构
    if "negative_remaining" in result["flags"]:
        questions.append("Which fixed expense is the biggest (rent, car, food, etc.)?")
        questions.append("Do you want me to suggest a target expense limit based on your income?")
        questions.append("Do you have any side income you can add?")
        return questions

    # 目标太高：问是想减少支出还是增收
    if "unrealistic_goal" in result["flags"] or "goal_too_high" in result["flags"]:
        questions.append("Do you want to cut expenses or increase income to reach this goal?")
        questions.append("What is your rent/housing cost? (This usually matters most.)")
        questions.append("Should I suggest a revised saving goal based on your current numbers?")
        return questions

    # 低风险：给更进阶的问题
    if result["risk"] == "Low":
        questions.append("Do you want a 30-day action plan to reach your goal?")
        questions.append("Do you want to split your budget into categories (50/30/20 or custom)?")
        questions.append("Do you want to estimate how long it takes to build a 3–6 month emergency fund?")
        return questions

    # 默认兜底
    questions.append("Do you want to run another scenario with different numbers?")
    return questions


def analyze_budget(income, fixed_expenses, saving_goal):
    remaining = income - fixed_expenses
    result = {
        "income": income,
        "fixed": fixed_expenses,
        "goal": saving_goal,
        "remaining": remaining,
        "risk": None,
        "ratio": None,
        "messages": [],
        "flags": set(),  # 用来标记情况，比如 "zero_goal" "unrealistic" 等
    }

    # 1) 基础输入检查
    if income <= 0:
        result["flags"].add("invalid_income")
        result["messages"].append("Income must be greater than 0.")
        return result

    if saving_goal <= 0:
        result["flags"].add("zero_goal")
        result["messages"].append("Saving goal is 0. You may want to set a small goal to start.")
        return result

    # 2) 风险判断
    if remaining <= 0:
        result["risk"] = "High"
        result["flags"].add("negative_remaining")
        result["messages"].append("Warning: Your expenses exceed your income.")
        return result

    if saving_goal > income:
        result["risk"] = "High"
        result["flags"].add("unrealistic_goal")
        result["messages"].append("Your saving goal is unrealistic (greater than income).")
        return result

    if saving_goal > remaining:
        result["risk"] = "Medium"
        result["flags"].add("goal_too_high")
        result["messages"].append("Your saving goal is too high based on current expenses.")
        # 不 return，让它继续算 ratio 并给建议
    else:
        result["risk"] = "Low"
        result["messages"].append("Your saving goal is achievable.")

    # 3) 计算比例
    result["ratio"] = round((saving_goal / income) * 100, 2)
    result["messages"].append(f"Recommended saving ratio: {result['ratio']}%")

    # 4) 通用建议
    result["messages"].append("Suggestions:")
    result["messages"].append("- Keep savings between 20% and 40% of income (if possible).")
    result["messages"].append("- Reduce non-essential spending if needed.")
    result["messages"].append("- Build an emergency fund (3–6 months).")

    return result


def read_float(prompt): #不停问用户输入，直到他输入一个“合法的数字”，或者输入 q 退出


    while True:  #直到用户输对，否则无限循环

        raw = input(prompt).strip().lower() #读取用户输入，并去掉前后空格，转换为小写
        if raw == "q": #如果用户输入q
            return None #返回None，结束这一函数读取程序
        if raw == "0": #如果用户输入0 #******修复了输入0被当作合法数字的问题 ********
            print("Zero is not allowed. Please enter a positive number or type q to quit.") #提示用户输入有效数据
            continue #继续下一次循环，重新问用户输入
        if raw < "0": #如果用户输入负数 #******修复了输入负数被当作合法数字的问题
            print("Please enter a non-negative number or type q to quit.") #提示用户输入有效数据
            continue #继续下一次循环，重新问用户输入

        if len(raw) > 1 and raw.startswith("0") and not raw.startswith("0."): #****** 修复了输入O1 02或03被当作合法数字的问题 ********
            print("Please enter a valid number or type q to quit.") #提示用户输入有效数据
            continue #继续下一次循环，重新问用户输入
        
        try: #尝试把用户输入转换为浮点数
            return float(raw) #如果成功，返回浮点数，结束这一函数读取程序
        except ValueError: #如果转换失败，捕获异常

            print("Please enter a valid number or type q to quit.") #提示用户输入有效数据
        


def main(): #定义主函数，这个是所有程序大脑，不可更改
    print("Personal Budget Assistant v2") #打印程序名称
    print("Type q at any prompt to quit.") #打印退出提示 

    while True: #无限循环，直到用户选择退出
        choice = input("Press Enter to calculate, or type q to quit:").strip().lower() #读取用户输入，并去掉前后空格，转换为小写

        if choice == "q": #如果用户输入q

            print("很高兴为您服务，下次见") #打印退出信息
            break #结束主函数程序

        income = read_float("Monthly income:") #调用读取函数，读取用户输入的月收入
        if income is None: #如果用户输入q
            print("Bye.") #打印退出信息
            break 

        fixed = read_float("Fixed expenses:") #调用读取函数，读取用户输入的固定支出
        if fixed is None: #如果用户输入q
            print("Bye.")   
            break


        goal = read_float("Saving goal:") #调用读取函数，读取用户输入的储蓄目标
        if goal is None:
            print("Bye.")
            break

        results = analyze_budget(income, fixed, goal) #调用分析函数，分析预算
        

        print("-------Result-------") 
        for line in results: #循环打印分析结果
            print(line) #打印分析结果
        print("--------------------")

        #主动追问
        questions = generate_followup_questions(results)
        if questions:
            print("Next questions (choose one):")
            for idx, q in enumerate(questions, 1):
                print(f"{idx}. {q}")
            print("0. Skip / new calculation")

            choice = input("Your choice: ").strip().lower()
            if choice == "q":
                print("Bye")
                break
            if choice == "0" or choice == "":
                continue

            # 这里先做“假响应”：你后面再慢慢把每个选项实现成具体功能
            if choice.isdigit() and 1 <= int(choice) <= len(questions):
                print(f"\nYou selected: {questions[int(choice)-1]}")
                print("(Feature coming next: we will implement this option.)\n")
            else:
                print("Invalid choice. Restarting...\n")

        fact_text = "\n".join(results) # 将下列列表合成一段话，作为发给AI的事实

        response = client.chat.completions.create(
            model="glm-4-flash",
            messages=[
            {
                "role": "system",
                "content": "You are a financial audit agent. "
                        "Based only on the computed financial facts, output a corrective action plan. "
                                "Each action must include: what to change, how much to change, and the expected impact. "
                                    "No greetings, no summaries, no disclaimers. "
                                        "Use numbered bullet points only."
            },
            {"role": "user", "content": fact_text}

            
            ]
        )
    
        print("---分析结果如下---")
        print(response.choices[0].message.content)


if __name__ == "__main__": #如果是主程序运行
    main()
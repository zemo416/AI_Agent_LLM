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




def analyze_budget(income, fixed_expenses, saving_goal): #定义一个函数，用来分析预算
    remaining = income - fixed_expenses #定义计算公式，计算月剩余金额
    messages = [] #把信息全放在这里
    
    if remaining <= 0: #如果月剩余金额小于等于0
        messages.append(" your expenses exceed your income") #添加输出屏幕的信息
        messages.append(" Action: reduce expenses or increase income.")
        return messages #直接返回信息，结束这一函数分析程序
    

    if saving_goal > income: #如果储蓄目标大于收入
        messages.append("Your saving goal is unrealistic.") #添加输出屏幕的信息
        messages.append("you are tring to save more than you earn.")
        messages.append("Action: increase income or lower the goal")
        return messages #直接返回信息，结束这一函数分析程序


    if saving_goal > remaining: #如果储蓄目标大于月剩余金额
        messages.append(" your saving goal is too high") #添加输出屏幕的信息
        messages.append("Action: lower the saving goal or cut expenses")


    else: #如果上述三个情况都没发生，那么否则
        ratio = round((saving_goal / income) * 100, 2) #计算推荐储蓄比例
        messages.append(" your saving goal is achievable.") #添加输出屏幕的信息
        messages.append(f"Recommended saving ratio: {ratio}%")  #添加输出屏幕的信息，显示推荐储蓄比例

    messages.append("Suggestions:") #添加输出屏幕的信息，显示建议
    messages.append(" keep savings between 20% and 40% of income") 
    messages.append(" Reduce non-essential spending if needed")
    messages.append(" Build an emergency fund (3-6) months")

    return messages #返回信息，结束这一函数分析程序
    



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
        



def main(): #定义主函数
    print("Personal Budget Assistant v2") #打印程序名称
    print("Type q at any prompt to quit.") #打印退出提示 

    while True: #无限循环，直到用户选择退出
        choice = input(" Press Enter to calculate, or type q to quit:").strip().lower() #读取用户输入，并去掉前后空格，转换为小写

        if choice == "q": #如果用户输入q

            print("Bye") #打印退出信息
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
        
        


if __name__ == "__main__": #如果是主程序运行
    main() 
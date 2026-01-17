def analyze_budget(income, fixed_expenses, saving_goal): #定义一个函数，用来分析预算
    remaining = income - fixed_expenses #定义计算公式，计算月剩余金额
    messages = [] #把信息全放在这里


    # -------- Risk Level Assessment --------
    if remaining <= 0:
        risk = "High"
    elif remaining < income * 0.1:
        risk = "Medium"
    else:
        risk = "Low"

    messages.append(f"Risk Level: {risk}")


    if remaining <= 0: #如果月剩余金额小于等于0
        messages.append(" your expenses exceed your income") #添加输出屏幕的信息https://chatgpt.com/c/695f2cd3-742c-8333-aa13-0b6b514da9b6
        messages.append(" Action: reduce expenses or increase income.")
        return messages #直接返回信息，结束这一函数分析程序
    

    if saving_goal > income: #如果储蓄目标大于收入
        messages.append("Your saving goal is unrealistic.") #添加输出屏幕的信息
        messages.append("you are tring to save more than you earn.")
        messages.append("Action: increase income or lower the goal")
        return messages #直接返回信息，结束这一函数分析程序


    if saving_goal > remaining: #如果储蓄目标大于月剩余金额
        messages.append("your saving goal is too high") #添加输出屏幕的信息
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
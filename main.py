from rules import analyze_budget
from agent import agent_summary







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


results = analyze_budget(income, fixed, goal)
final_text = agent_summary(results)

print(final_text)


if __name__ == "__main__": #如果是主程序运行
    main()


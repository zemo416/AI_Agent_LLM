import json
from zhipuai import ZhipuAI

# 1. 初始化大脑：填入你的 API Key
# 请确保引号内是你最新生成的 Key，不要有空格
client = ZhipuAI(api_key="d932...zE0F") 

# 2. 定义会计师函数：负责精准计算事实
def get_budget_report(income, expenses, goal):
    remaining = income - expenses
    # 使用结构化列表，强迫 AI 看清每个数字的含义
    report = f"""
    【用户财务数据核算】
    - 月度收入：{income} 元
    - 月度支出：{expenses} 元
    - 支出后剩余：{remaining} 元
    - 储蓄目标：{goal} 元
    """
    
    # 预先在 Python 里算好结论，防止 AI “幻觉”
    if expenses > income:
        report += f"\n判定结果：入不敷出，每月亏损 {expenses - income} 元。"
    elif remaining >= goal:
        report += f"\n判定结果：资金充足，可以轻松达成储蓄目标。"
    else:
        report += f"\n判定结果：资金不足，距离储蓄目标还差 {goal - remaining} 元。"
    
    return report

# 3. 主程序逻辑：数据采集与 AI 对话
def main():
    print("="*30)
    print("欢迎使用 AI 个人财务助手")
    print("="*30)

    try:
        # 获取用户输入并转为数字
        user_income = float(input("请输入您的月收入: "))
        user_expenses = float(input("请输入您的月支出: "))
        user_goal = float(input("请输入您的储蓄目标: "))

        # 第一步：Python 先算出账单报告 (存入变量 report_text)
        report_text = get_budget_report(user_income, user_expenses, user_goal)
        
        print("\n[系统信息] 正在分析数据并请求 AI 建议...\n")

        # 第二步：将账单发送给 AI 大脑
        # 注意这里 completions.create 之间是点号
        response = client.chat.completions.create(
            model="glm-4-flash",
            messages=[
                {
                    "role": "system", 
                    "content": "你是一个毒舌但专业的私人理财教练。请根据用户提供的财务事实，给出3条非常具体的理财改进建议。"
                },
                {
                    "role": "user", 
                    "content": report_text # 这里就是之前报错找不到的变量
                }
            ],
            top_p=0.7,
            temperature=0.9
        )

        # 第三步：解析并显示 AI 的回复
        print("-" * 30)
        print("AI 理财教练的建议：")
        print(response.choices[0].message.content)
        print("-" * 30)

    except ValueError:
        print("\n[错误] 请输入有效的数字，不要包含字母或特殊符号！")
    except Exception as e:
        print(f"\n[运行异常] {e}")

if __name__ == "__main__":
    main()
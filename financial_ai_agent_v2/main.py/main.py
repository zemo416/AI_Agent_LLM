# main.py （测试版，先跑通核心逻辑）

from decimal import Decimal
from core.analyzer import BudgetAnalyzer
from core.validator import validate_positive_decimal
from models import BudgetInput


def quick_test():
    income = validate_positive_decimal("月收入：")
    if income is None:
        return

    fixed = validate_positive_decimal("固定支出：")
    if fixed is None:
        return

    goal = validate_positive_decimal("储蓄目标：")
    if goal is None:
        return

    data = BudgetInput(income, fixed, goal)
    analyzer = BudgetAnalyzer()
    result = analyzer.analyze(data)

    print("\n" + "=" * 40)
    for msg in result.messages:
        print(msg)
    print("=" * 40)


if __name__ == "__main__":
    quick_test()
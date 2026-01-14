# core/analyzer.py
from decimal import Decimal
from .models import BudgetInput, BudgetAnalysis

class BudgetAnalyzer:
    def analyze(self, data: BudgetInput) -> BudgetAnalysis:
        remaining = data.income - data.fixed_expenses
        messages = []

        if remaining <= 0:
            messages.extend([
                "您的支出已经超过收入了！",
                "建议：立即减少开支或增加收入来源。"
            ])
            return BudgetAnalysis(remaining, False, messages)

        if data.saving_goal > data.income:
            messages.extend([
                "储蓄目标比您的全部收入还高...",
                "这有点像要从空气里变出钱来呢~",
                "建议：调低目标或寻找额外收入。"
            ])
            return BudgetAnalysis(remaining, False, messages)

        if data.saving_goal > remaining:
            messages.extend([
                "这个月想存的钱超过了您能省下来的部分。",
                "建议：降低目标 或 再砍一些非必要开支。"
            ])
            is_realistic = False
        else:
            ratio = round(float((data.saving_goal / data.income) * 100), 2)
            messages.extend([
                "这个目标看起来是可行的！加油💪",
                f"建议储蓄比例：{ratio}%"
            ])
            is_realistic = True

        # 通用建议
        messages.extend([
            "\n小财管家温馨建议：",
            "• 理想储蓄比例：收入的20%~40%",
            "• 优先建立3~6个月的紧急备用金",
            "• 非必要消费能省则省~"
        ])

        return BudgetAnalysis(
            remaining=remaining,
            is_realistic=is_realistic,
            messages=messages,
            recommended_ratio=ratio if is_realistic else None
        )
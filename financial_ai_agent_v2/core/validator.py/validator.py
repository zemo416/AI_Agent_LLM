# core/validator.py （简单版）
from decimal import Decimal, InvalidOperation

def validate_positive_decimal(prompt: str) -> Decimal | None:
    while True:
        raw = input(prompt).strip().lower()
        if raw == 'q':
            return None
        
        try:
            value = Decimal(raw)
            if value <= 0:
                print("请输入大于0的金额哦～")
                continue
            return value
        except (InvalidOperation, ValueError):
            print("请输入正确的数字格式（例如：5000 或 5000.00），或输入 q 退出")
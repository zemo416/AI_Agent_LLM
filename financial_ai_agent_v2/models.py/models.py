# models.py
from dataclasses import dataclass
from decimal import Decimal
from datetime import datetime
from typing import List, Optional

@dataclass
class BudgetInput:
    income: Decimal
    fixed_expenses: Decimal
    saving_goal: Decimal
    timestamp: datetime = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()

@dataclass
class BudgetAnalysis:
    remaining: Decimal
    is_realistic: bool
    messages: List[str]
    recommended_ratio: Optional[float] = None
def agent_summary(messages):
    summary = "Here is the financial analysis:\n"
    for m in messages:
        summary += "- " + m + "\n"
    return summary

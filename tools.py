import datetime

def calculate(expression: str):
    try:
        return str(eval(expression))
    except Exception as e:
        return f"Error: {e}"

def get_current_time():
    return str(datetime.datetime.now())

def log_triage(log_text: str):
    if "NullPointerException" in log_text:
        return "Likely Java Null Pointer issue. Check object initialization."
    elif "Timeout" in log_text:
        return "Possible network/service delay."
    else:
        return "Unknown error. Needs deeper analysis."

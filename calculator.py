import math

def calculate_scientific(operation, value):
    try:
        value = float(value)# value
        if operation == "sqrt":
            return math.sqrt(value)
        elif operation == "log":
            return math.log10(value)
        elif operation == "ln":
            return math.log(value)
        elif operation == "fact":
            return math.factorial(int(value))
        elif operation == "sin":
            return math.sin(math.radians(value))
        elif operation == "cos":
            return math.cos(math.radians(value))
        elif operation == "tan":
            return math.tan(math.radians(value))
        elif operation == "x2":
            return value ** 2
        elif operation == "x3":
            return value ** 3
        elif operation == "xy":
            return f"{value}**"
        elif operation == "1/x":
            return 1 / value
    except Exception as e:
        return f"Error: {e}"

def calculate(expression):
    try:
        allowed = "0123456789+-**/()). eπ"
        for char in expression:
            if char not in allowed:
                return "Error: invalid symbol"
        expression = expression.replace("π", str(math.pi))
        expression = expression.replace("e", str(math.e))
        return eval(expression)
    except ZeroDivisionError:
        return "Error: cannot divide by zero"
    except:
        return "Error"
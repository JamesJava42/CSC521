def tokenize(expression):
    """Tokenize the expression into numbers, operators, and parentheses."""
    tokens = []
    number = ''
    for char in expression:
        if char.isdigit():
            number += char
        else:
            if number:
                tokens.append(number)
                number = ''
            if char in "+-*/()":
                tokens.append(char)
    if number:
        tokens.append(number)
    return tokens

def handle_unary_minus(tokens):
    """Convert unary minus operators to a distinct symbol '^'."""
    result = []
    prev = '('  # Assume an opening '(' or a binary operator precedes the first token
    for token in tokens:
        if token == '-' and (prev == '(' or prev in "+-*/"):
            result.append('^')
        else:
            result.append(token)
        prev = token
    return result

def infix_to_prefix(tokens):
    def precedence(op):
        return {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}.get(op, 0)
    
    def operator_greater_precedence(op1, op2):
        return precedence(op1) > precedence(op2)
    
    output = []
    stack = []
    for token in reversed(tokens):  # Reverse the tokens for prefix conversion
        if token.isdigit():
            output.append(token)
        elif token == ')':
            stack.append(token)
        elif token == '(':
            while stack and stack[-1] != ')':
                output.append(stack.pop())
            stack.pop()  # Remove ')'
        else:
            while (stack and operator_greater_precedence(stack[-1], token)):
                output.append(stack.pop())
            stack.append(token)
    while stack:
        output.append(stack.pop())
    return list(reversed(output))  # Reverse to get the correct prefix order

def evaluate_prefix(tokens):
    stack = []
    for token in reversed(tokens):
        if token.isdigit():
            operand = int(token)
            operand = operand if operand <= 127 else operand - 256  # Adjust for two's complement
            stack.append(operand)
        elif token in ['+', '-', '*', '/', '^']:  # Added '^' for unary minus
            if token == '^':  # Unary minus operation
                if len(stack) < 1:
                    return 'Error: Not enough operands'
                operand = stack.pop()
                result = -operand & 0xFF  # Apply two's complement for negative numbers
            elif len(stack) >= 2:  # For binary operations, ensure there are enough operands
                b = stack.pop()
                a = stack.pop()
                if token == '+':
                    result = (a + b) & 0xFF
                elif token == '-':
                    result = (a - b) & 0xFF
                elif token == '*':
                    # Multiplication operation, with overflow check
                    result = (a * b) & 0xFF
                    if (a != 0 and b != 0) and result == 0:
                        print("Overflow occurs!")
                elif token == '/':
                    if b == 0:
                        return 'Div by 0'
                    result = int(a / b) if a / b >= 0 else int((a / b) - 1) 
                     # Floor division for negative results
            else:
                return 'Error: Not enough operands for operation'
            
            # Check for overflows in addition, subtraction, and multiplication
            if token in ['+', '-', '*'] and not (-128 <= result <= 127):
                print("Overflow occurs!")
                result = result & 0xFF  # Ensure the result fits in 8 bits
            
            stack.append(result)
    
    return stack.pop() if stack else 'Error: Invalid expression'

def main():
    file_path = "test.txt"
    with open(file_path, "r") as file:
        for line in file:
            expression = line.strip()
            if expression:
                print(f"Processing expression: {expression}")
                tokens = tokenize(expression)
                unary_handled_tokens = handle_unary_minus(tokens)
                prefix_tokens = infix_to_prefix(unary_handled_tokens)
                print(f"Prefix notation: {' '.join(prefix_tokens)}")
                result = evaluate_prefix(prefix_tokens)
                print(f"Evaluated result: {result}\n")

if __name__ == "__main__":
    main()

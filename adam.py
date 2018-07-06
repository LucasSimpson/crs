undefined = "undefined"
syntax = 'invalid syntax'
# Order of the operation list is understandably super important
op_list = ["+", "-", "*", "/"]
def clean(exp):
    return exp.replace(" ", "")
def valid_parens(exp):
    count = 0
    for char in exp:
        if char == "(":
            count += 1
        if char == ")":
            count -= 1
        if count < 0:
            return False
    if count > 0:
        return False
    return True
def find_close(exp):
    count = 1
    index = 0
    for char in exp:
        if char == "(":
            count += 1
        if char == ")":
            count -= 1
        if count <= 0:
            return index
        index += 1
def simplify(pair):
    if pair == '--':
        return '+'
    if pair == '++':
        return '+'
    if pair == '-+':
        return '-'
    if pair == '+-':
        return '-'
def simplify_sign(exp):
    if len(exp) <= 1:
        return exp
    for i in range(len(exp) - 1):
        if (exp[i] == '-' or exp[i] == '+') \
                and (exp[i+1] == '-' or exp[i+1] == '+'):
            return exp[:i] + simplify_sign(simplify(exp[i:i+2]) + exp[i+2:])
    return exp
def apply(op, left, right):
    if (left == undefined) or (right == undefined):
        return undefined
    if (left == syntax) or (right == syntax):
        return syntax
    if op == "-":
        return left - right
    if op == "+":
        return left + right
    if op == "/":
        if right == 0:
            return undefined
        return left / right
    if op == "*":
        return left * right
def repl():
    while True:
        print(read_eval())
def read_eval():
    exp = clean(input('>>> '))
    if not valid_parens(exp):
        return syntax
    return brackets(exp)
def brackets(exp):
    if '(' in exp:
        start = exp.find('(') + 1
        end = start + find_close(exp[start:])
        left = exp[:start - 1]
        mid = str(brackets(exp[start:end]))
        right = exp[end + 1:]
        return brackets(left + mid + right)
    return compute(simplify_sign(exp))
def compute(exp):
    if exp[0] == "-" or exp[0] == "+":
        return compute("0" + exp)
    for op in op_list:
        if op in exp:
            index = exp.rfind(op)
            left = exp[:index]
            right = exp[index + 1:]
            if left == '' or right == '':
                return syntax
            return apply(op, compute(left), compute(right))
    if '.' in exp:
        return float(exp)
    else:
        return int(exp)
test = '-6+(31*4+(15/5-1)+2*(3*(2+4)*8))+1-3*(12+5*7)'
# print(repl(test))
# print(repl('-15/0'))
# print(repl('10-5-5+6+6-6-6+6'))
# print(repl('--5'))
repl()

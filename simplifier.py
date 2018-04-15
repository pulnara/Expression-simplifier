import sys

OPS = {'|': 1, '&': 2, '^': 1, '~': 3, '>': 0, '=': 0}
VARS = "".join([chr(i) for i in range(97, 123)]) + "".join([chr(i) for i \
    in range(65, 91)]) + "".join(list(map(str, range(10))))


def validate(ex):
    ##    & - koniunkcja,
    ##    | alternatywa,
    ##    ^ - xor,
    ##    ~ - negacja,
    ##    > - implikacja,
    ##    = - rownowaznosc
    ex = ex.strip()
    #print(ex)
    par_count = 0
    before_last = ''
    last = ''
    var = 0

    # checks if there are spaces between VARS or invalid characters
    for i in ex:
        if i in VARS:
            if last == ' ' and var == 1:
                #print(i)
                raise ValueError("invalid VARS sequence")
            var = 1
        elif i in OPS.keys():
            var = 0
        elif i not in "()" + ' ':
            raise ValueError("invalid character")
        before_last = last
        last = i
    ex = "".join(ex.split())

    # simple enum
    Number, Letter, Operator, L_Bracket, R_Bracket = range(0, 5)

    flag = 0
    prev = None
    bracket_stack = []
    for i in ex:
        if i in VARS:
            #print(i)
            if prev in [R_Bracket]: raise ValueError("incorrect brackets")
            if prev in [Number] and flag == 0:
                raise ValueError("variable starting with a number")
            if i.isnumeric():
                if prev in [None, Operator, L_Bracket, R_Bracket]:
                    if int(i) not in [0, 1]:
                        raise ValueError("variable starting with a number")
                if prev == Letter:
                    flag = 1
                prev = Number
            else:
                flag = 0
                prev = Letter
        elif i in OPS.keys():
            if prev in [None, Operator, L_Bracket] and i != '~':
                raise ValueError("binary operator used as an unary")
            if prev in [R_Bracket, Letter, Number] and i == '~':
                raise ValueError("unary operator used as a binary")
            prev = Operator
        elif i == '(':
            if prev in [Letter, Number, R_Bracket]:
                raise ValueError("incorrect brackets")
            prev = L_Bracket
            bracket_stack.append(L_Bracket)
        elif i == ')':
            if len(bracket_stack) == 0:
                raise ValueError("incompatible brackets")
            bracket_stack.pop()
            if prev in [Operator, L_Bracket]:
                raise ValueError("incorrect brackets")
            prev = R_Bracket

    if prev == Operator: raise ValueError("operator shouldn't be at the end")
    if len(bracket_stack) > 0: raise ValueError("incompatible brackets")
    return ex

# shunting-yard algorithm
def convert_to_RPN(ex):
    stack = []
    converted = []
    variables = []

    variable_tmp = ""
    for i in ex:
        #print(i)
        if i in VARS:
            variable_tmp += i
        else:
            if variable_tmp != "":
                converted.append(variable_tmp)
                if variable_tmp not in variables: variables.append(variable_tmp)
                variable_tmp = ""
            if i in OPS.keys():
                while len(stack) > 0 and stack[len(stack)-1] in OPS.keys() and \
                OPS[stack[len(stack)-1]] >= OPS[i]:
                    converted += stack.pop()
                stack.append(i)
            elif i == '(':
                stack.append(i)
            elif i == ')':
                while stack[len(stack)-1] != '(':
                    converted += stack.pop()
                stack.pop()    # (
    if variable_tmp != "":
        if variable_tmp not in variables: variables.append(variable_tmp)
        converted.append(variable_tmp)
    while len(stack) > 0:
        converted += stack.pop()
    return converted, variables

def main():
    try:
        if len(sys.argv) < 2:
            raise Exception("no expression given")
        elif len(sys.argv) > 2:
            raise ValueError("too many arguments given")
    except Exception as e:
        print("Error: " + str(e))
        exit(1)

    expr = sys.argv[1]
    print("Input expression: ", expr)

    try:
        expr = validate(expr)
    except ValueError as e:
        print("Error: " + str(e))
        exit(1)
    #print(expr)

    rpn, variables = convert_to_RPN(expr)
    print("RPN: ", rpn)
    print(len(variables))

##    print("Minimalization result: " + expr)

if __name__ == "__main__":
    main()

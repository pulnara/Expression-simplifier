import sys
import itertools

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

def get_possible_arg_vals(arg_num):
    return list(itertools.product(range(2), repeat=arg_num))

def evaluate_expression(rpn, values):
    rpn2 = rpn[:]
    for el in rpn2:
        if el in values.keys():
            rpn2[rpn2.index(el)] = values[el]
            #print(values[el])
    #print(rpn)
    #print(rpn2)
    stack = []
    for el in rpn2:
        if el in OPS and el != '~':
            x = stack.pop()
            y = stack.pop()
            if el == '|':
                stack.append(x or y)
            elif el == '&':
                stack.append(x and y)
            elif el == '^':
                stack.append(bool(x) ^ bool(y))
            elif el == '>':
                stack.append((not y) or x)
            elif el == '=':
                stack.append(x == y)
        elif el == '~':
            x = stack.pop()
            stack.append(not x)
        else:
            stack.append(el)
    return stack.pop()

def get_positive_results(possible_vals, arguments, rpn):
    positive = []
    #print(rpn)
    for value in possible_vals:
        vals_list = list(value)
        # print(vals_list)
        # print(rpn)
        dictionary = dict(zip(arguments, vals_list))
        #print(dictionary)
        if evaluate_expression(rpn, dictionary):
            positive.append(vals_list)
    return positive

# def merge(x, y):
#     changes_ctr = 0
#     result = ""
#     for a, b in zip(x, y):
#         if a == b: result += str(a)
#         else:
#             result += "-"
#             changes_ctr += 1
#     if changes_ctr == 1: return result
#     return False
#
# def reduce(expr):
#     result = []
#     merge_flag = False      # czy nastapilo jakiekolwiek laczenie
#     for row1 in expr:
#         merge_tmp = False   # czy polaczylo dany element z czymkolwiek
#         for row2 in expr:
#             res = merge(row1, row2)
#             if res:
#                 result.append(res)
#                 merge_tmp = merge_flag = True
#         if not merge_tmp: result.append(row1)
#     if merge_flag: return reduce(result)
#     return result
#
# def get_simplified(expr, variables):
#     result = ""
#     for el in expr:
#         res = ""
#         for i in range(len(el)):
#             if el[i] == '-': continue
#             if el[i] == '0': res+="~"
#             res += variables[i] + "&"
#         result += "(" + res[:-1] + ")|"
#     return result[:-1]

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
    #print(len(variables))
    possible = get_possible_arg_vals(len(variables))

    #print(get_positive_results(possible, variables, rpn))

    # minimized = reduce(get_positive_results(possible, variables, rpn))
    #print(minimized)

    # print("Minimalization result: ", get_simplified(minimized, variables))

if __name__ == "__main__":
    main()

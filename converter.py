class RPN_converter:

    def __init__(self, operators, variables):
        self.operators = operators
        self.variables = variables

    # shunting-yard algorithm
    def convert(self, ex):
        stack = []
        converted = []
        expr_variables = []

        variable_tmp = ""
        for i in ex:
            #print(i)
            if i in self.variables:
                variable_tmp += i
            else:
                if variable_tmp != "":
                    converted.append(variable_tmp)
                    if variable_tmp not in expr_variables and variable_tmp not in ['0', '1']:
                        expr_variables.append(variable_tmp)
                    variable_tmp = ""
                if i in self.operators.keys():
                    while len(stack) > 0 and stack[len(stack)-1] in self.operators.keys() and \
                    self.operators[stack[len(stack)-1]] >= self.operators[i]:
                        converted += stack.pop()
                    stack.append(i)
                elif i == '(':
                    stack.append(i)
                elif i == ')':
                    while stack[len(stack)-1] != '(':
                        converted += stack.pop()
                    stack.pop()    # (
        if variable_tmp != "":
            if variable_tmp not in expr_variables and variable_tmp not in ['0', '1']:
                expr_variables.append(variable_tmp)
            converted.append(variable_tmp)
        while len(stack) > 0:
            converted += stack.pop()
        print(expr_variables)
        return converted, expr_variables

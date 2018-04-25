class RPN_converter:

    def __init__(self, operators, characters):
        self.operators = operators
        self.characters = characters

    # infix to RPN: shunting-yard algorithm
    def convert(self, ex):
        stack = []
        converted = []
        expr_variables = []
        variable_tmp = ""

        for i in ex:
            if i in self.characters:
                variable_tmp += i

            else:
                if variable_tmp != "":
                    if variable_tmp in "01":
                        converted.append(int(variable_tmp))
                    else:
                        converted.append(variable_tmp)

                    if variable_tmp not in expr_variables and variable_tmp not in "01":
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
            if variable_tmp not in expr_variables and variable_tmp not in "01":
                expr_variables.append(variable_tmp)

            if variable_tmp in "01":
                converted.append(int(variable_tmp))

            else:
                converted.append(variable_tmp)

        while len(stack) > 0:
            converted += stack.pop()

        # print("Variables: ", expr_variables)

        return converted, expr_variables

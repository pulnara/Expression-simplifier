import itertools

class Quine_McCluskey_simplifier:

    def __init__(self, operators, expr_variables, rpn):
        self.operators = operators
        self.variables = expr_variables
        self.rpn = rpn

    def __get_possible_arg_vals(self, arg_num):
        return list(itertools.product(range(2), repeat=arg_num))

    def __evaluate_expression(self, rpn, values):
        rpn2 = rpn[:]
        for el in rpn2:
            if el in values.keys():
                rpn2[rpn2.index(el)] = values[el]
                #print(values[el])
        #print(rpn)
        # print(rpn2)
        stack = []
        for el in rpn2:
            if el in self.operators and el != '~':
                x = stack.pop()
                y = stack.pop()
                if el == '|':
                    stack.append(x or y)
                elif el == '&':
                    stack.append(x and y)
                elif el == '^':
                    stack.append(x ^ y)
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

    def __get_positive_results(self, possible_vals, arguments, rpn):
        positive = []
        #print(rpn)
        for value in possible_vals:
            vals_list = list(value)
            # print(vals_list)
            # print(rpn)
            dictionary = dict(zip(arguments, vals_list))
            # print(dictionary)
            if self.__evaluate_expression(rpn, dictionary):
                positive.append(vals_list)
        # print("positive ", positive)
        return positive

    def simplify(self):
        possible = self.__get_possible_arg_vals(len(self.variables))
        #print(possible)
        self.__get_positive_results(possible, self.variables, self.rpn)

import itertools

class Quine_McCluskey_simplifier:

    def __init__(self, operators, variables, rpn):
        self.operators = operators
        self.variables = variables
        self.rpn = rpn

    def __get_possible_arg_vals(self, arg_num):
        return list(itertools.product(range(2), repeat=arg_num))

    def __evaluate_expression(self, values):
        rpn2 = self.rpn[:]
        for el in rpn2:
            if el in values.keys():
                rpn2[rpn2.index(el)] = values[el]
                #print(values[el])
        #print(self.rpn)
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

    def __get_positive_results(self, possible_vals):
        positive = []
        #print(rpn)
        for value in possible_vals:
            vals_list = list(value)
            # print(vals_list)
            # print(rpn)
            dictionary = dict(zip(self.variables, vals_list))
            # print(dictionary)
            if self.__evaluate_expression(dictionary):
                positive.append(vals_list)
        # print("positive ", positive)
        return positive

    def __sort_by_number_of_1(self, positive_res):
        result = []
        for i in range (0, len(self.variables)+1):
            tmp = filter(lambda x: sum(x) == i, positive_res)
            result += [list(tmp)]
        return result

    def simplify(self):
        possible = self.__get_possible_arg_vals(len(self.variables))
        # print("poss ", possible)
        positive_results = self.__get_positive_results(possible)
        sorted = self.__sort_by_number_of_1(positive_results)
        print(sorted)
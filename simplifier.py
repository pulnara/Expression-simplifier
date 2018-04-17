import itertools
from collections import OrderedDict

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
        dicti = {}
        for i in range (0, len(possible_vals)):
            value = possible_vals[i]
            vals_list = list(value)
            # print(vals_list)
            # print("fffs", self.rpn)
            dictionary = dict(zip(self.variables, vals_list))
            print(dictionary)
            if self.__evaluate_expression(dictionary):
                positive.append(vals_list)
                dicti[i] = vals_list
        # print("positive ", positive)
        return positive, dicti

    def __sort_by_number_of_ones(self, positive_res):
        result = []
        for i in range (0, len(self.variables)+1):
            tmp = filter(lambda x: sum(x) == i, positive_res)
            result += [list(tmp)]
        return result

    def __different_on_one_position(self, l1, l2):
        position = 0;
        for i in range (0, len(l1)):
            if l1[i] in [1, 0] and l2[i] in [1, 0] and l1[i] != l2[i]:
                if position > 0: return False
                position = i+1
        return position

    def __merge(self, el1, position):
        result = el1[:]
        result[position-1] = '-'
        return result

    def __get_number_of_ones(self, list):
        counter = 0
        for el in list:
            if el == 1: counter +=1
        return counter

    def __buid_expression(self, dictionary, positive_results):
        unique_simplified = []
        unique_rows = []
        for el in dictionary:
            # print(dictionary[el])
            if dictionary[el] not in unique_simplified:
                unique_simplified.append(dictionary[el])
                unique_rows.append(el)
        print(unique_simplified)
        print(unique_rows)

        matrix = [[0 for x in range(len(positive_results))] for y in range(len(unique_simplified))]

        values = list(positive_results.keys())
        for ind, value in enumerate(values):
            print(ind, value)
            for i in range(0, len(unique_rows)):
                el = unique_rows[i]
                if value in el:
                    matrix[i][ind] = 1

        for row in matrix:
            print(row)

    def __quine_mccluskey(self, values_dict):
        dictionary = values_dict
        matched = 1
        while matched:
            flag = 0
            # used = [][:]
            used = set()
            # print(used)
            print(dictionary)
            new_dict = {}
            k = list(dictionary.keys())
            for i in range(0, len(k)-1):
                flag = 0
                for j in range (i+1, len(k)):
                    el1 = dictionary[k[i]]; el2 = dictionary[k[j]]
                    if self.__get_number_of_ones(el1) + 1 == self.__get_number_of_ones(el2):
                        # print(el1, el2)
                        pos = self.__different_on_one_position(el1, el2)
                        if pos:
                            flag = 1
                            merged = self.__merge(el1, pos)
                            #print(merged)
                            if k[i].__class__ == tuple:
                                new_tuple = k[i] + k[j]
                            else:
                                new_tuple = k[i], k[j]
                            used.add(k[i])
                            used.add(k[j])
                            #print(new_tuple)
                            new_dict[new_tuple] = merged
            # used = list(set(used))
            print(used)
            for el in dictionary.keys():
                if el not in used: new_dict[el] = dictionary[el]
            # print(new_dict)
            dictionary = new_dict
            matched = flag
        print(dictionary)
        return dictionary

    def simplify(self):
        print(self.variables)
        print(self.rpn)
        possible = self.__get_possible_arg_vals(len(self.variables))
        print("poss ", possible)
        positive_results, dictionary = self.__get_positive_results(possible)
        # print(dictionary)
        print("posit", positive_results)

        if len(positive_results) == 0:
            print("Always false.")
            exit(0)


        d = {}
        for el in positive_results:
            d[int("".join(list(map(str,el))),2)] = el

        mccluskey_dict = self.__quine_mccluskey(d)
        result =  self.__buid_expression(mccluskey_dict, dictionary)
        # print("Simplified: ", result)
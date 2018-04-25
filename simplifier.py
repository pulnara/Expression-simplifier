import itertools

class Quine_McCluskey_simplifier:

    def __init__(self, operators, variables, rpn):
        self.operators = operators
        self.variables = variables
        self.rpn = rpn

    # gets all variations of possible arguments' values
    def __get_possible_arg_vals(self, arg_num):
        return list(itertools.product(range(2), repeat=arg_num))

    # evaluates given version of args' values
    def __evaluate_expression(self, values):
        rpn2 = self.rpn[:]
        for el in rpn2:
            if el in values.keys():
                rpn2[rpn2.index(el)] = values[el]

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
                elif el == "*":
                    stack.append(not (x and y))
            elif el == '~':
                x = stack.pop()
                stack.append(not x)
            else:
                stack.append(el)
        return stack.pop()

    # gets all versions of argument's values for which expression is true
    def __get_positive_results(self, possible_vals):
        positive = []
        dicti = {}
        if len(self.variables) == 0:
            result = self.__evaluate_expression({})

            if result:
                return "True", {}

            else:
                return "False", {}

        for i in range (0, len(possible_vals)):
            value = possible_vals[i]
            vals_list = list(value)
            dictionary = dict(zip(self.variables, vals_list))

            if self.__evaluate_expression(dictionary):
                positive.append(vals_list)
                dicti[i] = vals_list

        return positive, dicti

    # checks if given elements (f.e. [0, 0, 0] and [0, 0, 1]) differ on exactly one position, if yes - returns position
    def __different_on_one_position(self, l1, l2):
        position = 0
        for i in range (0, len(l1)):
            if ((l1[i] in [1, 0] and l2[i] in [1, 0]) or (l1[i] in [1, 0] and l2[i] == '-') or (l2[i] in [1, 0] and l1[i] == '-')) and l1[i] != l2[i]:
                if position > 0:
                    return False

                position = i+1

        return position

    # connects two elements that differ on one position (f.e. [0, 0, 1] + [0, 0, 0] = [0, 0, '-'])
    def __merge(self, el1, position):
        result = el1[:]
        result[position-1] = '-'
        return result

    # returns number of ones in element
    def __get_number_of_ones(self, list):
        counter = 0
        for el in list:
            if el == 1:
                counter += 1

        return counter

    # builds the last table in algorithm, chooses the least possible number of rows that cover all columns
    # builds the final expression
    def __build_expression(self, dictionary, positive_results):
        unique_simplified = []
        unique_rows = []

        for el in dictionary:
            if dictionary[el] not in unique_simplified:
                unique_simplified.append(dictionary[el])
                unique_rows.append(el)

        values_set = set()

        for el in unique_rows:
            if el.__class__ != int:
                for i in el:
                    values_set.add(i)
            else:
                values_set.add(el)

        matrix = [[0 for x in range(len(positive_results))] for y in range(len(unique_simplified))]
        values = list(positive_results.keys())

        for ind, value in enumerate(values):
            for i in range(0, len(unique_rows)):
                el = unique_rows[i]
                if el.__class__ == int and value == el or value in el:
                    matrix[i][ind] = 1

        flag = 1
        used = []
        dots = 1
        rows_taken = set()

        while flag:
            for j in range(0, len(values)):
                counter = 0
                tmp = -1

                for i in range(0, len(unique_rows)):
                    if matrix[i][j] == 1:
                        counter += 1
                        tmp = i

                if counter == dots:
                    for i in range(0, len(values)):
                        if matrix[tmp][i] == 1 and values[i] not in used:
                            used.append(values[i])
                            rows_taken.add(unique_rows[tmp])

            if set(used) == set(values_set):
                flag = 0

            else:
                dots += 1

        res = ""

        for index, i in enumerate(unique_simplified):
            for el in rows_taken:
                if dictionary[el] == i:
                    for j in range(len(i)):
                        if i[j] == 1:
                            if res != "" and res[len(res)-1] not in['|', '&']: res += "&"
                            res += self.variables[j]

                        elif i[j] == 0:
                            if res != "" and res[len(res)-1] not in['|', '&']: res += "&"
                            res += "~" + str(self.variables[j])

                    if index < len(unique_simplified)-1:
                        res += "|"
        return res

    # main part of Quine-McCluskey algorithm - minimizes function by searching for all matches
    def __quine_mccluskey(self, values_dict):
        dictionary = values_dict
        matched = 1

        while matched:
            # used = [][:]
            used = set()
            new_dict = {}
            k = list(dictionary.keys())
            flag = 0

            for i in range(0, len(k)-1):
                for j in range(i+1, len(k)):
                    el1 = dictionary[k[i]]; el2 = dictionary[k[j]]
                    if abs(self.__get_number_of_ones(el1)-self.__get_number_of_ones(el2)) == 1:
                        pos = self.__different_on_one_position(el1, el2)
                        if pos:
                            flag = 1
                            merged = self.__merge(el1, pos)

                            if k[i].__class__ == tuple:
                                new_tuple = k[i] + k[j]

                            else:
                                new_tuple = k[i], k[j]

                            used.add(k[i])
                            used.add(k[j])
                            new_dict[new_tuple] = merged

            for el in dictionary.keys():
                if el not in used: new_dict[el] = dictionary[el]

            dictionary = new_dict
            matched = flag

        return dictionary

    # main function that manages simplifying
    def simplify(self):
        possible = self.__get_possible_arg_vals(len(self.variables))

        positive_results, dictionary = self.__get_positive_results(possible)

        if len(positive_results) == 0 or positive_results == "False":
            return "0"

        if positive_results == "True":
            return "1"

        d = {}

        for el in positive_results:
            d[int("".join(list(map(str, el))), 2)] = el

        mccluskey_dict = self.__quine_mccluskey(d)

        for el in mccluskey_dict.values():
            flag = 1
            for i in el:
                if i != '-': flag = 0

            if flag:
                return "1"

        result =  self.__build_expression(mccluskey_dict, dictionary)

        return result

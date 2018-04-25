class Validator(object):

    def __init__(self, operators, characters):
        self.operators = operators
        self.characters = characters

    def validate(self, ex):
        ##    & - conjunction,
        ##    | - alternative,
        ##    ^ - xor,
        ##    ~ - negation,
        ##    > - implication,
        ##    = - equivalence
        ##    * - nand
        ex = ex.strip()
        last = ''
        var = 0

        # checks if there are: spaces between variables, invalid characters
        for i in ex:
            if i in self.characters:
                if last == ' ' and var == 1:
                    raise ValueError("invalid variables sequence")
                var = 1

            elif i in self.operators.keys():
                var = 0

            elif i not in "()" + ' ':
                raise ValueError("invalid character")

            last = i

        ex = "".join(ex.split())

        # simple enum
        NUMBER, LETTER, OPERATOR, L_BRACKET, R_BRACKET = range(0, 5)

        # checks grammar, brackets and variables' names
        flag = 0
        prev = None
        bracket_stack = []

        for i in ex:
            if i in self.characters:
                if prev in [R_BRACKET]: raise ValueError("incorrect brackets")

                if prev in [NUMBER] and flag == 0:
                    raise ValueError("variable starting with a number")

                if i.isnumeric():
                    if prev in [None, OPERATOR, L_BRACKET, R_BRACKET]:
                        if int(i) not in [0, 1]:
                            raise ValueError("variable starting with a number")

                    if prev == LETTER:
                        flag = 1
                    prev = NUMBER

                else:
                    flag = 0
                    prev = LETTER

            elif i in self.operators.keys():
                if prev in [None, OPERATOR, L_BRACKET] and i != '~':
                    raise ValueError("binary operator used as an unary")

                if prev in [R_BRACKET, LETTER, NUMBER] and i == '~':
                    raise ValueError("unary operator used as a binary")
                prev = OPERATOR

            elif i == '(':
                if prev in [LETTER, NUMBER, R_BRACKET]:
                    raise ValueError("incorrect brackets")
                prev = L_BRACKET
                bracket_stack.append(L_BRACKET)

            elif i == ')':
                if len(bracket_stack) == 0:
                    raise ValueError("incompatible brackets")
                bracket_stack.pop()

                if prev in [OPERATOR, L_BRACKET]:
                    raise ValueError("incorrect brackets")
                prev = R_BRACKET

        if prev == OPERATOR:
            raise ValueError("operator shouldn't be at the end")

        if len(bracket_stack) > 0:
            raise ValueError("incompatible brackets")

        return ex

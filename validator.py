class Validator(object):

    def __init__(self, operators, characters):
        self.operators = operators
        self.characters = characters

    def validate(self, ex):
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

        # checks if there are spaces between variables or invalid characters
        for i in ex:
            if i in self.characters:
                if last == ' ' and var == 1:
                    #print(i)
                    raise ValueError("invalid variables sequence")
                var = 1
            elif i in self.operators.keys():
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
            if i in self.characters:
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
            elif i in self.operators.keys():
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

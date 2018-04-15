import sys

operators = "|&^~>="
variables = "".join([chr(i) for i in range(97, 123)]) + "".join([chr(i) for i in range(65, 91)]) + "".join(list(map(str, range(10))))


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
    
    # checks if there are spaces between variables or invalid characters 
    for i in ex:
        if i in variables:
            if last == ' ' and var == 1:
                #print(i)
                error("invalid variables sequence")
            var = 1
        elif i in operators:
            var = 0
        elif i not in "()" + ' ':
            error("invalid character")
        before_last = last
        last = i
    ex = "".join(ex.split())
    
    # simple enum
    Number, Letter, Operator, L_Bracket, R_Bracket = range(0, 5)
    
    flag = 0
    prev = None
    bracket_stack = []
    for i in ex:
        if i in variables:
            if prev in [R_Bracket]: error("incorrect brackets")
            if prev in [Number] and flag == 0: error("variable starting with a number")
            if i.isnumeric():
                if prev in [None, Operator, L_Bracket, R_Bracket]:
                    if int(i) not in [0, 1]:
                        error("variable starting with a number")
                if prev == Letter:
                    flag = 1
                prev = Number
            else:
                flag = 0
                prev = Letter      
        elif i in operators:
            if prev in [None, Operator] and i != '~': error("binary operator used as an unary")
            prev = Operator
        elif i == '(':
            if prev in [Letter, Number, R_Bracket]: error("incorrect brackets")
            prev = L_Bracket
            bracket_stack.append(L_Bracket)
            
        elif i == ')':
            if len(bracket_stack) == 0: error("incompatible brackets")
            bracket_stack.pop()
            if prev in [Operator, L_Bracket]: error("incorrect brackets")
            prev = R_Bracket            
            
    if prev == Operator: error("operator shouldn't be at the end")           
    if len(bracket_stack) > 0: error("incompatible brackets")
    return ex
            

def error(info):
    print("Error: " + info)
    exit(1)
    
    
def main():
    if len(sys.argv) < 2:
        error("no expression given")
    elif len(sys.argv) > 2:
        error("too many arguments given")
    expr = sys.argv[1]
    #print(expr)
    expr = validate(expr)
    print(expr)
    #print(check_brackets_and_states(expr))
    
    
if __name__ == "__main__":
    main()
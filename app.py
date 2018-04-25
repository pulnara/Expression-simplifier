from validator import Validator
from converter import RPN_converter
from simplifier import Quine_McCluskey_simplifier
import sys
import string

def process(expr):
    operators = {'|': 1, '&': 2, '^': 1, '~': 3, '>': 0, '=': 0, '*': 2}
    characters = string.ascii_lowercase + string.ascii_uppercase + "".join(list(map(str, range(10))))
    try:
        validator = Validator(operators, characters)
        expr = validator.validate(expr)
        converter = RPN_converter(operators, characters)
        rpn, variables = converter.convert(expr)
        print("RPN: ", rpn)
        simplifier = Quine_McCluskey_simplifier(operators, variables, rpn)
        result = simplifier.simplify()
        print("Simplified: ", result)
        return result
    except ValueError as e:
        print("Error: " + str(e))
        exit(1)

def main():

    try:
        if len(sys.argv) < 2:
            raise Exception("no expression given")
        elif len(sys.argv) > 2:
            raise Exception("too many arguments given")
        expr = sys.argv[1]
        print("Input expression: ", expr)
        process(expr)
    except Exception as e:
        print("Error: " + str(e))
        exit(1)

if __name__ == "__main__":
    main()

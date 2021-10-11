import sys
from typing import List
from enum import Enum, auto
import logging
logging.basicConfig()
logging.root.setLevel(logging.WARNING)
logger = logging.getLogger("TCL_Machine")

from tokenizer.Tokenizer import Tokenizer, TT

# define the datatypes that are supported by the language
class DATTYP(Enum):
    INT = auto()

print("Tcl/Forth inspired language")

class TCL_machine:
    def run(self, cli_args : List[str]):
        if cli_args[0] == "exe":
            self.contents = self.load_file_contents(cli_args[1])
        
            logger.info("Starting to interpret code")
            # handle program operations on the stack
            self.stack = [] # initialize empty stack

            # Tokenize the contents of the file
            self.izer = Tokenizer(self.contents)

            self.typecheck_program(self.contents)
            self.stack = []
            self.interpret()
        elif cli_args[0] == "build":
            self.contents = self.load_file_contents(cli_args[1])
            self.compile()
        else:
            raise Exception(f"This Value should be 'exe' or 'build' ->{cli_args[0]}<-")
    
    def load_file_contents(self, path):
        with open(path) as f:
            return f.read()

    def compile(self):
        raise Exception("compiler not implemented")


    def typecheck_program(self, contents):
        lexer = Tokenizer(contents)

        while lexer.has_more_tokens():
            token = lexer.advance()
            match token[0]:
                case TT.INT_CONST:
                    self.stack.append(DATTYP.INT)
                case TT.COMMENT:
                    pass # ignore them comments
                case TT.COMPARISON:
                    if len(self.stack) < 2:
                        raise ValueError(f"Interpreter does not have 2 values to compare from the stack\nToken at line:{token[2]} column:{token[3]}")
                    self.stack.pop() # eq to 2 pops and a push because there is not a difference in datatype for the boolean ??YET??
                case TT.KEYWORD:
                    match token[1]:
                        case "print":
                            if len(self.stack) == 0:
                                raise ValueError(f"Interpreter has nothing to print from the stack\nToken at line:{token[2]} column:{token[3]}")
                            self.stack.pop()
                        case _:
                            raise Exception(f"UnImplemented keyword for the type checker:->{token[1]}<-")
                case _:
                    raise Exception(f"UnImplemented instruction for the type checker:->{token[0]}<-")

    def interpret(self):
        while self.izer.has_more_tokens(): # go through the program until there are no more tokens
            token = self.izer.advance()
            logger.info(token)
            self.interpret_token(token)

    def interpret_token(self, token):
        match token[0]: # match the tokentype
            case TT.COMMENT:
                pass # we ignore comments
            case TT.INT_CONST:
                self.stack.append(token[1])
            case TT.KEYWORD:
                self.interpret_keyword(token) # handle the keyword
            case TT.COMPARISON:
                if token[1] == "==":
                    y = self.stack.pop()
                    x = self.stack.pop()
                    if x == y:
                        self.stack.append(1)
                    else:
                        self.stack.append(0)
                else:
                    raise Exception(f"Interpreter does not handle this comparison ->{token[1]}<-")
            case _:
                raise Exception(f"Interpreter does not handle tokentype ->{token[0]}<-")

    def interpret_keyword(self, token):
        match token[1]:
            case "print":
                print(self.stack.pop())
            case _:
                raise Exception(f"Interpreter does not handle keyword ->{token[1]}<-")

# give some information about how to use from the cli
def cli_reference():
    print("""py pytcl.py <exe | build> <path> 
    Please First tell me the mode we are in 'exe' or 'build'
    then give me the program path""")


if __name__ == '__main__':
    if len(sys.argv) < 3:
        cli_reference()
        raise Exception("Please give the right amount of parameters to the program")

    machine = TCL_machine()
    # give the cli args to the machine
    machine.run(sys.argv[1:])
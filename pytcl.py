import sys
from typing import List
import logging
logging.basicConfig()
logging.root.setLevel(logging.WARNING)
logger = logging.getLogger("TCL_Machine")

from tokenizer.Tokenizer import Tokenizer, TT

print("Tcl/Forth inspired language")

class TCL_machine:
    def run(self, cli_args : List[str]):
        if cli_args[0] == "exe":
            self.contents = self.load_file_contents(cli_args[1])
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

    def interpret(self):
        logger.info("Starting to interpret code")

        # handle program operations on the stack
        self.stack = [] # initialize empty stack

        # Tokenize the contents of the file
        self.izer = Tokenizer(self.contents)

        while self.izer.has_more_tokens():
            token = self.izer.advance()
            logger.info(token)
            match token[0]: # match the tokentype
                case TT.COMMENT:
                    continue # we ignore comments
                case TT.INT_CONST:
                    self.stack.append(token[1])
                case TT.KEYWORD:
                    # handle the keyword
                    match token[1]:
                        case "print":
                            # TODO: Make typechecker that handles this edgecase so it does not have to be here
                            if len(self.stack) == 0:
                                line = token[2]
                                col = token[3]
                                err_msg = f"Interpreter has nothing to print from the stack\nToken at line:{line} column:{col}"
                                raise ValueError(err_msg)
                            print(self.stack.pop())
                        case _:
                            raise Exception(f"Interpreter does not handle keyword ->{token[1]}<-")
                case TT.COMPARISON:
                    # TODO: Make typechecker that handles this edgecase so it does not have to be here
                    if token[1] == "==":
                        if len(self.stack) < 2:
                            line = token[2]
                            col = token[3]
                            err_msg = f"Interpreter does not have 2 values to compare from the stack\nToken at line:{line} column:{col}"
                            raise ValueError(err_msg)
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
import sys
from typing import List
from enum import Enum, auto
from parse_ctl import Parse, CmdType, DatType, BinOp, CmdValue
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

            logger.info("Starting to interpret code")
            # handle program operations on the stack
            self.stack = [] # initialize empty stack
            self.ip = 0     # instruction pointer pointing to an index in the instruction list

            # Parse the contents of the file into a stream of commands
            self.cmd_stream = Parse(self.contents).parse() # function should return a generator


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

    def interpret(self): # use self.cmd_stream to interpret the commands from the source program
        cmds = [cmd for cmd in self.cmd_stream] # list all instructions for now

        logger.info("the program:")
        while self.ip < len(cmds):
            logger.info(cmds[self.ip])
            match cmds[self.ip].cmd:
                case CmdType.COMMENT:
                    self.ip += 1
                case CmdType.PUSH:
                    logger.info(cmds[self.ip])
                    self.stack.append(cmds[self.ip].value) # give the token whichs value should be pushed to the stack
                    self.ip += 1
                case CmdType.PRINT:
                    logger.info(self.stack)
                    val = self.stack.pop()
                    match val.typ:
                        case DatType.INT:
                            print(val.value)
                        case _:
                            raise Exception(f"Interpreter PRINT command unhandled datatype ->{val}<-")
                    self.ip += 1
                case CmdType.BINOP:
                    op = cmds[self.ip].value
                    match op:
                        case BinOp.EQ:
                            logger.info(self.stack)
                            # checking for equality
                            y_val = self.stack.pop()
                            x_val = self.stack.pop()
                            if x_val == y_val:
                                self.stack.append(CmdValue("1", DatType.INT))
                            else:
                                self.stack.append(CmdValue("0", DatType.INT))
                        case _:
                            raise Exception(f"Interpreter Binary operation unhandled ->{op}<-")
                    self.ip += 1


                    # self.binop_handler(cmds[self.ip].value)
                case _:
                    raise Exception(f"UnImplemented .cmd in interpreter command ->{cmds[self.ip]}<-")


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

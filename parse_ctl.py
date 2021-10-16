#!/usr/bin/env python
from enum import Enum, auto
from dataclasses import dataclass
from tokenizer.Tokenizer import Tokenizer, TT
import logging
logging.basicConfig() # Warning do not set_level use pytcl for changing that
logger = logging.getLogger("TCL_Parser")

# basic datatypes handled in the parsed version of the programming language
class DatType(Enum):
    INT = auto()
    STR = auto()

# splitoff binary operations
class BinOp(Enum):
    EQ = auto()

# commands that will run on the machine
class CmdType(Enum):
    PUSH = auto()
    POP = auto()
    COMMENT = auto()
    PRINT = auto()
    BINOP = auto()

@dataclass
class CmdValue: # a single value for the push command
    value : str
    typ : DatType

# the command structure that will be send to the machine
@dataclass
class Cmd:
    cmd : CmdType
    value : CmdValue
    meta : TT
    ip  : int


# parser that turns token data into commands for the TCL_machine
class Parse:
    def __init__(self, program_txt):
        "parse is initialized with the contents of the program"
        self.contents = program_txt
        self.stack = []
        self.izer = Tokenizer(program_txt)
        self.instr = 0 # keep track of the instruction index in the list

    def parse(self):
        "yields the commands from the tokenizer one by one for the machine"
        while self.izer.has_more_tokens(): # go through the program until there are no more tokens
            token = self.izer.advance()
            logger.info(token)
            match token.typ:
                case TT.COMMENT:
                    yield Cmd(CmdType.COMMENT, CmdValue(token.value, DatType.STR), token, self.instr)
                    self.instr += 1
                case TT.INT_CONST:
                    yield Cmd(CmdType.PUSH, CmdValue(token.value, DatType.INT), token, self.instr)
                    self.instr += 1
                case TT.KEYWORD:
                    yield self.handle_keyword(token)
                    self.instr += 1
                case TT.COMPARISON:
                    yield Cmd(CmdType.BINOP, BinOp.EQ, token, self.instr)
                    self.instr += 1
                case _:
                    raise Exception(f"UnImplemented token in the parser ->{token}<-")

    def handle_keyword(self, token):
        match token.value:
            case 'print':
                return Cmd(CmdType.PRINT, None, token, self.instr)
            case _:
                raise Exception(f"UnImplemented keyword in the parser ->{token}<-")



    # def typecheck_program(self, contents):
    #     lexer = Tokenizer(contents)

    #     while lexer.has_more_tokens():
    #         token = lexer.advance()
    #         match token[0]:
    #             case TT.INT_CONST:
    #                 self.stack.append(DatType.INT)
    #             case TT.COMMENT:
    #                 pass # ignore them comments
    #             case TT.COMPARISON:
    #                 if len(self.stack) < 2:
    #                     raise ValueError(f"Interpreter does not have 2 values to compare from the stack\nToken at line:{token[2]} column:{token[3]}")
    #                 self.stack.pop() # eq to 2 pops and a push because there is not a difference in datatype for the boolean ??YET??
    #             case TT.KEYWORD:
    #                 match token[1]:
    #                     case "print":
    #                         if len(self.stack) == 0:
    #                             raise ValueError(f"Interpreter has nothing to print from the stack\nToken at line:{token[2]} column:{token[3]}")
    #                         self.stack.pop()
    #                     case _:
    #                         raise Exception(f"UnImplemented keyword for the type checker:->{token[1]}<-")
    #             case _:
    #                 raise Exception(f"UnImplemented instruction for the type checker:->{token[0]}<-")

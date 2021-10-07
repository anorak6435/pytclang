from enum import Enum, auto
from typing import Tuple
import re
import logging
logging.basicConfig()
logging.root.setLevel(logging.NOTSET)
logger = logging.getLogger("TCL_Tokenizer")

# the tokens that will be recognized by the tokenizer
class TT(Enum):
    COMMENT = auto()

class Tokenizer:
    def __init__(self, file_contents):
        "start the tokenizer with the contents of the source_file"
        self.contents = file_contents
        # keep track of the line in the document
        self.line = 1

    def has_more_tokens(self) -> bool:
        "check if there is more source to tokenize"
        return len(self.contents) > 0

    def remove_whitespace(self):
        "whitespace removed from the stat of self.contents"
        m = re.match(r"\s+", self.contents)
        if m:
            self.contents = self.contents[len(m[0]):]
    
    def advance(self) -> Tuple:
        "Get the next token from the input file only called when self.has_more_tokens == True"
        self.remove_whitespace()

        if self.is_comment():
            return self.get_comment()
        else:
            raise Exception(f"No tokens found by tokenizer in ->{self.contents}<-")

    ## --------------------
    ## COMMENT functions
    ## --------------------

    def is_comment(self) -> bool:
        "check if the first part of self.contents is a comment"
        return bool(re.match(r"\#[^\n]*", self.contents))

    def get_comment(self):
        "returns comment at the start of self.contents only call if self.is_comment() == True"
        val = re.match(r"\#[^\n]*", self.contents)
        # update self. contents
        self.contents = self.contents[len(val[0]):]
        return (TT.COMMENT, val[0], self.line)# return the token
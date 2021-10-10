from enum import Enum, auto
from typing import Tuple
import re
import logging
logging.basicConfig() # Warning do not set_level use pytcl for changing that
logger = logging.getLogger("TCL_Tokenizer")

# the tokens that will be recognized by the tokenizer
class TT(Enum):
    COMMENT = auto()    # comment
    INT_CONST = auto()  # integer constant
    KEYWORD = auto()    # keyword
    COMPARISON = auto() # comparison

class Tokenizer:
    def __init__(self, file_contents):
        "start the tokenizer with the contents of the source_file"
        self.contents = file_contents
        # keep track of the line in the document
        self.line = 1
        self.col = 0
        # keywords that are recognised by the tokenizer
        keywords_txt = ["print"]
        # compile keywords ahead
        self.keywords = [re.compile(word) for word in keywords_txt]
        self.comparisons = ["=="]

    def has_more_tokens(self) -> bool:
        "check if there is more source to tokenize"
        return len(self.contents) > 0

    def is_new_line(self) -> bool:
        return bool(re.match(r"[\r\n]", self.contents))

    def remove_new_line(self):
        "removes the new line char from self.contents only call if self.is_new_line() == True"
        m = re.match(r"[\r\n]", self.contents)
        self.col = 0
        self.contents = self.contents[len(m[0]):]

    def remove_whitespace(self):
        "whitespace removed from the start of self.contents"
        m = re.match(r"[\t\f\v ]+?", self.contents)
        if m:
            self.contents = self.contents[len(m[0]):]
            self.col += len(m[0])

    def is_whitespace(self) -> bool:
        return bool(re.match(r"\s+?", self.contents))

    def handle_whitespace(self):
        while self.is_whitespace():
            self.remove_whitespace()
            if self.is_new_line():
                self.remove_new_line()
                self.line += 1
    
    def advance(self) -> Tuple:
        "Get the next token from the input file only called when self.has_more_tokens == True"
        self.handle_whitespace()

        if self.is_comment():
            return self.get_comment()
        elif self.is_int_const():
            return self.get_int_const()
        elif self.is_keyword():
            return self.get_keyword()
        elif self.is_comparison():
            return self.get_comparison()
        else:
            raise Exception(f"No tokens found by tokenizer in ->{self.contents}<-")


    ## --------------------
    ## COMPARISONS functions
    ## --------------------
    def is_comparison(self) -> bool:
        "check if the first part if self.contents is a comparison"
        return any([bool(re.match(val, self.contents)) for val in self.comparisons])
        
    def get_comparison(self):
        "returns the comparison at the beginning of self.contents only call if self.is_comparison() == True"
        for comp in self.comparisons:
            val = re.match(comp, self.contents)
            if val:
                self.contents = self.contents[len(val[0]):]
                column = self.col
                self.col += len(val[0])
                return (TT.COMPARISON, val[0], self.line, column)

    ## --------------------
    ## KEYWORD functions
    ## --------------------
    def is_keyword(self) -> bool:
        "check if the first part of self.contents is a keyword"
        return any([bool(word.match(self.contents)) for word in self.keywords])

    def get_keyword(self):
        "returns the keyword at the beginning of self.contents only call if self.is_keyword() == True"
        for word in self.keywords:
            val = word.match(self.contents)
            if val:
                self.contents = self.contents[len(val[0]):]
                column = self.col
                self.col += len(val[0])
                return (TT.KEYWORD, val[0], self.line, column)

    ## --------------------
    ## INT_CONST functions
    ## --------------------
    def is_int_const(self) -> bool:
        "check if the first part of self.contents is a integer constant"
        return bool(re.match(r"\d+", self.contents))

    def get_int_const(self):
        "returns the int constant at the beginning of self.contents only call if self.is_int_const() == True"
        val = re.match(r"\d+", self.contents)
        self.contents = self.contents[len(val[0]):]
        column = self.col
        self.col += len(val[0])
        return (TT.INT_CONST, int(val[0]), self.line, column)

    ## --------------------
    ## COMMENT functions
    ## --------------------
    def is_comment(self) -> bool:
        "check if the first part of self.contents is a comment"
        return bool(re.match(r"\#[^\n]*", self.contents))

    def get_comment(self):
        "returns comment at the start of self.contents only call if self.is_comment() == True"
        val = re.match(r"\#[^\n]*", self.contents)
        self.contents = self.contents[len(val[0]):]
        column = self.col
        self.col += len(val[0])
        return (TT.COMMENT, val[0], self.line, column)
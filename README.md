# PYTCLang
TCL And Forth Inspired Language
*reverse pollish notation used for the language*

# quick start
pyctlang> py .\pytcl.py
to know you can call the interpreter
```
pyctlang> py .\pytcl.py
Tcl/Forth inspired language
py pytcl.py <exe | build> <path> 
    Please First tell me the mode we are in 'exe' or 'build'      
    then give me the program path
Traceback (most recent call last):
	ect...
```

call pyctlang> py .\pytcl.py 'exe' .\test\comment.ptcl
to interpret a test file


## printing a integer to the command line

### print
Take the top value from the stack and print it
```
2 print
4 print
8 print
16 print
32 print
```
#### outputs
```
2
4
8
16
32
```

## Comparisons
== pop the top 2 values from the stack
if they are equal push 1 (truthy) else push 0 (false)

```
23 32 == print
155 155 == print
```
#### outputs
```
0
1
```

## If statement
when we encounter an If statement we check the top value from the stack.
If 1 (truty) run the instructions following the if statement
If 0 (false) skip the instructions in the if statement and jump to the matching end keyword

1 if 42 print end # print this
0 if 43 print end # don't print this
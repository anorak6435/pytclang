from pytcl import TCL_machine
import os
import logging
logging.basicConfig()
logging.root.setLevel(logging.NOTSET)
logger = logging.getLogger("TCL_TESTER")

# go into the test file directory
for f in os.listdir("./test"):
    # get the language test files
    if f.endswith(".ptcl"):
        print("TESTING file:", f)
        p = os.path.join("./test", f)
        machine = TCL_machine() # create a new machine for this test file
        machine.run(["exe", p]) # run this test file on the machine



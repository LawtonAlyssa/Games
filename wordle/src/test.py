from main import *
from time import time

def runTest(name, func, sol, *args, **kwargs):
    crashed = False
    startTime = time()
    try:
        attempt = func(*args, **kwargs)
    except:
        crashed = True
    elapsedTime = time() - startTime
    print("{}: {} ({}s)".format(name, "CRASH" if crashed else ("PASS" if attempt == sol else "Fail"), round(elapsedTime, 3)))

def positiveWordFiltrationTest():
    runTest("pos1", positiveListFiltration, ["abc"], letter_loc=[0,1,2], word_solution="abc", words_list=["abc", "def"])
    runTest("pos2", positiveListFiltration, ["abc", "dec"], letter_loc=[2], word_solution="abc", words_list=["abc", "def", "dec"])

def main():
    positiveWordFiltrationTest()

if __name__=="__main__":
    main()
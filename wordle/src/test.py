from main import *
from time import time
import traceback

def runTest(name, func, sol, *args, **kwargs):
    crashed = False
    startTime = time()
    try:
        attempt = func(*args, **kwargs)
    except:
        crashed = True
        attempt = None
        traceback.print_exc()
    elapsedTime = time() - startTime
    passTest = attempt == sol
    print("{}: {} ({}s)".format(name, "CRASH" if crashed else ("PASS" if passTest else "Fail"), round(elapsedTime, 3)))
    print("\n------------------------------------------------------")
    return 1 if passTest else 0

def positiveWordFiltrationTest():
    testCount = 2

    correct = 0
    correct += runTest("pos1", positiveListFiltration, ["abc"], letter_locs=[0,1,2], word_solution="abc", words_list=["abc", "def"])
    correct += runTest("pos2", positiveListFiltration, ["abc", "dec"], letter_locs=[2], word_solution="abc", words_list=["abc", "def", "dec"])
    print("Total:", round(100 * correct / testCount, 2), "%")

def main():
    positiveWordFiltrationTest()

if __name__=="__main__":
    main()
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
        print("\n------------------------------------------------------")
        traceback.print_exc()
    elapsedTime = time() - startTime
    passTest = attempt == sol
    print("{:16}: {} ({}s){}".format(name, "CRASH" if crashed else ("PASS" if passTest else "FAIL"), round(elapsedTime, 3), "" if passTest else " - Attempt: {}".format(attempt)))
    return 1 if passTest else 0

def positiveWordFiltrationTest():
    return [
        runTest("pos1", positiveListFiltration, ["abc"], letter_locs=[0,1,2], word_solution="abc", words_list=["abc", "def"]),
        runTest("pos2", positiveListFiltration, ["abc", "dec"], letter_locs=[2], word_solution="abc", words_list=["abc", "def", "dec"]),
        runTest("pos3", positiveListFiltration, [], letter_locs=[0,1,2], word_solution="abc", words_list=["aaa", "bbb", "ccc", "abb", "aac", "aba"]),
        runTest("pos4", positiveListFiltration, ["add"], letter_locs=[0], word_solution="abc", words_list=["add", "bbc", "bcc", "cbc"]),
        runTest("pos5", positiveListFiltration, ["abc", "def", "dec"], letter_locs=[], word_solution="abc", words_list=["abc", "def", "dec"]),
    ]
    

def main():
    print("Running Tests\n")
    runs = []
    runs += positiveWordFiltrationTest()
    print("--------------------------------------------")
    print("Total: {}/{} ({}%)".format(sum(runs), len(runs), round(100 * sum(runs) / len(runs), 2)))

if __name__=="__main__":
    main()
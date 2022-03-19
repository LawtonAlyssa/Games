from main import *

def negativeWordFiltrationTest():
    word_solution = "peeps"
    words_list = ['apple', 'green', 'label', 'zebra', 'range']
    letter_locs = [0, 1]
    neg_words_list = negativeWordFiltration(letter_locs=letter_locs, word_solution=word_solution, words_list=words_list)
    expected_results = ['apple', 'green', 'label', 'range']
    print("PASS" if neg_words_list == expected_results else "FAIL")

def main():
    negativeWordFiltrationTest()
    
if __name__ == "__main__":
    main()
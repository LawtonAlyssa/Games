def getWords():
    words = 'assets/words.txt'
    with open(words) as f: 
        return f.read().splitlines()
    
def negativeWordFiltration(letter_locs, word_solution, words_list):
    neg_words_list = words_list
    for letter_loc in letter_locs:
        neg_words_list = [word for word in neg_words_list if word[letter_loc] is not word_solution[letter_loc]]
    return neg_words_list

def main():
    words_list = getWords()
    words_length = len(words_list)
    # print("\n".join(words_list))
    print(words_length)
    
    
if __name__=="__main__":
    main()
def getWords():
    words = 'assets/words.txt'
    with open(words) as f: 
        return f.read().splitlines()
    
def positiveListFiltration(letter_loc, word_solution, words_list):
    return [word for word in words_list if word[letter_loc] is word_solution[letter_loc]]
        
    

def main():
    words_list = getWords()
    words_length = len(words_list)
    # print("\n".join(words_list))
    print(words_length)
    pos_words_list = positiveListFiltration(letter_loc=0, word_solution="apple", words_list=words_list)
    print(pos_words_list)
    
if __name__=="__main__":
    main()
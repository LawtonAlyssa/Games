def getWords():
    words = 'assets/words.txt'
    with open(words) as f: 
        return f.read().splitlines()

def main():
    words_list = getWords()
    words_length = len(words_list)
    # print("\n".join(words_list))
    print(words_length)
    
if __name__=="__main__":
    main()
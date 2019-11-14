from string import punctuation
from stemming.porter2 import stem
from random import randrange

f = open("stop_words.txt")
stopwords = [line.replace("\n", "") for line in f]
f.close()

def fiveMostCommon(my_list):
    freq = {} 
    for items in my_list: 
        freq[items] = my_list.count(items) 
    sorted_x = sorted(freq.items(), key=lambda kv: kv[1])
    sorted_x = sorted_x[-5:]
    a = []
    for (i,j) in sorted_x:
        a.append(i)
    return a

def ex8():
    ex8 = {}
    with open("Godfather.txt", encoding="UTF-8") as f:
        words = [word for line in f for word in line.split()]
        words = [word.lower().translate(str.maketrans('', '', punctuation)) for word in words]
        filtered_words = [w for w in words if not w in stopwords]
        #filtered_words = [stem(word) for word in filtered_words]
        last = ""
        for word in filtered_words:
            if len(last)>0:
                if last in ex8:
                    ex8[last].append(word)
                else:
                    ex8[last] = [word]
            last = word
        for item in ex8:
            if len(ex8[item]) > 5:
                ex8[item] = fiveMostCommon(ex8[item])
        return ex8

def generate_random_paragraph(dict, first_word, nr):
    currWord = first_word
    generated = ""
    for i in range(0, nr):
        length = len(dict[currWord])
        currWord = dict[currWord][randrange(length)]
        generated+=" "+currWord
    return generated

print(generate_random_paragraph(ex8(), "michael", 1000))
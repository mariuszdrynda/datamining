from string import punctuation
from stemming.porter2 import stem
from itertools import groupby
import numpy as np

#EXERCISE 5

def saveToFile(grouped_pairs, filename):
    ex5 = open(filename, "w")
    for (i,j) in grouped_pairs:
        if j < 200:
            for k in range(0,j):
                try:
                    #ex5.write(str(j)+" "+i+'\n')
                    ex5.write(i+'\n')
                except:
                    pass
    ex5.close()

f = open("stop_words.txt")
stopwords = [line.replace("\n", "") for line in f]
f.close()

with open("Godfather.txt", encoding="UTF-8") as f:
    words = [word for line in f for word in line.split()]
    words = [word.lower().translate(str.maketrans('', '', punctuation)) for word in words]
    filtered_words = [w for w in words if not w in stopwords]
    #filtered_words = [stem(word) for word in filtered_words]
    pairs = [(w,1) for w in filtered_words]
    pairs.sort()
    word = lambda pair : pair[0]
    grouped_pairs = [(w, sum(1 for _ in g)) for w, g in groupby(pairs, key=word)]
    occurrences = lambda pair: pair[1]
    grouped_pairs.sort(key=occurrences, reverse=True)
    saveToFile(grouped_pairs, "ex5.txt")

    #Build a word-cloud from the obtained list. You can use the service http://www.wordclouds.com/

#EXERCISE 6

number_of_docs_where_the_word_appears = {}

def calculate_number_of_docs_where_the_word_appears(allWords):
    global number_of_docs_where_the_word_appears
    for word in allWords:
        key = word[0]
        if key in number_of_docs_where_the_word_appears:
            number_of_docs_where_the_word_appears[key] += 1
        else:
            number_of_docs_where_the_word_appears[key] = 1

def idf(word,nrOfChapters):
    
    if word in number_of_docs_where_the_word_appears:
        assert number_of_docs_where_the_word_appears[word] <= 32
        return np.log(nrOfChapters/1+number_of_docs_where_the_word_appears[word]).item()
    else:
        return np.log(nrOfChapters).item()

def tf_idf(word,nrOfChapters):
    return float(word[1]) * idf(word[0],nrOfChapters)

listOfTdIdf = []

def ex6():
    global listOfTdIdf
    all_grouped_pairs = []
    for i in range(1,33):
        chapter = "chapter"+str(i)+".txt"
        f = open(chapter)
        words = [word for line in f for word in line.split()]
        words = [word.lower().translate(str.maketrans('', '', punctuation)) for word in words]
        filtered_words = [w for w in words if not w in stopwords]
        #filtered_words = [stem(word) for word in filtered_words]
        pairs = [(w,1) for w in filtered_words]
        #
        pairs.sort()
        word = lambda pair : pair[0]
        grouped_pairs_ex_5 = [(w, sum(1 for _ in g)) for w, g in groupby(pairs, key=word)]
        occurrences = lambda pair: pair[1]
        grouped_pairs_ex_5.sort(key=occurrences, reverse=True)
        calculate_number_of_docs_where_the_word_appears(grouped_pairs_ex_5)
        all_grouped_pairs.append(grouped_pairs_ex_5)  
    i = 1
    for grouped_pairs in all_grouped_pairs:
        chapter = "Ex6//ex6chapter"+str(i)+".txt"
        g = open(chapter,"w+")
        listOfTdIdfInChapter = {}
        for word in grouped_pairs:
            words_tf_idf = tf_idf(word,32) #calculate tf-idf
            #g.write(str(words_tf_idf)+" "+word[0]+'\n')
            for k in range(0,int(words_tf_idf)):
                g.write(word[0]+'\n')
            listOfTdIdfInChapter[word[0]] = words_tf_idf
        i += 1
        listOfTdIdf.append(listOfTdIdfInChapter)
        g.close()

def ex6_5():
    global listOfTdIdf
    with open("Godfather.txt", encoding="UTF-8") as f:
        words = [word for line in f for word in line.split()]
        words = [word.lower().translate(str.maketrans('', '', punctuation)) for word in words]
        filtered_words = [w for w in words if not w in stopwords]
        pairs = [(w,1) for w in filtered_words]
        pairs.sort()
        word = lambda pair : pair[0]
        grouped_pairs = [(w, sum(1 for _ in g)) for w, g in groupby(pairs, key=word)]
        occurrences = lambda pair: pair[1]
        grouped_pairs.sort(key=occurrences, reverse=True)
    g = open("ex6_5.txt","w+")
    for word in grouped_pairs:
        words_tf_idf = tf_idf(word,32) #calculate tf-idf
        for k in range(0,int(words_tf_idf)):
            try:
                g.write(word[0]+'\n')
            except:
                pass
    g.close()

ex6()
#ex6_5()

#Build a word cloud based on tf-idf weights for the entire book.

# EXERCISE 7
def ex7(word):
    global listOfTdIdf
    i = 1
    dictionary = {}
    for listOfTdIdfInChapter in listOfTdIdf:
        if word in listOfTdIdfInChapter:
            dictionary[i] = listOfTdIdfInChapter[word]
        i+=1
    ret = ""
    if not dictionary:
        print("Word doesn't occur")
    else:
        sorted_dictionary = sorted(dictionary.items(), key=lambda kv: kv[1])
        #print(sorted_dictionary)
        ret = [k[0] for k in sorted_dictionary]
        ret.reverse()
    return ret

print(ex7('corleone'))
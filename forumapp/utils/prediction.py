from forumapp.models import Question,Answer
import nltk  
import numpy as np  
import random  
import string
import numpy as np
import re  
import json
from django.core import serializers
from django.http import JsonResponse
from gensim.parsing.preprocessing import remove_stopwords
from nltk.corpus import stopwords
import heapq
from sklearn.model_selection import train_test_split
from sklearn import svm




def prediction():
    #call the function for json data
    # question_ser = serializers.serialize("json", Question.objects.all()) 

    ##load the data from .json file
    with open("/home/ramthapa/Documents/7th_project/question_new.json", "r") as read_file:
        data = json.load(read_file)

    ##append all questions in a and categories in categories list
    a = []
    categories = []
    for q in data:
        question = q["fields"]["question"]
        category = q["fields"]["category"]
        categories.append(category)        
        question = nltk.sent_tokenize(question)
        a.append(question)
    
    #converting the 2d array into array
    one_array = []
    for i in a:
        one_array.append(i[0])

    que = "What would a Trump presidency mean for current international masterâ?"
    one_array.append(que)


    #removing stopwords  and making all string lowercase
    for i in range(len(one_array)):
        one_array [i] = remove_stopwords(one_array[i])
        one_array [i] = one_array [i].lower()
        one_array [i] = re.sub(r'\W',' ',one_array[i])
        one_array [i] = re.sub(r'\s+',' ',one_array[i])    


    #tokenize the words
    wordfreq = {}
    for sentence in one_array:
        tokens = nltk.word_tokenize(sentence)
        for token in tokens:
            if token not in wordfreq.keys():
                wordfreq[token] = 1
            else:
                wordfreq[token] += 1

    #taking most frquently occured words
    most_freq = heapq.nlargest(60, wordfreq, key=wordfreq.get)
    print(most_freq)

    #tokenize the words into different labels
    sentence_vectors = []
    for sentence in one_array:
        sentence_tokens = nltk.word_tokenize(sentence)
        stopwords = ['what', 'who','when','why','how','where','which','whom','whose','how long','how much']
        resultwords  = [word for word in sentence_tokens if word.lower() not in stopwords]
        print(resultwords)


        # print('sentence taoejeje =',sentence_tokens)
        sent_vec = []   
        for token in most_freq:
    #         print(token)
            if token in resultwords:
                sent_vec.append(1)
            else:
                sent_vec.append(0)
        sentence_vectors.append(sent_vec)

    # converting into numpy array
    sentence_vectors = np.asarray(sentence_vectors)

    #vectorize the given data
    sentence_vectors_pop = []
    sentence_vectors = []
    for sentence in one_array:
        sentence_tokens = nltk.word_tokenize(sentence)
        
        sent_vec = []
        for token in most_freq:
            
            if token in sentence_tokens:
                sent_vec.append(1)
            else:
                sent_vec.append(0)
        sentence_vectors.append(sent_vec)
    sentence_vectors_pop =  sentence_vectors.pop()

    # print((sentence_vectors[0]))
    
    #converting into numpp array
    x = np.asarray(sentence_vectors)

    #get the catrgory
    y_cat = np.array(categories)
    print(y_cat.shape)
    print(y_cat)

    #using svm for splittinga adata where 80% traing and 20%test data
        #splitting a adata

    X_train, X_test, y_train, y_test = train_test_split(x, y_cat) 

    #predict te given model
    clf = svm.SVC(gamma=0.001, C=100.)
    clf.fit(x, y_cat)
    y_pred = clf.predict([sentence_vectors_pop])

    print('y prediction',y_pred)
    print('y predict shape',y_pred.shape)


    return {

    }
    









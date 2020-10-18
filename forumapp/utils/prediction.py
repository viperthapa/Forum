from forumapp.models import Question,Answer
import nltk  
import pandas as pd  
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
from itertools import chain 
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn import svm
from sklearn.svm import LinearSVC
from sklearn.multiclass import OneVsRestClassifier



def prediction(confirm_question):
    #call the function for json data
    # question_ser = serializers.serialize("json", Question.objects.all()) 

    ##load the data from .json file
    with open("/home/ramthapa/Documents/7th_project/question_new.json", "r") as read_file:
        data = json.load(read_file)

    ##append all questions in a and categories in categories list
   ##get the questions part only from json file
    for q in data:
        question = q["fields"]["question"]
    #     print(question)
        question = nltk.sent_tokenize(question)

    ##converting to the array
    a = []
    categories = []
    for q in data:
        question = q["fields"]["question"]
        category = q["fields"]["category"]
        categories.append(category)
       #tokenize  the sentences 
        question = nltk.sent_tokenize(question)
        a.append(question)

    #iteration of every list
    one_array = list(chain.from_iterable(a)) 
    one_array.append(confirm_question)

    #removing all the stop words and other unnecssary databases
    for i in range(len(one_array )):
        one_array [i] = remove_stopwords(one_array [i])
        one_array [i] = one_array [i].lower()
        one_array [i] = re.sub(r'\W',' ',one_array [i])
        one_array [i] = re.sub(r'\s+',' ',one_array [i])
      
    print('the last element of array = ',one_array[-1])
    #get the occurence of words in overall sentences
    wordfreq = {}
    for sentence in one_array:
        tokens = nltk.word_tokenize(sentence)

        
        
        for token in tokens:
            if token not in wordfreq.keys():
                wordfreq[token] = 1
            else:
                wordfreq[token] += 1

    #get the exact top 60 words from list
    most_freq = heapq.nlargest(60, wordfreq, key=wordfreq.get)
    filtered_numbers = [item for item in most_freq if not item.isdigit()]

    
    # CountVectorizer is used to convert a collection of text documents to a vector of term/token counts
    vectorizer = CountVectorizer()
    ##fitting the array
    vectorizer.fit(filtered_numbers)
    print(vectorizer)


    ##collect all the data into single array
    vectorizer.get_feature_names()

    dtm_que = vectorizer.transform(most_freq)

    x_test = pd.DataFrame(dtm_que.toarray(),columns=vectorizer.get_feature_names())

    #get the category nad vectorized it
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(categories)
    x = X.toarray()
    last_element = list(x[-1])
    print('token',last_element)


    #craeting a array of categories
    y = np.array(categories)

    #prediction 
    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.1) # 70% training and 30% test


    print(X_train.shape)
    print(X_test.shape)
    print(y_train.shape)
    print(y_test.shape)

    #use set method to differentiate a unique words from a list
    set_catgories = set(categories)
    target_names = list(set_catgories)


    #Create a svm Classifier
    clf = OneVsRestClassifier(LinearSVC())
    clf.fit(X_train, y_train)

    y_pred = clf.predict([last_element])
    print('y predicyt',y_pred)



    
    
    return {
        'y_pred':y_pred
    }
    









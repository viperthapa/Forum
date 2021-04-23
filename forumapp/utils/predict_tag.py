import nltk
import random
import json
import pickle
import numpy
import tflearn
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()
from tensorflow.python.framework import ops
from nltk.corpus import stopwords
import tensorflow as tf
import keras

#load the json files
with open(r"/home/ramthapa/Documents/7th_project/myforum_old/forum_new.json",'r') as file:
    data = json.load(file)
    print("data++++++++++++",data)

#creating an empty array for category and questions
words = []
labels = []
docs_x = [] #keeps all the associated data in multi dimensional array
docs_y = [] #keeps all the associated docs_x category
ignore_letters = ['?','!',',','.','{','}','(',')','what','where','which','when','who','whom','whose','why','how','how long','how much']
for intent in data['intents']:
    for pattern in intent['question']:
        wrds = nltk.word_tokenize(pattern)
        words.extend(wrds)
        docs_x.append(wrds)
        docs_y.append(intent["category"])
        
    if intent['category'] not in labels:
        labels.append(intent['category'])

#lower case 
words_stemmer = [stemmer.stem(w.lower()) for w in words if w not in ignore_letters]

# removing all the auxiliary verbs like is,am,are
words = [word for word in words_stemmer if word not in stopwords.words('english')]
words = sorted(list(set(words)))

#intialzing the category in ascending order
labels = sorted(labels)


#for training purposes
training = [] #for patterns 
output = [] #for tags

out_empty = [0 for _ in range(len(labels))] #intaializing the labels with all 0
print("training",training)
for x, doc in enumerate(docs_x):
    bag = []

    wrds = [stemmer.stem(w.lower()) for w in doc]

    #checking if 2 dimensional words exist in single dimesional words
    for w in words:
        if w in wrds:
            bag.append(1)
        else:
            bag.append(0)

    output_row = out_empty[:]
    output_row[labels.index(docs_y[x])] = 1

    training.append(bag)
    output.append(output_row)

#creating a numpy array for training and output
training = numpy.array(training)
output = numpy.array(output)

print("output",output)
print("training",training)



#training a given model using tf
ops.reset_default_graph()
net = tflearn.input_data(shape=[None, len(training[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
net = tflearn.regression(net)

model = tflearn.DNN(net)
#training the given models for 700 times as number of epochs helps to find accuaracy
model.fit(training, output, n_epoch=1000, batch_size=8, show_metric=True)
model.save("model.tflearn")

print("output",net)
print("training",training)



#coverting the user input into bag of words
def bag_of_words(s, words):
    print("question^^^^^^^^^^^^^^^^",words)

    bag = [0 for _ in range(len(words))]

    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]

    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1 #apply 1 if the words exists in word list
            
    return numpy.array(bag)


def predict_tag(question):
    print("question@@@@@@@@@@@",question)
    results = model.predict([bag_of_words(question, words)])
    print("results",results)
    
    results_index = numpy.argmax(results)
    tag = labels[results_index]
    print("tag###############3",tag)
    index = results_index
    print(index,"******************************")

    index_value = results[0][index]
    print("index_value",index_value)


    # prediction = tf.math.argmax(results_index, axis=1)
    # print("prediction",prediction)
    return tag,index_value
    








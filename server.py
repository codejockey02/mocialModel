#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pickle
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from firebase import firebase
import pyrebase

def create_word_features(words):
    useful_words = [word for word in words if word not in stopwords.words('english')]
    my_dict = dict([(word, True) for word in useful_words])
    return my_dict

model = pickle.load(open("model.pkl","rb"))


config = {
  "apiKey" : "key",
  "authDomain": "mocial-91b4a.firebaseapp.com",
  "databaseURL": "https://mocial-91b4a.firebaseio.com/",
  "storageBucket": "mocial-91b4a.appspot.com"
}

firebase1 = pyrebase.initialize_app(config)
db = firebase1.database()

app = firebase.FirebaseApplication('https://mocial-91b4a.firebaseio.com/',None)

#Streaming the Input.(Forever Stream)
def stream_handler(message):
    
    print('event={m[event]}; path={m[path]}; data={m[data]}'.format(m=message))
    data2 = message["path"]
    x = "Review"
    if x in data2:
        data1 = message["data"]
        print(data1)
        print("\n\nThe updated Review is:", data1['review'])
        strng = "/Users"
        data2 = data2[:-6]
        data3 = strng + data2 + 'Rating'
        print(data3)
        #rating = "Positive"
        def reviewmovie(dat):
            words=word_tokenize(dat)
            words=create_word_features(words)
            return(model.classify(words))
        
        send = reviewmovie(data1['review'])
        app.put(data3,'rating',send)          
    else:
        print("\n\nThe Review is not updated yet.")
    
    
my_stream =db.child('Users').stream(stream_handler)

# Run Stream Handler forever
while True:
    data = input("[{}] Type exit to disconnect: ".format('?'))
    if data.strip().lower() == 'exit':
        print('Stop Stream Handler')
        if my_stream: my_stream.close()
        break
response = db.child('Users').get()
print(response.val())
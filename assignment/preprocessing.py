import os
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords

#Handling Stopwords
#Creating our stopwords list
other_stopwords_dir = r'StopWords'
for i in os.listdir(other_stopwords_dir):
    with open(other_stopwords_dir + '/' + i, 'r') as f:
        data = f.read()
        other_stopwords_list = data.split('\n')

other_stopwords = list(map(lambda i: i.lower(), other_stopwords_list))
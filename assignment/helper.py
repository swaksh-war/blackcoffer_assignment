import os
import nltk
# Sentiment analysis -----------
#Handling Stopwords
#Creating our stopwords list
def create_stopwords():
    other_stopwords_dir = r'StopWords'
    for i in os.listdir(other_stopwords_dir):
        with open(other_stopwords_dir + '/' + i, 'r') as f:
            data = f.read()
            other_stopwords_list = data.split('\n')

    other_stopwords = list(map(lambda i: i.lower(), other_stopwords_list))
    return other_stopwords



#Creating positive and Negative word dictionary
def create_positive_dict():

    positivedictionary = r'MasterDictionary/positive-words.txt'
    with open(positivedictionary, 'r', encoding='Latin-1') as f:
        data = f.read()
        positive_words = data.split('\n')
    return positive_words

def create_negative_dict():
    negativedictionary = r'MasterDictionary/negative-words.txt'
    with open(negativedictionary, 'r', encoding='Latin-1') as f:
        data = f.read()
        negative_words = data.split('\n')
    return negative_words

#Tokenizing
def tokenziation(text):
    tokens = nltk.word_tokenize(text)
    return tokens

#Removing Stopwords
def removing_stop_words(tokens, other_stopwords):
    cleaned_words = [w for w in tokens if  w.lower() not in other_stopwords]
    return cleaned_words

def remove_punctuation(tokens):
    words = [w for w in tokens if w.isalnum()]
    return words

#Positive Score
def positive_score(cleaned_text, positive_words):
    total = 0
    for i in cleaned_text:
        if i.lower() in positive_words:
            total += 1
    return total

#Negative Score
def negative_score(cleaned_text, negative_words):
    total = 0
    for i in cleaned_text:
        if i.lower() in negative_words:
            total += 1
    return total

#calculating polarity score
def polarity_score(pos_score, neg_score):
    return ((pos_score - neg_score)/(pos_score + neg_score + 0.000001))

#calculating subjective score
def subjective_score(pos_score, neg_score, cleaned_text):
    return ((pos_score+neg_score)/(len(cleaned_text)+0.000001))

# END OF SENTIMENT ANALYSIS-----------


#START OF READABILITY ANALYSIS

#tokenizing on sentence
def sentence_tokenization(text):
    tokens = nltk.sent_tokenize(text)
    return tokens

#getting average length of sentence
def average_sentence_length(sent_token, word_token):
    try:
        x = (len(word_token)/len(sent_token))
    except:
        x = 0
    return x


def average_number_of_words_per_sentece(tokenized_sentence):
    word_count = 0
    for sentence in tokenized_sentence:
        for i in sentence:
            word_count += 1
    try:
        x = word_count/len(tokenized_sentence)
    except:
        x = 0
    return (word_count,x)

#creating syllable counter
def syllable_counter(text):
    #handling egde cases
    vowels = {'a','e','i','o','u','y'}
    all_count = []
    if len(text) > 2:
        if text[-2] == 'e':
            if text[-1] == 's' or text[-1] == 'd':
                text = text[:-2]

    #getting a list of vowels a word having
    for i in text:
        if i in vowels:
            all_count.append(i)
    
    #converting the list to set that we obtain after iterating
    # through the word to check the unique vowels because
    # y is considered as vowel if the word has no other vowels
    res = vowels.intersection(set(all_count))
    if len(res) > 1 and 'y' in res:
        return len(all_count) - all_count.count('y')
    else:
        return len(all_count)

def average_syllable(tokenized_word):
    total_syll = 0
    for i in tokenized_word:
        syll = syllable_counter(i)
        total_syll += syll
    try:
        x = total_syll/len(tokenized_word)
    except:
        x=0
    return x

#getting the number of complex words
def complexword(token):
    total = 0
    for i in token:
        syll = syllable_counter(i)
        if syll > 2:
            total += 1
    return total

def personal_pronoun(token):
    personal_pronoun = ['I', 'we', 'my', 'ours', 'us', 'We','My', 'Ours']
    total = 0
    for word in token:
        if word in personal_pronoun:
            total += 1
    return total

#Getting the percent of complex words
def percentagecomplexword(token, counts):
    total_words = len(token)
    try:
        x = (counts/total_words)*100
    except:
        x = 0
    return x

def avg_word_length(token):
    total_char = 0
    for word in token:
        total_char += len(word)
    try:
        x = total_char/len(token)
    except:
        x = 0
    return x

def fog_index(average_sentence_length, percentage_of_complex_word):
    return (0.4*(average_sentence_length + percentage_of_complex_word))

# if __name__ == '__main__':
#     with open('blackcoffer_assignment/scraped/scraped_37.txt', 'r') as f:
#         text = f.read()
#     token = tokenziation(text)
#     sent_token = sentence_tokenization(text)
#     cleaned_tokens = removing_stop_words(token, other_stopwords)
#     cleaned_tokens = remove_punctuation(cleaned_tokens)
#     pos_score = positive_score(cleaned_tokens)
#     neg_score = negative_score(cleaned_tokens)
#     pol_score = polarity_score(pos_score, neg_score)
#     sub_score = subjective_score(pos_score,neg_score, cleaned_tokens)
#     avg = average_sentence_length(sent_token, token)
#     compwords = complexword(token)
#     percent = percentagecomplexword(token, compwords)
#     fog = fog_index(avg, percent)
#     pronoun = personal_pronoun(cleaned_tokens)
#     average_word = avg_word_length(cleaned_tokens)
#     res = [str(pos_score),'\n',str(neg_score),'\n', str(pol_score),'\n' ,str(sub_score), '\n', str(avg), '\n',str(compwords), '\n',str(percent), '\n',str(pronoun),'\n', str(average_word), '\n', str(fog)]
#     with open('sample.txt', 'w') as f:
#         f.writelines(res)


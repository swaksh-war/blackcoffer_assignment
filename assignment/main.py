import helper
import pandas as pd
from data_extractor import fetch_data
import os
import tqdm

input_file_path = r'Input.xlsx'

#now lets fetch data
#getting the working urls along with the text files for the working urls and save it in the scraped directory
working_url = fetch_data(input_file_path)

all_text_directory = r'scraped'

#creating all stopwords dictionary
all_stopwords = helper.create_stopwords()

#creating positive words dictionary
positive_words_dict = helper.create_positive_dict()

#creating negative words dictionary
negative_words_dict = helper.create_negative_dict()

#now lets create the container to store the values for now and then we will create the excel file with it
positive_score, negative_score, polarity_score, subjectivity_score, average_sentence_length, percent_of_complex_word, fog_index, average_word_per_sentence, complex_word, word_count, syllable_per_word, personal_pronoun, average_word_length = [], [], [], [], [], [], [], [], [], [], [], [], []

#fetch all details from the texts
for i in tqdm.tqdm(os.listdir(all_text_directory)):
    with open(all_text_directory + '/' + i, 'r') as f:
        text = f.read()
    #word tokenization
    tokenized_text = helper.tokenziation(text)
    #sentence tokenization
    tokenized_sentence = helper.sentence_tokenization(text)

    #removing stopwords using the stopwords provided
    cleaned_text = helper.removing_stop_words(tokenized_text, all_stopwords)
    #removing punctuation from stop words removed tokenized text
    cleaned_text1 = helper.remove_punctuation(cleaned_text)

    #getting positive score
    pos_score = helper.positive_score(cleaned_text1, positive_words_dict)
    positive_score.append(pos_score)
    #getting negative score
    neg_score = helper.negative_score(cleaned_text1, negative_words_dict)
    negative_score.append(neg_score)
    #getting polarity score
    pol_score = helper.polarity_score(pos_score, neg_score)
    polarity_score.append(pol_score)
    #getting subjectivity score
    sub_score = helper.subjective_score(pos_score, neg_score, cleaned_text1)
    subjectivity_score.append(sub_score)
    #getting average sentence length
    avg_sentence_length = helper.average_sentence_length(tokenized_sentence, tokenized_text)
    average_sentence_length.append(avg_sentence_length)
    #getting complex word count
    complex_word_count = helper.complexword(cleaned_text1)
    complex_word.append(complex_word_count)
    #getting complex word percent
    complex_word_percent = helper.percentagecomplexword(tokenized_text, complex_word_count)
    percent_of_complex_word.append(complex_word_percent)
    #getting fog index
    fg_index = helper.fog_index(avg_sentence_length, complex_word_percent)
    fog_index.append(fg_index)
    #getting average number of word per sentence, and total words
    word_count_num, avg_wrd_p_sentence = helper.average_number_of_words_per_sentece(tokenized_sentence)
    word_count.append(word_count_num)
    average_word_per_sentence.append(avg_wrd_p_sentence)
    #average syllable
    avg_syllable = helper.average_syllable(tokenized_text)
    syllable_per_word.append(avg_syllable)
    #getting personal pronoun
    person_pronoun = helper.personal_pronoun(cleaned_text1)
    personal_pronoun.append(person_pronoun)
    #getting avg word length
    avg_word_len = helper.avg_word_length(cleaned_text1)
    average_word_length.append(avg_word_len)
    
df = pd.DataFrame([working_url,positive_score, negative_score, polarity_score, subjectivity_score, average_sentence_length, percent_of_complex_word, fog_index, average_word_per_sentence, complex_word, word_count, syllable_per_word, personal_pronoun, average_word_length])
df = df.transpose()
df.columns = ['Working URL', 'Positive Score', 'Negative Score', 'Polarity Score', 'Subjectivity Score', 'Average Sentence Length', 'Percent Of Complex Word', 'Fog Index', 'Average Word Per Sentence', 'Complex Word', 'Word Count', 'Syllable Per Word', 'Personal Pronoun', 'Average Word Length']
df.to_excel('output.xlsx')
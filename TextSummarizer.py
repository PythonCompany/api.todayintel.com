#Step 1. Importing Libraries

import sys
import math
import bs4 as bs
import urllib.request
import re
import nltk
from nltk.stem import WordNetLemmatizer 
import spacy


#Execute this line if you are running this code for first time
nltk.download('wordnet')

#Initializing few variable
nlp = spacy.load('en_core_web_md')
lemmatizer = WordNetLemmatizer() 

#Step 4. Defining functions to create Tf-Idf Matrix


#Function to calculate frequency of word in each sentence
#INPUT -> List of all sentences from text as spacy.Doc object
#OUTPUT -> freq_matrix (A dictionary with each sentence itself as key, 
# and a dictionary of words of that sentence with their frequency as value)

def frequency_matrix(sentences):
    freq_matrix = {}
    stopWords = nlp.Defaults.stop_words

    for sent in sentences:
        freq_table = {} #dictionary with 'words' as key and their 'frequency' as value
        
        #Getting all word from the sentence in lower case
        words = [word.text.lower() for word in sent  if word.text.isalnum()]
       
        for word in words:  
            word = lemmatizer.lemmatize(word)   #Lemmatize the word
            if word not in stopWords:           #Reject stopwords
                if word in freq_table:
                    freq_table[word] += 1
                else:
                    freq_table[word] = 1

        freq_matrix[sent[:15]] = freq_table

    return freq_matrix


#Function to calculate Term Frequency(TF) of each word
#INPUT -> freq_matrix
#OUTPUT -> tf_matrix (A dictionary with each sentence itself as key, 
# and a dictionary of words of that sentence with their Term-Frequency as value)

#TF(t) = (Number of times term t appears in  document) / (Total number of terms in the document)
def tf_matrix(freq_matrix):
    tf_matrix = {}

    for sent, freq_table in freq_matrix.items():
        tf_table = {}  #dictionary with 'word' itself as a key and its TF as value

        total_words_in_sentence = len(freq_table)
        for word, count in freq_table.items():
            tf_table[word] = count / total_words_in_sentence

        tf_matrix[sent] = tf_table

    return tf_matrix


#Function to find how many sentences contain a 'word'
#INPUT -> freq_matrix
#OUTPUT -> sent_per_words (Dictionary with each word itself as key and number of 
#sentences containing that word as value)

def sentences_per_words(freq_matrix):
    sent_per_words = {}

    for sent, f_table in freq_matrix.items():
        for word, count in f_table.items():
            if word in sent_per_words:
                sent_per_words[word] += 1
            else:
                sent_per_words[word] = 1

    return sent_per_words


#Function to calculate Inverse Document frequency(IDF) for each word
#INPUT -> freq_matrix,sent_per_words, total_sentences
#OUTPUT -> idf_matrix (A dictionary with each sentence itself as key, 
# and a dictionary of words of that sentence with their IDF as value)

#IDF(t) = log_e(Total number of documents / Number of documents with term t in it)
def idf_matrix(freq_matrix, sent_per_words, total_sentences):
    idf_matrix = {}

    for sent, f_table in freq_matrix.items():
        idf_table = {}

        for word in f_table.keys():
            idf_table[word] = math.log10(total_sentences / float(sent_per_words[word]))

        idf_matrix[sent] = idf_table

    return idf_matrix


#Function to calculate Tf-Idf score of each word
#INPUT -> tf_matrix, idf_matrix
#OUTPUT - > tf_idf_matrix (A dictionary with each sentence itself as key, 
# and a dictionary of words of that sentence with their Tf-Idf as value)
def tf_idf_matrix(tf_matrix, idf_matrix):
    tf_idf_matrix = {}

    for (sent1, f_table1), (sent2, f_table2) in zip(tf_matrix.items(), idf_matrix.items()):

        tf_idf_table = {}

       #word1 and word2 are same
        for (word1, tf_value), (word2, idf_value) in zip(f_table1.items(),
                                                    f_table2.items()):  
            tf_idf_table[word1] = float(tf_value * idf_value)

        tf_idf_matrix[sent1] = tf_idf_table

    return tf_idf_matrix


#Function to rate every sentence with some score calculated on basis of Tf-Idf
#INPUT -> tf_idf_matrix
#OUTPUT - > sentenceScore (Dictionary with each sentence itself as key and its score
# as value)
def score_sentences(tf_idf_matrix):
    
    sentenceScore = {}

    for sent, f_table in tf_idf_matrix.items():
        total_tfidf_score_per_sentence = 0

        total_words_in_sentence = len(f_table)
        for word, tf_idf_score in f_table.items():
            total_tfidf_score_per_sentence += tf_idf_score

        if total_words_in_sentence != 0:
            sentenceScore[sent] = total_tfidf_score_per_sentence / total_words_in_sentence

    return sentenceScore



#Function Calculating average sentence score 
#INPUT -> sentence_score
#OUTPUT -> average_sent_score(An average of the sentence_score) 
def average_score(sentence_score):
    
    total_score = 0
    for sent in sentence_score:
        total_score += sentence_score[sent]

    average_sent_score = (total_score / len(sentence_score))

    return average_sent_score


#Function to return summary of article
#INPUT -> sentences(list of all sentences in article), sentence_score, threshold
# (set to the average pf sentence_score)
#OUTPUT -> summary (String text)
def create_summary(sentences, sentence_score, threshold):
    summary = ''

    for sentence in sentences:
        if sentence[:15] in sentence_score and sentence_score[sentence[:15]] >= (threshold):
            summary += " " + sentence.text
        

    return summary




import string
import pandas as pd
import numpy as np
import re
import nltk

from nltk.stem.snowball import SnowballStemmer
stemmer = SnowballStemmer("english")

from nltk.corpus import stopwords
nltk.download('stopwords')

from nltk import word_tokenize

from sklearn.model_selection import train_test_split
from keras.utils.np_utils import to_categorical

def split_hashtags(text):    

    column = []

    letters = list(string.ascii_letters)
    sequence = '123456789'


    ## split text row
    split = text.split()

    ## Iterate over split and check for hashtags
    for word in split:
        if '#' in word:

            ## If a hashtag is found, split that word before every uppercase letter

            pulled_apart = re.sub( r"([A-Z])", r" \1", word).split()
            letter_index = []
            ## Iterate over the split apart items of the hashtag. 

            for idx in range(len(pulled_apart)):
                w = pulled_apart[idx]

                ## If an item is an uppercase letter,
                ## append that item's index to a list
                if w == w.upper():
                    letter_index.append(idx)

                elif w == w.title():
                    column.append(w)
                    continue

            ## Check to see if the indexes are consecutive
            check_index = ''.join([str(x) for x in letter_index])

            ## If consecutive join the unsplittable hashtag and append it to a test case list
            ## Append the  hashtag as a single word to column.

            if check_index in sequence:

                upper_word = [pulled_apart[x] for x in range(len(pulled_apart)) if x in letter_index]



                column.append(''.join(upper_word))

                continue


            ## Check to see if the index is sequencial but goes beyond 9
            check_index1 = np.array(letter_index[:-1]) + 1
            check_index2 = np.array(letter_index[1:])

            if np.array_equal(check_index1, check_index2):

                upper_word = [pulled_apart[x] for x in range(len(pulled_apart)) if x in letter_index]



                column.append(''.join(upper_word))

                continue
        else:
            column.append(word)     
    return column
    
def clean(text, split = True):

           
    digits = string.digits
    punctuation = string.punctuation
    punctuation += '’'
    
#     emoji_pattern = re.compile("["
#             u"\U0001F600-\U0001F64F"  # emoticons
#             u"\U0001F300-\U0001F5FF"  # symbols & pictographs
#             u"\U0001F680-\U0001F6FF"  # transport & map symbols
#             u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
#                                "]+", flags=re.UNICODE)
#     no_emoji = emoji_pattern.sub(r'', text)
    
    
    no_emoji  = text.encode('ascii', 'ignore').decode('ascii')
    
    d_trump = no_emoji.replace('realdonaldtrump', 'donald trump')
    no_stops  = remove_stops(d_trump)
    no_http = remove_http(no_stops)
    no_digits = no_http.translate(str.maketrans('', '', digits))
    cleaned = no_digits.translate(str.maketrans('', '', punctuation))
    

    
    
    if split:
        split = cleaned.split()
        return split
    else: 
        return cleaned 
    
def remove_http(text):
    split_text = text.split()
    for i in split_text:
        if 'http' in i:
            text = text.replace(i, '')
    
    return text

    
def remove_stops(text):
    stops = stopwords.words('english')
    stops += ['i’m', 'it’s', 
              'don’t', 'can’t', 
              'that’s', '2', 
              'lol', 'i',
             'get', 'the','i’m', '-',
             "i'm", 'it', 'a', 'u', 'amp', '•', 'i’ve',
             'chicago', 'tictac', 'flippen', 'click', 'link', 'bio', 'job',
             '_', 'apply', 'jobs', 'hiring', 'openings', 'opening', 'could', 'might',
             'via','im','gon', 'na','ive','f','like','il','j','one','us','en', 'el','ill',
            'lo', 'que','finna', 'gonna', 'yo', 'thats','de', 'la', 'got', 'ta', 'gram','buffalocialism',
            'actbrigitte','yik']


    split = text.split()
    removed = [x.lower() for x in split if x.lower() not in stops]
    
    return ' '.join(removed)

class process_dataframe(object):
    def __init__(self, dataframe, text_column):

        copy = dataframe.copy()
        copy[text_column] = copy[text_column].apply(split_hashtags)
        copy[text_column] = copy[text_column].apply(' '.join)
        copy[text_column] = copy[text_column].apply(clean)
        copy[text_column] = copy[text_column].apply(' '.join)
        copy[text_column] = copy[text_column].apply(stemmer.stem)
        copy[text_column] = copy[text_column].apply(word_tokenize)
        self.data = copy[text_column]

    def test_split(data, target):
        xtrain, xtest, ytrain_, ytest_ = train_test_split(data, target, train_split = .99)

        ytrain = to_categorical(ytrain_)
        ytest = to_categorical(ytest_)

        return xtrain, xtest, ytrain, ytest




    





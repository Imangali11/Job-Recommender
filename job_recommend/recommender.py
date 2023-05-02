import re
import nltk
import pandas as pd
import numpy as np
from tqdm.notebook import tqdm
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords as nltk_stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy import spatial
import warnings
warnings.filterwarnings('ignore')

# Clear text from html codes and unnecessary characters
def clear_text(text):
    # Remove the part of the job description that describes benefits
    ind = text.find('enefit')
    if ind<200:
        ind = text.find('enefit',200)
    clear_text = text[:ind-1] if ind!=-1 else text

    # Clear text from special characters
    clear_text = re.sub('</\[^>*]>?&$@!¬∑Ääìô', ' ', clear_text)
    clear_text = clear_text.lower()

    # Replace replacables as they only represent (')
    replacables=["äôre","äôs","äôll","äôd","äôt","äô","äò","‚",",","?",":","(",")"]
    for i in replacables:
        clear_text = clear_text.replace(i,"")
    return ' '.join(clear_text.split())

# Lemmatize words
def lemmatize(text, lemmatizer):
    # Make sure that the words are lemmatized to the root word
    word_list = nltk.word_tokenize(text)
    try:
        while True:
            word_list.remove(".")
    except ValueError:
        pass
    return ' '.join([lemmatizer.lemmatize(w) for w in word_list])

# Apply everythig above to the text
def modify_text(data, lemmatizer):
    corpus = list(data)
    for i in range(len(corpus)):
        corpus[i] = lemmatize(clear_text(corpus[i]), lemmatizer)
    return corpus

# Cosine similarity between objects
def cosine_similarity(x,y):
    return 1 - spatial.distance.cosine(x,y)

# Main algorithm
def recommend(resume, data):
    nltk.download('wordnet')
    lemmatizer = WordNetLemmatizer()
    # Transform input data to dataframe for convenient use
    data = pd.DataFrame(data)
    # Create a set of descriptions
    datas = data['description']
    # Create a corpus of preprocessed data
    corpus = modify_text(datas, lemmatizer)
    # Create a corpus of resume
    resume_corpus = modify_text([resume], lemmatizer)
    nltk.download('stopwords')
    # Set the stopwords
    stopwords = set(nltk_stopwords.words('english'))
    # Vectorize corpuses to input to the cosine similarity
    count = TfidfVectorizer(stop_words=list(stopwords), ngram_range=(1,1))
    vector_data = count.fit_transform(corpus)
    vector_data = vector_data.toarray()

    resume_vector = count.transform(resume_corpus)
    resume_vector = resume_vector.toarray()

    # Add cosine similarities in the original order
    result = []
    for i in range(len(vector_data)):
        result.append([cosine_similarity(resume_vector[0], vector_data[i]), i])

    # Sort the resulting similarities to obtain indexes of the highest matching joba
    k = sorted(result, reverse = True)

    # Add indexes of top 10 best jobs by cosine similarity
    best_ind = []
    for i in range(10):
        best_ind.append(k[i][1]+1)
    # Return indexes array
    return best_ind
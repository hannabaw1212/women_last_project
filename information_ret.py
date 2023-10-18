import spacy 
nlp = spacy.load("en_core_web_sm")
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk 
nltk.download('words')
nltk.download("punkt")
nltk.download("stopwords")

from nltk.corpus import stopwords
import string
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import random
english_words = set(nltk.corpus.words.words())
vocab = set()
from spellchecker import SpellChecker


# EDS symptoms = 15
# EDS causes = 10
# EDS diagnosis = 10

stop_words = set(stopwords.words('english'))
question_words = ["who", "what", "whom", "whose", "which", "when", "where", "how", "why"]
punctuations = list(string.punctuation)
# english_words_lemma = set()
# i = 1
# for word in english_words:
#     print(i)
#     doc = nlp(word)
#     i += 1
#     for tok in doc:
#         english_words_lemma.add(tok.lemma_)

# print(english_words_lemma)


def read_data_and_create_vocab(whatToKnow, topic):
    data = pd.DataFrame()
    if topic == 'eds_disease':
        if whatToKnow == 'symp':
            data = pd.read_csv("static/edsSymp.csv")
            data = data[data['label'] == 'symp']
        elif whatToKnow == 'types':
            data = pd.read_csv('static/edsSymp.csv')
            data = data[data['label'] == 'type']

    docs = list(data['Docs'])

    for doc in docs:
        tokens = nltk.word_tokenize(doc)
        tokens_caseFold = [token.lower() for token in tokens]
        token_after_remove_QW = [token for token in tokens_caseFold if token not in question_words]
        token_sofi = [token for token in token_after_remove_QW if token not in stop_words and token not in punctuations]
        text_sof = " ".join(token_sofi)
        docy = nlp(text_sof)
        lemmas = [token.lemma_ for token in docy]

        for lemma in lemmas:
            vocab.add(lemma)
    return data



def spelling_corr(prompt):
    tokens = nltk.word_tokenize(prompt)
    tokens_caseFold = [token.lower() for token in tokens]
    token_after_remove_QW = [token for token in tokens_caseFold if token not in question_words]
    token_sofi = [token for token in token_after_remove_QW if token not in stop_words and token not in punctuations]
    text_sof = " ".join(token_sofi)
    docy = nlp(text_sof)
    lemmas = [token.lemma_ for token in docy]

    corr_lemmas = []
    for lemma in lemmas:
        if lemma not in vocab:
            corr_lemmas.append(jaccard_sim(lemma))
        else:
            corr_lemmas.append(lemma)
    if not corr_lemmas :
        return "Please type a meaningful information"
    
    return " ".join(corr_lemmas)
          

def jaccard_sim(text):
    charas1 = set(text)
    wanted_word = text
    best_score = 0
    for word in vocab:

        charas2 = set(word)

        intersection  = charas1.intersection(charas2)
        union = charas1.union(charas2)

        score = len(intersection) / len(union)

        if score > best_score:
            best_score = score 
            wanted_word = word
    
    if best_score < 0.75:
        spell = SpellChecker(language='en')
        return spell.correction(text)
        
    return wanted_word
    


def pre_process(text): 
    """
    This function gets a text and then do the above operations:
        1) case folding
        2) removing stop words, punctuations, and Interrogative word
        3) lemmetazation

    Parameters:
    text (string): a text that the user want to pre process

    Returns: 
    a Processed text.
    """
    stop_words = set(stopwords.words('english'))
    question_words = ["who", "what", "whom", "whose", "which", "when", "where", "how", "why"]
    punctuations = list(string.punctuation)
    tokens = nltk.word_tokenize(text)
    tokens_case = [token.lower() for token in tokens]
    token_after_remove_QW = [token for token in tokens_case if token not in question_words]
    token_sofi = [token for token in token_after_remove_QW if token not in stop_words and token not in punctuations]
    text_sof = " ".join(token_sofi)
    doc = nlp(text_sof)


    lemmas = [token.lemma_ for token in doc]
    if lemmas is None:
        return "בבקשה לרשום משהו קריא או בעל משמעות"
    return " ".join(lemmas)


def get_most_similar_docs(prompt, whatToKnow, topic):
    our_docs = list(read_data_and_create_vocab(whatToKnow, topic)['Docs'])

    prompt = spelling_corr(prompt)

    our_prompt_and_docs = our_docs + [prompt]

    our_prompt_and_docs = [pre_process(text) for text in our_prompt_and_docs]
    tf_idf = TfidfVectorizer()
    tfidf_matrix = tf_idf.fit_transform(our_prompt_and_docs)
    input_text_index = len(our_prompt_and_docs) - 1
    similarity_scores = cosine_similarity(tfidf_matrix[input_text_index], tfidf_matrix[:-1])
# Convert similarity scores to a 1D NumPy array
    similarity_array = np.array(similarity_scores).flatten()
# Get the indices of the top 10 most similar texts
    top_10_indices = list(similarity_array.argsort()[-4:][::-1])

    random_index = random.choice(top_10_indices)

    for index in top_10_indices:
        print(our_docs[index])
        print("-"*100)
    return our_docs[random_index]




# if __name__ == "__main__":
#     get_most_similar_docs()

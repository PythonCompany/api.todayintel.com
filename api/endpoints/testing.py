from fastapi import APIRouter, Path, Query, Depends
from pydantic import BaseModel
from cachetools import TTLCache
import os
from seoanalyzer import analyze
from lighthouse import LighthouseRunner
import spacy
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk import pos_tag
import nltk
import random
nltk.download('averaged_perceptron_tagger')

router = APIRouter()
lemmatizer = WordNetLemmatizer()

class RewriteText(BaseModel):
    text: str

nlp = spacy.load("en_core_web_md")

def get_synonyms(word, pos):
    # Use NLTK to get synonyms for a word and a specific part of speech
    synonyms = set()
    try:
        for syn in wordnet.synsets(word, pos=pos):
            for lemma in syn.lemmas():
                synonyms.add(lemma.name().lower())
    except KeyError:
        # Handle the KeyError by using a default part-of-speech tag ('n' for noun)
        for syn in wordnet.synsets(word, pos='n'):
            for lemma in syn.lemmas():
                synonyms.add(lemma.name().lower())

    return list(synonyms)

def replace_with_synonyms(text):
    # Tokenize and tag parts of speech using NLTK
    tokens = word_tokenize(text)
    pos_tags = pos_tag(tokens)

    # Replace words with synonyms
    replaced_text = []
    for token, pos in pos_tags:
        if token.isalpha() and token.lower() not in nltk.corpus.stopwords.words('english'):
            # Get lemmatized word
            lemma = lemmatizer.lemmatize(token.lower(), pos[0].lower())

            # Get synonyms for the lemmatized word and part of speech
            synonyms = get_synonyms(lemma, pos[0].lower())

            if synonyms:
                # Choose a random synonym and append it to the replaced text
                replaced_text.append(random.choice(synonyms))
            else:
                # If no synonyms are found, keep the original word
                replaced_text.append(token)
        else:
            # Keep non-alphabetic and stop words as they are
            replaced_text.append(token)

    return " ".join(replaced_text)

@router.post("/testing/spacy")
async def root(data: RewriteText):
    original_text = data.text
    return {
        "original_text": original_text,
        "rewritten_text": replace_with_synonyms(original_text),
    }

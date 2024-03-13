# !pip install streamlit difflib

import streamlit as st
import json
#import difflib
# import os
# import warnings
# import sys
# import unidecode

# warnings.filterwarnings("ignore")

with open('optimized_scheme_questions.json', 'r') as f:
  data = json.load(f)

# with open('data/sc_json.json', 'r') as f:
#   odata = json.load(f)

st.title("Scheme Optimisation")
# st.set_page_config(page_title="Scheme Optimisation", page_icon="���", layout="wide")

def search_key(query, data):
    # For simplicity, this just checks if the query is a substring of the key
    # For more advanced semantic search, use Elasticsearch, or NLP libraries like Spacy or NLTK,
    # or even integrating with a service like OpenAI's embeddings.
    results = {}
    for key, value in data.items():
        if query.lower() in key.lower():  # Simple substring match, case-insensitive
            results[key] = value
        # or call openai LLM API to find the best match
    return results

query = st.text_input('Enter the scheme\'s name:')

if query:
    # Perform the search
    results = search_key(query, data)
    
    if results:
        for key, value in results.items():
            st.write(f'You only need to answer these questions for scheme - {key}')
            #st.write(type(value))
            if isinstance(value, list):  # Check if the value is a list
                output = '<br>'.join(value)  # Combine list elements into one string, each element on a new line
            else:
                output = value
            st.markdown(output, unsafe_allow_html=True)
    else:
        st.write('No matching scheme found.')


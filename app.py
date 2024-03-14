# !pip install streamlit difflib

import streamlit as st
import json
import difflib
# import os
# import sys
import warnings
import unidecode

warnings.filterwarnings("ignore")

with open('optimized_scheme_questions.json', 'r') as f:
  data = json.load(f)

# with open('data/sc_json.json', 'r') as f:
#   odata = json.load(f)

def get_closest_match(query, choices):
    return difflib.get_close_matches(query, choices, n=1, cutoff=0.6)

def main():
    st.title("Scheme Optimisation")
    # st.set_page_config(page_title="Scheme Optimisation", page_icon="���", layout="wide")
    
    user_input = st.text_input('Enter the scheme\'s name:')
    if user_input:
        scheme_keys = list(data.keys())
        matches = get_closest_match(user_input.lower(), [key.lower() for key in scheme_keys])
        
    if matches:
            matched_key = matches[0]
            st.multiselect('Multiselect', [matches[0],matches[1],matches[2]])
            matched_value = data[scheme_keys[[key.lower() for key in scheme_keys].index(matched_key)]]
            st.write(f"Eligibility criteria for {matched_key}:")
            st.write(matched_value)
        else:
            st.write("No matching scheme found.")
    
    st.slider('Rate your response', min_value=0, max_value=10)
    st.date_input('Today\'s date')

def alt_function():
    @st.cache_data
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

    def response():
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
                # st.cache_data.clear()

if __name__ == "__main__":
    main()

# def chat_history():
#     # Initialize chat history
#     if "messages" not in st.session_state:
#         st.session_state.messages = []

#     # Display chat messages from history on app rerun
#     for message in st.session_state.messages:
#         with st.chat_message(message["role"]):
#             st.markdown(message["content"])
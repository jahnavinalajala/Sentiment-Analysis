
import tensorflow as tf

from tensorflow.keras.datasets import imdb
from tensorflow.keras.preprocessing import sequence
from tensorflow.keras.models import load_model

word_index = imdb.get_word_index()
reverse_word_index = {value:key for key,value in word_index.items()}
import os


# Get current directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Print files in the directory (to debug)
print("Files in current directory:", os.listdir(BASE_DIR))

# Define model path
model_path = os.path.join(BASE_DIR, 'model_rnn_imdb.h5')

# Load the model
if os.path.exists(model_path):
    model = load_model(model_path)
else:
    raise FileNotFoundError(f"Model file not found at {model_path}")

def decode_review(encoded_review):
    return ' '.join([reverse_word_index.get(i -3,"?")for i in encoded_review])
def preprocess_text(text):
    words = text.lower().split()
    encoded_review = [word_index.get(word,2)+3 for word in words]
    padded_review = sequence.pad_sequences([encoded_review],maxlen =500)
    return padded_review 

import streamlit as st
## streamlit app
# Streamlit app
st.title('IMDB Movie Review Sentiment Analysis')
st.write('Enter a movie review to classify it as positive or negative.')

# User input
user_input = st.text_area('Movie Review')

if st.button('Classify'):

    preprocessed_input=preprocess_text(user_input)

    ## MAke prediction
    prediction=model.predict(preprocessed_input)
    sentiment='Positive' if prediction[0][0] > 0.40 else 'Negative'

    # Display the result
    st.write(f'Sentiment: {sentiment}')
    st.write(f'Prediction Score: {prediction[0][0]}')
else:
    st.write('Please enter a movie review.')

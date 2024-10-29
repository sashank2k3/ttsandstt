import streamlit as st
import speech_recognition as sr
import pyttsx3
import threading
import time
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

# Download VADER sentiment analysis lexicon
nltk.download('vader_lexicon')

# Initialize VADER sentiment analyzer
sia = SentimentIntensityAnalyzer()

# Function to handle text-to-speech in a separate thread
def speak_text(text):
    def run_in_thread(text):
        # Initialize the pyttsx3 engine inside the thread
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
    
    # Start TTS in a new thread
    tts_thread = threading.Thread(target=run_in_thread, args=(text,))
    tts_thread.start()

# Speech-to-Text Function
def speech_to_text():
    recognizer = sr.Recognizer()
    
    with sr.Microphone() as source:
        st.info("Listening... Please speak now.")
        audio_data = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio_data)
            return text
        except sr.UnknownValueError:
            return "Sorry, I did not understand that."
        except sr.RequestError:
            return "Sorry, the speech recognition service is down."

# Sentiment Analysis Function
def analyze_sentiment(text):
    sentiment_score = sia.polarity_scores(text)
    if sentiment_score['compound'] >= 0.05:
        return "Positive", "positive"
    elif sentiment_score['compound'] <= -0.05:
        return "Negative", "negative"
    else:
        return "Neutral", "neutral"

# Main Function for Streamlit
def main():
    st.markdown("<h1 class='title-text'>🎤 Speech-to-Text with Sentiment Analysis</h1>", unsafe_allow_html=True)
    st.markdown("<h3 class='subtitle-text'>Convert speech to text, analyze the sentiment, and hear the result! 😃</h3>", unsafe_allow_html=True)

    option = st.sidebar.selectbox("Select Action", ("Speech-to-Text and Sentiment Analysis", "Text-to-Speech"))

    if option == "Speech-to-Text and Sentiment Analysis":
        st.subheader("🎙️ Speak and Analyze Sentiment")
        if st.button("🎤 Start Recording"):
            with st.spinner("Recording..."):
                time.sleep(1)
                speech_text = speech_to_text()
                st.success("You said: " + speech_text)

                sentiment, sentiment_class = analyze_sentiment(speech_text)
                st.markdown(f"<p class='{sentiment_class}'>Sentiment: {sentiment}</p>", unsafe_allow_html=True)

                response = f"The sentiment of the sentence is {sentiment}."
                speak_text(response)
                st.success("Speaking: " + response)

    elif option == "Text-to-Speech":
        st.subheader("💬 Enter Text for Speech")
        user_input = st.text_area("Enter text to convert to speech:")
        if st.button("🔊 Convert to Speech"):
            if user_input.strip() != "":
                with st.spinner("Converting text to speech..."):
                    time.sleep(1)
                    speak_text(user_input)
                    st.success("Speech played successfully!")

if __name__ == '__main__':
    main()

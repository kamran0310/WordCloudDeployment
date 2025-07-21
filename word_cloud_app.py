import pandas as pd
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
import PyPDF2
from docx import Document
import plotly.express as px
import base64
from io import BytesIO

#function for file reading
def read_file(file):
    return file.getvalue().decode("utf-8")

def read_docx(file):
    doc = Document(file)
    return " ".join([para.text for para in doc.paragraphs])
 
def read_pdf(file):
    pdf = PyPDF2.PdfReader(file)
    return " ".join([page.extract_text() for page in pdf.pages])

# Function to filter out stopwords
def filter_stopwords(text):
    stopwords = set(STOPWORDS)
    return " ".join([word for word in text.split() if word.lower() not in stopwords])

# Function to generate a download link for the word cloud image
def generate_download_link(image, filename):
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    href = f'<a href="data:image/png;base64,{img_str}" download="{filename}">Download Word Cloud</a>'
    return href

# streamlit app
st.title("Word Cloud Generator")
st.write("Upload a text file, PDF, or DOCX to generate a word cloud.")
uploaded_file = st.file_uploader("Choose a file", type=["txt", "pdf", "docx"])

if uploaded_file:
    if uploaded_file.type == "text/plain":
        text = read_file(uploaded_file)
    elif uploaded_file.type == "application/pdf":
        text = read_pdf(uploaded_file)
    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        text = read_docx(uploaded_file)
    else:
        st.error("Unsupported file type.")
        st.stop()

    # Filter out stopwords
    filtered_text = filter_stopwords(text)

    # Generate word cloud
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(filtered_text)

    # Display word cloud
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    st.pyplot(plt)

    # Download link for the word cloud image
    download_link = generate_download_link(wordcloud.to_image(), "word_cloud.png")
    st.markdown(download_link, unsafe_allow_html=True)
    
    # word count table at the end
    word_counts = pd.Series(filtered_text.split()).value_counts().reset_index()
    word_counts.columns = ['Word', 'Count']
    st.write("Word Count Table:")
    st.dataframe(word_counts)
    # Plotting word counts using Plotly
    fig = px.bar(word_counts.head(20), x='Word', y='Count', title='Top 20 Words')
    st.plotly_chart(fig)
    st.write("Word Cloud generated successfully!")
    st.success("Word Cloud generated successfully!")
    st.balloons() 
else:
    st.info("Please upload a file to generate a word cloud.")
import PyPDF2
import os
# Ensure the necessary libraries are installed
if not os.path.exists("requirements.txt"):  
    with open("requirements.txt", "w") as f:
        f.write("streamlit\nwordcloud\nmatplotlib\nPyPDF2\ndocx2txt\nplotly\nnumpy\npandas\n")
    st.info("Requirements file created. Please install the necessary libraries.")
    st.stop()
import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import pycountry # pip install pycountry
# python 3.13

import os
from dotenv import load_dotenv
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

st.title("GPT-OSS Gen AI Language Translator 🔁📝")
col1, col2 = st.columns(2)
with col1:
    language = [lan.name for lan in pycountry.languages]
    Language = st.selectbox("Select the language to translate :-", options = language)
with col2:
    Text = st.text_area("Enter the text to translate :-")

if st.button("Translate") and Language and Text:
    llm = ChatGroq(model = "openai/gpt-oss-120b")
    prompt = ChatPromptTemplate.from_messages(
        [("system","Translate the text specified by user to that language specified by the user."),
        ("user", "Text: {text}, language: {language}")])
    output_parser = StrOutputParser()

    chain = prompt|llm|output_parser

    response = chain.invoke({"text":Text,"language":Language})
    st.success(response)
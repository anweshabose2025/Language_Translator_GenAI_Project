import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import pycountry # pip install pycountry
# python 3.13

st.sidebar.title("Settings")
groq_api_key = st.sidebar.text_input("Enter Groq API Key", type="password")
models = st.sidebar.selectbox("Select the Model", options=["openai/gpt-oss-120b","openai/gpt-oss-20b"])
st.sidebar.slider("Max Token", min_value=0.0, max_value=1.0)
st.sidebar.slider("Max Temperature", min_value=100, max_value=300)

st.title("GPT-OSS Gen AI Language Translator 🔁📝")
col1, col2 = st.columns(2)
with col1:
    language = [lan.name for lan in pycountry.languages]
    Language = st.selectbox("Select the language to translate :-", options = language)
with col2:
    Text = st.text_area("Enter the text to translate :-")

if not groq_api_key:
    st.warning("Please enter the api key")

if st.button("Translate") and Language and Text and groq_api_key:
    llm = ChatGroq(api_key=groq_api_key, model = models)
    prompt = ChatPromptTemplate.from_messages(
        [("system","Translate the text specified by user to that language specified by the user."),
        ("user", "Text: {text}, language: {language}")])
    output_parser = StrOutputParser()

    chain = prompt|llm|output_parser

    response = chain.invoke({"text":Text,"language":Language})
    st.success(response)
# (D:\Udemy\Complete_DSMLDLNLP_Bootcamp\UPractice1\venv) 
# D:\Udemy\Complete_GenAI_Langchain_Huggingface\UPractice2\GenAI Language Translator>python 2-Flask.py

from flask import Flask, render_template, request
import pycountry
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

app = Flask(__name__)

import os
from dotenv import load_dotenv
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

@app.route("/", methods=["GET", "POST"])
def welcome():
    languages = sorted([lang.name for lang in pycountry.languages if hasattr(lang, "name")])
    final_text = None

    if request.method == "POST":
        selected_language = request.form["language"]
        text_to_translate = request.form["text"]

        llm = ChatGroq(model = "openai/gpt-oss-120b")
        prompt = ChatPromptTemplate.from_messages(
            [("system","Translate the text specified by user to that language specified by the user."),
            ("user", "Text: {text}, language: {language}")])
        output_parser = StrOutputParser()
        chain = prompt|llm|output_parser
        response = chain.invoke({"text":text_to_translate,"language":selected_language})
        
        final_text = f"You entered: '{text_to_translate}' → Translated to: '{response}'"

    return render_template("front_page1.html", final_text=final_text, languages = languages)

if __name__ == "__main__":
    app.run(debug=True)

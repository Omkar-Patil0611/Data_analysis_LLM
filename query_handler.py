from groq import Groq  # type: ignore
import streamlit as st  # type: ignore
import spacy
from data_insights import generate_summary

# Load NLP model for query understanding
nlp = spacy.load("en_core_web_sm")

# Initialize Groq API
GROQ_API_KEY = "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"
groq_client = Groq(api_key=GROQ_API_KEY)

def preprocess_query(query):
    """
    Preprocess user query using NLP to extract key intent and entities.
    """
    doc = nlp(query)
    processed_query = " ".join([token.lemma_ for token in doc if not token.is_stop])
    return processed_query

def process_query(query, data_summary):
    """
    Process user query with NLP before sending it to the Groq model.
    """
    cleaned_query = preprocess_query(query)
    
    system_message = (
        f"You are a highly skilled and professional data analyst proficient in Python programming and data visualization tools like Pandas and Matplotlib.\n"
        f"Below is the summary of a dataset:\n{data_summary}\n"
        "Your task is to provide clean and well-structured Python code that fulfills the following requirements:\n"
        "1. The code must address the user's question or request explicitly. The question is: '{cleaned_query}'.\n"
        "2. Assume the dataset has already been loaded into a DataFrame named `df`.\n"
        "3. If the query involves generating a visualization (e.g., bar chart, line chart, etc.), ensure that:\n"
        "   a. The chart is well-labeled with appropriate titles, axis labels, and legends (if applicable).\n"
        "   b. The chart displays no more than the top or bottom 10 categories based on count or value unless the user explicitly requests to show all categories.\n"
        "   c. Include a brief annotation or highlight specific features of the visualization where necessary.\n"
        "4. If numerical analysis is requested, provide clear and concise insights such as statistical summaries, correlations, or trends.\n"
        "5. Include comments in the code to explain each major step for better readability.\n"
        "6. The output should contain only the Python code (no explanations or extraneous text).\n"
    )

    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": cleaned_query}
    ]

    # Query Groq API
    response = groq_client.chat.completions.create(
        model="llama3-70b-8192",
        messages=messages
    )
    
    print(response)
    return response.choices[0].message.content


# import google.generativeai as genai
# import streamlit as st  # type: ignore
# from data_insights import generate_summary
# import os

# # Initialize Gemini API
# GEMINI_API_KEY = "AIzaSyDfY97lFPNSKpRbFYIISdpnddIMIFuD28I"
# genai.configure(api_key=GEMINI_API_KEY)

# def process_query(query, data_summary):
#     system_message = (
#         f"You are a highly skilled and professional data analyst proficient in Python programming and data visualization tools like Pandas and Matplotlib.\n"
#         f"Below is the summary of a dataset:\n{data_summary}\n"
#         "Your task is to provide clean and well-structured Python code that fulfills the following requirements:\n"
#         "1. The code must address the user's question or request explicitly. The question is: '{query}'.\n"
#         "2. Assume the dataset has already been loaded into a DataFrame named `df`.\n"
#         "3. If the query involves generating a visualization (e.g., bar chart, line chart, etc.), ensure that:\n"
#         "   a. The chart is well-labeled with appropriate titles, axis labels, and legends (if applicable).\n"
#         "   b. The chart displays no more than the top or bottom 10 categories based on count or value unless the user explicitly requests to show all categories.\n"
#         "   c. Include a brief annotation or highlight specific features of the visualization where necessary.\n"
#         "4. If numerical analysis is requested, provide clear and concise insights such as statistical summaries, correlations, or trends.\n"
#         "5. Include comments in the code to explain each major step for better readability.\n"
#         "6. The output should contain only the Python code (no explanations or extraneous text).\n"
#     )

#     # Initialize Gemini model
#     model = genai.GenerativeModel("gemini-2.0-flash")

#     # Query Gemini
#     response = model.generate_content([system_message, query])
#     # print(response)

#     # Return generated code
#     return response.text


# from sentence_transformers import SentenceTransformer
# import spacy
# import re
# from groq import Groq  # type: ignore

# # Load NLP models
# nlp_model = SentenceTransformer("all-MiniLM-L6-v2")
# nlp = spacy.load("en_core_web_sm")

# # Initialize Groq API
# GROQ_API_KEY = "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"
# groq_client = Groq(api_key=GROQ_API_KEY)

# def preprocess_query(query):
#     """
#     Preprocess user query using NLP to extract key intent and entities.
#     """
#     doc = nlp(query)
#     processed_query = " ".join([token.lemma_ for token in doc if not token.is_stop])
#     return processed_query

# def extract_entities(query):
#     """
#     Extracts numeric values, column names, and keywords using regex.
#     """
#     numbers = re.findall(r"\d+", query)
#     keywords = [token.text.lower() for token in nlp(query) if token.pos_ in ["NOUN", "VERB", "ADJ"]]
#     return {"numbers": numbers, "keywords": keywords}

# def process_query_with_nlp(query: str, data_summary: dict) -> str:
#     """
#     Uses NLP to interpret the query and generate corresponding Pandas code with Groq API.
#     """
#     cleaned_query = preprocess_query(query)
#     extracted_info = extract_entities(query)

#     system_message = (
#         f"You are a highly skilled and professional data analyst proficient in Python programming and data visualization tools like Pandas and Matplotlib.\n"
#         f"Below is the summary of a dataset:\n{data_summary}\n"
#         "Your task is to provide clean and well-structured Python code that fulfills the following requirements:\n"
#         "1. The code must address the user's question or request explicitly. The question is: '{cleaned_query}'.\n"
#         "2. Assume the dataset has already been loaded into a DataFrame named `df`.\n"
#         "3. Extracted entities from the query: {extracted_info}.\n"
#         "4. If the query involves generating a visualization (e.g., bar chart, line chart, etc.), ensure that:\n"
#         "   a. The chart is well-labeled with appropriate titles, axis labels, and legends (if applicable).\n"
#         "   b. The chart displays no more than the top or bottom 10 categories based on count or value unless the user explicitly requests to show all categories.\n"
#         "   c. Include a brief annotation or highlight specific features of the visualization where necessary.\n"
#         "5. If numerical analysis is requested, provide clear and concise insights such as statistical summaries, correlations, or trends.\n"
#         "6. Include comments in the code to explain each major step for better readability.\n"
#         "7. The output should contain only the Python code (no explanations or extraneous text).\n"
#     )

#     messages = [
#         {"role": "system", "content": system_message},
#         {"role": "user", "content": cleaned_query}
#     ]

#     # Query Groq API
#     response = groq_client.chat.completions.create(
#         model="llama3-70b-8192",
#         messages=messages
#     )
    
#     return response.choices[0].message.content

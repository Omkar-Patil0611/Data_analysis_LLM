from groq import Groq #type: ignore
# import streamlit as st # type: ignore
# from data_insights import generate_summary

# Initialize Groq API
# GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
GROQ_API_KEY = ""
groq_client = Groq(api_key=GROQ_API_KEY)
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

#     # Chat messages for the LLM
#     messages = [
#         {"role": "system", "content": system_message},
#         {"role": "user", "content": query}
#     ]

#     # Query Llama
#     response = groq_client.chat.completions.create(
#         model="llama3-70b-8192",
#         messages=messages
#     )
#     print(response)

#     # Return generated code
#     return response.choices[0].message.content


import google.generativeai as genai
import streamlit as st  # type: ignore
from data_insights import generate_summary
import os

# Initialize Gemini API
GEMINI_API_KEY = ""
genai.configure(api_key=GEMINI_API_KEY)

def process_query(query, data_summary):
    system_message = (
        f"You are a highly skilled and professional data analyst proficient in Python programming and data visualization tools like Pandas and Matplotlib.\n"
        f"Below is the summary of a dataset:\n{data_summary}\n"
        "Your task is to provide clean and well-structured Python code that fulfills the following requirements:\n"
        "1. The code must address the user's question or request explicitly. The question is: '{query}'.\n"
        "2. Assume the dataset has already been loaded into a DataFrame named `df`.\n"
        "3. If the query involves generating a visualization (e.g., bar chart, line chart, etc.), ensure that:\n"
        "   a. The chart is well-labeled with appropriate titles, axis labels, and legends (if applicable).\n"
        "   b. The chart displays no more than the top or bottom 10 categories based on count or value unless the user explicitly requests to show all categories.\n"
        "   c. Include a brief annotation or highlight specific features of the visualization where necessary.\n"
        "4. If numerical analysis is requested, provide clear and concise insights such as statistical summaries, correlations, or trends.\n"
        "5. Include comments in the code to explain each major step for better readability.\n"
        "6. The output should contain only the Python code (no explanations or extraneous text).\n"
    )

    # Initialize Gemini model
    model = genai.GenerativeModel("gemini-2.0-flash")

    # Query Gemini
    response = model.generate_content([system_message, query])
    # print(response)

    # Return generated code
    return response.text


def process_NLP_query(query, data_summary):
    system_message = (
        f"You are a highly intelligent AI assistant with expertise in data analysis and NLP.\n"
        f"The dataset summary is provided below:\n{data_summary}\n"
        "Your task is to respond to user queries in a **conversational, natural language style**.\n"
        "Answer questions about the dataset based on the summary using the following guidelines:\n\n"
        "1. **For Descriptive Queries:**\n"
        "   - Explain the dataset's key insights in **simple language**.\n"
        "   - Mention top trends, correlations, and unusual patterns.\n"
        "   - Avoid technical jargon unless explicitly requested.\n\n"
        "2. **For Comparison Queries:**\n"
        "   - Compare different features in the dataset (e.g., 'Which product has higher ratings?').\n"
        "   - Use easy-to-understand explanations.\n\n"
        "3. **For Statistical Queries:**\n"
        "   - Provide direct answers like averages, maximums, minimums, and correlations.\n"
        "   - Avoid returning raw statistics without explanation.\n\n"
        "4. **For NLP Queries:**\n"
        "   - Summarize text-based insights if the dataset contains text columns.\n"
        "   - Answer like a friendly analyst by highlighting common keywords, sentiment, or patterns.\n\n"
        "**Always provide the answer directly — without Python code or complex numbers — unless the user specifically requests code.**"
    )

    # Chat messages for the LLM
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": query}
    ]

    # Query Llama model
    response = groq_client.chat.completions.create(
        model="llama3-70b-8192",
        messages=messages
    )

    # Return the natural language response
    return response.choices[0].message.content


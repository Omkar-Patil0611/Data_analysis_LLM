import pandas as pd

# Load CSV file
csv_file_path = "C:\\Users\\chinmay\\Downloads\\Revenue.csv"
df_csv = pd.read_csv(csv_file_path)

# Remove extra spaces in column names
df_csv.columns = df_csv.columns.str.strip()

# Save the cleaned CSV
cleaned_csv_path = "C:\\Users\\chinmay\\Downloads\\Cleaned_Revenue.csv"
df_csv.to_csv(cleaned_csv_path, index=False)

# Load the cleaned CSV into LangChain agent
from langchain_groq import ChatGroq
from langchain_experimental.agents.agent_toolkits import create_csv_agent

groq_api = "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"
llm = ChatGroq(temperature=0, model="llama3-70b-8192", api_key=groq_api)

# Use the cleaned CSV file
agent = create_csv_agent(llm, cleaned_csv_path, verbose=True, allow_dangerous_code=True)

def query_data(query):
    response = agent.invoke(query)
    return response

query = "Calculate the total revenue for Client B and return ONLY the exact numeric value in JSON format like {'total_revenue': 1737.0}."
response = query_data(query)
print(response)


#streamlit version
import streamlit as st
import pandas as pd
from langchain_groq import ChatGroq
from langchain_experimental.agents.agent_toolkits import create_csv_agent
import tempfile

# Streamlit UI
def main():
    st.title("CSV-based Data Query with LangChain")
    
    # File uploader
    uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])
    
    if uploaded_file is not None:
        # Read CSV file
        df = pd.read_csv(uploaded_file)
        df.columns = df.columns.str.strip()  # Remove extra spaces from column names
        
        # Save cleaned CSV to a temp file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".csv")
        df.to_csv(temp_file.name, index=False)
        
        # LangChain LLM setup
        groq_api = "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"
        llm = ChatGroq(temperature=0, model="llama3-70b-8192", api_key=groq_api)
        agent = create_csv_agent(llm, temp_file.name, verbose=True, allow_dangerous_code=True)
        
        # User input query
        query = st.text_input("Enter your query")
        if st.button("Ask") and query:
            response = agent.invoke(query)
            st.subheader("Response")
            st.write(response)

if __name__ == "__main__":
    main()

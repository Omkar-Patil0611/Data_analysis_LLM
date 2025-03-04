import streamlit as st  # type: ignore 
import pandas as pd
from data_insights import generate_summary, load_dataset
from query_processor import process_query 
from query_processor import process_NLP_query
from code_executor import run_generated_code
# from data_loader import load_dataset  # Importing data loader
import warnings

warnings.filterwarnings("ignore")

# Streamlit App UI
st.title("Data Navigator: Simplify Exploration")

# File uploader for CSV and Excel files
uploaded_file = st.file_uploader("Upload a CSV or Excel file to start exploring your data:", type=["csv", "xlsx", "xls"])

if uploaded_file:
    try:
        # Load dataset using data_loader
        dataset = load_dataset(uploaded_file)

        # Generate data summary
        data_summary = generate_summary(dataset)

        # Create two tabs: Data Overview & Chat with Data
        tab1, tab2 = st.tabs(["📊 Data Overview", "💬 Chat with Data"])

        with tab1:
            # Display dataset snapshot
            st.write("### Dataset Snapshot:")
            st.dataframe(dataset.head())

            # Detailed data insights
            if st.checkbox("View Detailed Data Insights"):
                insights_tabs = st.tabs(["Null Values", "Unique Values", "Duplicate Records", "Descriptive Stats", "Numeric Summary"])

                # Null values
                with insights_tabs[0]:
                    null_counts = dataset.isnull().sum()
                    st.write("Null Values by Column:")
                    st.dataframe(null_counts)
                    st.write(f"**Total Null Values:** {null_counts.sum()}")

                # Unique values
                with insights_tabs[1]:
                    unique_counts = {col: dataset[col].nunique() for col in dataset.columns}
                    st.write("Unique Values by Column:")
                    st.dataframe(pd.DataFrame(list(unique_counts.items()), columns=["Column", "Unique Count"]))

                # Duplicate records
                with insights_tabs[2]:
                    duplicate_count = dataset.duplicated().sum()
                    st.write(f"**Total Duplicate Records:** {duplicate_count}")

                # Descriptive statistics
                with insights_tabs[3]:
                    st.write("Statistical Summary:")
                    st.dataframe(dataset.describe())

                # Numeric column summary
                with insights_tabs[4]:
                    numeric_columns = dataset.select_dtypes(include="number")
                    if not numeric_columns.empty:
                        st.write("Numeric Column Summary:")
                        numeric_summary = numeric_columns.describe().T
                        st.dataframe(numeric_summary)
                    else:
                        st.write("No numeric columns in the dataset.")

            # Visualization Section
            st.subheader("Generate Visualizations")
            viz_query = st.text_input("Enter a request for visualization (e.g., 'Show a bar chart of sales by category'):")

            if viz_query:
                with st.spinner("Generating visualization..."):
                    try:
                        generated_code = process_query(viz_query, data_summary)
                        if st.checkbox("Display Generated Code"):
                            st.code(generated_code, language="python")

                        execution_results, execution_output = run_generated_code(generated_code, dataset)

                        if execution_output:
                            st.write(execution_output)

                        if "plt" in execution_results:
                            st.pyplot(execution_results["plt"].gcf())  # type: ignore

                        if isinstance(execution_results, str):
                            st.error(execution_results)
                        else:
                            st.success("Visualization created successfully!")

                    except Exception as e:
                        st.error(f"An error occurred: {e}")

        with tab2:
            st.write("### Chat with Data Summary")
            
            query = st.text_input("Ask a question about the dataset:")
            
            if query:
                with st.spinner("Analyzing your query..."):
                    try:
                        # Process the query
                        response = process_NLP_query(query, data_summary)

                        # Check if the response contains Python code (for data analysis/visualization)
                        if any(keyword in response for keyword in ["import ", "plt.", "df."]):
                            
                            # Option to display generated code
                            if st.checkbox("Display Generated Code", key="chat_code"):
                                st.code(response, language="python")

                            # Execute the generated code
                            execution_results, execution_output = run_generated_code(response, dataset)

                            # Display execution output (if any)
                            if execution_output:
                                st.write("### Execution Output:")
                                st.write(execution_output)

                            # Display matplotlib plots if generated
                            if "plt" in execution_results:
                                st.pyplot(execution_results["plt"].gcf())  # type: ignore

                            # Handle general execution results
                            if isinstance(execution_results, str):
                                st.error(execution_results)
                            else:
                                st.success("Query processed successfully!")

                        else:
                            # NLP-based response (plain text answer)
                            st.write("### Answer:")
                            st.write(response)

                    except Exception as e:
                        st.error(f"Error processing query: {e}")
    except Exception as e:
                        st.error(f"Error loading file: {e}")
            

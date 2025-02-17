# DIY-Analytics
Analyze your data using natural language. All you have to do is upload your CSV data :)

## DATA_ANALYTICS_LLM

```mermaid
graph TD;
    A[Data Collection] --> B[Pre-processing (Tokenization, Embedding)]
    B --> C[Embedding Generation (Hugging Face)]
    C --> D[FAISS Indexing (Semantic Search)]
    D --> E[RAG Framework (Data Retrieval)]
    E --> F[Response Generation]
    F --> G[User Evaluation (Relevance, Accuracy)]
    G --> H[Comparison with Traditional Methods (Manual Sorting)]
    H --> I[Analysis of Results]
```
# SwiftVisa: Visa Eligibility Screening

A Streamlit app that gives a quick, first-pass view of whether someone may be eligible for a study, work or tourist visa. Built as my Infosys Springboard virtual internship project.

The user fills in a multi-step form with their details and destination, and the app shows:

- a recommended visa type for USA, UK, Canada, Australia or Germany
- an eligibility result and an approval score from 0 to 100
- the positive factors and risk factors behind that score
- a written explanation, plus a help chat for questions about documents, the process and eligibility

## How it works

- **Decision logic (`src/rag_pipeline.py`):** a rule-based scoring system. It starts at 50, adds or subtracts points for factors such as an admission letter, English score, job offer, income and travel history, and treats 60 or above as eligible.
- **Help chat (`app.py`):** answers by matching keywords in the question. It does not call an AI model.
- **Document pipeline (`src/process_documents.py`):** a prototype for retrieval (RAG). It splits text files into chunks with LangChain, creates embeddings with sentence-transformers (`all-MiniLM-L6-v2`) and stores them in a FAISS index. It is not connected to the app yet: `retrieve_visa_info` currently returns simulated text.
- **Reference data (`visaRequirements.json`):** visa categories and requirements for 15 countries, not yet used by the app.

## Limitations

The score comes from hand-written rules, not from a model trained on real visa decisions, so it is not a real probability of approval. This is a learning project and not immigration advice. Always check the official government sources.

## Possible next steps

- Connect the FAISS retrieval and a language model to the help chat
- Use `visaRequirements.json` to support more countries and visa types
- Train and test a model on real visa outcomes

## Run it

```
pip install -r requirements.txt
streamlit run app.py
```

The document pipeline expects `.txt` files in `data/raw`, and can be run with `python src/process_documents.py`.

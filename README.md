
```markdown
# Smart Document Search

Smart Document Search is a powerful tool designed to help users efficiently search and retrieve information from a collection of documents. It leverages advanced search algorithms and natural language processing to deliver accurate and relevant results.

## Features

- **Fast and Accurate Search**: Quickly find the information you need from large document sets.
- **Natural Language Processing**: Understands queries in plain language for intuitive searching.
- **Customizable**: Tailor the search functionality to your specific needs.
- **Multi-format Support**: Works with various document formats (e.g., PDF, CSV).
- **User-friendly Interface**: Simple and intuitive design for a seamless user experience.

## Workflow

1. **First Setup**:
   - You can create a document search system using `main.py` and `vector.py`, where the file is stored and its path is given.
   - Run the system using the command:
   ```bash
   python main.py
   ```
   - A loop for questions is created until `q` is pressed to quit.

2. **Streamlit App**:
   - You can clone the `app.py` file and run the Streamlit app with the following command:
   ```bash
   streamlit run app.py
   ```

## How It Works

1. **Upload a Document**:
   - Click on the "Upload a document" button and select a CSV or PDF file. The document content will be processed, stored, and indexed.

2. **Ask Questions**:
   - After selecting an option, the questions related to that option will be displayed. Type your question into the input field and press Enter to retrieve the model's answer based on the content of the document.

## Installation

### Clone the repository:

```bash
git clone https://github.com/Adityaasati/Smart-Document-Search.git
```

### Install the required packages:

```bash
pip install -r requirements.txt
```

### Run the app:

```bash
streamlit run app.py
```

This will launch the application in your browser.

## Technology Stack

- **Streamlit**: A web framework for building interactive web applications.
- **Langchain**: A framework for building language model-powered applications.
- **Chroma**: A vector store for efficient content indexing and search.
- **PyPDF2**: A library to extract text from PDF files.
- **Pandas**: A library for data manipulation and handling CSV files.

```

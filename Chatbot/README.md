# UTD Academic Information Chatbot (FATIMA)

FATIMA (Flexible Academic Text Intelligence and Management Assistant) is an advanced AI-powered chatbot that leverages state-of-the-art Natural Language Processing (NLP) and Large Language Models (LLMs) to provide intelligent responses about the University of Texas at Dallas (UTD) academic programs, with a focus on the Jindal School of Management.

## Features

- Advanced NLP processing using HuggingFace transformers and LangChain
- Semantic search powered by FAISS vector embeddings
- Web scraping with intelligent content extraction
- Streamlit-based interactive web interface
- REST API server with intelligent response generation
- Context-aware conversation handling
- Multi-source data integration and processing

## Technical Stack

- **Natural Language Processing**: 
  - HuggingFace Transformers for text understanding
  - LangChain for LLM integration and prompt engineering
  - Sentence Transformers for semantic embeddings

- **Vector Search**:
  - FAISS for efficient similarity search
  - Custom embedding pipeline for domain-specific knowledge

- **Web Interface**:
  - Streamlit for interactive UI
  - Real-time response generation
  - Context-aware conversation history

- **Backend**:
  - Flask REST API server
  - Asynchronous processing
  - Intelligent caching and response optimization

## Project Structure

```
chatbot/
├── app.py                 # Streamlit web interface with NLP integration
├── chatbot.py            # Core NLP and LLM processing logic
├── chatbot_server.py     # Flask REST API with intelligent routing
├── scrape_data.py        # Web scraping with NLP content extraction
├── utd_data.json         # Structured knowledge base
└── faiss_index/          # Vector embeddings for semantic search
```

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)
- CUDA-capable GPU (optional, for faster LLM processing)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/utd-chatbot.git
cd utd-chatbot
```

2. Create and activate a virtual environment:
```bash
python -m venv chatbot
source chatbot/bin/activate  # On Windows: chatbot\Scripts\activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

## Usage

### 1. Data Collection and Processing

Run the web scraper with NLP processing:
```bash
python scrape_data.py
```
This will:
- Scrape UTD academic program information
- Process content using NLP techniques
- Generate semantic embeddings
- Create a FAISS vector store for efficient search

### 2. Start the Chatbot Server

In one terminal, start the Flask server with LLM integration:
```bash
python chatbot_server.py
```
The server will run on `http://localhost:8000`

### 3. Run the Web Interface

In another terminal, start the Streamlit app:
```bash
streamlit run app.py
```
Access the web interface at `http://localhost:8501`

## How It Works

1. **Data Processing Pipeline**:
   - Web scraping with intelligent content extraction
   - NLP-based text cleaning and structuring
   - Semantic embedding generation using transformer models
   - Vector store creation for efficient retrieval

2. **Query Processing**:
   - Natural language understanding using LLMs
   - Semantic search in vector space
   - Context-aware response generation
   - Source attribution and confidence scoring

3. **User Interface**:
   - Interactive chat interface
   - Real-time response generation
   - Context preservation across conversations
   - Source citation and confidence indicators

## API Endpoints

- `POST /chatbot`: Submit a query for NLP processing
- `GET /health`: Check server health status
- `POST /embed`: Generate embeddings for custom text
- `GET /context`: Retrieve conversation context

## Example Queries

- "Explain the Data Science track curriculum in detail"
- "What are the prerequisites for the Business Analytics program?"
- "Compare the different scholarship opportunities available"
- "How does the application process work for international students?"

## Acknowledgments

- UTD Jindal School of Management for the academic information
- HuggingFace for transformer models and NLP tools
- FAISS for efficient vector similarity search
- LangChain for LLM integration and prompt engineering
- Streamlit for the interactive web interface

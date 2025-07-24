from flask import Flask, request, jsonify
from chatbot import load_scraped_data, get_response, initialize_chatbot

app = Flask(__name__)

# Initialize chatbot with scraped data and vector store
print("Loading scraped data and initializing vector store...")
scraped_data, vector_store = initialize_chatbot()
print("Data and vector store loaded successfully!")

@app.route('/chatbot', methods=['POST'])
def chatbot_response():
    try:
        data = request.json
        query = data.get("query")
        if not query:
            return jsonify({"error": "No query provided"})
        
        # Get response using both semantic search and keyword matching
        response = get_response(query, scraped_data, vector_store)
        return jsonify(response)
    
    except Exception as e:
        print(f"Error in chatbot response: {str(e)}")
        return jsonify({
            "error": str(e),
            "answer": "An error occurred while processing your question."
        })

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"})

if __name__ == "__main__":
    print("Starting Flask server...")
    app.run(host='0.0.0.0', port=8000, debug=False) 

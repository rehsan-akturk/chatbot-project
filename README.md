# FunderPro FAQ Chatbot Documentation

## About the Project
This project makes a chatbot that answers customer questions using an FAQ list from FunderPro.com. It uses the OpenAI API, a vector database (FAISS), and the data from a provided funderpro-faqs files.

## Requirements
-Python 3.10 or higher
-OpenAI API Key
-Flask
-FAISS
-Required Python libraries (listed in requireme


## Setup

### Clone the Repository
```
git clone https://github.com/yourusername/chatbot-project.git
cd chatbot-project
```

## Create and Activate a Virtual Environment 
```
python3 -m venv chatbot-env
source chatbot-env/bin/activate  # Linux/MacOS
chatbot-env\Scripts\activate  # Windows ```

#Install Required Packages
pip install -r requirements.txt 
```

### Set Your OpenAI API Key
### Set Your OpenAI API Key

1. Create a `.env` file in the root directory of your project.
2. Add your OpenAI API key to the `.env` file:
    ```
    OPENAI_API_KEY=your_openai_api_key_here
    ```
You can find a Medium article on how to get an OpenAI API key here: [Unlocking the Power of OpenAI: A Guide to Obtaining Your API Key](https://medium.com/@akturkrehsan/unlocking-the-power-of-openai-a-guide-to-obtaining-your-api-key-9f5b0cf65a13).

### Steps
1. **Fetching and Processing Data**
    - `fetch_data.py`: This script gets and processes data from FunderPro.com and the provided funderpro-faqs files.
    - FAQs were fetched from FunderPro.com.
    - The data was cleaned and tokenized.
    - The processed data was saved into a `faqs.json` file.

2. **Vectorization and Creating the Vector Database**
    - `store.py`: This script handles the vectorization of the data and creates the vector database using FAISS.
    - Embeddings for each FAQ in the `faqs.json` file were created.
    - The embeddings were stored in the FAISS vector database.
    - The `faiss_index.bin` file was created and saved.

3. **Creating the Chatbot**
    - `bot.py`: This script handles user queries and returns the most relevant FAQ responses.
    - User queries were converted to embeddings.
    - The nearest vectors were searched in the FAISS database.
    - The most relevant FAQ responses were presented to the user.

4. **Web Interface**
    - `app.py`: A simple web interface was created using Flask.
    - A form was created to take user queries.
    - The results were displayed to the user.

### Additional Steps
5. **Docker Support**
    - The project can be easily set up and run using Docker. Use the following commands to run the project:
    
    #### Build the Docker image:
    ```
    docker build -t funderpro-faq-bot .
    ```

    #### Start the Docker container:
    ```
    docker-compose up
    ```

### Running the Project
1. Activate the virtual environment:
    ```
    source chatbot-env/bin/activate  # Linux/MacOS
    chatbot-env\Scripts\activate  # Windows
    ```

2. Start the Flask application:
    ```
    python app.py
    ```

3. Go to [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser to start using the chatbot.

### Project Structure

```
chatbot-project/
├── chatbot/
│ ├── data/
│ │ ├── __init__.py
│ │ ├── faqs.json
│ │ ├── fetch_data.py
│ │ ├── vectorized_faqs.json
│ ├── vector_store/
│ │ ├── faiss_index.bin
│ │ ├── __init__.py
│ ├── __init__.py
│ ├── bot.py
├── templates/
│ ├── index.html
├── app.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── README.md
└── test/
   ├── test_bot.py
   ├── unittest_bot.py


```

### Tests
Tests are located in the `test/` directory. They ensure that the bot functions correctly and handles various scenarios.

- `test_bot.py`: Script for testing the bot's response to different queries.
- `unittest_bot.py`: Unit tests for the FAQBot class.

To run the tests, use the following command:
```
python -m unittest discover -s test 
```



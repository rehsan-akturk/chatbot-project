import logging
import json
import os

import openai
import faiss
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import importlib.resources as pkg_resources
import chatbot.vector_store as vector_store

# Logging configuration
logging.basicConfig(level=logging.INFO)

# OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')


class FAQBot:
    def __init__(self):
        # Load FAQ data from JSON file
        with pkg_resources.open_text(vector_store, 'vectorized_faqs.json') as f:
            self.faqs = json.load(f)

        # Load FAISS index from file
        with pkg_resources.path(vector_store, 'faiss_index.bin') as faiss_index_path:
            self.index = faiss.read_index(str(faiss_index_path))

    def get_embedding(self, text):
        # Get embedding for input text
        response = openai.Embedding.create(input=text, model="text-embedding-ada-002")
        return response['data'][0]['embedding']

    def search_faqs(self, query, top_k=1, threshold=0.5, similarity_threshold=0.8):
        logging.debug(f"Query: {query}")
        # Get embedding for query text
        query_embedding = np.array(self.get_embedding(query)).astype('float32').reshape(1, -1)
        logging.debug(f"Query Embedding: {query_embedding}")
        # Search for nearest neighbors in FAISS index
        distances, indices = self.index.search(query_embedding, top_k)
        logging.debug(f"FAISS distances: {distances}, indices: {indices}")

        if len(distances[0]) > 0 and distances[0][0] < threshold:
            faq_index = int(indices[0][0])
            faq = self.faqs[faq_index]
            similarity = cosine_similarity(query_embedding, np.array(faq['question_embedding']).reshape(1, -1))[0][0]
            logging.debug(f"Similarity: {similarity}")
            if similarity > similarity_threshold:
                return [{'faq': faq, 'distance': distances[0][0], 'similarity': similarity}]

        return []

    def generate_response(self, query):
        logging.debug(f"Generating response for query: {query}")
        return self.handle_no_match(query)

    def handle_no_match(self, query):
        logging.debug(f"No match found for query: {query}")
        return [{
            'faq': {
                'question': query,
                'answer': (
                    "Sorry, I couldn't find an answer to your question. "
                    "Please try rephrasing your question or visit our "
                    "<a href='https://funderpro.com/faqs/'>FAQ page</a> for more information. "
                    "Here are some common topics you can ask about: "
                    "<ul>"
                    "<li>How to sign up</li>"
                    "<li>Return policy</li>"
                    "<li>Available services</li>"
                    "<li>Business hours</li>"
                    "<li>Contact information</li>"
                    "</ul>"
                )
            }
        }]

import json
import os

import openai
import faiss
import numpy as np
import importlib.resources as pkg_resources
import chatbot.data

# OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')


class FAQVectorStore:
    def __init__(self, faq_json):
        self.faqs = self.load_faqs(faq_json)

    def load_faqs(self, filename):
        with pkg_resources.open_text(chatbot.data, filename) as f:
            return json.load(f)

    def get_embedding(self, text):
        response = openai.Embedding.create(input=text, model="text-embedding-ada-002")
        return response['data'][0]['embedding']

    def vectorize_faqs(self):
        for faq in self.faqs:
            faq['question_embedding'] = self.get_embedding(faq['question'])
            faq['answer_embedding'] = self.get_embedding(faq['answer'])

    def save_faqs_to_json(self, filename):
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.faqs, f, ensure_ascii=False, indent=4)

    def create_faiss_index(self):
        dimension = len(self.faqs[0]['question_embedding'])
        index = faiss.IndexFlatL2(dimension)

        embeddings = np.array([faq['question_embedding'] for faq in self.faqs]).astype('float32')
        index.add(embeddings)
        return index

    def save_faiss_index(self, index, filename):
        faiss.write_index(index, filename)

def main():
    faq_json_filename = 'faqs.json'
    vector_store = FAQVectorStore(faq_json_filename)

    vector_store.vectorize_faqs()
    vector_store.save_faqs_to_json('vectorized_faqs.json')

    index = vector_store.create_faiss_index()
    vector_store.save_faiss_index(index, 'faiss_index.bin')

if __name__ == "__main__":
    main()

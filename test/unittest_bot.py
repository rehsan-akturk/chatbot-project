import unittest
import numpy as np
from unittest.mock import patch
from chatbot.bot import FAQBot

class TestFAQBot(unittest.TestCase):
    @patch('openai.Embedding.create')
    def test_get_embedding(self, mock_embedding_create):
        # Mock embedding response
        mock_embedding_create.return_value = {
            'data': [{'embedding': [0.1, 0.2, 0.3]}]
        }

        bot = FAQBot()
        embedding = bot.get_embedding("test query")
        self.assertEqual(embedding, [0.1, 0.2, 0.3])

    @patch('openai.Embedding.create')
    @patch('faiss.IndexFlatL2.search')
    def test_search_faqs(self, mock_faiss_search, mock_embedding_create):
        # Mock embedding and FAISS search response
        mock_embedding_create.return_value = {
            'data': [{'embedding': [0.1, 0.2, 0.3]}]
        }
        mock_faiss_search.return_value = (np.array([0.5]), np.array([0]))

        bot = FAQBot()
        bot.faqs = [{'question': 'What is your return policy?', 'question_embedding': [0.1, 0.2, 0.3], 'answer': 'Our return policy is...'}]
        results = bot.search_faqs("test query", top_k=1, threshold=0.8)
        self.assertEqual(len(results), 0)  # Expecting no match due to high distance

        # Test with lower threshold
        results = bot.search_faqs("test query", top_k=1, threshold=1.0)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['faq']['question'], 'What is your return policy?')

    def test_generate_response(self):
        bot = FAQBot()
        response = bot.generate_response("test query")
        self.assertIn("Sorry, I couldn't find an answer to your question.", response[0]['faq']['answer'])

    def test_handle_no_match(self):
        bot = FAQBot()
        response = bot.handle_no_match("test query")
        self.assertIn("Sorry, I couldn't find an answer to your question.", response[0]['faq']['answer'])

if __name__ == '__main__':
    unittest.main()

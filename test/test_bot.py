import logging
from chatbot.bot import FAQBot

# Logging
logging.basicConfig(level=logging.DEBUG)

def test_bot():
    bot = FAQBot()

    queries = [
        "How do I sign up?",
        "What is your return policy?",
        "Tell me about your services.",
        "My cat is pretty",
        "How can I go to Paris?",
        "Do you offer free trials?",
        "how to open account",
        "Contact information",
        "What is the meaning of life?",
        "Can I Scale My Account?"
    ]

    for query in queries:
        print(f"Query: {query}")
        results = bot.search_faqs(query)
        if results:
            print(f"Q: {results[0]['faq']['question']}")
            print(f"A: {results[0]['faq']['answer']}")
        else:
            no_match_response = bot.handle_no_match(query)
            print(f"Q: {no_match_response[0]['faq']['question']}")
            print(f"A: {no_match_response[0]['faq']['answer']}")
        print("-" * 50)

if __name__ == "__main__":
    test_bot()
